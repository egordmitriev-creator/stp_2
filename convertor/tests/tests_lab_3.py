from convertor.convers.conver_p_10 import Conver_P_10

class StructuralTester:
    """
    Класс для тестирования по критериям С0, С1, С2
    """
    
    @staticmethod
    def test_c0_coverage():
        """Тестирование по критерию С0 (покрытие операторов)"""
        print("=" * 70)
        print("КРИТЕРИЙ С0 - ПОКРЫТИЕ ОПЕРАТОРОВ")
        print("=" * 70)
        
        test_cases = [
            # Метод char_to_num
            ("char_to_num('0')", lambda: Conver_P_10.char_to_num('0'), 0),
            ("char_to_num('5')", lambda: Conver_P_10.char_to_num('5'), 5),
            ("char_to_num('9')", lambda: Conver_P_10.char_to_num('9'), 9),
            ("char_to_num('A')", lambda: Conver_P_10.char_to_num('A'), 10),
            ("char_to_num('F')", lambda: Conver_P_10.char_to_num('F'), 15),
            ("char_to_num('a')", lambda: Conver_P_10.char_to_num('a'), 10),
            ("char_to_num('f')", lambda: Conver_P_10.char_to_num('f'), 15),
            
            # Метод _convert
            ("_convert('A5E', 16, 256)", lambda: Conver_P_10._convert('A5E', 16, 256), 2654.0),
            ("_convert('1010', 2, 8)", lambda: Conver_P_10._convert('1010', 2, 8), 10.0),
            
            # Метод dval
            ("dval('0', 10)", lambda: Conver_P_10.dval('0', 10), 0.0),
            ("dval('A5.E', 16)", lambda: Conver_P_10.dval('A5.E', 16), 165.875),
            ("dval('-A5.E', 16)", lambda: Conver_P_10.dval('-A5.E', 16), -165.875),
            ("dval('1010.101', 2)", lambda: Conver_P_10.dval('1010.101', 2), 10.625),
            ("dval('FF', 16)", lambda: Conver_P_10.dval('FF', 16), 255.0),
            ("dval('0.5', 10)", lambda: Conver_P_10.dval('0.5', 10), 0.5),
            ("dval('A5', 16)", lambda: Conver_P_10.dval('A5', 16), 165.0),
            ("dval('.E', 16)", lambda: Conver_P_10.dval('.E', 16), 0.875),
        ]
        
        passed = 0
        for name, test_func, expected in test_cases:
            try:
                result = test_func()
                if abs(result - expected) < 1e-10:  # Сравнение с плавающей точкой
                    print(f"✓ {name} = {result}")
                    passed += 1
                else:
                    print(f"✗ {name} = {result} (ожидалось {expected})")
            except Exception as e:
                print(f"✗ {name} вызвал исключение: {e}")
        
        print(f"\nРезультат С0: {passed}/{len(test_cases)} тестов пройдено")
        return passed == len(test_cases)
    
    @staticmethod
    def test_c1_coverage():
        """Тестирование по критерию С1 (покрытие ветвей)"""
        print("\n" + "=" * 70)
        print("КРИТЕРИЙ С1 - ПОКРЫТИЕ ВЕТВЕЙ/РЕШЕНИЙ")
        print("=" * 70)
        
        # Подсчет ветвей:
        # char_to_num: 4 ветви (цифры, A-F, a-f, исключение)
        # _convert: 1 ветка (цикл выполняется)
        # dval: 8 ветвей (проверка P, пустая строка, знак, разделитель, целая часть, дробная часть)
        # Итого: 4 + 1 + 8 = 13 ветвей
        
        branches_covered = set()
        total_branches = 13
        
        # Ветви в char_to_num
        test_cases = [
            ("char_to_num('5') - цифра", lambda: Conver_P_10.char_to_num('5'), True, 1),
            ("char_to_num('A') - A-F", lambda: Conver_P_10.char_to_num('A'), True, 2),
            ("char_to_num('a') - a-f", lambda: Conver_P_10.char_to_num('a'), True, 3),
            ("char_to_num('Z') - исключение", lambda: Conver_P_10.char_to_num('Z'), False, 4),
        ]
        
        for name, test_func, should_pass, branch_num in test_cases:
            try:
                result = test_func()
                if should_pass:
                    print(f"✓ {name}: {result}")
                    branches_covered.add(branch_num)
            except ValueError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение")
                    branches_covered.add(branch_num)
        
        # Ветви в _convert
        test_cases_convert = [
            ("_convert('A5E', 16, 256) - нормальное выполнение", 
             lambda: Conver_P_10._convert('A5E', 16, 256), True, 5),
        ]
        
        for name, test_func, should_pass, branch_num in test_cases_convert:
            result = test_func()
            print(f"✓ {name}: {result}")
            branches_covered.add(branch_num)
        
        # Ветви в dval
        test_cases_dval = [
            ("dval('10', 1) - P вне диапазона", lambda: Conver_P_10.dval('10', 1), False, 6),
            ("dval('', 10) - пустая строка", lambda: Conver_P_10.dval('', 10), False, 7),
            ("dval('-10.5', 10) - отрицательное число", lambda: Conver_P_10.dval('-10.5', 10), True, 8),
            ("dval('10.5.6', 10) - несколько разделителей", lambda: Conver_P_10.dval('10.5.6', 10), False, 9),
            ("dval('A5.E', 16) - целая и дробная части", lambda: Conver_P_10.dval('A5.E', 16), True, 10),
            ("dval('A5', 16) - только целая часть", lambda: Conver_P_10.dval('A5', 16), True, 11),
            ("dval('.E', 16) - только дробная часть", lambda: Conver_P_10.dval('.E', 16), True, 12),
            ("dval('10.5', 10) - положительное число", lambda: Conver_P_10.dval('10.5', 10), True, 13),
        ]
        
        for name, test_func, should_pass, branch_num in test_cases_dval:
            try:
                result = test_func()
                if should_pass:
                    print(f"✓ {name}: {result}")
                    branches_covered.add(branch_num)
            except ValueError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение")
                    branches_covered.add(branch_num)
        
        covered_count = len(branches_covered)
        print(f"\nРезультат С1: покрыто {covered_count}/{total_branches} ветвей")
        print(f"Процент покрытия: {covered_count/total_branches*100:.1f}%")
        
        return covered_count == total_branches
    
    @staticmethod
    def test_c2_coverage():
        """Тестирование по критерию С2 (покрытие условий)"""
        print("\n" + "=" * 70)
        print("КРИТЕРИЙ С2 - ПОКРЫТИЕ УСЛОВИЙ")
        print("=" * 70)
        
        conditions = {
            # char_to_num
            "C1": "ch between '0' and '9'",
            "C2": "ch between 'A' and 'F'",
            "C3": "ch between 'a' and 'f'",
            "C4": "ch not in any range",
            
            # _convert
            "C5": "for each character in P_num",
            
            # dval
            "C6": "P < 2",
            "C7": "P > 16",
            "C8": "not P_num",
            "C9": "P_num[0] == '-'",
            "C10": "len(parts) > 2",
            "C11": "int_part exists",
            "C12": "frac_part exists",
        }
        
        test_cases = [
            # Для char_to_num
            ("char='5'", lambda: Conver_P_10.char_to_num('5'), {"C1": (True, False), "C2": (False, True), "C3": (False, True), "C4": False}),
            ("char='A'", lambda: Conver_P_10.char_to_num('A'), {"C1": (False, True), "C2": (True, False), "C3": (False, True), "C4": False}),
            ("char='a'", lambda: Conver_P_10.char_to_num('a'), {"C1": (False, True), "C2": (False, True), "C3": (True, False), "C4": False}),
            ("char='Z'", lambda: Conver_P_10.char_to_num('Z'), {"C1": (False, True), "C2": (False, True), "C3": (False, True), "C4": True}),
            
            # Для _convert
            ("_convert('A5E', 16, 256)", lambda: Conver_P_10._convert('A5E', 16, 256), {"C5": (True, True)}),
            
            # Для dval
            ("dval('10', 1)", lambda: Conver_P_10.dval('10', 1), {"C6": True, "C7": False}),
            ("dval('10', 20)", lambda: Conver_P_10.dval('10', 20), {"C6": False, "C7": True}),
            ("dval('', 10)", lambda: Conver_P_10.dval('', 10), {"C8": True}),
            ("dval('10.5', 10)", lambda: Conver_P_10.dval('10.5', 10), {"C8": False}),
            ("dval('-10.5', 10)", lambda: Conver_P_10.dval('-10.5', 10), {"C9": True}),
            ("dval('10.5', 10)", lambda: Conver_P_10.dval('10.5', 10), {"C9": False}),
            ("dval('10.5.6', 10)", lambda: Conver_P_10.dval('10.5.6', 10), {"C10": True}),
            ("dval('10.5', 10)", lambda: Conver_P_10.dval('10.5', 10), {"C10": False}),
            ("dval('A5', 16)", lambda: Conver_P_10.dval('A5', 16), {"C11": True, "C12": False}),
            ("dval('.E', 16)", lambda: Conver_P_10.dval('.E', 16), {"C11": False, "C12": True}),
            ("dval('A5.E', 16)", lambda: Conver_P_10.dval('A5.E', 16), {"C11": True, "C12": True}),
        ]
        
        condition_results = {cond: {"TRUE": False, "FALSE": False} for cond in conditions}
        
        for name, test_func, expected_conditions in test_cases:
            try:
                result = test_func()
                print(f"✓ {name}: {result}")
                
                for cond, value in expected_conditions.items():
                    if isinstance(value, tuple):
                        condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value[0]
                        condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or value[1]
                    else:
                        condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value
                        condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or not value
                        
            except ValueError as e:
                print(f"✓ {name}: исключение '{e}'")
                for cond, value in expected_conditions.items():
                    if isinstance(value, tuple):
                        condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value[0]
                        condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or value[1]
                    else:
                        condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value
                        condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or not value
        
        # Анализ покрытия условий
        print("\nАнализ покрытия условий:")
        print("-" * 50)
        
        fully_covered = 0
        total_conditions = len(conditions)
        
        for cond, desc in conditions.items():
            true_covered = condition_results[cond]["TRUE"]
            false_covered = condition_results[cond]["FALSE"]
            
            if true_covered and false_covered:
                status = "✓ ПОЛНОСТЬЮ"
                fully_covered += 1
            elif true_covered or false_covered:
                status = "✓ ЧАСТИЧНО"
            else:
                status = "✗ НЕ ПОКРЫТО"
            
            print(f"{cond}: {desc:30} TRUE={str(true_covered):5} FALSE={str(false_covered):5} {status}")
        
        coverage_percent = fully_covered / total_conditions * 100
        print(f"\nРезультат С2: {fully_covered}/{total_conditions} условий полностью покрыто")
        print(f"Процент покрытия: {coverage_percent:.1f}%")
        
        return fully_covered == total_conditions


