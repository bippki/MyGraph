import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d
import csv
import copy

''' Класс Ребро графа '''
class Edge:
    ''' Конструктор ребра (вес по умолчанию = 1) '''
    def __init__(self, dest, weight=1):
        # конечная вершина
        self.dest = dest
        # вес ребра
        self.weight = weight

''' Класс Граф '''
class Graph:
    ''' Конструктор по умолчанию
        [создает пустой граф с нулем вершин либо граф с заданным числом вершин
        указанного типа - (не)ориентированный (не)взвешенный] '''
    def __init__(self, vertices=0, weighted=False, directed=False):
        # заполнить список смежности пустыми списками по числу вершин графа
        self.al = [[] for i in range(vertices)]
        # установить свойство взвешенности графа
        self.weighted = weighted
        # установить свойство направленности графа
        self.directed = directed

    ''' Сохраняет граф в файл с указанным именем '''
    def save(self, filename):
        # Открыть файл на запись
        with open(filename, 'w', newline='') as file:
            # Создать объект для записи в файл (разделитель - запятая)
            writer = csv.writer(file, delimiter=',')
            # Записать информацию о типе графа [(не)ориентированный (не)взвешенный]
            writer.writerow((('True' if self.weighted else 'False'),
                            ('True' if self.directed else 'False')))
            # Для каждой начальной вершины в списке смежности выполнить:
            for i in range(len(self.al)):
                # Создать пустой список для хранения пар (конечная вершина, вес)
                row = []
                # Если длина списка для этой вершины = 0, то
                if len(self.al[i]) == 0:
                    # добавить ребро в -2 с весом -2 (маркер петли)
                    row.append((-2, -2))
                # Иначе (в списке есть вершины)
                else:
                    # Для каждой вершины в списке выполнить:
                    for edge in self.al[i]:
                        # Получить конечную вершину и вес ребра
                        d, w = edge.dest, edge.weight
                        # Записать в виде кортежа в список
                        row.append((d, w))
                # Записать список в строку в файл
                writer.writerow(row)

    ''' Читает граф из файла с указанным именем '''
    def read(self, filename):
        # Открыть файл на чтение и посчитать число вершин графа (число строк в файле)
        with open(filename, 'r') as file:
            vertices = sum(1 for row in file) - 1
        # Открыть файл на чтение снова
        with open(filename, 'r') as file:
            # Создать список смежности с указанным числом вершин
            self.al = [[] for i in range(vertices)]
            # Создать объект для чтения из файла (разделитель - запятая)
            reader = csv.reader(file, delimiter=',')
            # Считать первую строку для получения типа графа
            graph_type = next(reader)
            # Определить тип графа [(не)ориентированный (не)взвешенный]
            self.weighted = eval(graph_type[0])
            self.directed = eval(graph_type[1])
            # Для каждой строки (начальной вершины) выполнить:
            for i, line in enumerate(reader):
                # Для каждой пары в строке выполнить:
                for pair in line:
                    # Преобразовать пару в кортеж
                    edge = eval(pair)
                    # Получить конечную вершину
                    dest = edge[0]
                    # Получить вес ребра
                    weight = edge[1]
                    # Если ребро не является петлей, то
                    if dest != -2:
                        # добавить новую вершину и вес в список смежности
                        self.al[i].append(Edge(dest, weight))

    ''' Выполняет копию объекта класса '''
    def copy(self):
        return copy.deepcopy(self)

    ''' Добавляет новую вершину '''
    def insert_vertex(self):
        # Добавить в конец списка смежности пустой список
        self.al.append([])

    ''' Удаляет вершину '''
    def delete_vertex(self, v):
        if v >= len(self.al) or v < 0:
            print('Ошибка! Номер вершины за пределами диапазона')
        else:
            # Создать новый список смежности по числу элементов в исходном
            newal = [[] for i in range(len(self.al))]
            # Для каждой начальной вершины в исходном списке выполнить:
            for i in range(len(self.al)):
                # Для каждой смежной вершины:
                for edge in self.al[i]:
                    # Получить конечную вершину и вес ребра
                    d, w = edge.dest, edge.weight
                    # Если конечная вершина не совпадает с удаляемой, то
                    if d != v:
                        # записать ее с весом в новый список
                        newal[i].append(Edge(d, w))
                    else:
                        # иначе (петля) записать в качестве конечной вершины -1
                        newal[i].append(Edge(-1, w))
            # Записать в список смежности удаляемой вершины пару (-1, -1) - маркер удаляемой вершины
            newal[v] = [Edge(-1, -1)]
            # Выполнить копию списка смежности (присвоить новый список исходному)
            self.al = newal.copy()

    ''' Добавляет новое ребро '''
    def insert_edge(self, source, dest, weight=1):
        if source >= len(self.al) or dest >= len(self.al) or source < 0 or dest < 0:
            print('Ошибка! Номер вершины за пределами диапазона.')
        elif weight != 1 and not self.weighted:
            print('Ошибка! Нельзя добавить ребро с весом в невзвешенный граф.')
        else:
            # Добавить ребро для начальной вершины с указанным весом и конечной вершиной
            self.al[source].append(Edge(dest, weight))
            # Если граф не ориентированный и начальная вершина не совпадает с конечной (не петля)
            if not self.directed and dest != source:
                # добавить ребро для конечной вершины с указанным весом и начальной вершиной
                self.al[dest].append(Edge(source, weight))

    ''' Удаляет ребро с указанной начальной и конечной вершиной (вспомогательная функция) '''
    def delete_edge_(self, source, dest):
        i = 0
        for edge in self.al[source]:
            if edge.dest == dest:
                self.al[source].pop(i)
                return True # ребро было удалено
            i += 1
        return False # ребро не было удалено

    ''' Удаляет ребро с указанной начальной и конечной вершиной '''
    def delete_edge(self, source, dest):
        if source >= len(self.al) or dest >= len(self.al) or source < 0 or dest < 0:
            print('Ошибка! Номер вершины за пределами диапазона')
        else:
            deleted = self.delete_edge_(source, dest)
            if not self.directed:
                deleted = self.delete_edge_(dest, source)
        if not deleted:
            print('Ошибка! Ребро для удаления не найдено.')

    ''' Отображает список смежности графа '''
    def display(self):
        # Результат вывода - пустая строка
        res = ''
        # Для каждой начальной вершины выполнить:
        for i in range(len(self.al)):
            # Записать в строку вершину с указанием на смежные вершины
            row = str(i) + ' -> ['
            # Состояние удаления вершины
            removed = False
            # Для каждой пары в списке смежности текущей (начальной) вершины:
            for edge in self.al[i]:
                # Получить конечную вершину и вес ребра
                d, w = edge.dest, edge.weight
                # Если оба равны -1 (вершина была удалена), то
                if d == -1 and w == -1:
                    # Сменить состояние удаления вершины
                    removed = True
                # Иначе, если конечная вершина не равна -1, то
                elif d != -1:
                    # Записать ее в строку
                    row += str(d)
                    # Если граф взвешенный, то
                    if self.weighted:
                        # дописать в скобках вес ребра
                        row += '(' + str(w) + ')'
                    row += '   '
            # Если вершина не была удалена, то дописать строку в конец результирующей
            if not removed:
                res += row + ']\n'
        print(res)

    ''' Выполняет отрисовку графа '''
    def draw(self):
        # Задать масштаб
        scale = 30
        # Построить фигуру для графика
        fig, ax = plt.subplots()
        # Для каждой начальной вершины выполнить:
        for i in range(len(self.al)):
            # Состояние вершины = 0 (исходное)
            state = 0
            # Получить номер вершины и записать в строку
            res = str(i)
            # Для каждой пары в списке смежности текущей (начальной) вершины:
            for edge in self.al[i]:
                # Получить конечную вершину и вес ребра
                d, w = edge.dest, edge.weight
                # Если оба равны -1 (вершина была удалена), то
                if d == -1 and w == -1:
                    # сменить состояние на 2 (удаленная вершина)
                    state = 2
                # Иначе, если -1 равна только конечная вершина,
                elif d == -1 and w != -1:
                    # Сменить состояние на 1 (петля)
                    state = 1
                else:
                    # Иначе вернуться к исходному состоянию
                    state = 0
                # Если начальная вершина совпадает с конечной (петля),
                if i == d:
                    # дописать в строку с ее номером 'п'
                    res += 'п'
                # Иначе, если состояние не 2 и граф ориентированный либо конечная вершина больше начальной,
                elif state != 2 and (self.directed or d > i):
                    # Создать массив точек по X от начальной до конечной вершины с учетом масштаба
                    x = np.linspace(i * scale, d * scale)
                    # Создать массив из пяти точек по X от начальной до конечной вершины с учетом масштаба
                    x0 = np.linspace(i * scale, d * scale, num=5)
                    # Получить расстояние от начальной до конечной вершины
                    diff = np.abs(d - i)
                    # Если начальная и конечная вершины являются смежными, то
                    if diff == 1:
                        # Создать массив по Y, заполненный нулями (горизонтальная линия)
                        y0 = [0, 0, 0, 0, 0]
                    else:
                        # Иначе создать массив по Y с учетом расстояния (кривая линия)
                        y0 = [0, -6 * diff, -8 * diff, -6 * diff, 0]
                    # Выполнить интерполяцию кубическим сплайном по пяти точкам
                    f = interp1d(x0, y0, kind='cubic')
                    # Получить значение функции на x для y
                    y = f(x)
                    # Найти знак между начальной и конечной вершинами
                    s = np.sign(i - d)
                    # Если вершина не удалена и не является петлей, соединить ее с вершинами графа линиями (ребрами)
                    if state == 0:
                        ax.plot(x, s * y, linewidth=1, color='k')
                    # Если граф направленный, то нарисовать на линиях направление
                    if self.directed and state == 0:
                        xd = [x0[2] + 2 * s, x0[2], x0[2] + 2 * s]
                        yd = [y0[2] - 1, y0[2], y0[2] + 1]
                        yd = [y * s for y in yd]
                        ax.plot(xd, yd, linewidth=1, color='k')
                    # Если граф взвешенный, то подписать вес рядом с линиями
                    if self.weighted and state == 0:
                        xd = [x0[2] + 2 * s, x0[2], x0[2] + 2 * s]
                        yd = [y0[2] - 1, y0[2], y0[2] + 1]
                        yd = [y * s for y in yd]
                        ax.text(xd[2] - s * 2, yd[2] + 3 * s, str(w), size=12,
                                ha="center", va="center")
            # Если вершина не была удалена, нарисовать ее на графике и подписать номер
            if state != 2:
                ax.plot([i * scale, i * scale], [0, 0], linewidth=1, color='k')
                ax.text(i * scale, 0, res, size=20, ha="center", va="center",
                        bbox=dict(facecolor='w', boxstyle="circle"))
        # Вывести график на экран
        ax.axis('off')
        ax.set_aspect(1.0)
        fig.show()
