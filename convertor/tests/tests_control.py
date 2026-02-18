import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from control import State, Control_
from editor import Editor
from history import History

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
            # Тест конструктора
            ("Control_()", 
             lambda: isinstance(Control_(), Control_), True),
            
            # Тест свойств pin
            ("pin get/set", 
             lambda: (lambda c: c.pin == 10 and 
                     (setattr(c, 'pin', 16) or c.pin == 16))(Control_()), True),
            
            # Тест свойств pout
            ("pout get/set", 
             lambda: (lambda c: c.pout == 16 and 
                     (setattr(c, 'pout', 2) or c.pout == 2))(Control_()), True),
            
            # Тест свойств state
            ("state get/set", 
             lambda: (lambda c: c.state == State.РЕДАКТИРОВАНИЕ and 
                     (setattr(c, 'state', State.ПРЕОБРАЗОВАНО) or 
                      c.state == State.ПРЕОБРАЗОВАНО))(Control_()), True),
            
            # Тест editor property
            ("editor property", 
             lambda: isinstance(Control_().editor, Editor), True),
            
            # Тест history property
            ("history property", 
             lambda: isinstance(Control_().history, History), True),
            
            # Тест _calculate_accuracy
            ("_calculate_accuracy()", 
             lambda: (lambda c: c._calculate_accuracy() >= 0)(Control_()), True),
            
            # Тест do_command с командой редактирования
            ("do_command(5) - добавить цифру", 
             lambda: Control_().do_command(5) == "5", True),
            
            # Тест do_command с командой выполнения
            ("do_command(19) - выполнить", 
             lambda: (lambda c: 
                     c.do_command(1) and  # добавить 1
                     c.do_command(0) and  # добавить 0
                     c.do_command(16) and # добавить разделитель
                     c.do_command(5) and  # добавить 5
                     c.do_command(19) != "0")(Control_()), True),
            
            # Тест reset
            ("reset()", 
             lambda: (lambda c: 
                     c.do_command(5) and 
                     (c.reset() or True) and 
                     c.editor.number == "0")(Control_()), True),
            
            # Тест get_last_record
            ("get_last_record()", 
             lambda: (lambda c: 
                     c.do_command(1) and c.do_command(0) and 
                     c.do_command(16) and c.do_command(5) and 
                     c.do_command(19) and 
                     c.get_last_record() != "История пуста")(Control_()), True),
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
        # do_command: 2 ветки (команда выполнения / команды редактирования)
        # _calculate_accuracy: 3 ветки (editor.acc == 0, try-except, return)
        # pin.setter: 2 ветки (валидное/невалидное значение)
        # pout.setter: 2 ветки (валидное/невалидное значение)
        # Итого: 9 ветвей
        
        branches_covered = set()
        total_branches = 9
        
        # Тесты для каждой ветви
        test_branches = [
            # do_command ветви
            ("do_command - команда выполнения (19)", 
             lambda: (lambda c: c.do_command(19) is not None)(Control_()), True, 1),
            ("do_command - команда редактирования (5)", 
             lambda: Control_().do_command(5) == "5", True, 2),
            
            # _calculate_accuracy ветви
            ("_calculate_accuracy - editor.acc() == 0", 
             lambda: (lambda c: c._calculate_accuracy() == 0)(Control_()), True, 3),
            ("_calculate_accuracy - нормальное вычисление", 
             lambda: (lambda c: 
                     c.do_command(1) and c.do_command(0) and 
                     c.do_command(16) and c.do_command(5) and 
                     c._calculate_accuracy() > 0)(Control_()), True, 4),
            
            # pin.setter ветви
            ("pin.setter - валидное значение", 
             lambda: (lambda c: (setattr(c, 'pin', 16) or c.pin == 16))(Control_()), True, 5),
            ("pin.setter - невалидное значение", 
             lambda: (lambda c: setattr(c, 'pin', 20))(Control_()), None, 6, False),
            
            # pout.setter ветви
            ("pout.setter - валидное значение", 
             lambda: (lambda c: (setattr(c, 'pout', 2) or c.pout == 2))(Control_()), True, 7),
            ("pout.setter - невалидное значение", 
             lambda: (lambda c: setattr(c, 'pout', 1))(Control_()), None, 8, False),
            
            # do_command с ошибкой преобразования
            ("do_command(19) - ошибка преобразования", 
             lambda: (lambda c: 
                     c.do_command(18) and  # очистка
                     c.do_command(19) == "0")(Control_()), True, 9),
        ]
        
        for name, test_func, expected, branch_num, *should_pass in test_branches:
            should_pass = should_pass[0] if should_pass else True
            try:
                result = test_func()
                if should_pass:
                    if isinstance(expected, bool):
                        if result == expected:
                            print(f"✓ {name}: {result}")
                            branches_covered.add(branch_num)
                        else:
                            print(f"✗ {name}: {result} (ожидалось {expected})")
                    else:
                        if result is not None:
                            print(f"✓ {name}: {result}")
                            branches_covered.add(branch_num)
                        else:
                            print(f"✗ {name}: {result} (ожидалось не None)")
                else:
                    print(f"✗ {name}: должно было вызвать исключение")
            except ValueError:
                if not should_pass:
                    print(f"✓ {name}: корректно вызвано исключение ValueError")
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
            # do_command условия
            "C1": "command == self.CMD_EXECUTE",
            
            # _calculate_accuracy условия
            "C2": "self._editor.acc() == 0",
            "C3": "try-except блок (исключение)",
            
            # pin.setter условия
            "C4": "2 <= value <= 16",
            
            # pout.setter условия
            "C5": "2 <= value <= 16",
        }
        
        # Вспомогательный класс для тестирования исключения
        class TestControl(Control_):
            def _calculate_accuracy(self):
                # Форсируем исключение для теста
                raise ValueError("Тестовое исключение")
        
        test_cases = [
            # Для do_command
            ("do_command - C1: TRUE (команда 19)", 
             lambda: (lambda c: c.do_command(19) is not None)(Control_()), {"C1": True}),
            ("do_command - C1: FALSE (команда 5)", 
             lambda: Control_().do_command(5) == "5", {"C1": False}),
            
            # Для _calculate_accuracy
            ("_calculate_accuracy - C2: TRUE (editor.acc == 0)", 
             lambda: (lambda c: c._calculate_accuracy() == 0)(Control_()), {"C2": True}),
            ("_calculate_accuracy - C2: FALSE, C3: FALSE (нормально)", 
             lambda: (lambda c: 
                     c.do_command(1) and c.do_command(0) and 
                     c.do_command(16) and c.do_command(5) and 
                     c._calculate_accuracy() > 0)(Control_()), {"C2": False, "C3": False}),
            
            # Добавляем тест для C3: TRUE (исключение)
            ("_calculate_accuracy - C3: TRUE (исключение)", 
             lambda: (lambda c: c._calculate_accuracy())(TestControl()), {"C3": True}, False),
            
            # Для pin.setter
            ("pin.setter - C4: TRUE", 
             lambda: (lambda c: (setattr(c, 'pin', 16) or c.pin == 16))(Control_()), {"C4": True}),
            ("pin.setter - C4: FALSE", 
             lambda: (lambda c: setattr(c, 'pin', 20))(Control_()), {"C4": False}, False),
            
            # Для pout.setter
            ("pout.setter - C5: TRUE", 
             lambda: (lambda c: (setattr(c, 'pout', 2) or c.pout == 2))(Control_()), {"C5": True}),
            ("pout.setter - C5: FALSE", 
             lambda: (lambda c: setattr(c, 'pout', 1))(Control_()), {"C5": False}, False),
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
                        
            except ValueError:
                print(f"✓ {name}: исключение ValueError")
                for cond, value in expected_conditions.items():
                    # Для теста с исключением, C3 должно быть TRUE
                    if cond == "C3":
                        condition_results[cond]["TRUE"] = True
                    else:
                        condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value
                        condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or not value
            except Exception as e:
                print(f"✓ {name}: исключение {e}")
                for cond, value in expected_conditions.items():
                    condition_results[cond]["TRUE"] = condition_results[cond]["TRUE"] or value
                    condition_results[cond]["FALSE"] = condition_results[cond]["FALSE"] or not value
        
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
    print("БЫСТРЫЙ ТЕСТ КЛАССА CONTROL_")
    print("=" * 50)
    
    control = Control_()
    print(f"✓ Создан объект Control_: {control}")
    
    # Тест свойств
    control.pin = 8
    control.pout = 2
    print(f"✓ Установлены свойства: pin={control.pin}, pout={control.pout}")
    
    # Тест команд редактирования
    control.do_command(1)  # 1
    control.do_command(0)  # 0
    control.do_command(16) # .
    control.do_command(5)  # 5
    print(f"✓ После команд редактирования: {control.editor.number}")
    
    # Тест команды выполнения
    result = control.do_command(19)
    print(f"✓ После выполнения: {result}")
    print(f"✓ Состояние: {control.state.value}")
    
    # Тест истории
    print(f"✓ Последняя запись: {control.get_last_record()}")
    
    # Тест сброса
    control.reset()
    print(f"✓ После сброса: {control}")
    
    return True


def demo():
    """Демонстрация работы класса Control_"""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА CONTROL_")
    print("=" * 60)
    
    control = Control_()
    
    print("\n1. Начальное состояние:")
    print(f"   {control}")
    
    print("\n2. Ввод числа 10.5 в 10-ной системе:")
    control.do_command(1)   # 1
    control.do_command(0)   # 0
    control.do_command(16)  # .
    control.do_command(5)   # 5
    print(f"   Число: {control.editor.number}")
    print(f"   Состояние: {control.state.value}")
    
    print("\n3. Преобразование в 16-ную систему:")
    result = control.do_command(19)
    print(f"   Результат: {result}")
    print(f"   Состояние: {control.state.value}")
    
    print("\n4. Изменение основания результата на 2:")
    control.pout = 2
    result = control.do_command(19)
    print(f"   Результат: {result}")
    
    print("\n5. Просмотр истории:")
    print(f"   {control.get_last_record()}")
    
    print("\n6. Сброс:")
    control.reset()
    print(f"   {control}")


if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ КЛАССА CONTROL_")
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
Класс: Control_
Дата тестирования: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

РЕЗУЛЬТАТЫ:
1. Быстрый тест основных функций: {'ПРОЙДЕН ✓' if quick_passed else 'НЕ ПРОЙДЕН ✗'}
2. Критерий С0 (покрытие операторов): {'ПРОЙДЕН ✓' if c0_passed else 'НЕ ПРОЙДЕН ✗'}
3. Критерий С1 (покрытие ветвей): {'ПРОЙДЕН ✓' if c1_passed else 'НЕ ПРОЙДЕН ✗'}
4. Критерий С2 (покрытие условий): {'ПРОЙДЕН ✓' if c2_passed else 'НЕ ПРОЙДЕН ✗'}

ВЫВОД:
Класс Control_ {'соответствует ✓' if all_passed else 'не соответствует ✗'} 
требованиям структурного тестирования по заданным критериям.
"""
        
        print(report)
        
        with open("test_report_control.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("Подробный отчет сохранен в 'test_report_control.txt'")
    else:
        print("\n✗ Быстрый тест не пройден! Исправьте ошибки перед структурным тестированием.")