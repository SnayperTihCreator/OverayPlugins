import pulsectl
from typing import List, Dict
from .base import VolumeControl


class LinuxVolumeHandler(VolumeControl):
    def __init__(self):
        self.pulse = pulsectl.Pulse('volume-mixer')
    
    def get_applications(self) -> List[Dict]:
        apps = []
        
        # Добавляем системную громкость
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        apps.append({
            'id': 'system',
            'name': 'System Volume',
            'volume': sink.volume.value_flat * 100,
            'muted': bool(sink.mute),
            'sink': sink,
            'system': True
        })
        
        # Добавляем приложения
        for sink in self.pulse.sink_input_list():
            apps.append({
                'id': str(sink.index),
                'name': sink.proplist.get('application.name', 'Unknown'),
                'volume': sink.volume.value_flat * 100,
                'muted': bool(sink.mute),
                'sink': sink
            })
        
        return apps
    
    def set_application_volume(self, app_id: str, volume: float):
        for app in self.get_applications():
            if app['id'] == app_id and 'sink' in app:
                self.pulse.volume_set_all_chans(app['sink'], volume / 100)
                break
    
    def set_application_mute(self, app_id: str, muted: bool):
        for app in self.get_applications():
            if app['id'] == app_id and 'sink' in app:
                self.pulse.mute(app['sink'], muted)
                break
    
    def get_system_volume(self) -> float:
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        return sink.volume.value_flat * 100
    
    def set_system_volume(self, volume: float):
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        self.pulse.volume_set_all_chans(sink, volume / 100)
    
    def get_system_mute(self) -> bool:
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        return bool(sink.mute)
    
    def set_system_mute(self, muted: bool):
        sink = self.pulse.get_sink_by_name(self.pulse.server_info().default_sink_name)
        self.pulse.mute(sink, muted)
    
    def close(self):
        self.pulse.close()