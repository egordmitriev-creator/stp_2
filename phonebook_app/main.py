# main.py
import tkinter as tk
from utils.file_manager import FileManager
from models.subscriber_list import SubscriberList
from views.interface import PhoneBookInterface

class PhoneBookApp:
    """Основное приложение, связывающее все компоненты"""
    
    def __init__(self):
        # Создаем компоненты согласно диаграмме
        self.file_manager = FileManager("data/phonebook.dat")  # Файл
        self.subscriber_list = SubscriberList()                # СписокАбонентов
        
        # Устанавливаем связи между компонентами
        self.subscriber_list.set_file_manager(self.file_manager)
        
        # Создаем графический интерфейс
        self.root = tk.Tk()
        self.interface = PhoneBookInterface(self.root)         # Интерфейс
        
        # Устанавливаем связи интерфейса с другими компонентами
        self.interface.set_subscriber_list(self.subscriber_list)
        self.interface.set_file_manager(self.file_manager)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

def main():
    """Точка входа в приложение"""
    app = PhoneBookApp()
    app.run()

if __name__ == "__main__":
    main()