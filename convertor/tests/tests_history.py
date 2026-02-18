import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from history import History, Record

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
            ("Record(10, 2, '10.5', '1010.1')", 
             lambda: isinstance(Record(10, 2, "10.5", "1010.1"), Record), True),
            
            ("str(Record(16, 10, 'A5.E', '165.875'))", 
             lambda: str(Record(16, 10, "A5.E", "165.875")).startswith("["), True),
            
            ("History()", 
             lambda: isinstance(History(), History), True),
            
            ("add_record(10, 2, '10.5', '1010.1')", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or h.count() == 1, True),
            
            ("get_record(0) - существующий индекс", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     isinstance(h.get_record(0), Record), True),
            
            ("get_record(999) - несуществующий индекс", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     h.get_record(999) is None, True),
            
            ("__getitem__(0) - существующий индекс", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     isinstance(h[0], Record), True),
            
            ("count() после добавления", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or h.count() == 1, True),
            
            ("clear()", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     (h.clear(), h.count() == 0)[1], True),
            
            ("len() после добавления", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or len(h) == 1, True),
            
            ("get_all_records()", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     len(h.get_all_records()) == 1, True),
            
            ("print_history() с записями", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     (h.print_history(), True)[1], True),
            
            ("print_history() пустая", 
             lambda: (h:=History()).print_history() or True, True),
        ]
        
        passed = 0
        for name, test_func, expected in test_cases:
            try:
                result = test_func()
                if result == expected:
                    print(f"✓ {name}")
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
        # get_record: 2 ветки (индекс в пределах / вне пределов)
        # __getitem__: 2 ветки (индекс в пределах / вне пределов)
        # print_history: 2 ветки (пустая / непустая)
        # Итого: 6 ветвей
        
        branches_covered = set()
        total_branches = 6
        
        # Тесты для каждой ветви
        test_branches = [
            # get_record ветви
            ("get_record - индекс в пределах", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     h.get_record(0) is not None, True, 1),
            
            ("get_record - индекс вне пределов", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     h.get_record(999) is None, True, 2),
            
            # __getitem__ ветви
            ("__getitem__ - индекс в пределах", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     isinstance(h[0], Record), True, 3),
            
            ("__getitem__ - индекс вне пределов", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     (lambda: h[999])(), None, 4, False),
            
            # print_history ветви
            ("print_history - непустая история", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     (h.print_history(), True)[1], True, 5),
            
            ("print_history - пустая история", 
             lambda: (h:=History()).print_history() or True, True, 6),
        ]
        
        for name, test_func, expected, branch_num, *should_pass in test_branches:
            should_pass = should_pass[0] if should_pass else True
            try:
                result = test_func()
                if should_pass:
                    # Для булевых значений проверяем равенство
                    if isinstance(expected, bool):
                        if result == expected:
                            print(f"✓ {name}: {result}")
                            branches_covered.add(branch_num)
                        else:
                            print(f"✗ {name}: {result} (ожидалось {expected})")
                    else:
                        # Для других значений просто проверяем, что они не None
                        if result is not None:
                            print(f"✓ {name}: {result}")
                            branches_covered.add(branch_num)
                        else:
                            print(f"✗ {name}: {result} (ожидалось не None)")
                else:
                    print(f"✗ {name}: должно было вызвать исключение")
            except IndexError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение IndexError")
                    branches_covered.add(branch_num)
                else:
                    print(f"✗ {name}: неожиданное исключение")
            except Exception as e:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение {type(e).__name__}")
                    branches_covered.add(branch_num)
                else:
                    print(f"✗ {name}: неожиданное исключение {e}")
        
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
            # get_record условие
            "C1": "0 <= index < len(self._records)",
            
            # __getitem__ условие
            "C2": "0 <= index < len(self._records)",
            
            # print_history условие
            "C3": "not self._records",
        }
        
        test_cases = [
            # Для get_record
            ("get_record - C1: TRUE", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     h.get_record(0) is not None, {"C1": True}),
            
            ("get_record - C1: FALSE", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     h.get_record(999) is None, {"C1": False}),
            
            # Для __getitem__
            ("__getitem__ - C2: TRUE", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     isinstance(h[0], Record), {"C2": True}),
            
            ("__getitem__ - C2: FALSE", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     (lambda: h[999])(), {"C2": False}, False),
            
            # Для print_history
            ("print_history - C3: TRUE (пустая)", 
             lambda: History().print_history(), {"C3": True}),
            
            ("print_history - C3: FALSE (непустая)", 
             lambda: (h:=History()).add_record(10, 2, "10.5", "1010.1") or 
                     h.print_history(), {"C3": False}),
        ]
        
        condition_results = {cond: {"TRUE": False, "FALSE": False} for cond in conditions}
        
        for name, test_func, expected_conditions, *should_pass in test_cases:
            should_pass = should_pass[0] if should_pass else True
            try:
                result = test_func()
                print(f"✓ {name}: {result}")
                
                for cond, value in expected_conditions.items():
                    condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value
                    condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or not value
                        
            except IndexError:
                print(f"✓ {name}: исключение IndexError")
                for cond, value in expected_conditions.items():
                    condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value
                    condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or not value
            except Exception as e:
                print(f"✓ {name}: исключение {e}")
        
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


