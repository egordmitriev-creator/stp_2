from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Record:
    """
    Структура для хранения одной записи в истории
    Аналог struct в C#
    """
    p1: int
    p2: int
    number1: str
    number2: str
    timestamp: Optional[str] = None
    
    def __init__(self, p1: int, p2: int, n1: str, n2: str):
        self.p1 = p1
        self.p2 = p2
        self.number1 = n1
        self.number2 = n2
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self) -> str:
        return (f"[{self.timestamp}] "
                f"{self.number1} (осн.{self.p1}) -> "
                f"{self.number2} (осн.{self.p2})")
    
    def to_string(self) -> str:
        return self.__str__()


class History:
    """
    Класс для хранения истории преобразований чисел
    """
    
    def __init__(self):
        self._records: List[Record] = []
    
    def add_record(self, p1: int, p2: int, n1: str, n2: str) -> None:
        record = Record(p1, p2, n1, n2)
        self._records.append(record)
    
    def get_record(self, index: int) -> Optional[Record]:
        """Получить запись по индексу (поддерживает отрицательные индексы)"""
        if not self._records:
            return None
        
        # Преобразуем отрицательный индекс в положительный
        if index < 0:
            index = len(self._records) + index
        
        if 0 <= index < len(self._records):
            return self._records[index]
        return None
    
    def __getitem__(self, index: int) -> Record:
        """Перегрузка [] для доступа по индексу (поддерживает отрицательные индексы)"""
        if not self._records:
            raise IndexError("История пуста")
        
        # Преобразуем отрицательный индекс в положительный
        if index < 0:
            index = len(self._records) + index
        
        if 0 <= index < len(self._records):
            return self._records[index]
        raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._records)-1})")
    
    def clear(self) -> None:
        self._records.clear()
    
    def count(self) -> int:
        return len(self._records)
    
    def __len__(self) -> int:
        return len(self._records)
    
    def get_all_records(self) -> List[Record]:
        return self._records.copy()
    
    def print_history(self) -> None:
        if not self._records:
            print("История пуста")
            return
        
        print("\n" + "=" * 60)
        print("ИСТОРИЯ ПРЕОБРАЗОВАНИЙ")
        print("=" * 60)
        for i, record in enumerate(self._records):
            print(f"{i+1}. {record}")
        print("=" * 60)
    
    def get_last_record(self) -> Optional[Record]:
        """Получить последнюю запись"""
        if self._records:
            return self._records[-1]
        return None