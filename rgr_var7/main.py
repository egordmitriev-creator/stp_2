import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QGridLayout,
                             QLabel, QMenuBar, QMenu, QAction, QMessageBox, 
                             QDialog, QTextEdit, QVBoxLayout as QVBoxDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QClipboard


class PNumber:
    """Класс для работы с p-ичными числами (основание 2-16)"""
    
    DIGITS = '0123456789ABCDEF'
    
    def __init__(self, value='0', base=10, mode='real'):
        """
        Инициализация p-ичного числа
        value: строковое представление числа
        base: основание системы счисления (2-16)
        mode: режим работы ('integer' или 'real')
        """
        self.base = base
        self.mode = mode
        self.value = self._normalize(value)
    
    def _normalize(self, value):
        """Нормализация строки числа"""
        if not value:
            return '0'
        
        # Заменяем запятую на точку
        value = value.replace(',', '.')
        
        # Проверка на отрицательное число
        is_negative = value.startswith('-')
        if is_negative:
            value = value[1:]
        
        # Разделяем целую и дробную части
        parts = value.split('.')
        integer_part = parts[0] if parts[0] else '0'
        fractional_part = parts[1] if len(parts) > 1 else ''
        
        # Проверяем допустимые цифры для текущего основания
        valid_digits = self.DIGITS[:self.base]
        integer_part = ''.join([c for c in integer_part if c in valid_digits])
        fractional_part = ''.join([c for c in fractional_part if c in valid_digits])
        
        if not integer_part and not fractional_part:
            return '0'
        
        integer_part = integer_part or '0'
        
        # Убираем ведущие нули
        integer_part = integer_part.lstrip('0') or '0'
        
        # Формируем результат
        result = ('-' if is_negative else '') + integer_part
        if fractional_part and self.mode == 'real':
            # Убираем trailing zeros
            fractional_part = fractional_part.rstrip('0')
            if fractional_part:
                result += '.' + fractional_part
        
        return result
    
    def to_decimal(self):
        """Преобразование в десятичное число (float)"""
        try:
            is_negative = self.value.startswith('-')
            val = self.value[1:] if is_negative else self.value
            
            if '.' in val:
                int_part, frac_part = val.split('.')
            else:
                int_part, frac_part = val, ''
            
            # Перевод целой части
            decimal = 0
            for i, digit in enumerate(reversed(int_part)):
                decimal += int(digit, self.base) * (self.base ** i)
            
            # Перевод дробной части
            if frac_part:
                for i, digit in enumerate(frac_part, 1):
                    decimal += int(digit, self.base) * (self.base ** -i)
            
            return -decimal if is_negative else decimal
        except:
            return 0
    
    def from_decimal(self, decimal_value):
        """Создание p-ичного числа из десятичного"""
        if decimal_value == 0:
            return PNumber('0', self.base, self.mode)
        
        is_negative = decimal_value < 0
        decimal_value = abs(decimal_value)
        
        # Перевод целой части
        integer_part = int(decimal_value)
        if integer_part == 0:
            int_str = '0'
        else:
            int_str = ''
            temp = integer_part
            while temp > 0:
                int_str = self.DIGITS[temp % self.base] + int_str
                temp //= self.base
        
        # Перевод дробной части
        fractional_part = decimal_value - integer_part
        if fractional_part == 0 or self.mode == 'integer':
            result = ('-' if is_negative else '') + int_str
        else:
            frac_str = ''
            frac = fractional_part
            # Ограничим 10 знаками после запятой
            for _ in range(10):
                frac *= self.base
                digit = int(frac)
                if digit >= self.base:
                    break
                frac_str += self.DIGITS[digit]
                frac -= digit
                if abs(frac) < 1e-10:
                    break
            
            # Убираем trailing zeros
            frac_str = frac_str.rstrip('0')
            if frac_str:
                result = ('-' if is_negative else '') + int_str + '.' + frac_str
            else:
                result = ('-' if is_negative else '') + int_str
        
        return PNumber(result, self.base, self.mode)
    
    def __add__(self, other):
        """Сложение"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")
        a_dec, b_dec = self.to_decimal(), other.to_decimal()
        return self.from_decimal(a_dec + b_dec)
    
    def __sub__(self, other):
        """Вычитание"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")
        a_dec, b_dec = self.to_decimal(), other.to_decimal()
        return self.from_decimal(a_dec - b_dec)
    
    def __mul__(self, other):
        """Умножение"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")
        a_dec, b_dec = self.to_decimal(), other.to_decimal()
        return self.from_decimal(a_dec * b_dec)
    
    def __truediv__(self, other):
        """Деление"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")
        b_dec = other.to_decimal()
        if abs(b_dec) < 1e-15:
            raise ZeroDivisionError("Деление на ноль")
        a_dec = self.to_decimal()
        return self.from_decimal(a_dec / b_dec)
    
    def sqr(self):
        """Возведение в квадрат"""
        dec = self.to_decimal()
        return self.from_decimal(dec * dec)
    
    def rev(self):
        """Обратное значение (1/x)"""
        dec = self.to_decimal()
        if abs(dec) < 1e-15:
            raise ZeroDivisionError("Деление на ноль")
        return self.from_decimal(1.0 / dec)
    
    def __str__(self):
        return self.value
    
    def set_base(self, new_base):
        """Изменение основания системы счисления"""
        if new_base == self.base:
            return self
        decimal_value = self.to_decimal()
        new_num = PNumber('0', new_base, self.mode)
        return new_num.from_decimal(decimal_value)


