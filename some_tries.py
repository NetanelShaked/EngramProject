import matplotlib.pyplot as plt
import matplotlib.patches as ptc
from PIL import Image
import numpy as np
import pandas as pn
from scipy.spatial import distance
import xml.etree.ElementTree as ET
import matplotlib.lines as lines

#
# Image.MAX_IMAGE_PIXELS = 275727232
#
# image = plt.imread(
#     r'C:\Users\owner\Desktop\PartialImage.jp2')
#
# print (len(image))
# x_pixel=5957
# y_pixel=5025
# # x_pixel = 7641
# # y_pixel = 6001
# distance = 200
# cell_matrix = image[y_pixel - distance:y_pixel + distance, x_pixel - distance:x_pixel + distance]
# #
# ax = plt.gca()
# plt.imshow(cell_matrix, cmap='gray')
# rect = ptc.Rectangle((190, 190), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
# ax.add_patch(rect)
# #
# plt.show()
#
# # data = pn.read_csv(
# #     r'D:\engram\New_Converted_Folder\N2\0.5h\30min_N2_slide-2019-06-18T02-52-54-R1-S7\all_channels_0.5H_N2_points.csv',
# #     skiprows=1)
# # NeuN = data[data['Unnamed: 0'] == "NeuN"]
# # Dapi = data[data['Unnamed: 0'] == "DAPI"]
# # N = NeuN[NeuN['z'] == 445]
# # print(N[N['x']==6248])
#
# # print (distance.euclidean([1, 1, 0], [0, 1, 1]))
#
# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def __repr__(self):
#         return "x " + str(self.x) + " y: " + str(self.y)
#
#
# class Linear_Function:
#     def __init__(self, point1, point2):
#         self.point1 = point1
#         self.point2 = point2
#
#     def calc_distance(self, x, y):
#         return abs((self.point2.y - self.point1.y) * x - (
#                     self.point2.x - self.point1.x) * y + self.point2.x * self.point1.y - self.point2.y * self.point1.x) / np.sqrt(
#             (self.point2.y - self.point1.y) ** 2 + (self.point2.x - self.point1.x) ** 2)
#

# xml = ET.parse(
#     r'D:\engram\New_Converted_Folder\N2\0.5h\30min_N2_slide-2019-06-18T02-52-54-R1-S7\all_channels_0.5H_N2 - Copy.xml')
# root = xml.getroot()
#
# found = root.find("./contour[@name='corpus callosum-3']")
#
# points = [Point((float)(point.attrib['x']), (float)(point.attrib['y'])) for point in found.iter('point')]
# print(points)
# plt.imshow(image, cmap='gray')
# ax = plt.gca()
# (x, y) = zip(*[(points[-1].x, np.abs(points[-1].y)), (points[0].x, np.abs(points[0].y))])
# ax.add_line(lines.Line2D(x, y, linewidth=0.5, color='blue'))
#
# for p in range(1, len(points)):
#     (x, y) = zip(*[(points[p - 1].x, np.abs(points[p - 1].y)), (points[p].x, np.abs(points[p].y))])
#     ax.add_line(lines.Line2D(x, y, linewidth=0.5, color='blue'))
#
# p1=Point(0,0)
# p2=Point(0,1)
# l=Linear_Function(p1,p2)
# print (l.calc_distance(1,0))
# plt.show()


dataa = pn.read_csv(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\all_channels_0.5H_N2 _points.csv', skiprows=1)
data = dataa[dataa['Unnamed: 0'] == 'NeuN_region_check']
new_df = pn.DataFrame({'Bregma': [], 'Median': [], 'std': [], 'Median+4Std': []})
for bregma in data['z'].unique():
    new_df = new_df.append({'Bregma': bregma, 'Median': data[data['z'] == bregma]['Channel 2'].mean(),
                            'std': data[data['z'] == bregma]['Channel 2'].std(),
                            'Median+4Std': data[data['z'] == bregma]['Channel 2'].mean() + 4 *
                                           data[data['z'] == bregma]['Channel 2'].std()},
                           ignore_index=True)

new_df.to_csv(r'D:\engram\New_Converted_Folder\N2\0.5h\ttt.csv', index=False)
#
# manualy = pn.DataFrame({'Bregma': [], 'max': []})
# datab = dataa[dataa['Unnamed: 0'] == 'NeuN- Negative']
# for bregma in datab['z'].unique():
#     manualy = manualy.append({'Bregma': bregma, 'max': datab[datab['z'] == bregma]['Channel 2'].max()},
#                              ignore_index=True)
#
# manualy.to_csv(r'D:\engram\New_Converted_Folder\N2\0.5h\NeuN_Max.csv', index=False)


# Image.MAX_IMAGE_PIXELS = 10 ** 10
#
# b=plt.imread(r'D:\engram\New_Converted_Folder\N2\0.5h\separate Images\single Image_Section0001_Slide002_Contour001.jp2')
# plt.figure(figsize=(20,20))
# plt.subplot(131)
# plt.imshow(b[:,:,1])
# plt.subplot(132)
# plt.imshow(b[:,:,2])
# plt.show()