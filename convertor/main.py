import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QSlider, QSpinBox, QMenuBar,
    QMenu, QAction, QMessageBox, QTextEdit, QDialog, QFrame, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent, QPalette, QColor

from control import Control_, State
from history import History


# Темная тема для приложения
def setup_dark_theme(app):
    """Установка темной темы"""
    app.setStyle('Fusion')
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    
    app.setPalette(dark_palette)


class AboutDialog(QDialog):
    """Диалог "О программе" """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setFixedSize(450, 350)
        
        layout = QVBoxLayout()
        
        title = QLabel("Конвертер p1_p2")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        version = QLabel("Версия 1.0")
        version.setFont(QFont("Arial", 10))
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        description = QLabel(
            "Программа для преобразования чисел между различными системами счисления.\n\n"
            "Поддерживаются системы счисления с основанием от 2 до 16.\n\n"
            "Возможности:\n"
            "• Преобразование действительных чисел\n"
            "• Редактирование чисел с помощью кнопок или клавиатуры\n"
            "• Просмотр истории преобразований\n"
            "• Контекстная помощь\n\n"
            "Разработано в рамках курса\n"
            "Объектно-ориентированное программирование"
        )
        description.setFont(QFont("Arial", 10))
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(100)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, 0, Qt.AlignCenter)
        
        self.setLayout(layout)


