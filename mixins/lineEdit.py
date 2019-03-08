from PyQt5.QtWidgets import QLabel, QLineEdit

from utils.ui import build_lineEdit_widget


class PortLineEditMixin(object):
    '''创建port LineEdit部件'''

    def create_port_LineEdit(self, *args, **kwargs):
        label = kwargs.get("port_label", "端口:")
        port = kwargs.get("port", "5432")
        grid = self.get_grid()
        row = self.get_row()
        le = build_lineEdit_widget(grid=grid, lb_text=label, le_text=str(port), row=row)
        self.add_row()
        return le


class BkPathLineEditMixin(object):
    '''创建backup path LineEdit部件'''

    def create_BkPath_LineEdit(self, *args, **kwargs):
        label = kwargs.get("bk_path_label", "备份路径:")
        bk_path = kwargs.get("bk_path", ".")
        grid = self.get_grid()
        row = self.get_row()
        le = build_lineEdit_widget(grid=grid, lb_text=label, le_text=bk_path, row=row)
        self.add_row()
        return le


class DataPathLineEditMixin(object):
    '''创建data_path部件'''

    def create_DataPath_LineEdit(self, *args, **kwargs):
        label = kwargs.get("data_path_label", "数据路径:")
        data_path = kwargs.get("data_path", ".")
        grid = self.get_grid()
        row = self.get_row()
        le = build_lineEdit_widget(grid=grid, lb_text=label, le_text=data_path, row=row)
        self.add_row()
        return le


class TableLineEditMixin(object):
    '''创建table LineEdit部件'''

    def create_table_LineEdit(self, *args, **kwargs):
        label = kwargs.get("table_label", "数据表:")
        grid = self.get_grid()
        row = self.get_row()
        le = build_lineEdit_widget(grid=grid, lb_text=label, le_text="", row=row)
        self.add_row()
        return le


class UserLineEditMixin(object):
    '''创建user LineEdit部件'''

    def create_user_LineEdit(self, *args, **kwargs):
        label = kwargs.get("user_label", "用户名:")
        user = kwargs.get("user", "")
        grid = self.get_grid()
        row = self.get_row()
        le = build_lineEdit_widget(grid=grid, lb_text=label, le_text=user, row=row)
        self.add_row()
        return le


class PasswdLineEditMixin(object):
    '''创建password LineEdit部件'''

    def create_passwd_LineEdit(self, *args, **kwargs):
        label = kwargs.get("passwd_label", "密码:")
        password = kwargs.get("password", "")
        grid = self.get_grid()
        row = self.get_row()
        le = build_lineEdit_widget(grid=grid, lb_text=label, le_text=password, row=row)
        self.add_row()
        return le


class HostLineEditMixin(object):
    '''创建host LineEdit部件'''

    def create_host_LineEdit(self, *args, **kwargs):
        label = kwargs.get("host_label", "主机:")
        host = kwargs.get("host", "127.0.0.1")
        grid = self.get_grid()
        row = self.get_row()
        le = build_lineEdit_widget(grid=grid, lb_text=label, le_text=host, row=row)
        self.add_row()
        return le
