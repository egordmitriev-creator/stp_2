# models/subscriber_list.py
from typing import List, Dict, Optional
from models.subscriber import Subscriber

class SubscriberList:
    """
    Класс для работы со списком абонентов в оперативной памяти.
    Аналог 'СписокАбонентов' из диаграммы.
    """
    
    def __init__(self):
        self._subscribers = []  # Хранение в отсортированном виде
        self._file_manager = None
    
    def set_file_manager(self, file_manager):
        """Установка менеджера файлов для работы с диском"""
        self._file_manager = file_manager
    
    def add(self, name: str, phone: str) -> bool:
        """Добавление нового абонента"""
        if not name or not phone:
            return False
        
        new_subscriber = Subscriber(name, phone)
        
        # Проверка на уникальность
        for subscriber in self._subscribers:
            if subscriber == new_subscriber:
                return False
        
        self._subscribers.append(new_subscriber)
        self._sort_subscribers()
        return True
    
    def edit(self, index: int, name: str, phone: str) -> bool:
        """Редактирование абонента по индексу"""
        if 0 <= index < len(self._subscribers):
            self._subscribers[index] = Subscriber(name, phone)
            self._sort_subscribers()
            return True
        return False
    
    def delete(self, index: int) -> bool:
        """Удаление абонента по индексу"""
        if 0 <= index < len(self._subscribers):
            del self._subscribers[index]
            return True
        return False
    
    def delete_by_name(self, name: str) -> bool:
        """Удаление абонента по имени"""
        for i, subscriber in enumerate(self._subscribers):
            if subscriber.name == name:
                del self._subscribers[i]
                return True
        return False
    
    def search(self, name: str) -> List[Subscriber]:
        """Поиск абонентов по имени"""
        name_lower = name.lower()
        return [s for s in self._subscribers if name_lower in s.name.lower()]
    
    def get_all(self) -> List[Subscriber]:
        """Получение всех абонентов"""
        return self._subscribers.copy()
    
    def clear(self):
        """Очистка списка абонентов"""
        self._subscribers.clear()
    
    def _sort_subscribers(self):
        """Сортировка абонентов по имени"""
        self._subscribers.sort()
    
    def save_to_file(self) -> bool:
        """Сохранение данных в файл через FileManager"""
        if not self._file_manager:
            return False
        
        data = [subscriber.to_dict() for subscriber in self._subscribers]
        return self._file_manager.save(data)
    
    def load_from_file(self) -> bool:
        """Загрузка данных из файла через FileManager"""
        if not self._file_manager:
            return False
        
        data = self._file_manager.load()
        self._subscribers.clear()
        
        for item in data:
            subscriber = Subscriber.from_dict(item)
            self._subscribers.append(subscriber)
        
        self._sort_subscribers()
        return True
    
    def __len__(self) -> int:
        return len(self._subscribers)
    
    def __getitem__(self, index: int) -> Subscriber:
        return self._subscribers[index]