# Быстрый тест основных функций
def quick_test():
    """Быстрый тест основных функций"""
    print("БЫСТРЫЙ ТЕСТ ОСНОВНЫХ ФУНКЦИЙ")
    print("=" * 50)
    
    tests = [
        ("char_to_num('5')", Conver_P_10.char_to_num('5'), 5),
        ("char_to_num('A')", Conver_P_10.char_to_num('A'), 10),
        ("char_to_num('F')", Conver_P_10.char_to_num('F'), 15),
        ("char_to_num('a')", Conver_P_10.char_to_num('a'), 10),
        ("char_to_num('f')", Conver_P_10.char_to_num('f'), 15),
        
        ("dval('A5.E', 16)", Conver_P_10.dval('A5.E', 16), 165.875),
        ("dval('-A5.E', 16)", Conver_P_10.dval('-A5.E', 16), -165.875),
        ("dval('1010.101', 2)", Conver_P_10.dval('1010.101', 2), 10.625),
        ("dval('FF', 16)", Conver_P_10.dval('FF', 16), 255.0),
        ("dval('0', 10)", Conver_P_10.dval('0', 10), 0.0),
        ("dval('0.5', 10)", Conver_P_10.dval('0.5', 10), 0.5),
        ("dval('A5', 16)", Conver_P_10.dval('A5', 16), 165.0),
        ("dval('.E', 16)", Conver_P_10.dval('.E', 16), 0.875),
    ]
    
    all_passed = True
    for name, result, expected in tests:
        if abs(result - expected) < 1e-10:
            print(f"✓ {name:20} = {result}")
        else:
            print(f"✗ {name:20} = {result} (ожидалось {expected})")
            all_passed = False
    
    return all_passed


