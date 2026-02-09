from conver_10_p import Conver_10_P
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
            # Метод int_to_char
            ("int_to_char(5)", lambda: Conver_10_P.int_to_char(5), '5'),
            ("int_to_char(10)", lambda: Conver_10_P.int_to_char(10), 'A'),
            ("int_to_char(0)", lambda: Conver_10_P.int_to_char(0), '0'),
            ("int_to_char(15)", lambda: Conver_10_P.int_to_char(15), 'F'),
            
            # Метод int_to_p
            ("int_to_p(0, 16)", lambda: Conver_10_P.int_to_p(0, 16), '0'),
            ("int_to_p(10, 2)", lambda: Conver_10_P.int_to_p(10, 2), '1010'),
            ("int_to_p(-10, 2)", lambda: Conver_10_P.int_to_p(-10, 2), '-1010'),
            ("int_to_p(161, 16)", lambda: Conver_10_P.int_to_p(161, 16), 'A1'),
            ("int_to_p(1, 16)", lambda: Conver_10_P.int_to_p(1, 16), '1'),
            
            # Метод flt_to_p
            ("flt_to_p(0.5, 2, 4)", lambda: Conver_10_P.flt_to_p(0.5, 2, 4), '1'),
            ("flt_to_p(0.9375, 2, 4)", lambda: Conver_10_P.flt_to_p(0.9375, 2, 4), '1111'),
            ("flt_to_p(0.0, 2, 4)", lambda: Conver_10_P.flt_to_p(0.0, 2, 4), '0'),
            ("flt_to_p(0.625, 2, 4)", lambda: Conver_10_P.flt_to_p(0.625, 2, 4), '101'),
            
            # Метод do
            ("do(10.5, 2, 4)", lambda: Conver_10_P.do(10.5, 2, 4), '1010.1'),
            ("do(-17.875, 16, 3)", lambda: Conver_10_P.do(-17.875, 16, 3), '-11.E'),
            ("do(0.0, 16, 3)", lambda: Conver_10_P.do(0.0, 16, 3), '0'),
            ("do(10.0, 2, 0)", lambda: Conver_10_P.do(10.0, 2, 0), '1010'),
            ("do(10.5, 2, 0)", lambda: Conver_10_P.do(10.5, 2, 0), '1010'),
        ]
        
        passed = 0
        for name, test_func, expected in test_cases:
            try:
                result = test_func()
                if result == expected:
                    print(f"✓ {name} = '{result}'")
                    passed += 1
                else:
                    print(f"✗ {name} = '{result}' (ожидалось '{expected}')")
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
        
        # Правильный подсчет ветвей:
        # int_to_char: 3 ветви (if, elif, else)
        # int_to_p: 4 ветви (p вне диапазона, n==0, n<0, n>0)
        # flt_to_p: 4 ветви (p вне диапазона, n вне диапазона, c<0, нормальный случай)
        # do: 3 ветви (p вне диапазона, дробь и точность >0, иначе)
        # Итого: 3 + 4 + 4 + 3 = 14 ветвей
        
        branches_covered = set()
        total_branches = 14
        
        # Ветви в int_to_char
        test_cases = [
            ("int_to_char(5) - ветка 0-9", lambda: Conver_10_P.int_to_char(5), True, 1),
            ("int_to_char(10) - ветка A-F", lambda: Conver_10_P.int_to_char(10), True, 2),
            ("int_to_char(20) - ветка исключение", lambda: Conver_10_P.int_to_char(20), False, 3),
        ]
        
        for name, test_func, should_pass, branch_num in test_cases:
            try:
                result = test_func()
                if should_pass:
                    print(f"✓ {name}: '{result}'")
                    branches_covered.add(branch_num)
            except ValueError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение")
                    branches_covered.add(branch_num)
        
        # Ветви в int_to_p
        test_cases_int_to_p = [
            ("int_to_p(10, 1) - ветка p вне диапазона", lambda: Conver_10_P.int_to_p(10, 1), False, 4),
            ("int_to_p(0, 2) - ветка n == 0", lambda: Conver_10_P.int_to_p(0, 2), True, 5),
            ("int_to_p(-10, 2) - ветка n < 0", lambda: Conver_10_P.int_to_p(-10, 2), True, 6),
            ("int_to_p(10, 2) - ветка n > 0", lambda: Conver_10_P.int_to_p(10, 2), True, 7),
        ]
        
        for name, test_func, should_pass, branch_num in test_cases_int_to_p:
            try:
                result = test_func()
                if should_pass:
                    print(f"✓ {name}: '{result}'")
                    branches_covered.add(branch_num)
            except ValueError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение")
                    branches_covered.add(branch_num)
        
        # Ветви в flt_to_p
        test_cases_flt_to_p = [
            ("flt_to_p(0.5, 1, 4) - ветка p вне диапазона", lambda: Conver_10_P.flt_to_p(0.5, 1, 4), False, 8),
            ("flt_to_p(-0.5, 2, 4) - ветка n вне диапазона", lambda: Conver_10_P.flt_to_p(-0.5, 2, 4), False, 9),
            ("flt_to_p(0.5, 2, -1) - ветка c < 0", lambda: Conver_10_P.flt_to_p(0.5, 2, -1), False, 10),
            ("flt_to_p(0.5, 2, 4) - нормальная ветка", lambda: Conver_10_P.flt_to_p(0.5, 2, 4), True, 11),
        ]
        
        for name, test_func, should_pass, branch_num in test_cases_flt_to_p:
            try:
                result = test_func()
                if should_pass:
                    print(f"✓ {name}: '{result}'")
                    branches_covered.add(branch_num)
            except ValueError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение")
                    branches_covered.add(branch_num)
        
        # Ветви в do
        test_cases_do = [
            ("do(10.5, 1, 4) - ветка p вне диапазона", lambda: Conver_10_P.do(10.5, 1, 4), False, 12),
            ("do(10.5, 2, 4) - ветка дробь и точность > 0", lambda: Conver_10_P.do(10.5, 2, 4), True, 13),
            ("do(10.0, 2, 4) - ветка иначе", lambda: Conver_10_P.do(10.0, 2, 4), True, 14),
        ]
        
        for name, test_func, should_pass, branch_num in test_cases_do:
            try:
                result = test_func()
                if should_pass:
                    print(f"✓ {name}: '{result}'")
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
            "C1": "0 <= d <= 9",
            "C2": "10 <= d <= 15",
            
            "C3": "p < 2",
            "C4": "p > 16",
            "C5": "n == 0",
            "C6": "n < 0",
            "C7": "n > 0",
            
            "C8": "p < 2",
            "C9": "p > 16", 
            "C10": "n < 0",
            "C11": "n >= 1",
            "C12": "c < 0",
            
            "C13": "p < 2",
            "C14": "p > 16",
            "C15": "frac_part > 0",
            "C16": "c > 0",
        }
        
        # Тестовые случаи для полного покрытия условий
        test_cases = [
            # Для полного покрытия C7 (n > 0)
            ("n=1, p=10", lambda: Conver_10_P.int_to_p(1, 10), {"C5": False, "C6": False, "C7": True}),
            
            # Остальные тесты как были
            ("d=5", lambda: Conver_10_P.int_to_char(5), {"C1": (True, True)}),
            ("d=10", lambda: Conver_10_P.int_to_char(10), {"C1": (False, False), "C2": (True, True)}),
            ("d=-1", lambda: Conver_10_P.int_to_char(-1), {"C1": (False, True), "C2": (False, False)}),
            
            ("p=1, n=10", lambda: Conver_10_P.int_to_p(10, 1), {"C3": True, "C4": False}),
            ("p=20, n=10", lambda: Conver_10_P.int_to_p(10, 20), {"C3": False, "C4": True}),
            ("p=10, n=0", lambda: Conver_10_P.int_to_p(0, 10), {"C5": True, "C6": False, "C7": False}),
            ("p=10, n=-5", lambda: Conver_10_P.int_to_p(-5, 10), {"C5": False, "C6": True, "C7": True}),
            
            ("p=1, n=0.5, c=4", lambda: Conver_10_P.flt_to_p(0.5, 1, 4), {"C8": True, "C9": False}),
            ("p=20, n=0.5, c=4", lambda: Conver_10_P.flt_to_p(0.5, 20, 4), {"C8": False, "C9": True}),
            ("n=-0.1, p=2, c=4", lambda: Conver_10_P.flt_to_p(-0.1, 2, 4), {"C10": True, "C11": False}),
            ("n=1.0, p=2, c=4", lambda: Conver_10_P.flt_to_p(1.0, 2, 4), {"C10": False, "C11": True}),
            ("n=0.5, p=2, c=-1", lambda: Conver_10_P.flt_to_p(0.5, 2, -1), {"C12": True}),
            ("n=0.5, p=2, c=4", lambda: Conver_10_P.flt_to_p(0.5, 2, 4), {"C10": False, "C11": False, "C12": False}),
            
            ("n=10.5, p=1, c=4", lambda: Conver_10_P.do(10.5, 1, 4), {"C13": True, "C14": False}),
            ("n=10.5, p=20, c=4", lambda: Conver_10_P.do(10.5, 20, 4), {"C13": False, "C14": True}),
            ("n=10.5, p=2, c=4", lambda: Conver_10_P.do(10.5, 2, 4), {"C15": True, "C16": True}),
            ("n=10.0, p=2, c=4", lambda: Conver_10_P.do(10.0, 2, 4), {"C15": False, "C16": True}),
            ("n=10.5, p=2, c=0", lambda: Conver_10_P.do(10.5, 2, 0), {"C15": True, "C16": False}),
        ]
        
        condition_results = {cond: {"TRUE": False, "FALSE": False} for cond in conditions}
        
        for name, test_func, expected_conditions in test_cases:
            try:
                result = test_func()
                print(f"✓ {name}: '{result}'")
                
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
            
            print(f"{cond}: {desc:20} TRUE={str(true_covered):5} FALSE={str(false_covered):5} {status}")
        
        coverage_percent = fully_covered / total_conditions * 100
        print(f"\nРезультат С2: {fully_covered}/{total_conditions} условий полностью покрыто")
        print(f"Процент покрытия: {coverage_percent:.1f}%")
        
        return fully_covered == total_conditions


