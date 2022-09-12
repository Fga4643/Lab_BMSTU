import sys
def is_float(a):
    try:
        float(a)
        return True
    except:
        print("Введите число")
        return False
def get_coef(index, prompt):
    '''
    Читаем коэффициент из командной строки или вводим с клавиатуры
    Args:
        index (int): Номер параметра в командной строке
        prompt (str): Приглашение для ввода коэффицента
    Returns:
        float: Коэффициент квадратного уравнения
    '''
    try:
        # Пробуем прочитать коэффициент из командной строки
        coef_str = sys.argv[index]
    except:
        # Вводим с клавиатуры
        print(prompt)
        coef_str = input()
    # Переводим строку в действительное число
    try:
        coef = float(coef_str)
    except:
        coef=None
    return coef


def get_roots(a, b, c):
    '''
    Вычисление корней квадратного уравнения
    Args:
        a (float): коэффициент А
        b (float): коэффициент B
        c (float): коэффициент C
    Returns:
        list[float]: Список корней
    '''
    result = []
    D = b*b - 4*a*c
    if D == 0.0:
        root = -b / (2.0*a)
        if root>0:
            result.append(root**0.5)
            result.append((root**0.5)*(-1))
    elif D > 0.0:
        sqD = D**0.5
        root1 = (-b + sqD) / (2.0*a)
        root2 = (-b - sqD) / (2.0*a)
        if root1>0:
            result.append(root1**0.5)
            result.append((root1**0.5)*(-1))
        if root2>0:
            result.append(root2**0.5)
            result.append((root2**0.5)*(-1))      
    return result


def main():
    '''
    Основная функция
    '''
    i=0
    a=None
    b=None
    c=None
    try:
        while not is_float(a):
            i+=1
            a = get_coef(i, 'Введите коэффициент А:')
        while not is_float(b):
            i+=1
            b = get_coef(i, 'Введите коэффициент B:')
        while not is_float(c):
            i+=1
            c = get_coef(i, 'Введите коэффициент C:')            
        # Вычисление корней
        rots = get_roots(a,b,c)
        roots=[]
        # Вывод корней
        for i in rots:
            if i not in roots:
                roots.append(i)
        len_roots = len(roots)
        if len_roots == 0:
            print('Нет корней')
        elif len_roots == 1:
            print('Один корень: {}'.format(roots[0]))           
        elif len_roots == 2:
            print('Два корня: {} и {}'.format(roots[0], roots[1]))
        elif len_roots == 3:
            print('Два корня: {}, {} и {}'.format(roots[0], roots[1], roots[2]))        
        elif len_roots == 4:
            print('Четыре корня: {}, {}, {} и {}'.format(roots[0], roots[1], roots[2], roots[3])) 
    except:
        print("Коэффицент A не может быть равен 0")
    input("Нажмите любую кнопку...")
    

# Если сценарий запущен из командной строки
if __name__ == "__main__":
    main()
