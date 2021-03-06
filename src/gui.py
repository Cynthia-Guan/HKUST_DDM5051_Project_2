# -*- coding: utf-8 -*-
# Author    : Cynthia Guan
# Create    : 12/04/2021  14:54:36
# Final Edit: 12/04/2021  03:35:36
# Software: PyCharm
"""
The whole GUI should look like this:
master_frame--------------------------------------------------------------------------------------
    |                                                                                             |
    |  Search(LabelFrame)----------------------------------------------------------------------   |
    |  |   Type(cbox)-   DT_O(tbox)-   GID_O(cbox)-   DT_D(tbox)-   GID_D(cbox)-   TE(cbox)-   |  |
    |  |  |           | |  (2 tbox) | |            | | (2 tbox)  | |            | |         |  |  |
    |  |   -----------   -----------   ------------   -----------   ------------   ---------   |  |
    |  ----------------------------------------------------------------------------------------   |
    |                                                                                             |
    |  Sort(LabelFrame)------------------------------------------------------------------------   |
    |  |   Type(LbFm)----   DT_O(LbFm)----   GID_O(LbFm)---   DTD(LbFm)-----  GID_D(LbFm)----  |  |
    |  |  |    tick      | |      tick    | |      tick    | |      tick    | |      tick    | |  |
    |  |  | ascend(cbox) | | ascend(cbox) | | ascend(cbox) | | ascend(cbox) | | ascend(cbox) | |  |
    |  |   --------------   --------------   --------------   --------------   --------------  |  |
    |   ---------------------------------------------------------------------------------------
    |                                       -----------                                           |
    |                                      |   Search  |                                          |
    |                                       -----------                                           |
     ---------------------------------------------------------------------------------------------
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import time

import pandas as pd


class GUI:
    def __init__(self,vehicle_list, gantry_id_olist, gantry_id_dlist):
        self.root_window = tk.Tk()
        self.root_window.title('5051 project2')
        self.root_window.minsize(1600, 300)
        self.root_window.geometry('1600x400')

        hello = tk.Label(self.root_window, text='Hello, visitor. Please tell me what you are looking for.', font=30)
        hello.pack(expand=1, fill=tk.X)

        box1 = tk.LabelFrame(self.root_window, text="Search for", font=30)
        box1.pack(expand=1, fill=tk.X, padx=40)
        self.vehicle_type = NamedCombobox(box1, "Vehicle Type", vehicle_list)
        self.dtime_O = Namedtimetextbox(box1, "First Detection Time")
        self.gantry_id_O = NamedCombobox(box1, "First Gantry ID", gantry_id_olist)
        self.dtime_D = Namedtimetextbox(box1, "Last Detection Time")
        self.gantry_id_D = NamedCombobox(box1, "Last Gantry ID", gantry_id_dlist)
        self.trip_end = NamedCombobox(box1, "Trip Finished", ['Yes', 'No',''])
        box2 = tk.LabelFrame(self.root_window, text="Sort by", font=30)
        self.vt = SelectionBox(box2, "Vehicle Type")
        self.dto = SelectionBox(box2, "First Detection Time")
        self.gido = SelectionBox(box2, "First Gantry ID")
        self.dtd = SelectionBox(box2, "Last Detection Time")
        self.gidd = SelectionBox(box2, "Last Gantry ID")
        self.triplen = SelectionBox(box2, "Trip Length")
        box2.pack(expand=1, fill=tk.X, padx=40)
        self.begin = tk.Button(self.root_window, text="Search", font=20, height=1, width=10)
        self.begin.pack(pady=10)

    def error_message(self, error_type):
        tk.messagebox.showerror(title='Wrong value', message=error_type)

    def no_result(self):
        tk.messagebox.showinfo(title='No result', message='Sorry, we can\'t find compatible results')

    def show_result(self, result: pd.DataFrame):
        human_readable = ['Vehicle Type', 'First Detection Time', "First Gantry ID", "Last Detection Time",\
                          'Last Gantry ID', 'Trip Length', 'Trip Finished', 'Trip Info']
        newwindow = tk.Toplevel()
        newwindow.title = 'Your Result'
        newwindow.geometry('1600x400')
        columns = result.columns
        tree = ttk.Treeview(newwindow, show="headings", selectmode='browse', columns=columns)

        tree.column(columns[0], width=100)
        tree.column(columns[1], width=200)
        tree.column(columns[2], width=100)
        tree.column(columns[3], width=200)
        tree.column(columns[4], width=100)
        tree.column(columns[5], width=80)
        tree.column(columns[6], width=80)
        tree.column(columns[7], width=400)
        tree.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, pady=10, padx=10)

        for i in range(len(columns)):
            tree.heading(columns[i], text= human_readable[i])

        # add data to the treeview
        stt = time.time()
        for idx in result.index:
            if time.time() - stt > 5:
                break
            row = [i for i in result.loc[idx]]
            tree.insert('', tk.END, values=row)


        # add a scrollbar
        scrollbar = ttk.Scrollbar(newwindow, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)


class NamedCombobox:
    def __init__(self, master, name, valuelist):
        frame = tk.Frame(master)
        label = tk.Label(frame,text = name, font = 15)
        label.pack(expand=1)
        self.combo = ttk.Combobox(frame, state='readonly')
        self.combo['values'] = valuelist
        self.combo.pack(expand=1)
        frame.pack(side=tk.LEFT, expand=1, pady=10, padx=10)


class Namedtimetextbox:
    def __init__(self, master, name):
        frame = tk.Frame(master)
        label = tk.Label(frame, text=name, font=15)
        label.pack(expand=1)
        subframe = tk.Frame(frame)
        start = tk.Label(subframe, text="Between", font=9)
        start.pack(side=tk.LEFT, expand=1)
        self.s_time = tk.Entry(subframe)
        self.s_time.pack(side=tk.LEFT, expand=1)
        end = tk.Label(subframe, text="and", font=9)
        end.pack(side=tk.LEFT, expand=1)
        self.e_time = tk.Entry(subframe)
        self.e_time.pack(side=tk.LEFT, expand=1)
        subframe.pack(expand=1)
        frame.pack(side=tk.LEFT, expand=1, pady=10, padx=10)


class SelectionBox:
    def __init__(self, master, name):
        self.v_type = tk.BooleanVar()
        frame = tk.Frame(master)
        self.check = tk.Checkbutton(frame, text=name, font=15, variable= self.v_type, width=20)
        self.check.pack(expand=1, side=tk.TOP)
        frame.pack(side=tk.LEFT, expand=1, pady=10, padx=10)
        subframe = tk.Frame(frame)
        label = tk.Label(subframe, text='Order', font=8)
        self.order = ttk.Combobox(subframe, state='disabled')
        self.order['values'] = ['Ascending', "Descending"]
        label.pack(side=tk.LEFT, expand=1, pady=10)
        self.order.pack(side=tk.LEFT, expand=1, pady=10)
        subframe.pack(side=tk.TOP)