class HistoryDialog(QDialog):
    """Диалог истории"""
    
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("История преобразований")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        title = QLabel("История преобразований")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Courier", 10))
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        
        if history.count() == 0:
            self.text_edit.setText("История пуста")
        else:
            text = ""
            for i in range(history.count()):
                record = history[i]
                text += f"{i+1}. {record}\n\n"
            self.text_edit.setText(text)
        
        close_button = QPushButton("Закрыть")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, 0, Qt.AlignCenter)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """
    Главное окно приложения
    """
    
    # Константы команд
    CMD_DIGIT_0 = 0
    CMD_DIGIT_1 = 1
    CMD_DIGIT_2 = 2
    CMD_DIGIT_3 = 3
    CMD_DIGIT_4 = 4
    CMD_DIGIT_5 = 5
    CMD_DIGIT_6 = 6
    CMD_DIGIT_7 = 7
    CMD_DIGIT_8 = 8
    CMD_DIGIT_9 = 9
    CMD_DIGIT_A = 10
    CMD_DIGIT_B = 11
    CMD_DIGIT_C = 12
    CMD_DIGIT_D = 13
    CMD_DIGIT_E = 14
    CMD_DIGIT_F = 15
    CMD_DELIM = 16      # Разделитель
    CMD_BS = 17         # Забой
    CMD_CLEAR = 18      # Очистка
    CMD_EXECUTE = 19    # Выполнить
    
    def __init__(self):
        super().__init__()
        
        self.ctl = Control_()
        self.buttons = []  # Список всех кнопок
        
        self.init_ui()
        self.on_load()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Конвертер p1_p2")
        self.setFixedSize(600, 750)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Создание меню
        self.create_menu()
        
        # === Верхняя панель с числами ===
        
        # Исходное число
        input_title = QLabel("Исходное число:")
        input_title.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(input_title)
        
        self.input_label = QLabel("0")
        self.input_label.setFont(QFont("Courier", 16, QFont.Bold))
        self.input_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.input_label.setFixedHeight(50)
        self.input_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.input_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #00ff00;
                padding: 8px;
                border: 2px solid #555;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.input_label)
        
        # Результат
        result_title = QLabel("Результат:")
        result_title.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(result_title)
        
        self.result_label = QLabel("0")
        self.result_label.setFont(QFont("Courier", 16, QFont.Bold))
        self.result_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.result_label.setFixedHeight(50)
        self.result_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #ffaa00;
                padding: 8px;
                border: 2px solid #555;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.result_label)
        
        # === Панель выбора оснований ===
        bases_group = QGroupBox("Основания систем счисления")
        bases_group.setFont(QFont("Arial", 10))
        bases_layout = QHBoxLayout()
        bases_layout.setSpacing(30)
        
        # Основание p1
        p1_layout = QVBoxLayout()
        p1_label = QLabel("Основание p1:")
        p1_label.setFont(QFont("Arial", 11))
        p1_layout.addWidget(p1_label)
        
        p1_controls = QHBoxLayout()
        p1_controls.setSpacing(10)
        
        self.trackbar1 = QSlider(Qt.Horizontal)
        self.trackbar1.setMinimum(2)
        self.trackbar1.setMaximum(16)
        self.trackbar1.setValue(self.ctl.pin)
        self.trackbar1.setTickPosition(QSlider.TicksBelow)
        self.trackbar1.setTickInterval(1)
        self.trackbar1.setFixedWidth(180)
        self.trackbar1.valueChanged.connect(self.on_trackbar1_changed)
        p1_controls.addWidget(self.trackbar1)
        
        self.spin1 = QSpinBox()
        self.spin1.setMinimum(2)
        self.spin1.setMaximum(16)
        self.spin1.setValue(self.ctl.pin)
        self.spin1.setFixedWidth(70)
        self.spin1.setFont(QFont("Arial", 11))
        self.spin1.valueChanged.connect(self.on_spin1_changed)
        p1_controls.addWidget(self.spin1)
        
        p1_layout.addLayout(p1_controls)
        bases_layout.addLayout(p1_layout)
        
        # Основание p2
        p2_layout = QVBoxLayout()
        p2_label = QLabel("Основание p2:")
        p2_label.setFont(QFont("Arial", 11))
        p2_layout.addWidget(p2_label)
        
        p2_controls = QHBoxLayout()
        p2_controls.setSpacing(10)
        
        self.trackbar2 = QSlider(Qt.Horizontal)
        self.trackbar2.setMinimum(2)
        self.trackbar2.setMaximum(16)
        self.trackbar2.setValue(self.ctl.pout)
        self.trackbar2.setTickPosition(QSlider.TicksBelow)
        self.trackbar2.setTickInterval(1)
        self.trackbar2.setFixedWidth(180)
        self.trackbar2.valueChanged.connect(self.on_trackbar2_changed)
        p2_controls.addWidget(self.trackbar2)
        
        self.spin2 = QSpinBox()
        self.spin2.setMinimum(2)
        self.spin2.setMaximum(16)
        self.spin2.setValue(self.ctl.pout)
        self.spin2.setFixedWidth(70)
        self.spin2.setFont(QFont("Arial", 11))
        self.spin2.valueChanged.connect(self.on_spin2_changed)
        p2_controls.addWidget(self.spin2)
        
        p2_layout.addLayout(p2_controls)
        bases_layout.addLayout(p2_layout)
        
        bases_group.setLayout(bases_layout)
        main_layout.addWidget(bases_group)
        
        # Подписи для оснований
        self.label_p1 = QLabel(f"Основание с.сч. исходного числа {self.ctl.pin}")
        self.label_p1.setFont(QFont("Arial", 10))
        self.label_p1.setStyleSheet("color: #aaa; padding: 5px;")
        main_layout.addWidget(self.label_p1)
        
        self.label_p2 = QLabel(f"Основание с.сч. результата {self.ctl.pout}")
        self.label_p2.setFont(QFont("Arial", 10))
        self.label_p2.setStyleSheet("color: #aaa; padding: 5px;")
        main_layout.addWidget(self.label_p2)
        
        # === Панель кнопок ===
        buttons_group = QGroupBox("Клавиатура")
        buttons_group.setFont(QFont("Arial", 11))
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setVerticalSpacing(12)
        
        # Создание кнопок в правильном порядке
        # Первый ряд: 7 8 9
        self.add_button(buttons_layout, "7", self.CMD_DIGIT_7, 0, 0)
        self.add_button(buttons_layout, "8", self.CMD_DIGIT_8, 0, 1)
        self.add_button(buttons_layout, "9", self.CMD_DIGIT_9, 0, 2)
        
        # Второй ряд: 4 5 6
        self.add_button(buttons_layout, "4", self.CMD_DIGIT_4, 1, 0)
        self.add_button(buttons_layout, "5", self.CMD_DIGIT_5, 1, 1)
        self.add_button(buttons_layout, "6", self.CMD_DIGIT_6, 1, 2)
        
        # Третий ряд: 1 2 3
        self.add_button(buttons_layout, "1", self.CMD_DIGIT_1, 2, 0)
        self.add_button(buttons_layout, "2", self.CMD_DIGIT_2, 2, 1)
        self.add_button(buttons_layout, "3", self.CMD_DIGIT_3, 2, 2)
        
        # Четвертый ряд: 0 A B
        self.add_button(buttons_layout, "0", self.CMD_DIGIT_0, 3, 0)
        self.add_button(buttons_layout, "A", self.CMD_DIGIT_A, 3, 1)
        self.add_button(buttons_layout, "B", self.CMD_DIGIT_B, 3, 2)
        
        # Пятый ряд: C D E
        self.add_button(buttons_layout, "C", self.CMD_DIGIT_C, 4, 0)
        self.add_button(buttons_layout, "D", self.CMD_DIGIT_D, 4, 1)
        self.add_button(buttons_layout, "E", self.CMD_DIGIT_E, 4, 2)
        
        # Шестой ряд: F . BS CL
        self.add_button(buttons_layout, "F", self.CMD_DIGIT_F, 5, 0)
        self.add_button(buttons_layout, ".", self.CMD_DELIM, 5, 1)
        self.add_button(buttons_layout, "BS", self.CMD_BS, 5, 2)
        self.add_button(buttons_layout, "CL", self.CMD_CLEAR, 5, 3)
        
        # Седьмой ряд: Execute (на всю ширину)
        execute_btn = QPushButton("Execute")
        execute_btn.setFixedHeight(30)
        execute_btn.setFont(QFont("Arial", 14, QFont.Bold))
        execute_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #34495e;
                border-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #1e2b3a;
            }
        """)
        execute_btn.clicked.connect(lambda: self.button_click(self.CMD_EXECUTE))
        buttons_layout.addWidget(execute_btn, 6, 0, 1, 4)
        
        buttons_group.setLayout(buttons_layout)
        main_layout.addWidget(buttons_group)
        
        # Статусная строка
        self.status_label = QLabel("Приложение загружено")
        self.status_label.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.status_label.setFixedHeight(30)
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                color: #aaa;
                padding: 5px;
                border: 1px solid #333;
                border-radius: 3px;
            }
        """)
        main_layout.addWidget(self.status_label)
    
    def add_button(self, layout, text, cmd, row, col):
        """Добавление кнопки в сетку"""
        btn = QPushButton(text)
        btn.setFixedSize(50, 30)
        btn.setFont(QFont("Arial", 12, QFont.Bold))
        
        # Разный цвет для разных типов кнопок
        if cmd <= 9:  # Цифры
            base_color = "#3498db"
        elif cmd <= 15:  # Буквы A-F
            base_color = "#9b59b6"
        elif cmd == self.CMD_DELIM:  # Разделитель
            base_color = "#f39c12"
        elif cmd == self.CMD_BS:  # Забой
            base_color = "#e74c3c"
        elif cmd == self.CMD_CLEAR:  # Очистка
            base_color = "#e67e22"
        else:
            base_color = "#2c3e50"
        
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(base_color)};
                border-color: #777;
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(base_color)};
            }}
            QPushButton:disabled {{
                background-color: #444;
                color: #666;
                border: 2px solid #333;
            }}
        """)
        
        btn.clicked.connect(lambda checked, c=cmd: self.button_click(c))
        btn.cmd = cmd  # Сохраняем команду (аналог Tag)
        layout.addWidget(btn, row, col)
        self.buttons.append(btn)
    
    def lighten_color(self, color):
        """Осветление цвета"""
        # Простая реализация - возвращаем тот же цвет
        # В реальности можно реализовать осветление
        return color.replace("db", "ff").replace("b6", "d8").replace("12", "45").replace("3c", "5c").replace("22", "45")
    
    def darken_color(self, color):
        """Затемнение цвета"""
        # Простая реализация - возвращаем тот же цвет
        return color
    
    def create_menu(self):
        """Создание главного меню"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2b2b2b;
                color: white;
                border-bottom: 1px solid #444;
            }
            QMenuBar::item:selected {
                background-color: #444;
            }
        """)
        
        # Меню Файл
        file_menu = menubar.addMenu("Меню")
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.exit_menu_click)
        file_menu.addAction(exit_action)
        
        # Меню История
        history_menu = menubar.addMenu("История")
        
        show_history_action = QAction("Просмотр истории", self)
        show_history_action.triggered.connect(self.history_menu_click)
        history_menu.addAction(show_history_action)
        
        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.help_menu_click)
        help_menu.addAction(about_action)
    
    # === Обработчики событий ===
    
    def on_load(self):
        """Загрузка формы"""
        self.input_label.setText(self.ctl.editor.number)
        self.trackbar1.setValue(self.ctl.pin)
        self.trackbar2.setValue(self.ctl.pout)
        self.label_p1.setText(f"Основание с.сч. исходного числа {self.ctl.pin}")
        self.label_p2.setText(f"Основание с.сч. результата {self.ctl.pout}")
        self.result_label.setText("0")
        self.update_buttons()
        self.status_label.setText("Приложение загружено")
    
    def button_click(self, cmd):
        """Нажатие кнопки"""
        print(f"Нажата кнопка с командой: {cmd}")
        self.do_command(cmd)
    
    def do_command(self, cmd):
        """Выполнение команды"""
        if cmd == self.CMD_EXECUTE:
            result = self.ctl.do_command(cmd)
            self.result_label.setText(result)
            self.status_label.setText(f"Выполнено преобразование: {result}")
            print(f"Результат преобразования: {result}")
        else:
            if self.ctl.state == State.ПРЕОБРАЗОВАНО:
                # Очистить редактор
                self.input_label.setText(self.ctl.do_command(self.CMD_CLEAR))
            
            result = self.ctl.do_command(cmd)
            self.input_label.setText(result)
            self.result_label.setText("0")
            self.status_label.setText(f"Редактирование: {result}")
            print(f"После редактирования: {result}")
    
    def update_buttons(self):
        """Обновление состояния кнопок"""
        pin = self.trackbar1.value()
        
        for btn in self.buttons:
            cmd = btn.cmd
            if cmd < pin:
                btn.setEnabled(True)
            elif cmd <= 15:  # Цифры A-F
                btn.setEnabled(False)
    
    def update_p1(self):
        """Обновление при изменении p1"""
        pin = self.trackbar1.value()
        self.spin1.setValue(pin)
        self.label_p1.setText(f"Основание с.сч. исходного числа {pin}")
        self.ctl.pin = pin
        self.update_buttons()
        self.input_label.setText(self.ctl.do_command(self.CMD_CLEAR))
        self.result_label.setText("0")
        self.status_label.setText(f"Изменено основание p1 = {pin}")
    
    def update_p2(self):
        """Обновление при изменении p2"""
        pout = self.trackbar2.value()
        self.spin2.setValue(pout)
        self.ctl.pout = pout
        result = self.ctl.do_command(self.CMD_EXECUTE)
        self.result_label.setText(result)
        self.label_p2.setText(f"Основание с.сч. результата {pout}")
        self.status_label.setText(f"Изменено основание p2 = {pout}")
    
    # === Обработчики изменения оснований ===
    
    def on_trackbar1_changed(self, value):
        self.update_p1()
    
    def on_spin1_changed(self, value):
        self.trackbar1.setValue(value)
        self.update_p1()
    
    def on_trackbar2_changed(self, value):
        self.update_p2()
    
    def on_spin2_changed(self, value):
        self.trackbar2.setValue(value)
        self.update_p2()
    
    # === Обработчики клавиатуры ===
    
    def keyPressEvent(self, event: QKeyEvent):
        text = event.text()
        
        if text:
            cmd = -1
            
            if text.isdigit():
                cmd = int(text)
            elif 'A' <= text <= 'F':
                cmd = ord(text) - ord('A') + 10
            elif 'a' <= text <= 'f':
                cmd = ord(text) - ord('a') + 10
            elif text == '.':
                cmd = self.CMD_DELIM
            
            pin = self.trackbar1.value()
            if 0 <= cmd < pin or cmd >= 16:
                self.do_command(cmd)
        
        key = event.key()
        if key == Qt.Key_Backspace:
            self.do_command(self.CMD_BS)
        elif key == Qt.Key_Delete:
            self.do_command(self.CMD_CLEAR)
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.do_command(self.CMD_EXECUTE)
    
    # === Обработчики меню ===
    
    def exit_menu_click(self):
        reply = QMessageBox.question(
            self, "Выход",
            "Вы действительно хотите выйти?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
    
    def history_menu_click(self):
        dialog = HistoryDialog(self.ctl.history, self)
        dialog.exec_()
    
    def help_menu_click(self):
        dialog = AboutDialog(self)
        dialog.exec_()


def main():
    app = QApplication(sys.argv)
    setup_dark_theme(app)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()