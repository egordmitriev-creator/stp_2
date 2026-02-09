class Conver_10_P:
    """
    Преобразователь действительных чисел из десятичной системы счисления 
    в систему счисления с основанием p (2..16)
    """
    
    @staticmethod
    def int_to_char(d: int) -> str:
        """
        Преобразовать целое значение в цифру системы счисления с основанием p
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
        
        # Удаляем незначащие нули в конце
        while result and result[-1] == '0':
            result.pop()
        
        return ''.join(result) if result else '0'
    
    @staticmethod
    def do(n: float, p: int, c: int) -> str:
        """
        Преобразовать десятичное действительное число в систему счисления с основанием p
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
            return f"{int_str}.{frac_str}" if frac_str else int_str
        else:
            return int_str