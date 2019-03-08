from PyQt5.QtWidgets import QLabel, QCheckBox

from configParser import get_db
from utils.ui import process_checked


class DbCheckBoxMixin(object):
    '''创建db CheckBox部件'''

    def create_db_CheckBox(self, *args, **kwargs):
        col = 0
        label = kwargs.get("db_label", "数据库:")
        lb = QLabel(label)
        self.add_widget(lb, col)
        col += 1

        dbs = get_db()
        ck_list = []
        for db in dbs:
            ck = QCheckBox(db)
            self.add_widget(ck, col)
            ck_list.append(ck)

            # 每行显示4个
            if col > 3:
                self.add_row()
                col = 1
            else:
                col += 1

        [ck.stateChanged.connect(lambda: process_checked(ck_list, self.dbs)) for ck in ck_list]
        self.add_row()
        return ck_list