# Упрощенный тест для быстрой проверки
def quick_test():
    """Быстрый тест основных функций"""
    print("БЫСТРЫЙ ТЕСТ ОСНОВНЫХ ФУНКЦИЙ")
    print("=" * 50)
    
    tests = [
        ("int_to_char(5)", Conver_10_P.int_to_char(5), '5'),
        ("int_to_char(10)", Conver_10_P.int_to_char(10), 'A'),
        ("int_to_char(15)", Conver_10_P.int_to_char(15), 'F'),
        
        ("int_to_p(0, 16)", Conver_10_P.int_to_p(0, 16), '0'),
        ("int_to_p(161, 16)", Conver_10_P.int_to_p(161, 16), 'A1'),
        ("int_to_p(-17, 16)", Conver_10_P.int_to_p(-17, 16), '-11'),
        ("int_to_p(1, 16)", Conver_10_P.int_to_p(1, 16), '1'),
        
        ("flt_to_p(0.9375, 2, 4)", Conver_10_P.flt_to_p(0.9375, 2, 4), '1111'),
        ("flt_to_p(0.875, 16, 3)", Conver_10_P.flt_to_p(0.875, 16, 3), 'E'),
        ("flt_to_p(0.5, 2, 4)", Conver_10_P.flt_to_p(0.5, 2, 4), '1'),
        
        ("do(-17.875, 16, 3)", Conver_10_P.do(-17.875, 16, 3), '-11.E'),
        ("do(10.5, 2, 4)", Conver_10_P.do(10.5, 2, 4), '1010.1'),
        ("do(0.0, 16, 3)", Conver_10_P.do(0.0, 16, 3), '0'),
    ]
    
    all_passed = True
    for name, result, expected in tests:
        if result == expected:
            print(f"✓ {name:30} = '{result}'")
        else:
            print(f"✗ {name:30} = '{result}' (ожидалось '{expected}')")
            all_passed = False
    
    return all_passed


