from operator import itemgetter


def task_01(one_to_many) -> list:
    """ ЗАДАНИЕ №1.
    Вывести имя IDE, которое заканчивается на "e" и количество пользователей и отсортированный список языков,
    которые поддерживается данным IDE.
    :param one_to_many: Список один ко многим.
    :return: Отфильтрованный список по первой букве, с отсортированным внутренним списком.
    """
    # Пояснение. Сначала отфильтровал список one_to_many по принципу: последняя буква равна 'e', потом
    # создал новый список res, сортируя список класса. Новая переменная, так как tuple нельзя изменять.
    return [(name, count, sorted(lst)) for name, count, lst in
            list(filter(lambda el: el[0][-1].lower() == 'e', one_to_many))]


def task_02(one_to_many) -> list:
    """ Задание 2.
    Вывести список IDE, которое поддерживает среднее количество языков. Вывод совершить в порядке убывания.
    :param one_to_many:
    :return: Список кортежей, состоящий из имени IDE и кол-ва языков, которые поддерживает.
    """
    # Пояснение. Сначала создаю список, состоящий из кортежей. Первый элемент - имя IDE, второй - кол-во языков,
    # которое он поддерживает.
    # Потом сортирую список по второму элементу.
    return sorted([(el[0], len(el[2])) for el in one_to_many],
                  key=itemgetter(1),
                  reverse=True)


def task_03(many_to_many) -> list:
    """
    Выведите список всех связанных IDE поддерживающие языки, которые начинаются с "c",
    :param many_to_many: список созданный связями многие ко многим.
    :return: Список IDE и языков, отобранный по языкам.
    """
    # Пояснение. Изначально сортирую many_to_many по IDE.name, после чего возвращаю список кортежей:
    # имя и список языков.
    rez=[]
    for i in range(len(many_to_many)):
        lst=False
        for i1 in range(len(many_to_many[i][2])):
            if many_to_many[i][2][i1][0].lower()=="c":
                lst=True
                break
        if lst:
            rez.append( (many_to_many[i][0],many_to_many[i][2]))
    return rez