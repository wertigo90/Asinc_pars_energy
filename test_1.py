import datetime
from pprint import pprint

# ls = list(range(10))
#
#
# for i in ls.copy():
#     if i < 5:
#         ls.remove(i)
# print(ls)

# print(ls)

# alphabet = {
#     'охран',
#     'лкс',
#     'обрыв',
# }
#
# messages = [
#     {'ext_info': '',
#      'text': 'ЛУ1 М70 ( РШ 3464 , Гр 358, п 98 )',
#      'timestamp': '0000000001cee8ee'},
#     {'ext_info': 'Сигнал создан 18.08.2009 пользователем Администратор',
#      'text': 'ЛУ3 лкс М-03 (РШ 56-35,ПСЭ-56,МС 13/92).  Длина=1595 м  R >= 254 '
#              'кОм  C=0,096 мкФ',
#      'timestamp': '0000000001cee8f4'},
#     {'ext_info': '',
#      'text': 'ЛУ1 Обрыв М70 ( РШ 3464 , Гр 358, п 98 )',
#      'timestamp': '0000000001cee8f2'},
#     {'ext_info': '',
#      'text': 'ЛУ1 Обрыв М70 ( РШ 3464 , Гр 358, п 98 )',
#      'timestamp': '0000000001cee8f6'},
#     {'ext_info': 'Сигнал создан 18.08.2009 пользователем Администратор',
#      'text': 'ЛУ3 Обрыв М-03 (РШ 56-35,ПСЭ-56,МС 13/92).  Длина=1617 м  R >= 254 '
#              'кОм  C=0,097 мкФ',
#      'timestamp': '0000000001cee8f9'}
# ]
#
# [messages.remove(i) for i in messages.copy() if any(map(lambda x: x in str(i["text"]).lower(), alphabet))]
# #
# pprint(messages)


a = 5/3

b = 60*a


min = int(b//60)
sec = int(b%60)

time = (f"{min}:{sec}")
if min>60:
    time = f"{sec}"
    time = datetime.datetime.strptime(time, "%S")
    time = f"{min}"+datetime.datetime.strftime(time, ":%S")
else:
    time = datetime.datetime.strptime(time, "%M:%S")
    time = datetime.datetime.strftime(time, "%M:%S")

print(time)
