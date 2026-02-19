import tkinter as tk
from tkinter import ttk

class AboutBox:
    """Форма "О программе" (аналог AboutBox1 в C#)"""
    
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("О программе")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Основной фрейм
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(frame, text="Конвертер p1_p2", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 10))
        
        # Версия
        ttk.Label(frame, text="Версия 1.0", 
                 font=("Arial", 10)).pack(pady=(0, 20))
        
        # Описание
        description = """Программа для преобразования чисел между различными системами счисления.

Поддерживаются системы счисления с основанием от 2 до 16.

Возможности:
• Преобразование действительных чисел
• Редактирование чисел с помощью кнопок или клавиатуры
• Просмотр истории преобразований
• Контекстная помощь

Разработано в рамках курса
"Объектно-ориентированное программирование" """
        
        ttk.Label(frame, text=description, justify=tk.CENTER,
                 wraplength=350).pack(pady=10)
        
        # Кнопка закрытия
        ttk.Button(frame, text="OK", width=15,
                  command=self.window.destroy).pack(pady=20)