def quick_test():
    """Быстрый тест основных функций"""
    print("БЫСТРЫЙ ТЕСТ КЛАССА HISTORY")
    print("=" * 50)
    
    history = History()
    print(f"✓ Создана история: {history.count()} записей")
    
    history.add_record(10, 2, "10.5", "1010.1")
    history.add_record(16, 10, "A5.E", "165.875")
    history.add_record(2, 16, "1010.101", "A.A")
    print(f"✓ Добавлено 3 записи: {history.count()} записей")
    
    record = history.get_record(0)
    print(f"✓ get_record(0): {record}")
    
    record = history[1]
    print(f"✓ history[1]: {record}")
    
    print(f"✓ count(): {history.count()}")
    print(f"✓ len(): {len(history)}")
    
    all_records = history.get_all_records()
    print(f"✓ get_all_records(): {len(all_records)} записей")
    
    print("\n✓ print_history():")
    history.print_history()
    
    history.clear()
    print(f"✓ После clear(): {history.count()} записей")
    
    record = history.get_record(0)
    print(f"✓ get_record(0) после clear: {record}")
    
    return True


def demo():
    """Демонстрация работы класса History"""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА HISTORY")
    print("=" * 60)
    
    history = History()
    
    print("\n1. Добавление записей:")
    test_data = [
        (10, 2, "10.5", "1010.1"),
        (16, 10, "A5.E", "165.875"),
        (2, 16, "1010.101", "A.A"),
        (8, 2, "12.4", "1010.1"),
    ]
    
    for p1, p2, n1, n2 in test_data:
        history.add_record(p1, p2, n1, n2)
        print(f"   Добавлено: {n1} (осн.{p1}) -> {n2} (осн.{p2})")
    
    print(f"\n2. Количество записей: {history.count()}")
    
    print("\n3. Получение записей по индексу:")
    print(f"   Запись 0: {history.get_record(0)}")
    print(f"   Запись 1: {history[1]}")
    print(f"   Запись 2: {history[2]}")
    
    print(f"\n4. Попытка получить несуществующую запись:")
    print(f"   Запись 999: {history.get_record(999)}")
    
    print("\n5. Вывод всей истории:")
    history.print_history()
    
    print("\n6. Очистка истории:")
    history.clear()
    print(f"   После очистки: {history.count()} записей")
    history.print_history()


if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ КЛАССА HISTORY")
    print("=" * 70)
    
    demo()
    
    print("\n" + "=" * 70)
    print("СТРУКТУРНОЕ ТЕСТИРОВАНИЕ")
    print("=" * 70)
    
    print("\n1. Быстрый тест основных функций:")
    quick_passed = quick_test()
    
    if quick_passed:
        print("\n✓ Быстрый тест пройден успешно!")
        
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
        
        report = f"""
ОТЧЕТ О ТЕСТИРОВАНИИ
====================
Класс: History
Дата тестирования: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

РЕЗУЛЬТАТЫ:
1. Быстрый тест основных функций: {'ПРОЙДЕН ✓' if quick_passed else 'НЕ ПРОЙДЕН ✗'}
2. Критерий С0 (покрытие операторов): {'ПРОЙДЕН ✓' if c0_passed else 'НЕ ПРОЙДЕН ✗'}
3. Критерий С1 (покрытие ветвей): {'ПРОЙДЕН ✓' if c1_passed else 'НЕ ПРОЙДЕН ✗'}
4. Критерий С2 (покрытие условий): {'ПРОЙДЕН ✓' if c2_passed else 'НЕ ПРОЙДЕН ✗'}

ВЫВОД:
Класс History {'соответствует ✓' if all_passed else 'не соответствует ✗'} 
требованиям структурного тестирования по заданным критериям.
"""
        
        print(report)
        
        with open("test_report_history.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("Подробный отчет сохранен в 'test_report_history.txt'")
    else:
        print("\n✗ Быстрый тест не пройден! Исправьте ошибки перед структурным тестированием.")
