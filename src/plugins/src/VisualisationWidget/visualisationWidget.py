from collections import deque
from typing import Optional

import numpy as np
import pyaudio

from PySide6.QtCharts import QChart, QChartView, QAreaSeries, QValueAxis, QLineSeries
from PySide6.QtGui import QLinearGradient, QBrush, QColor, QPen, QPainter
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QComboBox, QPushButton, QVBoxLayout, QWidget

from oapi import Config, OWindow, PluginSettingWindow

# Константы аудио
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SMOOTHING = 3
SILENCE_THRESHOLD = 50
SILENCE_DURATION = 15


class CustomPluginWindow(PluginSettingWindow):
    
    def __init__(self, obj, name_plugin, parent=None):
        super().__init__(obj, name_plugin, parent)
        self.p_audio = pyaudio.PyAudio()
        self.comboListDevice = QComboBox()
        self.listDevice = set()
        self.updateLoaderDevice()
        self.formLayout.addRow("Устройство", self.comboListDevice)
        
        self.btnUpdateDevice = QPushButton("Обновить устройства")
        self.btnUpdateDevice.pressed.connect(self.updateLoaderDevice)
        self.formLayout.addRow(self.btnUpdateDevice)
    
    def loader(self):
        super().loader()
        idx = self.comboListDevice.findData({"idx": self.obj.idx_device or 0}, Qt.ItemDataRole.UserRole,
                                            Qt.MatchFlag.MatchContains)
        self.comboListDevice.setCurrentIndex(idx)
    
    def updateLoaderDevice(self):
        self.comboListDevice.clear()
        self.listDevice.clear()
        for idx in range(self.p_audio.get_device_count()):
            info = self.p_audio.get_device_info_by_index(idx)
            if info["maxInputChannels"] <= 0: continue
            try:
                name = info["name"].encode("cp1251").decode("utf-8")
            except:
                name = info["name"]
            if name in self.listDevice: continue
            self.comboListDevice.addItem(name, {"idx": idx})
            self.listDevice.add(name)
    
    def send_data(self):
        data = super().send_data()
        idx = self.comboListDevice.currentIndex()
        uData = self.comboListDevice.itemData(idx, Qt.ItemDataRole.UserRole)
        data.set("idx_device", uData["idx"] if uData else None)
        return data


