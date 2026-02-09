class Conver_10_P:
    """
    Преобразователь действительных чисел из десятичной системы счисления 
    в систему счисления с основанием p (2..16)
    """
    
    @staticmethod
    def int_to_char(d: int) -> str:
        """
        Преобразовать целое значение в цифру системы счисления с основанием p
        
        Args:
            d: целое число (0-15)
        
        Returns:
            символ, представляющий цифру в системе счисления (0-9, A-F)
        
        Examples:
            >>> Conver_10_P.int_to_char(10)
            'A'
            >>> Conver_10_P.int_to_char(14)
            'E'
        """
        if 0 <= d <= 9:
            return chr(ord('0') + d)
        elif 10 <= d <= 15:
            return chr(ord('A') + d - 10)
        else:
            raise ValueError(f"Значение {d} вне диапазона 0-15")
    
    @staticmethod
    def int_to_p(n: int, p: int) -> str:
        """
        Преобразовать целое десятичное число в строку в системе счисления с основанием p
        
        Args:
            n: целое десятичное число
            p: основание системы счисления (2..16)
        
        Returns:
            строка, представляющая число в системе счисления с основанием p
        
        Examples:
            >>> Conver_10_P.int_to_p(161, 16)
            'A1'
        """
        if p < 2 or p > 16:
            raise ValueError(f"Основание системы счисления {p} должно быть в диапазоне 2..16")
        
        if n == 0:
            return "0"
        
        is_negative = n < 0
        n = abs(n)
        
        result = []
        while n > 0:
            digit = n % p
            result.append(Conver_10_P.int_to_char(digit))
            n //= p
        
        result_str = ''.join(reversed(result))
        return '-' + result_str if is_negative else result_str
    
    @staticmethod
    def flt_to_p(n: float, p: int, c: int) -> str:
        """
        Преобразовать десятичную дробь в строку в системе счисления с основанием p
        
        Args:
            n: десятичная дробь (0 <= n < 1)
            p: основание системы счисления (2..16)
            c: точность (количество разрядов дробной части)
        
        Returns:
            строка, представляющая дробь в системе счисления с основанием p
        
        Examples:
            >>> Conver_10_P.flt_to_p(0.9375, 2, 4)
            '1111'
        """
        if p < 2 or p > 16:
            raise ValueError(f"Основание системы счисления {p} должно быть в диапазоне 2..16")
        
        if n < 0 or n >= 1:
            raise ValueError(f"Дробь {n} должна быть в диапазоне [0, 1)")
        
        if c < 0:
            raise ValueError(f"Точность {c} должна быть неотрицательной")
        
        result = []
        fraction = n
        
        for _ in range(c):
            fraction *= p
            digit = int(fraction)
            result.append(Conver_10_P.int_to_char(digit))
            fraction -= digit
        
        return ''.join(result)
    
    @staticmethod
    def do(n: float, p: int, c: int) -> str:
        """
        Преобразовать десятичное действительное число в систему счисления с основанием p
        
        Args:
            n: десятичное действительное число
            p: основание системы счисления (2..16)
            c: точность (количество разрядов дробной части)
        
        Returns:
            строка, представляющая число в системе счисления с основанием p
        
        Examples:
            >>> Conver_10_P.do(-17.875, 16, 3)
            '-11.E'
        """
        if p < 2 or p > 16:
            raise ValueError(f"Основание системы счисления {p} должно быть в диапазоне 2..16")
        
        # Отделяем целую и дробную части
        int_part = int(n)
        frac_part = abs(n - int_part)
        
        # Преобразуем целую часть
        int_str = Conver_10_P.int_to_p(int_part, p)
        
        # Преобразуем дробную часть (если она есть и требуется точность)
        if frac_part > 0 and c > 0:
            frac_str = Conver_10_P.flt_to_p(frac_part, p, c)
            return f"{int_str}.{frac_str}"
        else:
            return int_str


# Примеры использования и тестирования
if __name__ == "__main__":
    print("Тестирование класса Conver_10_P:")
    print("=" * 50)
    
    # Тест int_to_char
    print("1. Тест int_to_char:")
    test_cases = [(0, '0'), (5, '5'), (10, 'A'), (14, 'E'), (15, 'F')]
    for d, expected in test_cases:
        result = Conver_10_P.int_to_char(d)
        status = "✓" if result == expected else "✗"
        print(f"  int_to_char({d}) = '{result}' (ожидалось '{expected}') {status}")
    
    print("\n2. Тест int_to_p:")
    test_cases = [
        (161, 16, 'A1'),
        (-17, 16, '-11'),
        (0, 16, '0'),
        (255, 16, 'FF'),
        (10, 2, '1010')
    ]
    for n, p, expected in test_cases:
        result = Conver_10_P.int_to_p(n, p)
        status = "✓" if result == expected else "✗"
        print(f"  int_to_p({n}, {p}) = '{result}' (ожидалось '{expected}') {status}")
    
    print("\n3. Тест flt_to_p:")
    test_cases = [
        (0.9375, 2, 4, '1111'),
        (0.5, 2, 4, '1000'),
        (0.0, 2, 4, '0000'),
        (0.625, 2, 4, '1010')
    ]
    for n, p, c, expected in test_cases:
        result = Conver_10_P.flt_to_p(n, p, c)
        status = "✓" if result == expected else "✗"
        print(f"  flt_to_p({n}, {p}, {c}) = '{result}' (ожидалось '{expected}') {status}")
    
    print("\n4. Тест do (полное преобразование):")
    test_cases = [
        (-17.875, 16, 3, '-11.E'),  # 17 = 0x11, 0.875 = 0.0xE (0.875*16=14=E)
        (10.625, 2, 4, '1010.1010'),
        (0.0, 16, 3, '0'),
        (255.9375, 16, 2, 'FF.F0')
    ]
    for n, p, c, expected in test_cases:
        result = Conver_10_P.do(n, p, c)
        status = "✓" if result == expected else "✗"
        print(f"  do({n}, {p}, {c}) = '{result}' (ожидалось '{expected}') {status}")
    
    print("\n5. Тест обработки ошибок:")
    try:
        Conver_10_P.int_to_p(10, 17)  # Неверное основание
    except ValueError as e:
        print(f"  ✓ Правильно обработана ошибка: {e}")
    
    try:
        Conver_10_P.flt_to_p(-0.5, 2, 4)  # Отрицательная дробь
    except ValueError as e:
        print(f"  ✓ Правильно обработана ошибка: {e}")
    
    print("\n" + "=" * 50)
    print("Тестирование завершено!")