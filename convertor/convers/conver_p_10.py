class Conver_P_10:
    @staticmethod
    def char_to_num(ch: str) -> int:
        if '0' <= ch <= '9':
            return ord(ch) - ord('0')
        elif 'A' <= ch <= 'F':
            return ord(ch) - ord('A') + 10
        elif 'a' <= ch <= 'f':
            return ord(ch) - ord('a') + 10
        else:
            raise ValueError(f"Недопустимый символ '{ch}' для системы счисления")
    
    @staticmethod
    def _convert(P_num: str, P: int, weight: float) -> float:
        result = 0.0
        current_weight = weight
        
        for ch in P_num:
            digit = Conver_P_10.char_to_num(ch)
            result += digit * current_weight
            current_weight /= P
        
        return result
    
    @staticmethod
    def dval(P_num: str, P: int) -> float:
        # Проверка входных данных
        if P < 2 or P > 16:
            raise ValueError(f"Основание системы счисления {P} должно быть в диапазоне 2..16")
        
        # Проверка на пустую строку
        if not P_num:
            raise ValueError("Пустая строка недопустима")
        
        # Обработка знака
        is_negative = False
        num_str = P_num
        if P_num[0] == '-':
            is_negative = True
            num_str = P_num[1:]
        
        # Разделение на целую и дробную части
        parts = num_str.split('.')
        if len(parts) > 2:
            raise ValueError(f"Некорректный формат числа: {P_num}")
        
        int_part = parts[0]
        frac_part = parts[1] if len(parts) == 2 else ""
        
        # Преобразование целой части
        result = 0.0
        if int_part:
            # Вес старшего разряда целой части = P^(len-1)
            weight = P ** (len(int_part) - 1)
            result += Conver_P_10._convert(int_part, P, weight)
        
        # Преобразование дробной части
        if frac_part:
            # Вес первого разряда дробной части = 1/P
            weight = 1.0 / P
            result += Conver_P_10._convert(frac_part, P, weight)
        
        return -result if is_negative else result