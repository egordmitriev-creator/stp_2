from convertor.convers.conver_10_p import Conver_10_P
from convertor.convers.conver_p_10 import Conver_P_10

result = Conver_10_P.do(-17.875, 16, 1)
print(result)  # Выведет: -11.E

result2 = Conver_P_10.char_to_num('A')
print(result2)