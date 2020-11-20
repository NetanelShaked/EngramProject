import numpy as np
import pandas as pn
import xml.etree.ElementTree as ET
from export_region_csv import Export_Region_CSV


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "x " + str(self.x) + " y: " + str(self.y)


class Linear_Function:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def calc_distance(self, x, y):
        return abs((self.point2.y - self.point1.y) * x - (
                self.point2.x - self.point1.x) * y + self.point2.x * self.point1.y - self.point2.y * self.point1.x) / np.sqrt(
            (self.point2.y - self.point1.y) ** 2 + (self.point2.x - self.point1.x) ** 2)


xml = ET.parse(
    r'D:\engram\New_Converted_Folder\N1\0.5h-Done\stack_image_all_channels_marge.xml')
root = xml.getroot()

found = root.find("./contour[@name='corpus callosum-5']")

points = [Point((float)(point.attrib['x']), (float)(point.attrib['y'])) for point in found.iter('point')]

csv_data = pn.read_csv(
    r'D:\engram\New_Converted_Folder\N1\0.5h-Done\separate files\-2355.csv')
functions = [Linear_Function(points[-1], points[0])]

for i in range(1, len(points)):
    functions.append(Linear_Function(points[i - 1], points[i]))
new_csv_data = csv_data.copy()
for index, rows in csv_data.iterrows():
    if any([func.calc_distance(rows['x'], abs(rows['y'])) < 5 for func in functions]) and rows[
        'id name'] == 'corpus callosum, splenium':
        # print(rows)
        new_csv_data.drop(index=index, inplace=True)

new_csv_data.to_csv(r'D:\engram\New_Converted_Folder\N1\0.5h-Done\separate files\new_2355.csv', index=False)