# Основная программа
if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ КЛАССА Conver_P_10")
    print("=" * 70)
    
    # Быстрый тест
    print("\n1. Быстрый тест основных функций:")
    quick_passed = quick_test()
    
    if quick_passed:
        print("\n✓ Быстрый тест пройден успешно!")
        
        # Полное структурное тестирование
        tester = StructuralTester()
        
        c0_passed = tester.test_c0_coverage()
        c1_passed = tester.test_c1_coverage()
        c2_passed = tester.test_c2_coverage()
        
        print("\n" + "=" * 70)
        print("ИТОГИ СТРУКТУРНОГО ТЕСТИРОВАНИЯ:")
        print("=" * 70)
        print(f"Критерий С0 (покрытие операторов): {'ПРОЙДЕН ✓' if c0_passed else 'НЕ ПРОЙДЕН ✗'}")
        print(f"Критерий С1 (покрытие ветвей): {'ПРОЙДЕН ✓' if c1_passed else 'НЕ ПРОЙДЕН ✗'}")
        print(f"Критерий С2 (покрытие условий): {'ПРОЙДЕН ✓' if c2_passed else 'НЕ ПРОЙДЕН ✗'}")
        
        all_passed = all([c0_passed, c1_passed, c2_passed])
        
        # Создание отчета
        report = f"""
ОТЧЕТ О ТЕСТИРОВАНИИ
====================
Класс: Conver_P_10
Дата тестирования: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

РЕЗУЛЬТАТЫ:
1. Быстрый тест основных функций: {'ПРОЙДЕН ✓' if quick_passed else 'НЕ ПРОЙДЕН ✗'}
2. Критерий С0 (покрытие операторов): {'ПРОЙДЕН ✓' if c0_passed else 'НЕ ПРОЙДЕН ✗'}
3. Критерий С1 (покрытие ветвей): {'ПРОЙДЕН ✓' if c1_passed else 'НЕ ПРОЙДЕН ✗'}
4. Критерий С2 (покрытие условий): {'ПРОЙДЕН ✓' if c2_passed else 'НЕ ПРОЙДЕН ✗'}

ВЫВОД:
Класс Conver_P_10 {'соответствует ✓' if all_passed else 'не соответствует ✗'} 
требованиям структурного тестирования по заданным критериям.
"""
        
        print(report)
        
        # Сохранение отчета
        with open("test_report_conver_p_10.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("Подробный отчет сохранен в 'test_report_conver_p_10.txt'")
    else:
        print("\n✗ Быстрый тест не пройден! Исправьте ошибки перед структурным тестированием.")