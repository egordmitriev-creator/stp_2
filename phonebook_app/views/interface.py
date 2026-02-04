# views/interface.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

class PhoneBookInterface:
    """
    Граничный класс для взаимодействия с пользователем.
    Аналог 'Интерфейс' из диаграммы.
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Телефонная книга")
        self.root.geometry("800x600")
        
        # Ссылки на другие компоненты (будут установлены позже)
        self._subscriber_list = None
        self._file_manager = None
        
        self._setup_ui()
    
    def set_subscriber_list(self, subscriber_list):
        """Установка связи с СписокАбонентов"""
        self._subscriber_list = subscriber_list
    
    def set_file_manager(self, file_manager):
        """Установка связи с Файл"""
        self._file_manager = file_manager
    
    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка расширения
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        
        # Заголовок
        title = ttk.Label(main_container, 
                         text="Телефонная книга", 
                         font=("Helvetica", 24, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Панель ввода данных
        input_frame = ttk.LabelFrame(main_container, text="Данные абонента", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        ttk.Label(input_frame, text="Телефон:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(input_frame, textvariable=self.phone_var, width=40)
        self.phone_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=5)
        
        # Панель кнопок
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 15))
        
        self.add_btn = ttk.Button(button_frame, text="Добавить", 
                                 command=self._on_add)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.edit_btn = ttk.Button(button_frame, text="Изменить", 
                                  command=self._on_edit, state=tk.DISABLED)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(button_frame, text="Удалить", 
                                    command=self._on_delete, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.search_btn = ttk.Button(button_frame, text="Найти", 
                                    command=self._on_search)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="Очистить книгу", 
                                   command=self._on_clear)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Панель поиска
        search_frame = ttk.Frame(main_container)
        search_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(search_frame, text="Поиск по имени:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda e: self._on_search())
        
        # Список абонентов
        list_frame = ttk.LabelFrame(main_container, text="Абоненты", padding="10")
        list_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # TreeView для отображения
        self.tree = ttk.Treeview(list_frame, columns=('name', 'phone'), 
                                show='headings', height=15)
        self.tree.heading('name', text='Имя')
        self.tree.heading('phone', text='Телефон')
        self.tree.column('name', width=350)
        self.tree.column('phone', width=200)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Привязка события выбора
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        
        # Статусная строка
        self.status_var = tk.StringVar(value="Готово")
        status_bar = ttk.Label(main_container, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Меню
        self._create_menu()
        
        # Загрузка данных при запуске
        self.root.after(100, self._load_initial_data)
    
    def _create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить", command=self._on_load)
        file_menu.add_command(label="Сохранить", command=self._on_save)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self._show_about)
    
    def _load_initial_data(self):
        """Загрузка данных при старте приложения"""
        if self._subscriber_list and self._file_manager:
            self._subscriber_list.load_from_file()
            self._update_display()
            self.status_var.set("Данные загружены")
    
    def _update_display(self, subscribers=None):
        """Обновление отображения списка"""
        # Очистка текущего списка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение данных
        if subscribers is None and self._subscriber_list:
            subscribers = self._subscriber_list.get_all()
        
        # Добавление данных
        if subscribers:
            for subscriber in subscribers:
                self.tree.insert('', tk.END, values=(subscriber.name, subscriber.phone))
    
    def _clear_input(self):
        """Очистка полей ввода"""
        self.name_var.set("")
        self.phone_var.set("")
    
    def _on_tree_select(self, event):
        """Обработка выбора в дереве"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.name_var.set(item['values'][0])
            self.phone_var.set(item['values'][1])
            self.edit_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.edit_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
    
    def _on_add(self):
        """Обработка добавления абонента"""
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        
        if not name or not phone:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        
        if self._subscriber_list and self._subscriber_list.add(name, phone):
            self._update_display()
            self._clear_input()
            self.status_var.set(f"Абонент '{name}' добавлен")
            
            # Автосохранение
            if self._subscriber_list:
                self._subscriber_list.save_to_file()
        else:
            messagebox.showwarning("Ошибка", "Не удалось добавить абонента!")
    
    def _on_edit(self):
        """Обработка редактирования абонента"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите абонента для редактирования!")
            return
        
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        
        if not name or not phone:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        
        # Получаем индекс выбранного элемента
        item_id = selection[0]
        children = self.tree.get_children()
        if item_id in children:
            index = children.index(item_id)
            if self._subscriber_list and self._subscriber_list.edit(index, name, phone):
                self._update_display()
                self._clear_input()
                self.status_var.set(f"Абонент обновлен")
                
                # Автосохранение
                if self._subscriber_list:
                    self._subscriber_list.save_to_file()
            else:
                messagebox.showwarning("Ошибка", "Не удалось обновить абонента!")
    
    def _on_delete(self):
        """Обработка удаления абонента"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите абонента для удаления!")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить выбранного абонента?"):
            return
        
        # Получаем индекс выбранного элемента
        item_id = selection[0]
        children = self.tree.get_children()
        if item_id in children:
            index = children.index(item_id)
            if self._subscriber_list and self._subscriber_list.delete(index):
                self._update_display()
                self._clear_input()
                self.status_var.set(f"Абонент удален")
                
                # Автосохранение
                if self._subscriber_list:
                    self._subscriber_list.save_to_file()
            else:
                messagebox.showwarning("Ошибка", "Не удалось удалить абонента!")
    
    def _on_search(self):
        """Обработка поиска"""
        search_text = self.search_var.get().strip()
        if not search_text:
            self._update_display()
            return
        
        if self._subscriber_list:
            results = self._subscriber_list.search(search_text)
            self._update_display(results)
            self.status_var.set(f"Найдено: {len(results)} записей")
    
    def _on_clear(self):
        """Обработка очистки книги"""
        if not messagebox.askyesno("Подтверждение", 
                                  "Очистить всю телефонную книгу?"):
            return
        
        if self._subscriber_list:
            self._subscriber_list.clear()
            self._update_display()
            self._clear_input()
            self.status_var.set("Телефонная книга очищена")
            
            # Автосохранение
            self._subscriber_list.save_to_file()
    
    def _on_save(self):
        """Обработка сохранения"""
        if self._subscriber_list:
            if self._subscriber_list.save_to_file():
                self.status_var.set("Данные сохранены")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить данные!")
    
    def _on_load(self):
        """Обработка загрузки"""
        if self._subscriber_list:
            if self._subscriber_list.load_from_file():
                self._update_display()
                self.status_var.set("Данные загружены")
            else:
                messagebox.showwarning("Предупреждение", 
                                      "Не удалось загрузить данные!")
    
    def _show_about(self):
        """Показать информацию о программе"""
        about_text = """Телефонная книга
        
Версия 1.0
Разработка приложения под macOS
в технологии ООП на Python

Функциональность:
• Добавление/редактирование/удаление абонентов
• Поиск по имени
• Сортировка по имени
• Сохранение в файл"""
        
        messagebox.showinfo("О программе", about_text)