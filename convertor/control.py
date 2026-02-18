import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from enum import Enum
from editor import Editor
from history import History
from convers.conver_10_p import Conver_10_P
from convers.conver_p_10 import Conver_P_10
import math

class State(Enum):
    РЕДАКТИРОВАНИЕ = "Редактирование"
    ПРЕОБРАЗОВАНО = "Преобразовано"


class Control_:
    # Константы по умолчанию
    DEFAULT_PIN = 10      # Основание исходной системы счисления по умолчанию
    DEFAULT_POUT = 16     # Основание результирующей системы счисления по умолчанию
    DEFAULT_ACCURACY = 10 # Точность по умолчанию
    
    # Коды команд
    CMD_EXECUTE = 19  # Команда выполнения преобразования
    
    def __init__(self):
        # Создание объектов
        self._editor = Editor()      # Редактор
        self._history = History()    # История
        
        # Свойства
        self._pin = self.DEFAULT_PIN      # Основание исходной системы счисления
        self._pout = self.DEFAULT_POUT    # Основание результирующей системы счисления
        self._state = State.РЕДАКТИРОВАНИЕ  # Состояние
        
        # Дополнительные поля для точности
        self._default_accuracy = self.DEFAULT_ACCURACY
    
    # Свойства (аналог свойств в C#)
    @property
    def pin(self) -> int:
        return self._pin
    
    @pin.setter
    def pin(self, value: int):
        if 2 <= value <= 16:
            self._pin = value
        else:
            raise ValueError(f"Основание должно быть в диапазоне 2..16, получено {value}")
    
    @property
    def pout(self) -> int:
        return self._pout
    
    @pout.setter
    def pout(self, value: int):
        if 2 <= value <= 16:
            self._pout = value
        else:
            raise ValueError(f"Основание должно быть в диапазоне 2..16, получено {value}")
    
    @property
    def state(self) -> State:
        return self._state
    
    @state.setter
    def state(self, value: State):
        self._state = value
    
    @property
    def editor(self) -> Editor:
        return self._editor
    
    @property
    def history(self) -> History:
        return self._history
    
    def _calculate_accuracy(self) -> int:
        if self._editor.acc() == 0:
            return 0
        
        try:
            # Формула: round(ed.Acc() * log(Pin) / log(Pout) + 0.5)
            result = int(round(
                self._editor.acc() * math.log(self._pin) / math.log(self._pout) + 0.5
            ))
            return max(1, result)  # Минимум 1 разряд
        except (ValueError, ZeroDivisionError):
            return self._default_accuracy
    
    def do_command(self, command: int) -> str:
        # Команда выполнения преобразования
        if command == self.CMD_EXECUTE:
            try:
                # Проверяем, что число не пустое
                if not self._editor.number or self._editor.number == "0":
                    return "0"
                
                # 1. Преобразование из p1 в десятичную систему
                decimal_value = Conver_P_10.dval(self._editor.number, self._pin)
                
                # 2. Расчет точности
                accuracy = self._calculate_accuracy()
                
                # 3. Преобразование из десятичной в p2
                result = Conver_10_P.do(decimal_value, self._pout, accuracy)
                
                # 4. Изменение состояния
                self._state = State.ПРЕОБРАЗОВАНО
                
                # 5. Сохранение в историю
                self._history.add_record(
                    self._pin, 
                    self._pout, 
                    self._editor.number, 
                    result
                )
                
                return result
                
            except Exception as e:
                # В случае ошибки возвращаем исходное число
                self._state = State.РЕДАКТИРОВАНИЕ
                return self._editor.number
        
        # Команды редактирования
        else:
            self._state = State.РЕДАКТИРОВАНИЕ
            return self._editor.do_edit(command, self._pin)
    
    def reset(self) -> None:
        self._editor.clear()
        self._state = State.РЕДАКТИРОВАНИЕ
    
    def get_last_record(self) -> str:
        last_record = self._history.get_last_record()
        if last_record:
            return str(last_record)
        return "История пуста"
    
    def __str__(self) -> str:
        return (f"Control_[pin={self._pin}, pout={self._pout}, "
                f"state={self._state.value}, number={self._editor.number}]")