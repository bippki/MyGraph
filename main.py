import matplotlib.pyplot as plt
import graphs as graph

''' Выполняет проверку ввода числа
    с подсказкой s и ограничением сверху n '''


'''def check_input(s):
    #correct_inputs = False
    #while not correct_inputs:
        #try:
           # key = input(s)
           # if 0 <= key :
            #    correct_inputs = True
       # except:
           #print('Некорректный ввод!')
           continue
    return key'''
def check_input(s,n):
    return(input(s))

def graph_type(s):
    res = input(s + ' True / False ')
    if res == 'True':
        return True
    else:
        return False


if __name__ == "__main__":
    plt.close("all")
    g = graph.Graph()

    # Выбрать тип графа
    print('Выберите тип графа.')
    weighted = graph_type('Взвешенный?')
    directed = graph_type('Ориентированный?')

    # Создать граф с заданным числом вершин
    g = graph.Graph(weighted, directed)
    print('Создан граф.')

    key = -1  # номер команды меню

    n = 10  # число команд меню в списке

    # Пока не введена команда меню "Выход", выполнить:
    while key != 0:
        # Вывести меню на экран
        print('Меню: ')
        print('1 - Добавить ребро')
        print('2 - Удалить ребро')
        print('3 - Добавить вершину')
        print('4 - Удалить вершину')
        print('5 - Вывести список смежности')
        print('6 - Сохранить в файл')
        print('7 - Cчитать из файла')
        print('8 - Задание 1')
        print('9 - Вернуть копию графа')
        print('10 - Задание 2')
        print('11 - Задание 4 - Цикломатическое число графа')
        print('0 - Выход')

        # Ввести команду меню с клавиатуры
        r = check_input('> ', n)
        if r.isnumeric():
            key=int(r)
        else:
            print('Неккоректный ввод')

        # Выбрать и выполнить действие согласно команде меню:
        if key == 0:
            break
        elif key == 1:
            source = check_input('Введите начальную вершину: ', 1)
            dest = check_input('Введите конечную вершину: ', 1)
            if g.weighted:
                weight = check_input('Введите вес ребра: ', 100000000000)
                g.insert_edge(source, dest, weight)
            else:
                g.insert_edge(source, dest)
        elif key == 2:
            source = check_input('Введите начальную вершину: ', 1)
            dest = check_input('Введите конечную вершину: ', 1)
            g.delete_edge(source, dest)
        elif key == 3:

            g.insert_vertex(input('Введите имя вершины:'))
        elif key == 4:
            vert = check_input('Введите вершину: ',1)
            g.delete_vertex(vert)
        elif key == 5:
            g.display()
        elif key == 6:
            fname = input('Введите имя файла для записи: ')
            g.save(fname)
        elif key ==7:
            fname = input('Введите имя файла для чтения: ')
            g.read(fname)
        elif key ==8:
            vert = check_input('Введите вершину: ',1)
            g.halfs(vert)
        elif key ==9:
            g.copy()
        elif key==10:
            v1 = check_input('Введите вершину: ',1)
            v2 = check_input('Введите вершину: ',1)
            g.task2(v1,v2)
        elif key==11:
            g.task4()