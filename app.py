from flask import Flask, request, jsonify, render_template
import heapq

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve_dijkstra():
    data = request.get_json()
    node_count = data['nodeCount']
    edges = data['edges']
    start_node = data['startNode']
    end_node = data['endNode']

    # Crear grafo como lista de adyacencia
    graph = {i: [] for i in range(node_count)}
    for edge in edges:
        graph[edge['from']].append((edge['to'], edge['distance']))
        graph[edge['to']].append((edge['from'], edge['distance']))  # grafo no dirigido

    # Algoritmo de Dijkstra
    distances = [float('inf')] * node_count
    distances[start_node] = 0
    prev = [None] * node_count
    pq = [(0, start_node)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node]:
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                prev[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))

    # Construir ruta desde el nodo de inicio hasta el nodo de destino
    path = []
    node = end_node
    while node is not None:
        path.insert(0, node)
        node = prev[node]

    return jsonify({
        'distances': distances,
        'paths': [path] if path else []
    })

if __name__ == '__main__':
    app.run(debug=True)
