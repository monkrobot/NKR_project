import shapely.geometry as sg
import descartes
from math import sqrt, pi
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


def center_intersection(circles):

    a = sg.Point(circles[0].x,circles[0].y).buffer(circles[0].r)
    for circle in circles[1:]:
        # poligons have problems when they have only one common point
        # that's whe we add .0000000000001 to circles radius, it adds some points,
        # which are very close (10**(-13)) to the intersection dot
        # b = sg.Point(circle.x,circle.y).buffer(circle.r + .0000000000001)
        # a = a.intersection(b)

        # It's better not to take into account circles with only one common point
        b = sg.Point(circle.x,circle.y).buffer(circle.r)
        try:
            list(a.intersection(b).centroid.coords)[0]
        except IndexError:
            print(f"{circle.name} doesn't have more than one common points")
            continue
        a = a.intersection(b)

    print('a:', a)
    center_intersection_coors = list(a.centroid.coords)[0]
    area = a.area
    radius = sqrt(area/pi)

    obj_area = sg.Point(center_intersection_coors).buffer(radius)

    return a, center_intersection_coors, obj_area


# plot figure
def circles_plot(c_plot, intersection_area, center_intersection, obj_area):
    '''Plot circles and intersection dots
    
    c_plot: list of Circle instances
    data_intersect: list, result of intersection function
    center_intersection: list, intersection coordinates of two intersection lines
    '''
    fig, ax = plt.subplots()

    # plot circles
    for c in c_plot:
        ax.add_patch(plt.Circle((c.x, c.y), c.r, color='#000000', alpha=0.5))
        plt.plot(c.x, c.y, 'yo')
        ax.set_aspect('equal', adjustable='datalim')
        ax.plot()

    ax.add_patch(descartes.PolygonPatch(intersection_area, fc='g', ec='k', alpha=0.2))

    plt.plot(center_intersection[0], center_intersection[1], 'bo')
    ax.add_patch(descartes.PolygonPatch(obj_area, fc='r', ec='k', alpha=1))

    plt.show()


circle1 = Circle(1, 1, 5, 'circle1')
circle2 = Circle(8, 1, 2, 'circle2')
circle3 = Circle(10, 1.1, 13, 'circle3')
circle4 = Circle(2, -6, 8, 'circle4')
circle5 = Circle(-10, 1.1, 14.9, 'circle5')
circle6 = Circle(5.9, 5.9, 11, 'circle6')
circle7 = Circle(0, 8, 12, 'circle7')
circle8 = Circle(5, 4, 9, 'circle8')

circles = [circle1, circle2, circle3, circle4] #, circle5, circle6] # , circle7, circle8]

intersection_area, center_intersection, obj_area = center_intersection(circles)

circles_plot(circles, intersection_area, center_intersection, obj_area)

