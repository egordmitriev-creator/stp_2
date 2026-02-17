class Editor:
    # Константы
    DELIM = "."  # Разделитель целой и дробной частей
    ZERO = "0"   # Строковое представление нуля
    
    # Коды команд
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
    CMD_DELIM = 16    # Добавить разделитель
    CMD_BS = 17       # Забой (удалить последний символ)
    CMD_CLEAR = 18    # Очистить
    
    def __init__(self):
        self._number = ""  # Поле для хранения редактируемого числа
        self._has_delim = False  # Флаг наличия разделителя
    
    @property
    def number(self) -> str:
        return self._number if self._number else self.ZERO
    
    def _is_valid_digit(self, n: int, p: int) -> bool:
        return 0 <= n < p
    
    def _digit_to_char(self, n: int) -> str:
        if 0 <= n <= 9:
            return chr(ord('0') + n)
        elif 10 <= n <= 15:
            return chr(ord('A') + n - 10)
        else:
            raise ValueError(f"Недопустимая цифра: {n}")
    
    def add_digit(self, n: int, p: int = 10) -> str:
        # Проверка допустимости цифры
        if not self._is_valid_digit(n, p):
            # Если цифра недопустима, возвращаем текущее число без изменений
            return self.number
        
        # Проверка на ведущие нули
        if self._number == self.ZERO and n == 0:
            # Не добавляем лишние ведущие нули
            return self.number
        
        # Если число было пустым и добавляется ноль
        if not self._number and n == 0:
            self._number = self.ZERO
            return self.number
        
        # Если число было пустым и добавляется ненулевая цифра
        if not self._number:
            self._number = self._digit_to_char(n)
            return self.number
        
        # Добавление цифры к существующему числу
        digit_char = self._digit_to_char(n)
        self._number += digit_char
        return self.number
    
    def add_zero(self, p: int = 10) -> str:
        return self.add_digit(0, p)
    
    def add_delim(self) -> str:
        # Проверка, что число не пустое
        if not self._number:
            self._number = self.ZERO
        
        # Проверка, что разделитель еще не добавлен
        if not self._has_delim:
            self._number += self.DELIM
            self._has_delim = True
        
        return self.number
    
    def bs(self) -> str:
        if not self._number:
            return self.number
        
        # Проверка, удаляем ли разделитель
        if self._number[-1] == self.DELIM:
            self._has_delim = False
        
        # Удаление последнего символа
        self._number = self._number[:-1]
        
        return self.number
    
    def clear(self) -> str:
        self._number = ""
        self._has_delim = False
        return self.number
    
    def acc(self, p_in: int = 10, p_out: int = 10) -> int:
        if not self._number or self.DELIM not in self._number:
            return 0
        
        # Получаем дробную часть
        frac_part = self._number.split(self.DELIM)[1]
        return len(frac_part)
    
    def do_edit(self, j: int, p: int = 10) -> str:
        if 0 <= j <= 15:  # Команды добавления цифр
            return self.add_digit(j, p)
        elif j == self.CMD_DELIM:  # Разделитель
            return self.add_delim()
        elif j == self.CMD_BS:  # Забой
            return self.bs()
        elif j == self.CMD_CLEAR:  # Очистка
            return self.clear()
        else:
            raise ValueError(f"Неизвестная команда: {j}")