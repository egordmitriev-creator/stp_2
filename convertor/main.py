from convers.conver_10_p import Conver_10_P
from convers.conver_p_10 import Conver_P_10
from editor import Editor

result = Conver_10_P.do(-17.875, 16, 1)
print(result)  # Выведет: -11.E

result2 = Conver_P_10.char_to_num('A')
print(result2)

editor = Editor()
editor.add_digit(1, 10)      # "1"
print(editor.number)
editor.add_digit(0, 10)      # "10"
print(editor.number)
editor.add_delim()            # "10."
print(editor.number)
editor.add_digit(5, 10)       # "10.5"
acc = editor.acc()                  # 1
print(editor.number)
print(acc)
editor.bs()                   # "10."
print(editor.number)
acc = editor.acc()                  # 1
print(acc)
editor.clear()  
print(editor.number)