import csv
import copy

''' Класс Ребро графа '''
class Edge:
    def __init__(self, dest, weight=1):
        self.dest = dest
        self.weight = weight

''' Класс Граф '''
class Graph:
    def __init__(self, weighted=False, directed=False):
        # заполнить список смежности пустыми списками по числу вершин графа
        self.al = []
        # установить свойство взвешенности графа
        self.weighted = weighted
        # установить свойство направленности графа
        self.directed = directed
        self.names=dict()

    def get_name(self, i):
        return list(self.names.keys())[list(self.names.values()).index(i)]

    def get_indeg(self,v):
        return len({i for i in self.names if v in self.names[i]})

    def save(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self.weighted) + " " + str(self.directed) + '\n')
            for i in range(len(self.al)):
                file.write(self.get_name(i) + " ")
                for edg in self.al[i]:
                    file.write(f"{edg.dest} {edg.weight} ")
                file.write('\n')

    def read(self, filename):
        with open(filename, 'r') as file:
            self.weighted, self.directed = map(bool, file.readline().split())
            self.al = []
            self.names = {}
            for line in file:
                spl = line.split()
                name = spl[0]
                self.names[name] = len(self.al)
                self.al.append([])
                for i in range(1,len(spl), 2):
                    des = spl[i]
                    wei = spl[i + 1]
                    self.al[self.names[name]].append(Edge(des, wei))


    def copy(self):
        return copy.deepcopy(self)

    def insert_vertex(self,name):
        # Добавить в конец списка смежности пустой список
        if name not in self.names:
            self.al.append([])
            self.names[name]=len(self.al)-1
        else:
            print("Ошибка! Вершина с таким именем уже существует")

    def delete_vertex(self, name):
        if name not in self.names:
            print(f'Ошибка! Нет вершины с именем {name}')
            return 0
        v=self.names[name]
        if v >= len(self.al) or v < 0:
            print('Ошибка! Номер вершины за пределами диапазона')
        else:
            newal = [[] for i in range(len(self.al))]
            for i in range(len(self.al)):
                if i!=v:
                    for edge in self.al[i]:
                        d, w = edge.dest, edge.weight
                        if d != name:
                            newal[i].append(Edge(d, w))
                        else:
                            self.al[i].remove(edge)

            self.al.pop(v)
            self.names = {n: val + (0 if val < v else -1) for (n, val) in self.names.items() if n != name}

    def insert_edge(self, source, dest, weight=None):
        if source not in self.names:
            print(f'Ошибка! Нет вершины с именем {source}')
            return 0
        _source=self.names[source]
        if dest not in self.names:
            print(f'Ошибка! Нет вершины с именем {dest}')
            return 0
        _dest=self.names[dest]
        mark=True
        for edge in self.al[_dest]:
            d, w = edge.dest, edge.weight
            if d == source:
                if self.directed:
                    mark=False
                else:
                    print("Ошибка! Ребро уже есть")
                    return 0
        for edge in self.al[_source]:
            d, w = edge.dest, edge.weight
            if d == source and mark==False:
                print("Ошибка! Ребро уже есть")
                return 0

        if weight != None and not self.weighted:
            print('Ошибка! Нельзя добавить ребро с весом в невзвешенный граф.')
        else:
            self.al[_source].append(Edge(dest, weight))
            if not self.directed and dest != source:
                self.al[_dest].append(Edge(source, weight))


    def delete_edge_(self, source, dest):
        i = 0
        _source=self.names[source]
        _dest=self.names[dest]
        for edge in self.al[_source]:
            if edge.dest == dest:
                self.al[_source].pop(i)
                return True # ребро было удалено
            i += 1
        return False # ребро не было удалено

    def delete_edge(self, source, dest):
        if source not in self.names and dest not in self.names:
            print(f'Ошибка! Нет вершин с именами {source} и {dest}')
            return 0
        if source not in self.names:
            print(f'Ошибка! Нет вершины с именем {source}')
            return 0
        _source=self.names[source]
        if dest not in self.names:
            print(f'Ошибка! Нет вершины с именем {dest}')
            return 0
        else:
            _dest=self.names[dest]
            deleted = self.delete_edge_(source, dest)
            if not self.directed:
                deleted = self.delete_edge_(dest, source)
        if not deleted:
            print('Ошибка! Ребро для удаления не найдено.')

    def display(self):
        res = ''
        for i in range(len(self.al)):
            row = str(list(self.names.keys())[list(self.names.values()).index(i)]) + ' -> ['
            for edge in self.al[i]:
                d, w = edge.dest, edge.weight
                if d != '@':
                    row += str(d)
                    if self.weighted:
                        row += '(' + str(w) + ')'
                    row += '   '
            res += row + ']\n'
            '''for name in self.names[i]:
                print(name)'''
        print(res)

    def halfs(self, name):
        
        if name not in self.names:
            print(f'Ошибка! Нет вершины с именем {name}')
            return 0
        v=self.names[name]
        if (self.directed==False):
            print(f'Ошибка! В неориентированном графе нет полустепени исхода')
        else:
            mas=list()
            halfcount=len(self.al[v])
            for i in range(len(self.al)):
                if len(self.al[i])>halfcount:
                    mas.append(list(self.names.keys())[list(self.names.values()).index(i)])
            str=""
            for i in mas:
                str+=i+" "
            print(f"Вершины с большей полустепенью исхода:{str}")

    def task2(self,name1,name2):
        if name1 not in self.names:
            print(f'Ошибка! Нет вершины с именем {name1}')
            return 0
        v1=self.names[name1]
        if name2 not in self.names:
            print(f'Ошибка! Нет вершины с именем {name2}')
            return 0
        v2=self.names[name2]
        if (self.directed==False):
            print(f'Ошибка! В неориентированном графе нет дуг')
        else:
            mas1=set()
            mas2=set()
            for edge in self.al[v1]:
                d, w = edge.dest, edge.weight
                mas1.add(d)
            for edge1 in self.al[v2]:
                d, w = edge1.dest, edge1.weight
                mas2.add(d)
            if  mas1&mas2==0:
                print("Нет вершин")
            else:
                print(*(mas1&mas2))

    '''def task3(self, g):
        for i in range(len(g.al)):
            if g.get_name(i) not in self.al:
                self.al.append([])
                name=
                self.names[name]=len(self.al)-1'''
    def task4(self):
        z=0
        vert=len(self.al)
        for i in range(len(self.al)):
            for j in self.al[i]:
                z+=1
        if self.dest:
            print("Цикломатическое число графа:",z-vert+1)
        else:
            print("Цикломатическое число графа:",z//2-vert+1)

    '''def dfs(self,v):
        stack=[v]
        used={v}
        cur=set()
        while len(stack)>0:
            up=stack[-1]
            cur.add(up)
            ex=False
            for x in self.names[up]:
                if x not in used:
                    stack.append(x)
                    used.add(x)
                    ex = True
                elif x in cur:
                    return True
            if ex==False:
                stack.pop()
                cur.remove(up)
        return False'''


    def task5(self):
        if (self.directed==False):
            print(f'Ошибка! Требуется ориентированный граф')
            return 0
        ways=[self.get_indeg(i) for i in self.get_name()]
        if any(i > 1 for i in ways):
            print("Не дерево и не лес")
            return 0

        def dfs(self,v):
            stack=[v]
            used={v}
            cur=set()
            while len(stack)>0:
                up=stack[-1]
                cur.add(up)
                ex=False
                for x in self.names[up]:
                    if x not in used:
                        stack.append(x)
                        used.add(x)
                        ex = True
                    elif x in cur:
                        return True
                if ex==False:
                    stack.pop()
                    cur.remove(up)
        return False
        if any(dfs(self,x) for x in self.get_names()):
            print("Не дерево и не лес")
            return 0
        if ways.count(0) !=1:
            print("Лес")
            return 0
        print("Дерево")
        return 0
    '''def dfs(self,v,p =-1):
        used[v]=true'''
