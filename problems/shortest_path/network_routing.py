import math

class DistNode:
    def __init__(self, key, distance):
        self.key = key
        self.distance = distance

    def __str__(self):
        return f"({self.key}: {self.distance})"

    def __lt__(self, other):
        return self.distance < other.distance

class LinearPriorityQueue:
    def __init__(self):
        self.index = dict()
        self.dist = []
        self.prev = dict()

    def insert(self, key):
        self.dist.append(DistNode(key, math.inf))
        self.index[key] = len(self.dist) - 1
        self.prev[key] = None

    def make_queue(self, nodes: dict):
        for key in nodes.keys():
            self.insert(key)

    def delete_min(self):
        least = min(self.dist)
        i = self.index[least.key]
        ret = self.dist.pop(i)
        if i < len(self.dist):
            self.index[least.key] = len(self.dist)
            self.dist.insert(i, self.dist.pop())
            self.index[self.dist[i].key] = i
        return ret

    def decrease_key(self, key, distance, previous):
        self.dist[self.index[key]].distance = distance
        self.prev[key] = previous

class HeapPriorityQueue:

    def __init__(self):
        self.heap: [DistNode] = []
        self.index = dict()
        self.prev = dict()

    def swap(self, key1, key2):
        temp_dist = self.heap[self.index[key1]]
        temp_index = self.index[key1]
        self.heap[self.index[key1]] = self.heap[self.index[key2]]
        self.index[key1] = self.index[key2]
        self.heap[self.index[key2]] = temp_dist
        self.index[key2] = temp_index

    def min_child(self, key):
        left_child_index = (self.index[key] * 2) + 1
        right_child_index = (self.index[key]* 2) + 2
        if left_child_index < len(self.heap):
            if right_child_index >= len(self.heap):
                return self.heap[left_child_index].key
            else:
                left_child = self.heap[left_child_index]
                right_child = self.heap[right_child_index]
                if left_child.distance < right_child.distance:
                    return left_child.key
                return right_child.key
        else:
            return key

    def sift_down(self, key):
        min_child = self.min_child(key)
        if (self.heap[self.index[key]].distance >
                self.heap[self.index[min_child]].distance):
            self.swap(key, min_child)
            self.sift_down(key)

    def bubble_up(self, key):
        if self.index[key] > 0:
            parent = self.heap[((self.index[key] + 1) // 2) -1]
            if (parent.distance >
                    self.heap[self.index[key]].distance):
                self.swap(key, parent.key)
                self.bubble_up(key)

    def insert(self, key):
        self.heap.append(DistNode(key, math.inf))
        self.index[key] = len(self.heap) - 1
        self.prev[key] = None

    def make_queue(self, nodes: dict):
        for key in nodes.keys():
            self.insert(key)

    def delete_min(self):
        least = self.heap[0]
        self.swap(least.key, self.heap[len(self.heap) - 1].key)
        self.heap.pop()
        self.sift_down(self.heap[0].key)
        return least

    def decrease_key(self, key, distance, previous):
        self.heap[self.index[key]].distance = distance
        self.prev[key] = previous
        self.bubble_up(key)


def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    pq = HeapPriorityQueue()
    pq.make_queue(graph)
    pq.decrease_key(source, 0, None)
    while len(pq.heap) > 1:
        least = pq.delete_min()
        for key in graph[least.key].keys():
            if pq.index[key] < len(pq.heap):
                old_dist = pq.heap[pq.index[key]].distance
                new_dist = least.distance + graph[least.key][key]
                if old_dist > new_dist:
                    pq.decrease_key(key, new_dist, least.key)
    cost = 0
    current = target
    path = [current]
    while current != source:
        cost += graph[pq.prev[current]][current]
        current = pq.prev[current]
        path.insert(0, current)
    return path, cost

def find_shortest_path_with_array(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    pq = LinearPriorityQueue()
    pq.make_queue(graph)
    pq.decrease_key(source, 0, None)
    while len(pq.dist) > 1:
        least = pq.delete_min()
        for key in graph[least.key].keys():
            if pq.index[key] < len(pq.dist):
                old_dist = pq.dist[pq.index[key]].distance
                new_dist = least.distance + graph[least.key][key]
                if old_dist > new_dist:
                    pq.decrease_key(key, new_dist, least.key)
    cost = 0
    current = target
    path = [current]
    while current != source:
        cost += graph[pq.prev[current]][current]
        current = pq.prev[current]
        path.insert(0, current)
    return path, cost