# Изменения цвета шрифта
# 30	Чёрный
# 31	Красный
# 32	Зелёный
# 33	Жёлтый
# 34	Синий
# 35	Фиолетовый
# 36	Бирюзовый
# 37	Белый
#
# Изменения цвета фона
# 40	Чёрный
# 41	Красный
# 42	Зелёный
# 43	Жёлтый
# 44	Синий
# 45	Фиолетовый
# 46	Бирюзовый
# 47	Белый
#
# Модификатор
# 38	RGB цвет (см. раздел "Совсем много цветов")
# 21	Двойное подчёркивание
# 51	Обрамлённый
# 52	Окружённый
# 53	Надчёркнутый

# black foreground | red background
#print('\033[41m\033[30m TEXT \033[0m')
#
## black foreground | green background
#print('\033[42m\033[30m TEXT \033[0m')
#
## black foreground | white background
#print('\033[47m\033[30m TEXT \033[0m')
#
##
#print('\033[43m\033[30m TEXT \033[0m')

import time
import sys

eipList = []
eipStringList = []

eipDiscovered = 'eipalloc-0515386b6d9e01fff	None	test	54.88.193.11\neipalloc-8015386b6d9e01ddd	i-45238759873	test2	100.99.193.7\n'
eipDiscoveredList = eipDiscovered[:-1].split('\n')
for i in range(len(eipDiscoveredList)):
	eipStringList = eipDiscoveredList[i].split('\t')
	if eipStringList[1] == 'None':
		#eipList.append(f'{eipDiscoveredList[i]} !!! not associated \n')
		eipList.append(f'{eipStringList[0]}\tnot associated\t{eipStringList[2]}\t{eipStringList[3]}\n')
	else:
		eipList.append(f'{eipDiscoveredList[i]}\n')

for res in eipList:
	sys.stderr.write(res)


