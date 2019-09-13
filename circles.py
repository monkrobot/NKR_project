from math import sqrt, fabs
from collections import namedtuple

# for VSCode
# import matplotlib
# matplotlib.rcParams["backend"] = "TkAgg"
# matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


class Circle:
    def __init__(self, x, y, r, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.name = name


def intersection(circles):
    '''Check circles intersection, return coors of intersection

    circles: list of Circle instances
    return: data for ploting circles: circles coors and radius, height coor, coors of intersection
    '''
    data_intersect = []

    for num, c1 in enumerate(circles[:-1]):
        for c2 in circles[num+1:]:
            # distance between circle centers
            dist = sqrt((fabs(c2.x - c1.x)) ** 2 + (fabs(c2.y - c1.y)) ** 2)

            if c1.r + c2.r > dist:
                dist_to_height = dist - (c2.r**2 - c1.r**2 + dist**2)/(2*dist)
                height = sqrt(c1.r**2 - dist_to_height**2)

                angle_cos = (c2.x - c1.x)/dist
                angle_sin = (c2.y - c1.y)/dist

                # P0 dot coordinates
                p0_x = c1.x + angle_cos * dist_to_height
                p0_y = c1.y + angle_sin * dist_to_height

                # 2 intersection dots
                inter_dot_1_x = p0_x + (c2.y - c1.y) * height / dist
                inter_dot_1_y = p0_y - (c2.x - c1.x) * height / dist

                inter_dot_2_x = p0_x - (c2.y - c1.y) * height / dist
                inter_dot_2_y = p0_y + (c2.x - c1.x) * height / dist

                # Intersection center dot


                Intersect_data = namedtuple('Intersect_data', ['p0_x', 'p0_y', 'inter_dot_1_x',
                                                               'inter_dot_1_y', 'inter_dot_2_x', 'inter_dot_2_y'])
                intersect = Intersect_data(p0_x, p0_y, inter_dot_1_x, inter_dot_1_y,
                                      inter_dot_2_x, inter_dot_2_y)

                data_intersect.append(intersect)

            else:
                print('No intersection:', c1.name, c2.name)
    print('data:', data_intersect)
    print('data:', data_intersect[0].inter_dot_1_x)
    return data_intersect


# plot figure
def circles_plot(c_plot, data_intersect):

    fig, ax = plt.subplots()

    # plot circles
    for c in c_plot:
        ax.add_patch(plt.Circle((c.x, c.y), c.r, color='r', alpha=0.5))
        plt.plot(c.x, c.y, 'ro')
        ax.set_aspect('equal', adjustable='datalim')
        ax.plot()

    # plot intersection points
    for points_coors in data_intersect:
        plt.plot(points_coors.inter_dot_1_x, points_coors.inter_dot_1_y, 'ro')
        plt.plot(points_coors.inter_dot_2_x, points_coors.inter_dot_2_y, 'ro')
        plt.plot([points_coors.inter_dot_1_x, points_coors.inter_dot_2_x],
                 [points_coors.inter_dot_1_y, points_coors.inter_dot_2_y])
        plt.plot(points_coors.p0_x, points_coors.p0_y, 'go')

    plt.show()


circle1 = Circle(0, 1, 5, 'circle1')
circle2 = Circle(10, -4, 10, 'circle2')
circle3 = Circle(-5, -5, 7, 'circle3')
circle4 = Circle(3, 8, 6, 'circle4')

circles = [circle1, circle2, circle3, circle4]

data = intersection(circles)
circles_plot(circles, data)
