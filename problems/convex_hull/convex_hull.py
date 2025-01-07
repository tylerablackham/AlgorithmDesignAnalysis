# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point

class Node:
    def __init__(self, coordinates:tuple[float, float]):
        self.coordinates = coordinates
        self.clockwise = None
        self.counterclockwise = None

    def add_clockwise(self, node: 'Node'):
        self.clockwise = node
        node.counterclockwise = self

    def add_counterclockwise(self, node: 'Node'):
        self.counterclockwise = node
        node.clockwise = self

def slope(left: Node, right: Node) -> float:
    return ((right.coordinates[1] - left.coordinates[1])
            / (right.coordinates[0] - left.coordinates[0]))

class Hull:
    def __init__(self, coordinates:tuple[float, float]):
        node: Node = Node(coordinates)
        node.clockwise = node
        node.counterclockwise = node
        self.rightmost = node
        self.leftmost = node

    def join_two_nodes(self, right_hull: 'Hull'):
        """Only use when joining two hulls that both only have one node each"""
        self.rightmost.add_clockwise(right_hull.leftmost)
        self.rightmost.add_counterclockwise(right_hull.leftmost)
        self.rightmost = right_hull.rightmost

    def hull_join(self, right_hull: 'Hull'):
        ul, ur = self.set_upper_tangent(right_hull)
        ll, lr = self.set_lower_tangent(right_hull)
        ul.add_clockwise(ur)
        ll.add_counterclockwise(lr)
        self.rightmost = right_hull.rightmost

    def set_upper_tangent(self, right_hull: 'Hull') -> (Node, Node):
        l = self.rightmost
        r = right_hull.leftmost
        tan = slope(l,r)
        done = False
        while not done:
            done = True
            while True:
                if l.counterclockwise == self.rightmost:
                    break
                temp = slope(l.counterclockwise, r)
                if temp < tan:
                    tan = temp
                    l = l.counterclockwise
                    done = False
                else:
                    break
            while True:
                if r.clockwise == right_hull.leftmost:
                    break
                temp = slope(l, r.clockwise)
                if temp > tan:
                    tan = temp
                    r = r.clockwise
                    done = False
                else:
                    break
        return l, r

    def set_lower_tangent(self, right_hull: 'Hull') -> (Node, Node):
        l = self.rightmost
        r = right_hull.leftmost
        tan = slope(l,r)
        done = False
        while not done:
            done = True
            while True:
                if l.clockwise == self.rightmost:
                    break
                temp = slope(l.clockwise, r)
                if temp > tan:
                    tan = temp
                    l = l.clockwise
                    done = False
                else:
                    break
            while True:
                if r.counterclockwise == right_hull.leftmost:
                    break
                temp = slope(l, r.counterclockwise)
                if temp < tan:
                    tan = temp
                    r = r.counterclockwise
                    done = False
                else:
                    break
        return l, r



def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    sorted_points = sorted(points, key=lambda point: point[0])
    hull: Hull = recursive_hull(sorted_points)
    hull_list: list[tuple[float, float]] = []
    hull_node: Node = hull.leftmost
    hull_list.append(hull_node.coordinates)
    while True:
        hull_node = hull_node.clockwise
        if hull_node == hull.leftmost:
            break
        else:
            hull_list.append(hull_node.coordinates)
    return hull_list

def recursive_hull(points: list[tuple[float, float]]) -> Hull:
    if len(points) == 1:
        return Hull(points[0])
    if len(points) == 2:
        left_hull = recursive_hull([points[0]])
        right_hull = recursive_hull([points[1]])
        left_hull.join_two_nodes(right_hull)
        return left_hull
    else:
        mid = len(points) // 2
        left_hull = recursive_hull(points[:mid])
        right_hull = recursive_hull(points[mid:])
        left_hull.hull_join(right_hull)
        return left_hull
