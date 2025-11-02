from typing import Any, Callable, Optional, Union, Self
from enum import IntEnum, auto
import inspect
import weakref

from attrs import define, field
from colorama import colorama_text, Fore

from .utils import check_type_simple


class ConnectionType(IntEnum):
    Default = auto()
    OneShot = auto()


@define(eq=True)
class Slot:
    owner: Any = field(eq=False, repr=False)
    handler: Callable
    conType: ConnectionType
    
    _runnable: weakref.ref = field(repr=False, init=False)
    
    def __attrs_post_init__(self):
        if inspect.ismethod(self.handler):
            self._runnable = weakref.WeakMethod(self.handler)
        else:
            self._runnable = weakref.ref(self.handler)
    
    def __call__(self, *args, **kwargs):
        slot = self._runnable()
        if slot is not None:
            return slot(*args, **kwargs)
        return None
    
    def is_alive(self) -> bool:
        """Проверяет, жив ли еще слот"""
        return self._runnable() is not None


@define
class SignalInstance:
    _owner: Any
    _name: str
    _types: tuple[type | str, ...]
    
    _slots: list[Slot] = field(factory=list, init=False, repr=False)
    _emitting: bool = field(default=False, init=False, repr=False)
    
    def connect(self, handler: Callable, conType: ConnectionType = ConnectionType.Default):
        """Подключает обработчик к сигналу"""
        if not callable(handler):
            raise TypeError(f"Slot must be callable, got {type(handler)}")
        
        slot = Slot(self._owner, handler, conType)
        if slot not in self._slots:
            self._slots.append(slot)
    
    def disconnect(self, handler: Callable):
        """Отключает обработчик от сигнала"""
        self._slots = [slot for slot in self._slots if slot.handler != handler]
    
    def disconnect_all(self):
        """Отключает все обработчики"""
        self._slots.clear()
    
    def emit(self, *args, **kwargs):
        """Испускает сигнал с аргументами"""
        # Проверка типов
        if self._types and len(args) != len(self._types):
            raise TypeError(f"Signal {self._name} expected {len(self._types)} arguments, got {len(args)}")
        
        for i, (arg, expected_type) in enumerate(zip(args, self._types)):
            if not check_type_simple(arg, expected_type):
                raise TypeError(f"Signal {self._name} argument {i} must be {expected_type}, got {type(arg)}")
        
        # Защита от рекурсивных вызовов
        if self._emitting:
            return
        
        self._emitting = True
        try:
            # Создаем копию для безопасной итерации
            slots_to_remove = []
            
            for slot in self._slots[:]:
                # Проверяем, жив ли еще слот
                if not slot.is_alive():
                    slots_to_remove.append(slot)
                    continue
                
                try:
                    slot(*args, **kwargs)
                except Exception as e:
                    with colorama_text():
                        print(Fore.RED + f"Error in slot {slot.handler} for signal {self._name}: {e}")
                
                # Удаляем одноразовые слоты
                if slot.conType == ConnectionType.OneShot:
                    slots_to_remove.append(slot)
            
            # Удаляем мертвые и одноразовые слоты
            for slot in slots_to_remove:
                if slot in self._slots:
                    self._slots.remove(slot)
        
        finally:
            self._emitting = False
    
    def __call__(self, *args, **kwargs):
        self.emit(*args, **kwargs)
    
    @property
    def slots(self):
        """Возвращает копию списка слотов"""
        return self._slots.copy()
    
    @property
    def is_connected(self) -> bool:
        """Проверяет, есть ли подключенные слоты"""
        return len(self._slots) > 0


class Signal:
    """Дескриптор для создания сигналов в классах"""
    
    def __init__(self, *types: Union[type, str]):
        self._types = types
        self._name: Optional[str] = None
    
    def __set_name__(self, owner, name):
        self._name = name
        self._signal_name = f"__signal_instance_{self._name}__"
    
    def __get__(self, instance, owner) -> SignalInstance | Self:
        if instance is None:
            return self
        
        if not hasattr(instance, self._signal_name):
            signal_instance = SignalInstance(instance, self._name, self._types)
            setattr(instance, self._signal_name, signal_instance)
        
        return getattr(instance, self._signal_name)
    
    def __set__(self, instance, value):
        raise AttributeError("Signals cannot be reassigned")
    
    # Методы для статического доступа (НАДО)
    def emit(self, *args, **kwargs):
        raise RuntimeError("Signal must be accessed through class instance")
    
    def __call__(self, *args, **kwargs):
        raise RuntimeError("Signal must be accessed through class instance")
    
    def connect(self, handler: Callable, conType: ConnectionType = ConnectionType.Default):
        raise RuntimeError("Signal must be accessed through class instance")
    
    def disconnect(self, handler: Callable):
        raise RuntimeError("Signal must be accessed through class instance")

__all__ = ["Signal"]