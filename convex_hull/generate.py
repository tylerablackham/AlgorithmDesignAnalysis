import random


def rand1to1():
    return (random.random() - 0.5) * 2  # -1 to 1


def generate_random_points(distribution: str, n: int, seed: int | None = None) -> list[tuple[float, float]]:
    random.seed(seed)
    distribution = distribution.lower()

    if distribution in ['normal', 'guassian']:
        def rand_func():
            return random.normalvariate(0, 0.4), random.normalvariate(0, 0.4)

    elif distribution == 'uniform':
        def rand_func():
            return rand1to1(), rand1to1()

    elif distribution in ['oval', 'circular', 'circle']:
        def rand_func():
            while (x := rand1to1()) ** 2 + (y := rand1to1()) ** 2 > 0.98 ** 2:
                pass  # generate x,y pairs until they fit in the circle
            return x, y

    elif distribution in ['spherical', 'sphere']:
        def rand_func():
            while (x := rand1to1()) ** 2 + (y := rand1to1()) ** 2 + (rand1to1()) > 0.98 ** 2:
                pass  # generate x,y,z pairs until they fit in the sphere
            return x, y  # only return the x,y part

    else:
        raise NotImplementedError(f'Random distribution of type: {distribution}')

    # Generate points with unique x values
    points = []
    xs = set()
    while len(points) < n:
        point = rand_func()
        if point[0] not in xs:
            points.append(point)
            xs.add(point[0])

    return points
