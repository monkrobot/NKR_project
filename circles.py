from math import sqrt, fabs
from collections import namedtuple
import numpy as np

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
    return: data for ploting circles intersection: height coor, coors of intersection
    '''
    data_intersect = []

    for num, c1 in enumerate(circles[:-1]):
        for c2 in circles[num+1:]:
            # distance between circle centers
            dist = sqrt((fabs(c2.x - c1.x)) ** 2 + (fabs(c2.y - c1.y)) ** 2)

            # centers' line direction from c1 to c2
            angle_cos = (c2.x - c1.x)/dist
            angle_sin = (c2.y - c1.y)/dist

            Intersect_data = namedtuple('Intersect_data', ['p0_x', 'p0_y', 'inter_dot_1_x',
                                                               'inter_dot_1_y', 'inter_dot_2_x', 'inter_dot_2_y'])

            if c1.r + c2.r > dist:
                dist_to_height = dist - (c2.r**2 - c1.r**2 + dist**2)/(2*dist)
                print('name:', c1.name, c2.name)
                height = sqrt(c1.r**2 - dist_to_height**2)

                # P0 dot coordinates
                p0_x = c1.x + angle_cos * dist_to_height
                p0_y = c1.y + angle_sin * dist_to_height

                # 2 intersection dots
                inter_dot_1_x = p0_x + (c2.y - c1.y) * height / dist
                inter_dot_1_y = p0_y - (c2.x - c1.x) * height / dist

                inter_dot_2_x = p0_x - (c2.y - c1.y) * height / dist
                inter_dot_2_y = p0_y + (c2.x - c1.x) * height / dist

                intersect = Intersect_data(p0_x, p0_y, inter_dot_1_x, inter_dot_1_y,
                                      inter_dot_2_x, inter_dot_2_y)

                data_intersect.append(intersect)

            elif c1.r + c2.r == dist:
                # 1 intersection dot
                inter_dot_1_x = c1.x + angle_cos * c1.r
                inter_dot_1_y = c1.y + angle_sin * c1.r

                intersect = Intersect_data(False, False, inter_dot_1_x, inter_dot_1_y, False, False)

                data_intersect.append(intersect)

            else:
                print('No intersection:', c1.name, c2.name)
                return False

    return data_intersect


# plot figure
def circles_plot(c_plot, data_intersect, center_intersection):
    '''Plot circles and intersection dots
    
    c_plot: list of Circle instances
    data_intersect: list, result of intersection function
    center_intersection: list, intersection coordinates of two intersection lines
    '''
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
        if points_coors.inter_dot_2_x:
            plt.plot(points_coors.inter_dot_2_x, points_coors.inter_dot_2_y, 'ro')
            plt.plot([points_coors.inter_dot_1_x, points_coors.inter_dot_2_x],
                     [points_coors.inter_dot_1_y, points_coors.inter_dot_2_y])
            plt.plot(points_coors.p0_x, points_coors.p0_y, 'go')

    plt.plot(center_intersection[0], center_intersection[1], 'bo')

    plt.show()


def center_of_intersection(data1, data2):
    '''intersection dots line function
    
    data1: data from intersection function about first circle
    data2: data from intersection function about second circle
    result: list of intersection coordinates of two intersection lines
    '''
    # y = (x*(inter_dot_2_y - inter_dot_1_y) - inter_dot_2_y*inter_dot_1_x + inter_dot_1_y*inter_dot_1_x)/(inter_dot_2_x - inter_dot_1_x) + inter_dot_1_y
    # y = k*x + b
    if data1.inter_dot_2_x and data2.inter_dot_2_x:
        print('Hello', data1.p0_x, data1.p0_y)
        k1 = (data1.inter_dot_2_y - data1.inter_dot_1_y) / (data1.inter_dot_2_x - data1.inter_dot_1_x)
        k2 = (data2.inter_dot_2_y - data2.inter_dot_1_y) / (data2.inter_dot_2_x - data2.inter_dot_1_x)
        b1 = data1.inter_dot_1_x*(data1.inter_dot_1_y - data1.inter_dot_2_y) / (data1.inter_dot_2_x - data1.inter_dot_1_x) + data1.inter_dot_1_y
        b2 = data2.inter_dot_1_x*(data2.inter_dot_1_y - data2.inter_dot_2_y) / (data2.inter_dot_2_x - data2.inter_dot_1_x) + data2.inter_dot_1_y
        M1 = np.array([[-k1, 1.], [-k2, 1.]])
        v1 = np.array([b1, b2])

        center_of_intersection = np.linalg.solve(M1, v1)
    else:
        print('data1:', data1)
        print('data2:', data2)
        center_of_intersection = [(data1.inter_dot_2_x or data2.inter_dot_2_x), (data1.inter_dot_2_y or data2.inter_dot_2_y)]
    print('center_of_intersection:', center_of_intersection)
    return center_of_intersection


circle1 = Circle(1.15, 1, 8.5, 'circle1')
circle2 = Circle(1, -8.7, 6, 'circle2')
circle3 = Circle(10, 1.1, 13, 'circle3')
# circle4 = Circle(8.9, -9, 8, 'circle4')
# circle5 = Circle(-10, 1.1, 15, 'circle5')
# circle6 = Circle(8.9, -9, 8, 'circle6')
# circle7 = Circle(0, 8, 9, 'circle7')
# circle8 = Circle(5, 5, 5, 'circle8')

circles = [circle1, circle2, circle3] #, circle4, circle5, circle6, circle7, circle8]

data = intersection(circles)
if data:
    center_intersection = center_of_intersection(data[0], data[1])
    circles_plot(circles, data, center_intersection)
