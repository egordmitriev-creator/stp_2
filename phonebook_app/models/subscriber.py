# models/subscriber.py
class Subscriber:
    """Модель данных абонента"""
    
    def __init__(self, name: str, phone: str):
        self.name = name.strip()
        self.phone = phone.strip()
    
    def __str__(self) -> str:
        return f"{self.name}: {self.phone}"
    
    def __repr__(self) -> str:
        return f"Subscriber(name={self.name}, phone={self.phone})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Subscriber):
            return self.name == other.name and self.phone == other.phone
        return False
    
    def __lt__(self, other) -> bool:
        """Для сортировки по имени"""
        return self.name.lower() < other.name.lower()
    
    def to_dict(self) -> dict:
        """Преобразование в словарь для сериализации"""
        return {"name": self.name, "phone": self.phone}
    
    @classmethod
    def from_dict(cls, data: dict):
        """Создание из словаря"""
        return cls(data["name"], data["phone"])