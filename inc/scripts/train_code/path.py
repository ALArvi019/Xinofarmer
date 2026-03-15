
import numpy as np
from queue import PriorityQueue
import cv2 as cv
import heapq

class Path:

	def __init__(self) -> None:
		pass

	def a_star(colision_matrix, start0, start1, end0, end1):
		start = (start0, start1)
		end = (end0, end1)

		# Funcion heuristica
		def heuristic(a, b):
			return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

		# Funcion para obtener los vecinos de un nodo
		def get_neighbors(node):
			neighbors = []
			for i in range(-1, 2):
				for j in range(-1, 2):
					if i == 0 and j == 0:
						continue
					if node[0] + i < 0 or node[0] + i >= colision_matrix.shape[0]:
						continue
					if node[1] + j < 0 or node[1] + j >= colision_matrix.shape[1]:
						continue
					if colision_matrix[node[0] + i, node[1] + j] == 0:
						continue
					neighbors.append((node[0] + i, node[1] + j))
			return neighbors
		# Inicializar variables
		came_from = {}
		cost_so_far = {}
		priority_queue = PriorityQueue()
		priority_queue.put(start, 0)
		came_from[start] = None
		cost_so_far[start] = 0

		# Iterar hasta que la cola este vacia
		while not priority_queue.empty():
			current = priority_queue.get()

			# Si llegamos al final, terminamos
			if current == end:
				break

			# Iterar por los vecinos
			for next in get_neighbors(current):
				new_cost = cost_so_far[current] + 1
				if next not in cost_so_far or new_cost < cost_so_far[next]:
					cost_so_far[next] = new_cost
					priority = new_cost + heuristic(end, next)
					priority_queue.put(next, priority)
					came_from[next] = current

		return came_from

	
	def astar(self, start, end, grid):
		rows, cols = len(grid), len(grid[0])
		heap = [(0, start)]
		visited = set()
		came_from = {}	

		while heap:
			dist, curr = heapq.heappop(heap)
			if curr == end:
				path = [curr]
				while curr != start:
					curr = came_from[curr]
					path.append(curr)
				return list(reversed(path)), dist
		# avoid TypeError: unhashable type: 'list' when using set to store visited nodes
			visited.add((curr[0], curr[1]))
			
			for nei in [(curr[0] + dx, curr[1] + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]]:
				if 0 <= nei[0] < rows and 0 <= nei[1] < cols and grid[nei[0]][nei[1]] == 1:
					new_dist = dist + 1
					if nei not in visited:
						heapq.heappush(heap, (new_dist, nei))
						came_from[nei] = curr
		return [], 0

	def get_path(came_from, start0, start1, end0, end1):
		start = (start0, start1)
		end = (end0, end1)
		current = end
		path = [current]
		while current != start:
			current = came_from[current]
			path.append(current)
		path.reverse()
		return path

	def draw_path_on_img(path, img):
		for i in range(len(path) - 1):
			cv.line(img, path[i], path[i+1], (0, 0, 255), 2)