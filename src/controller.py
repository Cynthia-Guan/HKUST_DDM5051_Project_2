# -*- coding: utf-8 -*-
# Author    : Cynthia Guan
# Create    : 12/04/2021  22:32:06
# Final Edit: 12/05/2021  03:32:06
# Software: PyCharm

import gui
import re
import search
import model
import sort


def check_order1():
    if window.vt.v_type.get():
        window.vt.order.config(state='readonly')
        window.vt.order.current(0)
    else:
        window.vt.order.config(state='disabled')
        window.vt.order.set('')


def check_order2():
    if window.dto.v_type.get():
        window.dto.order.config(state='readonly')
        window.dto.order.current(0)
    else:
        window.dto.order.config(state='disabled')
        window.dto.order.set('')


def check_order3():
    if window.gido.v_type.get():
        window.gido.order.config(state='readonly')
        window.gido.order.current(0)
    else:
        window.gido.order.config(state='disabled')
        window.gido.order.set('')


def check_order4():
    if window.dtd.v_type.get():
        window.dtd.order.config(state='readonly')
        window.dtd.order.current(0)
    else:
        window.dtd.order.config(state='disabled')
        window.dtd.order.set('')


def check_order5():
    if window.gidd.v_type.get():
        window.gidd.order.config(state='readonly')
        window.gidd.order.current(0)
    else:
        window.gidd.order.config(state='disabled')
        window.gidd.order.set('')


def check_order6():
    if window.triplen.v_type.get():
        window.triplen.order.config(state='readonly')
        window.triplen.order.current(0)
    else:
        window.triplen.order.config(state='disabled')
        window.triplen.order.set('')


def check_legality():
    search_list = [window.vehicle_type.combo.get(), window.dtime_O.s_time.get(),\
                   window.dtime_O.e_time.get(), window.gantry_id_O.combo.get(),\
                   window.dtime_D.s_time.get(), window.dtime_D.e_time.get(),\
                   window.gantry_id_D.combo.get(), window.trip_end.combo.get()]
    dates = search_list[1:3] + search_list[4:6]

    legal = True

    for date in dates:
        if not date:
            continue
        if re.match('2[0-3]:[0-5][0-9]:[0-5][0-9]', date):
            continue
        if re.match('[0-2][0-9]:[0-5][0-9]:[0-5][0-9]', date):
            continue
        legal = False

    if not legal:
        window.error_message('Please input time in this format:\n xx:xx:xx')
    else:
        for i in range(4):
            if dates[i]:
                dates[i] = '2019/08/30 ' + dates[i]
        search_list[1] = dates[0] + '-' + dates[1]
        search_list[4] = dates[2] + '-' + dates[3]
        del search_list[2]
        del search_list[4]
        if search_list[-1]:
            search_list[-1] = 'Y' if search_list[-1] == 'Yes' else 'N'
        search_result = search.Search(data.sheet, search_list)
        sort_list = [window.vt.order.get(), window.dto.order.get(), window.gido.order.get(),\
                     window.dtd.order.get(), window.gidd.order.get(), window.triplen.order.get()]
        sort_result = sort.sort(search_result, sort_list)
        if not sort_result.shape[0]:
            window.no_result()
        else:
            window.show_result(sort_result)




if __name__ == '__main__':
    data = model.Sheet()
    vehicle_type = data.get_vehichle_type()
    gantry_o = data.get_gantry_id_o()
    gantry_d = data.get_gantry_id_d()
    window = gui.GUI(vehicle_type + [''], gantry_o + [''], gantry_d + [''])
    window.begin.config(command=check_legality)
    window.vt.check.config(command=check_order1)
    window.dto.check.config(command=check_order2)
    window.gido.check.config(command=check_order3)
    window.dtd.check.config(command=check_order4)
    window.gidd.check.config(command=check_order5)
    window.triplen.check.config(command=check_order6)
    window.root_window.mainloop()