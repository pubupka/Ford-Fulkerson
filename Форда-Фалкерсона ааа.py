import numpy
import math

i = math.inf

matrix = numpy.array([[0, 95, i, i, 75, 32, 57, i],  # Матрица смежности
                      [i, 0, 6, i, 18, i, i, i],  # проверить элемент [2][6] в тетради
                      [i, i, 0, 7, 9, i, 11, i],
                      [i, i, i, 0, i, i, i, 81],
                      [i, i, 9, i, 0, i, 24, i],
                      [i, 5, i, i, i, 0, 20, 16],
                      [i, i, i, 20, i, i, 0, 94],
                      [i, i, i, i, i, i, i, 0]])

def deykstra():
    m = numpy.full((8, 8), math.inf)

    start = 0  # вершина 1
    minim = 0
    node = start
    n = 8
    ostov = {node}  # Множество вершин, которые потом не надо будет рассматривать
    rez = {node: 0}  # Итоговый словарь

    for iter in range(n - 1):
        stroke = []

        for j in range(n):
            if j not in ostov:
                column = m[:, j]
                stroke.append(min(min(column), matrix[node][j] + minim))
            else:
                stroke.append(math.inf)

        m[node] = stroke
        minim = min(m[node])
        s = m[node]
        node = numpy.where(s == minim)[0][0]
        ostov.add(node)
        rez[node] = minim
        m[node] = stroke
    return rez


def reconstruction_path(deykstra_dict):
    end = 7  # 8 вершина
    length = deykstra_dict[end]
    rez = []
    deykstra_dict[0] = 0  # если до какой-то вершины нельзя дойти, то от старта до старта становится бесконечность

    while length != 0:
        for num in deykstra_dict.keys():
            if matrix[num][end] + deykstra_dict[num] == deykstra_dict[end]:
                length -= matrix[num][end]
                rez.insert(0, (num, end))
                end = num
    return rez


path = reconstruction_path(deykstra())
deykstra_dict = deykstra()
flow = 0  # суммарный поток

while 7 in deykstra_dict.keys():  # пока до вершины 8 можно добраться
    path = reconstruction_path(deykstra())
    values = [matrix[rebro[0]][rebro[1]] for rebro in path]  # список весов рёбер из пути
    minim = min(values)
    flow += minim
    for rebro in path:
        i = rebro[0]
        j = rebro[1]
        if matrix[i][j] == minim:
            matrix[i][j] = math.inf
        else:
            matrix[i][j] -= minim

    deykstra_dict = deykstra()

print(f"Поток равен: {flow}")