class HistoryDialog(QDialog):
    """Диалог истории вычислений"""
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("История вычислений")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxDialog()
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont('Monospace', 10))
        
        for entry in history[-50:]:
            self.text_edit.append(entry)
        
        layout.addWidget(self.text_edit)
        self.setLayout(layout)


class AboutDialog(QDialog):
    """Диалог о программе"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setFixedSize(300, 250)
        
        layout = QVBoxDialog()
        layout.setAlignment(Qt.AlignCenter)
        
        info = [
            "P-ичный калькулятор",
            "",
            "Разработчик: Дмитриев Егор",
            "Группа: ИП-213",
            "",
            "СибГУТИ, 2026",
            "",
            "Калькулятор для работы с числами",
            "в системах счисления 2-16"
        ]
        
        for line in info:
            label = QLabel(line)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
        
        self.setLayout(layout)


class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Переменные состояния
        self.current_number = PNumber('0', base=10, mode='real')
        self.accumulator = None  # Накопленный результат
        self.pending_operation = None  # Ожидающая операция
        self.last_operation = None  # Последняя операция
        self.waiting_for_operand = True  # Ждем ввод операнда
        self.memory = PNumber('0', base=10, mode='real')
        self.memory_active = False
        self.history = []
        self.base = 10
        self.mode = 'real'
        self.just_calculated = False
        self.last_result = None  # Последний результат для повторных операций
        
        self.initUI()
    
    def initUI(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("P-ичный калькулятор")
        self.setFixedSize(550, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        
        # Создание меню
        self.create_menu()
        
        # Верхняя панель с информацией
        info_layout = QHBoxLayout()
        
        self.base_label = QLabel(f"Основание: {self.base}")
        self.base_label.setFont(QFont('Arial', 10))
        info_layout.addWidget(self.base_label)
        
        self.mode_label = QLabel("Режим: действительные")
        self.mode_label.setFont(QFont('Arial', 10))
        info_layout.addWidget(self.mode_label)
        
        info_layout.addStretch()
        
        self.memory_label = QLabel("")
        self.memory_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.memory_label.setStyleSheet("color: blue;")
        info_layout.addWidget(self.memory_label)
        
        main_layout.addLayout(info_layout)
        
        # Дисплей
        self.display = QLineEdit()
        self.display.setFont(QFont('Monospace', 28))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setMinimumHeight(80)
        self.display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #888;
                border-radius: 5px;
                padding: 5px;
                background-color: black;
                color: white;
            }
        """)
        main_layout.addWidget(self.display)
        
        # Панель памяти
        memory_layout = QHBoxLayout()
        
        memory_buttons = [
            ('MC', self.memory_clear, 'Очистить память'),
            ('MS', self.memory_save, 'Сохранить в память'),
            ('MR', self.memory_recall, 'Восстановить из памяти'),
            ('M+', self.memory_add, 'Добавить к памяти')
        ]
        
        for text, slot, tooltip in memory_buttons:
            btn = QPushButton(text)
            btn.setFixedSize(80, 35)
            btn.clicked.connect(slot)
            btn.setToolTip(tooltip)
            btn.setFont(QFont('Arial', 10))
            memory_layout.addWidget(btn)
        
        memory_layout.addStretch()
        main_layout.addLayout(memory_layout)
        
        # Панель редактирования
        edit_layout = QHBoxLayout()
        
        edit_buttons = [
            ('⌫', self.backspace, 'Удалить последний символ'),
            ('CE', self.clear_entry, 'Очистить текущее число'),
            ('C', self.clear_all, 'Очистить всё')
        ]
        
        for text, slot, tooltip in edit_buttons:
            btn = QPushButton(text)
            btn.setFixedSize(120, 35)
            btn.clicked.connect(slot)
            btn.setToolTip(tooltip)
            btn.setFont(QFont('Arial', 10))
            edit_layout.addWidget(btn)
        
        edit_layout.addStretch()
        main_layout.addLayout(edit_layout)
        
        # Основная панель кнопок
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setSpacing(5)
        
        self.digit_buttons = []
        
        # Расположение кнопок
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3), ('Sqr', 0, 4),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3), ('Rev', 1, 4),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3), ('=', 2, 4),
            ('0', 3, 0), ('A', 3, 1), ('B', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('D', 4, 1), ('E', 4, 2), ('F', 4, 3)
        ]
        
        if self.mode == 'real':
            buttons.append(('.', 5, 0))
        
        for btn_info in buttons:
            text, row, col = btn_info[:3]
            btn = QPushButton(text)
            btn.setFixedSize(80, 60)
            btn.setFont(QFont('Arial', 14, QFont.Bold))
            
            if text in '+-*/=':
                btn.setStyleSheet("background-color: #FFA500; color: white;")
            elif text in ('Sqr', 'Rev'):
                btn.setStyleSheet("background-color: #4CAF50; color: white;")
            elif text in ('⌫', 'CE', 'C'):
                btn.setStyleSheet("background-color: #f44336; color: white;")
            else:
                btn.setStyleSheet("background-color: black;")
            
            if text in '0123456789ABCDEF.':
                btn.clicked.connect(lambda checked, x=text: self.digit_click(x))
                self.digit_buttons.append(btn)
            elif text == '+':
                btn.clicked.connect(self.add_operation)
            elif text == '-':
                btn.clicked.connect(self.sub_operation)
            elif text == '*':
                btn.clicked.connect(self.mul_operation)
            elif text == '/':
                btn.clicked.connect(self.div_operation)
            elif text == 'Sqr':
                btn.clicked.connect(self.sqr_function)
            elif text == 'Rev':
                btn.clicked.connect(self.rev_function)
            elif text == '=':
                btn.clicked.connect(self.equals)
            
            buttons_layout.addWidget(btn, row, col)
        
        main_layout.addWidget(buttons_widget)
        
        self.update_display()
        self.update_buttons_state()
    
    def create_menu(self):
        """Создание меню"""
        menubar = self.menuBar()
        
        edit_menu = menubar.addMenu('Правка')
        
        copy_action = QAction('Копировать', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy_to_clipboard)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('Вставить', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.paste_from_clipboard)
        edit_menu.addAction(paste_action)
        
        settings_menu = menubar.addMenu('Настройка')
        
        base_menu = settings_menu.addMenu('Основание')
        for b in range(2, 17):
            action = QAction(f'Основание {b}', self)
            action.triggered.connect(lambda checked, x=b: self.change_base(x))
            base_menu.addAction(action)
        
        mode_menu = settings_menu.addMenu('Режим')
        int_action = QAction('Целые числа', self)
        int_action.triggered.connect(lambda: self.change_mode('integer'))
        mode_menu.addAction(int_action)
        
        real_action = QAction('Действительные числа', self)
        real_action.triggered.connect(lambda: self.change_mode('real'))
        mode_menu.addAction(real_action)
        
        help_menu = menubar.addMenu('Справка')
        
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        history_action = QAction('История', self)
        history_action.triggered.connect(self.show_history)
        help_menu.addAction(history_action)
    
    def update_display(self):
        """Обновление дисплея"""
        self.display.setText(str(self.current_number))
        self.memory_label.setText("M" if self.memory_active else "")
    
    def update_buttons_state(self):
        """Обновление состояния кнопок цифр"""
        available_digits = PNumber.DIGITS[:self.base]
        for btn in self.digit_buttons:
            text = btn.text()
            if text in available_digits or text == '.':
                btn.setEnabled(True)
            else:
                btn.setEnabled(False)
    
    def digit_click(self, digit):
        """Обработка нажатия цифровой кнопки"""
        if self.waiting_for_operand or self.just_calculated:
            self.current_number = PNumber('0', self.base, self.mode)
            self.waiting_for_operand = False
            self.just_calculated = False
        
        if digit == '.':
            if '.' not in self.current_number.value:
                self.current_number.value += '.'
        else:
            if self.current_number.value == '0':
                self.current_number.value = digit
            else:
                self.current_number.value += digit
        
        self.current_number = PNumber(self.current_number.value, self.base, self.mode)
        self.update_display()
    
    def handle_operation(self, op):
        """Обработка бинарной операции"""
        if self.accumulator is None:
            # Первая операция
            self.accumulator = self.current_number
            self.pending_operation = op
            self.last_operation = op
            self.waiting_for_operand = True
            self.just_calculated = False
            self.add_to_history(f"{self.accumulator} {op}")
        else:
            # Если есть второй операнд (не ждем ввод), вычисляем предыдущую операцию
            if not self.waiting_for_operand:
                self.calculate()
            self.pending_operation = op
            self.last_operation = op
            self.waiting_for_operand = True
            self.just_calculated = False
    
    def add_operation(self):
        self.handle_operation('+')
    
    def sub_operation(self):
        self.handle_operation('-')
    
    def mul_operation(self):
        self.handle_operation('*')
    
    def div_operation(self):
        self.handle_operation('/')
    
    def sqr_function(self):
        """Функция Sqr"""
        try:
            result = self.current_number.sqr()
            self.add_to_history(f"Sqr({self.current_number}) = {result}")
            self.current_number = result
            
            if self.accumulator is None:
                # Первый операнд
                self.accumulator = result
                self.waiting_for_operand = True
            else:
                # Второй операнд - оставляем waiting_for_operand = False, чтобы при следующей операции выполнить calculate
                self.waiting_for_operand = False
            
            self.just_calculated = True
            self.update_display()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def rev_function(self):
        """Функция Rev"""
        try:
            result = self.current_number.rev()
            self.add_to_history(f"1/({self.current_number}) = {result}")
            self.current_number = result
            
            if self.accumulator is None:
                self.accumulator = result
                self.waiting_for_operand = True
            else:
                self.waiting_for_operand = False
            
            self.just_calculated = True
            self.update_display()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def calculate(self):
        """Вычисление текущей операции"""
        if self.accumulator is not None and self.pending_operation is not None:
            try:
                second = self.current_number
                
                if self.pending_operation == '+':
                    result = self.accumulator + second
                elif self.pending_operation == '-':
                    result = self.accumulator - second
                elif self.pending_operation == '*':
                    result = self.accumulator * second
                elif self.pending_operation == '/':
                    result = self.accumulator / second
                else:
                    return
                
                self.add_to_history(f"{self.accumulator} {self.pending_operation} {second} = {result}")
                self.accumulator = result
                self.current_number = result
                self.last_result = result
                self.just_calculated = True
                self.waiting_for_operand = True  # После вычисления ждем следующий операнд
                self.update_display()
                
            except ZeroDivisionError:
                QMessageBox.critical(self, "Ошибка", "Деление на ноль!")
                self.clear_all()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
                self.clear_all()
    
    def equals(self):
        """Обработка знака равенства"""
        if self.accumulator is not None and self.pending_operation is not None:
            self.calculate()
            self.pending_operation = self.last_operation  # Сохраняем для повторения
            self.waiting_for_operand = True
    
    def backspace(self):
        """Удаление последнего символа"""
        if not self.waiting_for_operand and not self.just_calculated:
            if len(self.current_number.value) > 1:
                self.current_number.value = self.current_number.value[:-1]
            else:
                self.current_number.value = '0'
            self.current_number = PNumber(self.current_number.value, self.base, self.mode)
            self.update_display()
    
    def clear_entry(self):
        """Очистка текущего числа (CE)"""
        self.current_number = PNumber('0', self.base, self.mode)
        self.waiting_for_operand = False
        self.just_calculated = False
        self.update_display()
    
    def clear_all(self):
        """Полная очистка (C)"""
        self.current_number = PNumber('0', self.base, self.mode)
        self.accumulator = None
        self.pending_operation = None
        self.last_operation = None
        self.last_result = None
        self.waiting_for_operand = True
        self.just_calculated = False
        self.update_display()
    
    def memory_clear(self):
        """MC - очистка памяти"""
        self.memory = PNumber('0', self.base, self.mode)
        self.memory_active = False
        self.update_display()
    
    def memory_save(self):
        """MS - сохранить в память"""
        self.memory = PNumber(self.current_number.value, self.base, self.mode)
        self.memory_active = True
        self.update_display()
    
    def memory_recall(self):
        """MR - восстановить из памяти"""
        if self.memory_active:
            self.current_number = PNumber(self.memory.value, self.base, self.mode)
            self.waiting_for_operand = False
            self.just_calculated = False
            self.update_display()
    
    def memory_add(self):
        """M+ - добавить к памяти"""
        if self.memory_active:
            self.memory = self.memory + self.current_number
        else:
            self.memory = PNumber(self.current_number.value, self.base, self.mode)
            self.memory_active = True
        self.update_display()
    
    def copy_to_clipboard(self):
        """Копирование в буфер обмена"""
        clipboard = QApplication.clipboard()
        clipboard.setText(str(self.current_number))
    
    def paste_from_clipboard(self):
        """Вставка из буфера обмена"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            try:
                self.current_number = PNumber(text.upper(), self.base, self.mode)
                self.waiting_for_operand = False
                self.just_calculated = False
                self.update_display()
            except:
                QMessageBox.warning(self, "Ошибка", "Некорректные данные в буфере обмена")
    
    def change_base(self, new_base):
        """Изменение основания системы счисления"""
        self.base = new_base
        self.base_label.setText(f"Основание: {self.base}")
        self.current_number = self.current_number.set_base(new_base)
        if self.accumulator is not None:
            self.accumulator = self.accumulator.set_base(new_base)
        if self.last_result is not None:
            self.last_result = self.last_result.set_base(new_base)
        if self.memory_active:
            self.memory = self.memory.set_base(new_base)
        self.update_display()
        self.update_buttons_state()
    
    def change_mode(self, new_mode):
        """Изменение режима работы"""
        self.mode = new_mode
        self.current_number.mode = new_mode
        self.mode_label.setText(f"Режим: {'целые' if new_mode == 'integer' else 'действительные'}")
        self.clear_all()
        self.close()
        new_window = CalculatorWindow()
        new_window.show()
    
    def add_to_history(self, entry):
        """Добавление записи в историю"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {entry}"
        self.history.append(history_entry)
        print(history_entry)
    
    def show_history(self):
        """Показать окно истории"""
        dialog = HistoryDialog(self.history, self)
        dialog.exec_()
    
    def show_about(self):
        """Показать информацию о программе"""
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        key = event.text().upper()
        
        if key in PNumber.DIGITS[:self.base]:
            self.digit_click(key)
        elif key == '.' and self.mode == 'real':
            self.digit_click('.')
        elif key == '+':
            self.add_operation()
        elif key == '-':
            self.sub_operation()
        elif key == '*':
            self.mul_operation()
        elif key == '/':
            self.div_operation()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.equals()
        elif event.key() == Qt.Key_Backspace:
            self.backspace()
        elif event.key() == Qt.Key_Escape:
            self.clear_all()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = CalculatorWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()