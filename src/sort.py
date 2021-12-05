# -*- coding: utf-8 -*-
# Author    : Cynthia Guan
# Create    : 12/05/2021  03:33:36
# Final Edit: 12/05/2021  03:33:36
# Software: PyCharm


def sort(data, sortlist):
    sort_columns = []
    ascending = []
    for i in range(6):
        if sortlist[i]:
            sort_columns.append(i)
            if sortlist[i] == 'Ascending':
                ascending.append(True)
            else:
                ascending.append(False)
    if not sort_columns:
        return data

    sort_result = data.sort_values(by=sort_columns, ascending=ascending)
    return sort_result
