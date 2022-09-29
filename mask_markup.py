import os
from PIL import Image
import numpy as np

def markup(masks_path : str, save_path : str) -> None:
    masks = os.listdir(masks_path)

    for i in range(len(masks)):

        with Image.open(masks_path + "/" + str(masks[i])) as img:
            img_as_array = np.asarray(img)

            color_dict = {}
            obj_coordinate_list = [] 
            obj_xy_dict = {}

            img_name = masks[i].split(".")[0]
            save_name = save_path + "/" + img_name + ".txt"

            #print(img_name)

            for i in range(img_as_array.shape[0]):
                for j in range(img_as_array.shape[1]):
                    color = img_as_array[i][j].tolist()
                    if color != [0, 0, 0]: 
                        color_dict[str(color)] = []


            # мб можно так, но не вышло из-за порядка нахождения цветов как я понял, надо проверять
            # colors_test = list(map(lambda x: x[1], img.getcolors()))[:-1:]
            # color_dict= dict.fromkeys(colors_test, [])


            for i in range(img_as_array.shape[0]):
                for j in range(img_as_array.shape[1]):
                    color = img_as_array[i][j].tolist()
                    if color != [0, 0, 0]:
                        color_dict[str(color)].append([i, j])


            for key in color_dict.keys():

                size_y = [10000, 0]
                size_x = [10000, 0]
                obj_xy_dict[key] = []

                for coordinate in color_dict[key]:
                    if coordinate[0] > size_y[1]:
                        size_y[1] = coordinate[0]

                    if coordinate[0] < size_y[0]:
                        size_y[0] = coordinate[0]

                    if coordinate[1] > size_x[1]:
                        size_x[1] = coordinate[1]

                    if coordinate[1] < size_x[0]:
                        size_x[0] = coordinate[1]
                obj_xy_dict[key] = [size_x, size_y]


            for key in obj_xy_dict.keys():
                coordinate_dict = {}
                x_coordinate = obj_xy_dict[key][0]
                y_coordinate = obj_xy_dict[key][1]

                x = (((x_coordinate[1] - x_coordinate[0]) / 2) + x_coordinate[0]) / img_as_array.shape[1]
                y = (((y_coordinate[1] - y_coordinate[0]) / 2) + y_coordinate[0]) / img_as_array.shape[0]

                x_size = (x_coordinate[1] - x_coordinate[0]) / img_as_array.shape[1]
                y_size = (y_coordinate[1] - y_coordinate[0]) / img_as_array.shape[0]

                coordinate_dict['x'] = x
                coordinate_dict['y'] = y
                coordinate_dict['x_size'] = x_size
                coordinate_dict['y_size'] = y_size
                obj_coordinate_list.append(coordinate_dict)

            with open(save_name, 'w') as save_file:
                for coordinates in obj_coordinate_list:
                    save_file.write("0 {} {} {} {}\n".format(coordinates['x'],
                                                     coordinates['y'],
                                                     coordinates['x_size'],
                                                     coordinates['y_size']))