class Visualisation(OWindow):
    
    def __init__(self, parent=None):
        super().__init__(Config("VisualisationWidget", "window"), parent)
        self.time_msec = 30
        
        self.idx_device = None
        self.stream = None
        self.p = pyaudio.PyAudio()
        
        self.smoothing_buffer = deque(maxlen=SMOOTHING)
        self.peak_data = np.zeros(CHUNK // 2)
        self.fall_speed = 15
        self.silence_counter = 0
        
        self.chart = QChart()
        # ОТКЛЮЧАЕМ АНИМАЦИЮ - это убирает лаги при обновлении
        self.chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)
        self.chart.setBackgroundVisible(False)
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.legend().hide()  # Лишние вычисления
        
        self.series_top = QLineSeries()
        self.series_bottom = QLineSeries()
        
        # Чтобы не было "квадратиков", ставим косметическое перо или NoPen
        self.series_top.setPen(QPen(Qt.PenStyle.NoPen))
        self.series_bottom.setPen(QPen(Qt.PenStyle.NoPen))
        
        self.area_series = QAreaSeries(self.series_top, self.series_bottom)
        
        # НАСТРОЙКА ГРАДИЕНТА
        # Используем ObjectBoundingMode, чтобы 0.5 всегда был центром виджета
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
        
        gradient.setColorAt(0.0, QColor.fromHsv(0, 255, 255, 200))  # Верх (Красный)
        gradient.setColorAt(0.25, QColor.fromHsv(120, 255, 255, 200))  # Зеленый
        gradient.setColorAt(0.5, QColor.fromHsv(240, 255, 255, 255))  # Центр (Синий)
        gradient.setColorAt(0.75, QColor.fromHsv(120, 255, 255, 200))  # Зеленый
        gradient.setColorAt(1.0, QColor.fromHsv(0, 255, 255, 200))  # Низ (Красный)
        
        self.area_series.setBrush(QBrush(gradient))
        self.area_series.setPen(QPen(Qt.PenStyle.NoPen))
        
        # Пики
        self.peaks_top = QLineSeries()
        self.peaks_bottom = QLineSeries()
        peak_pen = QPen(QColor(255, 255, 255, 200))
        peak_pen.setWidth(1)
        self.peaks_top.setPen(peak_pen)
        self.peaks_bottom.setPen(peak_pen)
        
        self.chart.addSeries(self.area_series)
        self.chart.addSeries(self.peaks_top)
        self.chart.addSeries(self.peaks_bottom)
        
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, 8000)
        self.axis_x.setVisible(False)
        
        self.axis_y = QValueAxis()
        self.axis_y.setRange(-1100, 1100)
        self.axis_y.setVisible(False)
        
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        
        for s in [self.area_series, self.peaks_top, self.peaks_bottom]:
            s.attachAxis(self.axis_x)
            s.attachAxis(self.axis_y)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        # self.chart_view.setViewport(QOpenGLWidget())
        
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        self.chart_view.setStyleSheet("background: transparent; border: none;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.updateStream()
    
    def __process__(self):
        if self.stream is None: return
        
        try:
            # Читаем меньше CHUNK, если RATE высокий, чтобы не копить задержку
            raw_data = self.stream.read(CHUNK, exception_on_overflow=False)
            audio = np.frombuffer(raw_data, dtype=np.int16)
        except Exception:
            return
        
        max_amp = np.max(np.abs(audio))
        if max_amp < SILENCE_THRESHOLD:
            self.silence_counter += 1
            if self.silence_counter > SILENCE_DURATION:
                # Очистка через replace пустым списком быстрее, чем clear()
                self.series_top.replace([])
                self.series_bottom.replace([])
                return
        else:
            self.silence_counter = 0
        
        # Окно Хэннинга уберет "шум" по краям FFT (сделает график чище)
        window = np.hanning(len(audio))
        fft = np.abs(np.fft.fft(audio * window)[: CHUNK // 2])
        freqs = np.fft.fftfreq(CHUNK, 1 / RATE)[: CHUNK // 2]
        
        # Логарифмическая нормализация (визуально приятнее)
        fft_norm = np.log1p(fft)
        max_val = np.max(fft_norm)
        if max_val > 0:
            fft_norm = (fft_norm / max_val) * 1000
        
        self.smoothing_buffer.append(fft_norm)
        smoothed = np.mean(self.smoothing_buffer, axis=0)
        
        self.peak_data = np.maximum(self.peak_data, smoothed)
        self.peak_data = np.maximum(0, self.peak_data - self.fall_speed)
        
        # Подготовка данных (сокращаем количество точек в 2 раза для FPS)
        step = 2
        p_t = [QPointF(freqs[i], smoothed[i]) for i in range(0, len(freqs), step)]
        p_b = [QPointF(freqs[i], -smoothed[i]) for i in range(0, len(freqs), step)]
        
        pk_t = [QPointF(freqs[i], self.peak_data[i] + 10) for i in range(0, len(freqs), step)]
        pk_b = [QPointF(freqs[i], -self.peak_data[i] - 10) for i in range(0, len(freqs), step)]
        
        # Обновление
        self.series_top.replace(p_t)
        self.series_bottom.replace(p_b)
        self.peaks_top.replace(pk_t)
        self.peaks_bottom.replace(pk_b)
        
        super().__process__()
    
    def updateStream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        try:
            self.stream = self.p.open(
                format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK,
                input_device_index=self.idx_device
            )
        except:
            self.stream = None
    
    def closeEvent(self, event):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        event.accept()
    
    @classmethod
    def createSettingWidget(cls, window, name_plugin, parent):
        return CustomPluginWindow(window, name_plugin, parent)
    
    def load_status(self, status):
        super().load_status(status)
        self.idx_device = status.get("idx_device", None)
    
    def save_status(self):
        ldt = super().save_status()
        ldt.set("idx_device", self.idx_device)
        return ldt
