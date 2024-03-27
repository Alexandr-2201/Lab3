import networkx as nx
import matplotlib.pyplot as plt
from collections import deque




def levit(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    queue = deque([start])
    circl = []
    negative_sum = sum(weight for i, j, weight in graph.edges(data='weight') if weight < 0) - 1

    while queue:
        node = queue.popleft()

        for neighbor in graph.neighbors(node):
            weight = graph[node][neighbor]['weight']
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                if neighbor not in (queue or circl):
                    if weight == 0:
                        queue.appendleft(neighbor)
                    else:
                        queue.append(neighbor)
                # Защита от бесконечного зацикливания
                if dist[neighbor] < -negative_sum:
                   circl.append(neighbor)
                   dist[neighbor] = float('inf') *(-1)

    return dist



def graph_from_file(file_name):
    # Считывание матрицы смежности из текстового файла
    adjacency_matrix = []
    with open(file_name, 'r') as file:
        for line in file:
            row = [int(x) for x in line.strip().split()]
            adjacency_matrix.append(row)
    # Преобразование матрицы смежности в граф nx.DiGraph()
    graph = nx.DiGraph()
    num_nodes = len(adjacency_matrix)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adjacency_matrix[i][j] != 0:
                vertex_1 = chr(ord('A') + i)
                vertex_2 = chr(ord('A') + j)
                graph.add_edge(vertex_1, vertex_2, weight=adjacency_matrix[i][j])
    return graph




file_name = "matrix.txt"
graph = graph_from_file(file_name)

#pos = nx.spring_layout(graph)
pos = nx.circular_layout(graph)
nx.draw(graph, pos, with_labels=True, node_size=700, font_size=10)
labels = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

start_node = 'A'
start_time = time.time()
shortest_paths = levit(graph, start_node)
print("--- {0} ms ---".format(round((time.time() - start_time) * 1000)))
for node, distance in shortest_paths.items():
    print(f'Кратчайший путь из {start_node} в {node}: {distance}')

plt.show()
