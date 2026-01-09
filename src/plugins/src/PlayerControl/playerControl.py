from PySide6.QtWidgets import QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor

from oapi import Config, OWindow, modulateIcon

from .utils import fakeInput, PlayerCode
from .config import PlayerControlConfig
# noinspection PyUnresolvedReferences
from . import icons_rc


class PlayerControl(OWindow):
    def __init__(self, parent=None):
        super().__init__(Config("PlayerControl", "window", scheme=PlayerControlConfig), parent)
        self.runs = True
        self.icons = None
        
        self.shortcut("play/pause media", "toggle_play")
        sizeIcon = QSize(1, 1) * self.config.data.icons.size
        
        self.box = QVBoxLayout()
        self.central_widget.setLayout(self.box)
        
        self.btn_play_pause = QPushButton()
        self.btn_play_pause.setMinimumHeight(self.config.data.icons.size+2)
        self.btn_play_pause.setIconSize(sizeIcon)
        self.btn_play_pause.pressed.connect(lambda: self.toggle_play_pause())
        
        self.btn_next_track = QPushButton()
        self.btn_next_track.setMinimumHeight(self.config.data.icons.size + 2)
        self.btn_next_track.setIconSize(sizeIcon)
        self.btn_next_track.pressed.connect(
            lambda: self.send_media_key(PlayerCode.NEXT_TRACK)
        )
        
        self.btn_prev_track = QPushButton()
        self.btn_prev_track.setMinimumHeight(self.config.data.icons.size + 2)
        self.btn_prev_track.setIconSize(sizeIcon)
        self.btn_prev_track.pressed.connect(
            lambda: self.send_media_key(PlayerCode.PREV_TRACK)
        )
        
        self.btn_vol_up = QPushButton()
        self.btn_vol_up.setMinimumHeight(self.config.data.icons.size + 2)
        self.btn_vol_up.setIconSize(sizeIcon)
        self.btn_vol_up.pressed.connect(
            lambda: self.send_media_key(PlayerCode.VOLUME_UP)
        )
        
        self.btn_vol_down = QPushButton()
        self.btn_vol_down.setMinimumHeight(self.config.data.icons.size + 2)
        self.btn_vol_down.setIconSize(sizeIcon)
        self.btn_vol_down.pressed.connect(
            lambda: self.send_media_key(PlayerCode.VOLUME_DOWN)
        )
        
        self.btn_vol_mute = QPushButton()
        self.btn_vol_mute.setMinimumHeight(self.config.data.icons.size + 2)
        self.btn_vol_mute.setIconSize(sizeIcon)
        self.btn_vol_mute.pressed.connect(
            lambda: self.send_media_key(PlayerCode.VOLUME_MUTE)
        )
        
        self.box.addWidget(self.btn_next_track)
        self.box.addWidget(self.btn_play_pause)
        self.box.addWidget(self.btn_prev_track)
        
        self.box.addWidget(self.btn_vol_up)
        self.box.addWidget(self.btn_vol_down)
        self.box.addWidget(self.btn_vol_mute)
        
        self.header = QPushButton()
        self.header.setMinimumHeight(self.config.data.icons.size + 2)
        self.header.setObjectName("Header")
        self.header.setIconSize(sizeIcon)
        self.header.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        self.box.insertWidget(0, self.header)
        self.updateIcons()
        
        self.playing = fakeInput.isPlayingMusic()
        self.set_state_play_pause(self.playing)
        
    def updateIcons(self):
        self.btn_play_pause.setIcon(self.getIcon("play", self.config.data.icons.modulate))
        self.btn_next_track.setIcon(self.getIcon("track_next", self.config.data.icons.modulate))
        self.btn_prev_track.setIcon(self.getIcon("track_prev", self.config.data.icons.modulate))
        self.btn_vol_up.setIcon(self.getIcon("volume_up", self.config.data.icons.modulate))
        self.btn_vol_down.setIcon(self.getIcon("volume_down", self.config.data.icons.modulate))
        self.btn_vol_mute.setIcon(self.getIcon("volume_mute", self.config.data.icons.modulate))
        self.header.setIcon(self.getIcon("header", self.config.data.icons.modulate))
    
    def shortcut_run(self, name):
        match name:
            case "toggle_play" if not self.runs:
                self.playing = not self.playing
                self.set_state_play_pause(self.playing)
        if hasattr(self, "runs") and self.runs:
            self.runs = False
    
    def set_state_play_pause(self, state):
        icon = self.getIcon("play" if not state else "pause", self.config.data.icons.modulate)
        self.btn_play_pause.setIcon(icon)
        
    def send_media_key(self, keycode):
        fakeInput.send_key(keycode)
    
    def toggle_play_pause(self):
        self.runs = True
        fakeInput.send_key(PlayerCode.PLAY_PAUSE)
    
    @staticmethod
    def getIcon(name, color):
        return modulateIcon(QIcon(f":/player_control/{name}.png"), QColor(color))
    
    def reload_config(self):
        super().reload_config()
        self.updateIcons()
        
        
        
