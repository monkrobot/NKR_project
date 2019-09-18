import shapely.geometry as sg
import matplotlib.pyplot as plt
import descartes

# create the circles with shapely
a = sg.Point(0,0).buffer(1.)
b = sg.Point(1,0).buffer(1.)

c = sg.Point(0,-1).buffer(0.7)
d = sg.Point(1,-1).buffer(0.6)

# compute the 3 parts
left = a.difference(b)
right = b.difference(a)
middle = a.intersection(b)

intersect = c.intersection(middle)
# print('middle:', middle)
# print('intersect:', intersect)
# print('-'*18)

intersect2 = d.intersection(intersect)
# print('intersect2:', intersect2)
print('dir:', intersect2.__geo_interface__['coordinates'][0])

# use descartes to create the matplotlib patches
ax = plt.gca()
ax.add_patch(descartes.PolygonPatch(left, fc='b', ec='k', alpha=0.2))
ax.add_patch(descartes.PolygonPatch(right, fc='r', ec='k', alpha=0.2))
ax.add_patch(descartes.PolygonPatch(c, fc='r', ec='k', alpha=0.2))
ax.add_patch(descartes.PolygonPatch(d, fc='r', ec='k', alpha=0.2))
ax.add_patch(descartes.PolygonPatch(middle, fc='g', ec='k', alpha=0.2))
ax.add_patch(descartes.PolygonPatch(intersect, fc='y', ec='k', alpha=0.2))
ax.add_patch(descartes.PolygonPatch(intersect2, fc='b', ec='k', alpha=0.2))

# control display
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
ax.set_aspect('equal')
plt.show()