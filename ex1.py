import sys
import numpy as np
import matplotlib.pyplot as plt
image_name, centroids_name, out_file = sys.argv[1], sys.argv[2], sys.argv[3]
centorids = np.loadtxt(centroids_name)
org_pixel = plt.imread(image_name)
pixels = org_pixel.astype(float) / 255
pixels = pixels.reshape(-1, 3)

def dis_pixel(c, pixel):
    return np.sqrt(pow(c[0] - pixel[0], 2) + pow(c[1] - pixel[1], 2) + pow(c[2] - pixel[2], 2))


def min_distance(min_cur, second_min):
    if second_min < min_cur:
        return second_min
    return min_cur


def find_dis_cenroids_index(arr_centro, pixel):
    min_dis = dis_pixel(arr_centro[0], pixel)
    index = 0
    for c, k in enumerate(arr_centro):
        temp_dis = min_dis
        min_dis = min_distance(min_dis, dis_pixel(k, pixel))
        if min_dis != temp_dis:
            index = c
    return index, min_dis


def update(index_c, cur_pixel):
    lst = list(update_centroids[index_c])
    lst[2] += 1
    lst[1] = np.add(lst[1], cur_pixel)
    update_centroids[index_c] = tuple(lst)


def update_list():
    new_cenrtoids = []
    stop_update = True
    for index, c in enumerate(update_centroids):
        t = list(c)
        if t[2] != 0:
            t[0] = t[1] / t[2]
            t[0] = t[0].round(4)
            t[2] = 0
            t[1] = (0, 0, 0)
            update_centroids[index] = tuple(t)
        new_cenrtoids.append(t[0])
        if (t[0] != c[0]).any():
            stop_update = False
    return stop_update, new_cenrtoids


def init():
    for i in centorids:
        update_centroids.append((i, (0, 0, 0), 0))


update_centroids = []
init()

stop = False
text_file = open(out_file, "w")
x_arr = []
y_arr = []
for j in range(20):
    sum_error = 0
    if not stop:
        for p in pixels:
            index_centroids, error = find_dis_cenroids_index(centorids, p)
            sum_error += pow(error, 2)
            update(index_centroids, p)
        # y_arr.append(sum_error / len(pixels))
        # x_arr.append(j)
        stop, centorids = update_list()
        line = f"[iter {j}]:{','.join([str(i[0].round(4)) for i in update_centroids])}"
        text_file.write(line + "\n")
# plt.plot(x_arr, y_arr, marker="o")
# plt.xlabel("iterations")
# plt.ylabel("loss")
# plt.title(f"k={len(centorids)}")
# plt.show()
text_file.close()
