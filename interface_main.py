import tkinter
from os.path import exists
from tkinter import messagebox

top = tkinter.Tk()
top.geometry("500x500")

tkinter.Label(top, text="Path").place(x=250, y=0)
fileAdress = tkinter.Entry(top, state='normal')
fileAdress.place(x=330, y=0)

tkinter.Label(top, text="file name / image name").place(x=190, y=30)
fileName = tkinter.Entry(top)
fileName.place(x=330, y=30)

tkinter.Label(top, text="CSV name / mouse name").place(x=190, y=60)
another_name = tkinter.Entry(top)
another_name.place(x=330, y=60)


def calculateCfosIntensity():
    # all the class dependes:
    if not (exists(fileAdress.get())):
        messagebox.showinfo("No file exist", "No file exist in this address")
    elif (fileName.get() == ""):
        messagebox.showinfo("Empty Name", "Image Name is null")
    elif (another_name.get() == ""):
        messagebox.showinfo("Empty Name", "CSV Name is null")
    else:
        print("delete this row")
        # CalculateCfosIntensity(fileAdress.get(),fileName.get(),another_name.get())
        # same shit for all and do what ever you want / expect to do


def cell_present():
    messagebox.showinfo("Hello Python", "Hello World")


def cfos_count():
    messagebox.showinfo("Hello Python", "Hello World")


def csv_section_initialize():
    messagebox.showinfo("Hello Python", "Hello World")


def Dentate_Corpose():
    messagebox.showinfo("Hello Python", "Hello World")


def export_region_csv():
    messagebox.showinfo("Hello Python", "Hello World")


def filter_coordinate():
    messagebox.showinfo("Hello Python", "Hello World")


def find_unknow_id():
    messagebox.showinfo("Hello Python", "Hello World")


def getCSVbyBregma():
    messagebox.showinfo("Hello Python", "Hello World")


def one_side():
    messagebox.showinfo("Hello Python", "Hello World")


def otsu():
    messagebox.showinfo("Hello Python", "Hello World")


def separate_dorsal_ventral_hippocampus():
    messagebox.showinfo("Hello Python", "Hello World")


def separate_regions():
    messagebox.showinfo("Hello Python", "Hello World")


def some_tries():
    messagebox.showinfo("Hello Python", "Hello World")


def summary_data():
    messagebox.showinfo("Hello Python", "Hello World")


calculateCfosIntensity_but = tkinter.Button(top, text="calculateCfosIntensity", command=calculateCfosIntensity)
calculateCfosIntensity_but.place(x=0, y=0)

cell_present_but = tkinter.Button(top, text="cell present", command=cell_present)
cell_present_but.place(x=0, y=30)

cfos_count_but = tkinter.Button(top, text="cfos count", command=cfos_count)
cfos_count_but.place(x=0, y=60)

csv_section_initialize_but = tkinter.Button(top, text="csv section initialize", command=csv_section_initialize)
csv_section_initialize_but.place(x=0, y=90)

Dentate_Corpose_but = tkinter.Button(top, text="Dentate Corpose", command=Dentate_Corpose)
Dentate_Corpose_but.place(x=0, y=120)

export_region_csv_but = tkinter.Button(top, text="export region csv", command=export_region_csv)
export_region_csv_but.place(x=0, y=150)

filter_coordinate_but = tkinter.Button(top, text="filter coordinate", command=filter_coordinate)
filter_coordinate_but.place(x=0, y=180)

find_unknow_id_but = tkinter.Button(top, text="find unknow id", command=find_unknow_id)
find_unknow_id_but.place(x=0, y=210)

one_side_but = tkinter.Button(top, text="one side", command=one_side)
one_side_but.place(x=0, y=240)

otsu_but = tkinter.Button(top, text="otsu", command=otsu)
otsu_but.place(x=0, y=270)

separate_dorsal_ventral_hippocampus_but = tkinter.Button(top, text="separate dorsal ventral hippocampus",
                                                         command=separate_dorsal_ventral_hippocampus)
separate_dorsal_ventral_hippocampus_but.place(x=0, y=300)

separate_regions_but = tkinter.Button(top, text="separate regions", command=separate_regions)
separate_regions_but.place(x=0, y=330)

some_tries_but = tkinter.Button(top, text="some tries", command=some_tries)
some_tries_but.place(x=0, y=360)

summary_data_but = tkinter.Button(top, text="summary data", command=summary_data)
summary_data_but.place(x=0, y=390)

# Code to add widgets will go here...
top.mainloop()
