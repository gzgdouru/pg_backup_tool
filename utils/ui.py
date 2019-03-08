from PyQt5.QtWidgets import QCheckBox, QLabel, QLineEdit


def build_widget(grid, widget_class, text, row, col):
    '''创建常规部件'''
    widget = widget_class(text) if text else widget_class()
    grid.addWidget(widget, row, col)
    return widget


def build_lineEdit_widget(grid, lb_text, le_text, row):
    '''创建常规LineEdit'''
    build_widget(grid=grid, widget_class=QLabel, text=lb_text, row=row, col=0)
    le = build_widget(grid=grid, widget_class=QLineEdit, text=le_text, row=row, col=1)
    return le


def build_checkbox_widget(grid, row, col, items):
    '''创建check box部件'''
    ck_list = []
    for item in items:
        ck = QCheckBox(item)
        grid.addWidget(ck, row, col)
        ck_list.append(ck)
        col += 1
        if col > 3:
            row += 1
            col = 1
    return row, ck_list


def build_widget_items(widget, items):
    '''创建部件选项'''
    index = 0
    for item in items:
        widget.insertItem(index, item)
        index += 1


def process_checked(all_ck, items):
    '''check box按钮点击处理'''
    for ck in all_ck:
        item = ck.text()
        if ck.isChecked():
            if item not in items:
                items.add(item)
        else:
            if item in items:
                items.remove(item)


if __name__ == "__main__":
    pass
