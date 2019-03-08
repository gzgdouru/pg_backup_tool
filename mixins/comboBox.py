from PyQt5.QtWidgets import QLabel, QComboBox

from configParser import get_host, get_db
from utils.ui import build_widget_items


class HostComboxMixin(object):
    '''创建host ComboBox部件'''

    def create_host_ComboBox(self, *args, **kwargs):
        label = kwargs.get("host_label", "主机:")
        lb = QLabel(label)
        self.add_widget(lb, 0)

        hosts = get_host()
        cb = QComboBox()
        build_widget_items(cb, hosts)
        self.add_widget(cb, 1)

        self.add_row()
        return cb


class DbComboBoxMixin(object):
    '''创建db CommoBox部件'''

    def create_db_ComboBox(self, *args, **kwargs):
        label = kwargs.get("db_label", "数据库")
        ld = QLabel(label)
        self.add_widget(ld, 0)

        dbs = get_db()
        cb = QComboBox()
        build_widget_items(cb, dbs)
        self.add_widget(cb, 1)

        self.add_row()
        return cb


class PgpassComboBoxMinxin(object):
    '''创建pgpass ComboBox部件'''

    def create_pgpass_ComboBox(self, *args, **kwargs):
        label = kwargs.get("pgpass_label", "pgpass记录")
        ld = QLabel(label)
        self.add_widget(ld, 0)

        cb = QComboBox()
        records = kwargs.get("pgpass_records", [])
        build_widget_items(cb, records)
        self.add_widget(cb, 1)

        self.add_row()
        return cb
