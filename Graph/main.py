import matplotlib.pyplot as plt
import Graph as graph

''' Выполняет проверку ввода числа
    с подсказкой s и ограничением сверху n '''


def check_input(s, n):
    correct_inputs = False
    while not correct_inputs:
        try:
            key = int(input(s))
            if 0 <= key <= n:
                correct_inputs = True
        except:
            print('Некорректный ввод!')
            continue
    return key


''' Получеет информацию и типе графа из подсказки s '''


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
    while True:
        v = check_input('Введите число вершин (от 0 до 10): ', 10)
        if 0 <= v <= 10:
            g = graph.Graph(v, weighted, directed)
            break
    print('Создан граф с числом вершин ' + str(v) + '.')

    key = -1  # номер команды меню

    n = 6  # число команд меню в списке

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
        print('0 - Выход')

        # Ввести команду меню с клавиатуры
        key = check_input('> ', n)

        # Выбрать и выполнить действие согласно команде меню:
        if key == 0:
            break
        elif key == 1:
            source = check_input('Введите начальную вершину: ', v - 1)
            dest = check_input('Введите конечную вершину: ', v - 1)
            if g.weighted:
                weight = check_input('Введите вес ребра: ', 100000000000)
                g.insert_edge(source, dest, weight)
            else:
                g.insert_edge(source, dest)
        elif key == 2:
            source = check_input('Введите начальную вершину: ', v - 1)
            dest = check_input('Введите конечную вершину: ', v - 1)
            g.delete_edge(source, dest)
        elif key == 3:
            g.insert_vertex()
            v += 1
        elif key == 4:
            vert = check_input('Введите вершину: ', v - 1)
            g.delete_vertex(vert)
        elif key == 5:
            g.display()
        elif key == 6:
            fname = input('Введите имя файла для записи: ')
            g.save(fname)

    # Отрисовать итоговый граф
    g.draw()
