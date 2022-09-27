from lab_python_oop.rectangle import Rectangle
from lab_python_oop.circle import Circle
from lab_python_oop.square import Square
import pandas as pd
def is_float(a):
    try:
        float(a)
        return True
    except:
        return False
def get_coef(index, prompt):
    try:
        # Пробуем прочитать коэффициент из командной строки
        coef_str = sys.argv[index]
    except:
        print(prompt)
        coef_str = input()
    # Переводим строку в действительное число
    try:
        coef = float(coef_str)
    except:
        coef=None
    return coef

def get_str(index, prompt):
    try:
        # Пробуем прочитать коэффициент из командной строки
        coef_str = sys.argv[index]
    except:
        print(prompt)
        coef_str = input()
    # Переводим строку в действительное число
    try:
        coef = str(coef_str)
    except:
        coef=None
    return coef

def main():
    print('\n ---- LAB-01 ----\n')
    a,b=None,None
    i=0
    while not is_float(a):
        i+=1
        a = get_coef(i, 'Введите сторону ширину прямоугольника:')    
    while not is_float(b):
        i+=1
        b = get_coef(i, 'Введите сторону высоту прямоугольника:') 
    i+=1
    color=get_str(i,'Введите какого цвета будет ваш прямоугольник:')
    r = Rectangle(color, a, b)
    a,b=None,None
    while not is_float(b):
        i+=1
        b = get_coef(i, 'Введите радиус круга:') 
    i+=1
    color=get_str(i,'Введите какого цвета будет ваш круг:')    
    c = Circle(color, b)
    while not is_float(a):
        i+=1
        a = get_coef(i, 'Введите сторону квадрата:')  
    i+=1
    color=get_str(i,'Введите какого цвета будет ваш квадрат:')    
    s = Square(color, a)
    print(r, c, s, sep='\n')

    # пример выполнения импортированной библеотеки.
    print('\n ---- Module Pandas ----\n')
    table = pd.DataFrame({'Anton': ['Python', 2, 'BKIT'], 'Obukhov': ["Developer", 'informathion', 11]}, )
    print(table)


if __name__ == "__main__":
    main()