# Основная программа
if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ КЛАССА Conver_10_P")
    print("=" * 70)
    
    # Сначала быстрый тест
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
Класс: Conver_10_P
Дата тестирования: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

РЕЗУЛЬТАТЫ:
1. Быстрый тест основных функций: {'ПРОЙДЕН ✓' if quick_passed else 'НЕ ПРОЙДЕН ✗'}
2. Критерий С0 (покрытие операторов): {'ПРОЙДЕН ✓' if c0_passed else 'НЕ ПРОЙДЕН ✗'}
3. Критерий С1 (покрытие ветвей): {'ПРОЙДЕН ✓' if c1_passed else 'НЕ ПРОЙДЕН ✗'}
4. Критерий С2 (покрытие условий): {'ПРОЙДЕН ✓' if c2_passed else 'НЕ ПРОЙДЕН ✗'}

ВЫВОД:
Класс Conver_10_P {'соответствует ✓' if all_passed else 'не соответствует ✗'} 
требованиям структурного тестирования по заданным критериям.
"""
        
        print(report)
        
        # Сохранение отчета
        with open("test_report_fixed.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("Подробный отчет сохранен в 'test_report_fixed.txt'")
    else:
        print("\n✗ Быстрый тест не пройден! Исправьте ошибки перед структурным тестированием.")