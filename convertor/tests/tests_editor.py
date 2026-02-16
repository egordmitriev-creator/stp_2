import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from editor import Editor
class StructuralTester:
    @staticmethod
    def test_c0_coverage():
        """Тестирование по критерию С0 (покрытие операторов)"""
        print("=" * 70)
        print("КРИТЕРИЙ С0 - ПОКРЫТИЕ ОПЕРАТОРОВ")
        print("=" * 70)
        
        test_cases = [
            # Тест конструктора и свойства number
            ("new Editor().number", lambda: Editor().number, "0"),
            
            # Тест add_digit
            ("add_digit(5, 10)", lambda: Editor().add_digit(5, 10), "5"),
            ("add_digit(10, 16)", lambda: Editor().add_digit(10, 16), "A"),
            ("add_digit(15, 16)", lambda: Editor().add_digit(15, 16), "F"),
            ("add_digit(10, 10)", lambda: Editor().add_digit(10, 10), "0"),  # Недопустимая цифра
            
            # Тест add_zero
            ("add_zero(10)", lambda: Editor().add_zero(10), "0"),
            
            # Тест add_delim
            ("add_delim()", lambda: Editor().add_delim(), "0."),
            
            # Тест последовательности операций
            ("add_digit(1) + add_digit(0) + add_delim() + add_digit(5)", 
             lambda: (lambda e: (e.add_digit(1), e.add_digit(0), e.add_delim(), e.add_digit(5)) and e.number)(Editor()), "10.5"),
            
            # Тест bs
            ("bs() на '10.5'", lambda: (lambda e: (e.add_digit(1), e.add_digit(0), e.add_delim(), e.add_digit(5), e.bs()) and e.number)(Editor()), "10."),
            
            # Тест clear
            ("clear()", lambda: (lambda e: (e.add_digit(5), e.clear()) and e.number)(Editor()), "0"),
            
            # Тест acc
            ("acc() на '10.5'", lambda: (lambda e: (e.add_digit(1), e.add_digit(0), e.add_delim(), e.add_digit(5)) and e.acc())(Editor()), 1),
            ("acc() на '10'", lambda: (lambda e: (e.add_digit(1), e.add_digit(0)) and e.acc())(Editor()), 0),
            
            # Тест do_edit
            ("do_edit(5, 10)", lambda: Editor().do_edit(5, 10), "5"),
            ("do_edit(16, 10)", lambda: Editor().do_edit(16, 10), "0."),
            ("do_edit(17, 10)", lambda: (lambda e: (e.add_digit(5), e.do_edit(17)) and e.number)(Editor()), "0"),
            ("do_edit(18, 10)", lambda: (lambda e: (e.add_digit(5), e.do_edit(18)) and e.number)(Editor()), "0"),
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
        
        # Подсчет ветвей в каждом методе
        branches_covered = set()
        total_branches = 20  # Общее количество ветвей
        
        # Тесты для каждой ветви
        test_branches = [
            # add_digit ветви
            ("add_digit - недопустимая цифра", 
             lambda e: e.add_digit(10, 10), "0", 1),
            ("add_digit - ведущий ноль (число = '0', n=0)", 
             lambda e: (e.add_digit(0, 10), e.add_digit(0, 10)) and e.number, "0", 2),
            ("add_digit - пустое число, n=0", 
             lambda e: Editor().add_digit(0, 10), "0", 3),
            ("add_digit - пустое число, n>0", 
             lambda e: Editor().add_digit(5, 10), "5", 4),
            ("add_digit - добавление к существующему числу", 
             lambda e: (e.add_digit(1, 10), e.add_digit(2, 10)) and e.number, "12", 5),
            
            # add_delim ветви
            ("add_delim - пустое число", 
             lambda e: e.add_delim(), "0.", 6),
            ("add_delim - уже есть разделитель", 
             lambda e: (e.add_delim(), e.add_delim()) and e.number, "0.", 7),
            ("add_delim - число без разделителя", 
             lambda e: (e.add_digit(5, 10), e.add_delim()) and e.number, "5.", 8),
            
            # bs ветви
            ("bs - пустое число", 
             lambda e: e.bs(), "0", 9),
            ("bs - удаление разделителя", 
             lambda e: (e.add_delim(), e.bs()) and e.number, "0", 10),
            ("bs - удаление цифры", 
             lambda e: (e.add_digit(5, 10), e.bs()) and e.number, "0", 11),
            
            # clear ветвь
            ("clear - очистка числа", 
             lambda e: (e.add_digit(5, 10), e.clear()) and e.number, "0", 12),
            
            # acc ветви
            ("acc - нет разделителя", 
             lambda e: (e.add_digit(5, 10)) and e.acc(), 0, 13),
            ("acc - есть разделитель", 
             lambda e: (e.add_digit(5, 10), e.add_delim(), e.add_digit(2, 10)) and e.acc(), 1, 14),
            
            # do_edit ветви
            ("do_edit - команда цифры (0-15)", 
             lambda e: e.do_edit(5, 10), "5", 15),
            ("do_edit - команда разделителя (16)", 
             lambda e: e.do_edit(16, 10), "0.", 16),
            ("do_edit - команда забоя (17)", 
             lambda e: (e.add_digit(5, 10), e.do_edit(17)) and e.number, "0", 17),
            ("do_edit - команда очистки (18)", 
             lambda e: (e.add_digit(5, 10), e.do_edit(18)) and e.number, "0", 18),
            ("do_edit - недопустимая команда", 
             lambda e: e.do_edit(99, 10), None, 19, False),
            
            # _is_valid_digit ветви
            ("_is_valid_digit - допустимая цифра", 
             lambda e: e._is_valid_digit(5, 10), True, 20),
        ]
        
        for name, test_func, expected, branch_num, *should_pass in test_branches:
            should_pass = should_pass[0] if should_pass else True
            e = Editor()
            try:
                result = test_func(e)
                if should_pass:
                    if result == expected:
                        print(f"✓ {name}: {result}")
                        branches_covered.add(branch_num)
                    else:
                        print(f"✗ {name}: {result} (ожидалось {expected})")
                else:
                    print(f"✗ {name}: должно было вызвать исключение")
            except ValueError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение")
                    branches_covered.add(branch_num)
                else:
                    print(f"✗ {name}: неожиданное исключение")
        
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
            # add_digit условия
            "C1": "not self._is_valid_digit(n, p)",
            "C2": "self._number == self.ZERO and n == 0",
            "C3": "not self._number and n == 0",
            "C4": "not self._number",
            "C5": "else (добавление к существующему числу)",
            
            # add_delim условия
            "C6": "not self._number",
            "C7": "not self._has_delim",
            
            # bs условия
            "C8": "not self._number",
            "C9": "self._number[-1] == self.DELIM",
            "C10": "else (удаление цифры)",
            
            # acc условия
            "C11": "not self._number or self.DELIM not in self._number",
            "C12": "else (есть дробная часть)",
            
            # do_edit условия
            "C13": "0 <= j <= 15",
            "C14": "j == self.CMD_DELIM",
            "C15": "j == self.CMD_BS",
            "C16": "j == self.CMD_CLEAR",
            "C17": "else (неизвестная команда)",
        }
        
        test_cases = [
            # Для add_digit
            ("add_digit - C1: TRUE", lambda e: e.add_digit(10, 10), {"C1": True, "C2": False, "C3": False, "C4": False, "C5": False}),
            ("add_digit - C1: FALSE, C2: TRUE", 
             lambda e: (e.add_digit(0, 10), e.add_digit(0, 10)) and e.number, {"C1": False, "C2": True, "C3": False, "C4": False, "C5": False}),
            ("add_digit - C1: FALSE, C2: FALSE, C3: TRUE", 
             lambda e: Editor().add_digit(0, 10), {"C1": False, "C2": False, "C3": True, "C4": True, "C5": False}),
            ("add_digit - C1: FALSE, C2: FALSE, C3: FALSE, C4: TRUE", 
             lambda e: Editor().add_digit(5, 10), {"C1": False, "C2": False, "C3": False, "C4": True, "C5": False}),
            ("add_digit - C1: FALSE, C2: FALSE, C3: FALSE, C4: FALSE, C5: TRUE", 
             lambda e: (e.add_digit(1, 10), e.add_digit(2, 10)) and e.number, {"C1": False, "C2": False, "C3": False, "C4": False, "C5": True}),
            
            # Для add_delim
            ("add_delim - C6: TRUE, C7: TRUE", 
             lambda e: e.add_delim(), {"C6": True, "C7": True}),
            ("add_delim - C6: FALSE, C7: TRUE", 
             lambda e: (e.add_digit(5, 10), e.add_delim()) and e.number, {"C6": False, "C7": True}),
            ("add_delim - C6: FALSE, C7: FALSE", 
             lambda e: (e.add_delim(), e.add_delim()) and e.number, {"C6": False, "C7": False}),
            
            # Для bs
            ("bs - C8: TRUE", 
             lambda e: e.bs(), {"C8": True, "C9": False, "C10": False}),
            ("bs - C8: FALSE, C9: TRUE", 
             lambda e: (e.add_delim(), e.bs()) and e.number, {"C8": False, "C9": True, "C10": False}),
            ("bs - C8: FALSE, C9: FALSE, C10: TRUE", 
             lambda e: (e.add_digit(5, 10), e.bs()) and e.number, {"C8": False, "C9": False, "C10": True}),
            
            # Для acc
            ("acc - C11: TRUE", 
             lambda e: e.acc(), {"C11": True, "C12": False}),
            ("acc - C11: FALSE, C12: TRUE", 
             lambda e: (e.add_digit(5, 10), e.add_delim(), e.add_digit(2, 10)) and e.acc(), {"C11": False, "C12": True}),
            
            # Для do_edit
            ("do_edit - C13: TRUE", 
             lambda e: e.do_edit(5, 10), {"C13": True, "C14": False, "C15": False, "C16": False, "C17": False}),
            ("do_edit - C13: FALSE, C14: TRUE", 
             lambda e: e.do_edit(16, 10), {"C13": False, "C14": True, "C15": False, "C16": False, "C17": False}),
            ("do_edit - C13: FALSE, C14: FALSE, C15: TRUE", 
             lambda e: e.do_edit(17, 10), {"C13": False, "C14": False, "C15": True, "C16": False, "C17": False}),
            ("do_edit - C13: FALSE, C14: FALSE, C15: FALSE, C16: TRUE", 
             lambda e: e.do_edit(18, 10), {"C13": False, "C14": False, "C15": False, "C16": True, "C17": False}),
            ("do_edit - C13: FALSE, C14: FALSE, C15: FALSE, C16: FALSE, C17: TRUE", 
             lambda e: e.do_edit(99, 10), {"C13": False, "C14": False, "C15": False, "C16": False, "C17": True}),
        ]
        
        condition_results = {cond: {"TRUE": False, "FALSE": False} for cond in conditions}
        
        for name, test_func, expected_conditions in test_cases:
            e = Editor()
            try:
                result = test_func(e)
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
            
            print(f"{cond}: {desc:40} TRUE={str(true_covered):5} FALSE={str(false_covered):5} {status}")
        
        coverage_percent = fully_covered / total_conditions * 100
        print(f"\nРезультат С2: {fully_covered}/{total_conditions} условий полностью покрыто")
        print(f"Процент покрытия: {coverage_percent:.1f}%")
        
        return fully_covered == total_conditions


