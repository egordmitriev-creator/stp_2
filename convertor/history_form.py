import tkinter as tk
from tkinter import ttk

class HistoryForm:
    """Форма для отображения истории (аналог Form2 в C#)"""
    
    def __init__(self, history):
        self.window = tk.Toplevel()
        self.window.title("История преобразований")
        self.window.geometry("600x400")
        self.window.resizable(True, True)
        
        # Создание текстового поля для отображения истории
        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(frame, text="История преобразований", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Текстовое поле с прокруткой (аналог textBox1 в C#)
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_box = tk.Text(text_frame, wrap=tk.WORD, 
                                yscrollcommand=scrollbar.set,
                                font=("Courier", 10))
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.text_box.yview)
        
        # Кнопка закрытия
        ttk.Button(frame, text="Закрыть", 
                  command=self.window.destroy).pack(pady=10)
        
        # Заполнение истории
        self.display_history(history)
    
    def display_history(self, history):
        """Отображение истории (аналог цикла в C#)"""
        if history.count() == 0:
            self.text_box.insert(tk.END, "История пуста")
            return
        
        for i in range(history.count()):
            record = history[i]
            self.text_box.insert(tk.END, f"{i+1}. {record}\n\n")
        
        # Отключаем редактирование
        self.text_box.config(state=tk.DISABLED)