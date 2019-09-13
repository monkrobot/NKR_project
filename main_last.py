import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from math import sqrt, fabs, ceil


gate_w_x = 5
gate_w_y = 15
module_coor_x = [12,1,8,22,3,17,22,4,32,6,11,30,6,24,12]
module_coor_y = [4,10,1,22,29,3,16,1,7,12,32,7,3,6,23]
robot_path = [[15,16,19,22,25,27,32],[12,24,32,32,24,17,12]]
module_dist = {}
ready_module = [[gate_w_x, gate_w_y]]

distance = 3


# make dots on robot's path and add their coors to module_coor
robot_coor = []
for coor in zip(robot_path[0], robot_path[1]):
    if robot_coor:
        dist = sqrt((fabs(robot_coor[0] - coor[0])) ** 2 + (fabs(robot_coor[1] - coor[1])) ** 2)
        module_num = ceil(dist / distance)
        angle1 = (robot_coor[1] - coor[1]) / dist
        angle0 = (robot_coor[0] - coor[0]) / dist

        for num in range(1, module_num + 1):
            new_mod_coor_x = robot_coor[0] - angle0 * (dist / module_num) * num
            new_mod_coor_y = robot_coor[1] - angle1 * (dist / module_num) * num
            #ready_module.append([new_mod_coor_x, new_mod_coor_y])
            module_coor_x.append(new_mod_coor_x)
            module_coor_y.append(new_mod_coor_y)

        robot_coor = coor
    else:
        robot_coor = coor


# make list of distance between modules to gate_way
for coor in range(len(module_coor_x)):
    dist = sqrt((fabs(gate_w_x-module_coor_x[coor]))**2 + (fabs(gate_w_y-module_coor_y[coor]))**2)
    module_dist[dist] = [module_coor_x[coor], module_coor_y[coor]]

# module_dist_sort = dict(sorted(module_dist.items()))
# print(module_dist_sort)

for module in dict(sorted(module_dist.items())).values():
    dist_to_mod = []

    # find the nearest module in ready_module for connection to it
    for ready_m in ready_module:
        dist = sqrt((fabs(ready_m[0] - module[0])) ** 2 + (fabs(ready_m[1] - module[1])) ** 2)
        angle1 = (ready_m[1]-module[1])/dist
        angle0 = (ready_m[0] - module[0]) / dist

        if dist_to_mod == []:
            dist_to_mod.extend([dist, angle0, angle1, module, ready_m])
        elif dist_to_mod[0] > dist:
            dist_to_mod = [dist, angle0, angle1, module, ready_m]
        else:
            continue

    # find the coors of additional points between module and nearest ready module
    module_num = ceil(dist_to_mod[0]/distance)
    for num in range(1, module_num+1):
        # new_mod_coor = ready_m[x or y] - angle * (dist/module_num)*num
        new_mod_coor_x = dist_to_mod[4][0] - dist_to_mod[1] * (dist_to_mod[0]/module_num)*num
        new_mod_coor_y = dist_to_mod[4][1] - dist_to_mod[2] * (dist_to_mod[0]/module_num)*num
        ready_module.append([new_mod_coor_x, new_mod_coor_y])

        # from gateway to every point
        # new_mod_coor_x = num * (dist_to_mod[4][0] - dist_to_mod[1] * dist_to_mod[0]) / module_num
        # new_mod_coor_y = num * (dist_to_mod[4][1] - dist_to_mod[2] * dist_to_mod[0]) / module_num
        # ready_module.append([new_mod_coor_x, new_mod_coor_y])

print('ready_module:', ready_module)


for coor in ready_module:
    plt.plot(coor[0], coor[1], 'yo')
plt.plot(gate_w_x, gate_w_y, 'ro')
plt.plot(module_coor_x, module_coor_y, 'bo')
plt.plot(*robot_path)
plt.show()