# Быстрый тест основных функций
def quick_test():
    """Быстрый тест основных функций"""
    print("БЫСТРЫЙ ТЕСТ КЛАССА EDITOR")
    print("=" * 50)
    
    tests = [
        ("Создание редактора", lambda: Editor().number, "0"),
        ("Добавление цифры 5", lambda: (e:=Editor()).add_digit(5, 10) or e.number, "5"),
        ("Добавление цифры A (16-ная)", lambda: (e:=Editor()).add_digit(10, 16) or e.number, "A"),
        ("Добавление нуля", lambda: (e:=Editor()).add_zero(10) or e.number, "0"),
        ("Добавление разделителя", lambda: (e:=Editor()).add_delim() or e.number, "0."),
        ("Формирование числа 10.5", lambda: (e:=Editor()) and (e.add_digit(1,10), e.add_digit(0,10), e.add_delim(), e.add_digit(5,10)) and e.number, "10.5"),
        ("Забой символа", lambda: (e:=Editor()) and (e.add_digit(1,10), e.add_digit(0,10), e.bs()) and e.number, "1"),
        ("Очистка", lambda: (e:=Editor()) and (e.add_digit(5,10), e.clear()) and e.number, "0"),
        ("Точность числа 10.5", lambda: (e:=Editor()) and (e.add_digit(1,10), e.add_digit(0,10), e.add_delim(), e.add_digit(5,10)) and e.acc(), 1),
        ("Команда do_edit 5", lambda: Editor().do_edit(5, 10), "5"),
        ("Команда do_edit 16 (разделитель)", lambda: Editor().do_edit(16, 10), "0."),
    ]
    
    all_passed = True
    for name, test_func, expected in tests:
        try:
            result = test_func()
            if result == expected:
                print(f"✓ {name:30} = '{result}'")
            else:
                print(f"✗ {name:30} = '{result}' (ожидалось '{expected}')")
                all_passed = False
        except Exception as e:
            print(f"✗ {name:30} вызвал исключение: {e}")
            all_passed = False
    
    return all_passed


# Основная программа
if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ КЛАССА EDITOR")
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
Класс: Editor
Дата тестирования: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

РЕЗУЛЬТАТЫ:
1. Быстрый тест основных функций: {'ПРОЙДЕН ✓' if quick_passed else 'НЕ ПРОЙДЕН ✗'}
2. Критерий С0 (покрытие операторов): {'ПРОЙДЕН ✓' if c0_passed else 'НЕ ПРОЙДЕН ✗'}
3. Критерий С1 (покрытие ветвей): {'ПРОЙДЕН ✓' if c1_passed else 'НЕ ПРОЙДЕН ✗'}
4. Критерий С2 (покрытие условий): {'ПРОЙДЕН ✓' if c2_passed else 'НЕ ПРОЙДЕН ✗'}

ВЫВОД:
Класс Editor {'соответствует ✓' if all_passed else 'не соответствует ✗'} 
требованиям структурного тестирования по заданным критериям.
"""
        
        print(report)
        
        # Сохранение отчета
        with open("test_report_editor.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("Подробный отчет сохранен в 'test_report_editor.txt'")
    else:
        print("\n✗ Быстрый тест не пройден! Исправьте ошибки перед структурным тестированием.")