import sys
import abc

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, QGridLayout
from PyQt5.QtWidgets import QPushButton, QTextEdit, QComboBox, QMessageBox, QMainWindow
from PyQt5.QtGui import QTextCursor

from backup import LocalBackup, RemoteBackup
from utils.ui import build_widget, build_widget_items, build_checkbox_widget, process_checked
from utils.common import write_local_pgpass, write_remote_pgpass
from configParser import get_host, get_db
import settings


class BaseWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.ui_init()
        self.setLayout(self.grid)
        self.setWindowTitle(title)
        self._center()

    def ui_init(self):
        pass

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class BackupWindow(BaseWindow):
    '''数据库备份窗口'''

    def __init__(self):
        super().__init__(title="backup")
        self.dbs = set()

    def ui_init(self):
        row = 0

        # 创建host部件
        build_widget(grid=self.grid, widget_class=QLabel, text="host:", row=row, col=0)
        self.cb_host = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        hosts = get_host()
        build_widget_items(self.cb_host, hosts)
        row += 1

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text="5432", row=row, col=1)
        row += 1

        # 创建db部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db:", row=row, col=0)
        dbs = get_db()
        row, ck_db = build_checkbox_widget(grid=self.grid, row=row, col=1, items=dbs)
        [ck.stateChanged.connect(lambda: process_checked(ck_db, self.dbs)) for ck in ck_db]
        row += 1

        # 创建bk_path部件
        build_widget(grid=self.grid, widget_class=QLabel, text="bk_path:", row=row, col=0)
        self.le_bk_path = build_widget(grid=self.grid, widget_class=QLineEdit, text=".", row=row, col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

    def _commit(self):
        try:
            host = self.cb_host.currentText()
            port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()
            local_bk = LocalBackup(host, port, self.dbs, bk_path)
            local_bk.db_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class RestoreWindow(BaseWindow):
    '''数据库恢复窗口'''

    def __init__(self):
        super().__init__(title="restore")
        self.dbs = set()

    def ui_init(self):
        row = 0

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text="5432", row=row, col=1)
        row += 1

        # 创建db部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db:", row=row, col=0)
        dbs = get_db()
        row, ck_db = build_checkbox_widget(grid=self.grid, row=row, col=1, items=dbs)
        [ck.stateChanged.connect(lambda: process_checked(ck_db, self.dbs)) for ck in ck_db]
        row += 1

        # 创建data path部件
        build_widget(grid=self.grid, widget_class=QLabel, text="data path:", row=row, col=0)
        self.le_data_path = build_widget(grid=self.grid, widget_class=QLineEdit, text=".", row=row, col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

    def _commit(self):
        try:
            port = int(self.le_port.text())
            data_path = self.le_data_path.text()
            local_bk = LocalBackup("127.0.0.1", port, self.dbs)
            local_bk.db_restore(data_path)
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class StructBackupWindow(BaseWindow):
    '''数据库结构备份窗口'''

    def __init__(self):
        super().__init__(title="struct backup")
        self._dbs = set()

    def ui_init(self):
        row = 0

        # 创建host部件
        build_widget(grid=self.grid, widget_class=QLabel, text="host:", row=row, col=0)
        hosts = get_host()
        self.cb_host = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        build_widget_items(self.cb_host, hosts)
        row += 1

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text="5432", row=row, col=1)
        row += 1

        # 创建db部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db:", row=row, col=0)
        dbs = get_db()
        row, ck_db = build_checkbox_widget(grid=self.grid, row=row, col=1, items=dbs)
        [ck.stateChanged.connect(lambda: process_checked(ck_db, self._dbs)) for ck in ck_db]
        row += 1

        # 创建bk_path部件
        build_widget(grid=self.grid, widget_class=QLabel, text="bk_path:", row=row, col=0)
        self.le_bk_path = build_widget(grid=self.grid, widget_class=QLineEdit, text=".", row=row, col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

    def _commit(self):
        try:
            host = self.cb_host.currentText()
            port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()
            local_bk = LocalBackup(host, port, self._dbs, bk_path)
            local_bk.table_struct_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class DataBackupWindow(BaseWindow):
    '''数据库数据备份窗口'''

    def __init__(self):
        super().__init__(title="data backup")
        self._dbs = set()

    def ui_init(self):
        row = 0

        # 创建host部件
        build_widget(grid=self.grid, widget_class=QLabel, text="host:", row=row, col=0)
        hosts = get_host()
        self.cb_host = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        build_widget_items(self.cb_host, hosts)
        row += 1

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text="5432", row=row, col=1)
        row += 1

        # 创建db部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db:", row=row, col=0)
        dbs = get_db()
        row, ck_db = build_checkbox_widget(grid=self.grid, row=row, col=1, items=dbs)
        [ck.stateChanged.connect(lambda: process_checked(ck_db, self._dbs)) for ck in ck_db]
        row += 1

        # 创建bk_path部件
        build_widget(grid=self.grid, widget_class=QLabel, text="bk_path:", row=row, col=0)
        self.le_bk_path = build_widget(grid=self.grid, widget_class=QLineEdit, text=".", row=row, col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

    def _commit(self):
        try:
            host = self.cb_host.currentText()
            port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()
            local_bk = LocalBackup(host, port, self._dbs, bk_path)
            local_bk.table_data_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class SingleBackupWindow(BaseWindow):
    '''单表备份窗口'''

    def __init__(self, operation="all"):
        super().__init__(title="single table backup")
        self._operation = operation

    def ui_init(self):
        row = 0

        # 创建host部件
        build_widget(grid=self.grid, widget_class=QLabel, text="host:", row=row, col=0)
        hosts = get_host()
        self.cb_host = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        build_widget_items(self.cb_host, hosts)
        row += 1

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text="5432", row=row, col=1)
        row += 1

        # 创建db部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db:", row=row, col=0)
        dbs = get_db()
        self.cb_db = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        build_widget_items(self.cb_db, dbs)
        row += 1

        # 创建table部件
        build_widget(grid=self.grid, widget_class=QLabel, text="table:", row=row, col=0)
        self.le_table = build_widget(grid=self.grid, widget_class=QLineEdit, text="", row=row, col=1)
        row += 1

        # 创建bk_path部件
        build_widget(grid=self.grid, widget_class=QLabel, text="bk_path:", row=row, col=0)
        self.le_bk_path = build_widget(grid=self.grid, widget_class=QLineEdit, text=".", row=row, col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

    def _commit(self):
        try:
            host = self.cb_host.currentText()
            port = int(self.le_port.text())
            db = self.cb_db.currentText()
            table = self.le_table.text()
            bk_path = self.le_bk_path.text()
            local_bk = LocalBackup(host, port, [db], bk_path=bk_path)
            local_bk.single_table_backup(db, table, self._operation)
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class RemoteBkWindow(BaseWindow):
    '''远程备份窗口'''

    def __init__(self, host, port, user, password):
        super().__init__(title="remote bakup")
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._dbs = set()

    def ui_init(self):
        row = 0

        # 创建host部件
        build_widget(grid=self.grid, widget_class=QLabel, text="host:", row=row, col=0)
        hosts = get_host()
        self.cb_host = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        build_widget_items(self.cb_host, hosts)
        row += 1

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text="5432", row=row, col=1)
        row += 1

        # 创建db部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db:", row=row, col=0)
        dbs = get_db()
        row, ck_db = build_checkbox_widget(grid=self.grid, row=row, col=1, items=dbs)
        [ck.stateChanged.connect(lambda: process_checked(ck_db, self._dbs)) for ck in ck_db]
        row += 1

        # 创建bk_path部件
        build_widget(grid=self.grid, widget_class=QLabel, text="bk_path:", row=row, col=0)
        self.le_bk_path = build_widget(grid=self.grid, widget_class=QLineEdit, text=".", row=row, col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

    def _commit(self):
        try:
            bk_host = self.cb_host.currentText()
            bk_port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()
            remote_bk = RemoteBackup(bk_host, bk_port, self._dbs, bk_path)
            remote_bk.init_remove_server(self._host, self._port, self._user, self._password)
            remote_bk.db_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class PgpassWindow(BaseWindow):
    '''pgpass配置文件窗口'''

    def __init__(self, host="", port=0, user="", password=""):
        super().__init__(title="pgpass配置文件窗口")
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    def ui_init(self):
        row = 0

        # 创建host部件
        build_widget(grid=self.grid, widget_class=QLabel, text="host:", row=row, col=0)
        hosts = get_host()
        self.cb_host = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        build_widget_items(self.cb_host, hosts)
        row += 1

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text="5432", row=row, col=1)
        row += 1

        # 创建db部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db:", row=row, col=0)
        dbs = get_db()
        self.cb_db = build_widget(grid=self.grid, widget_class=QComboBox, text="", row=row, col=1)
        build_widget_items(self.cb_db, dbs)
        self.cb_db.insertItem(0, "*")
        row += 1

        # 创建db_user部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db_user:", row=row, col=0)
        self.le_dbuser = build_widget(grid=self.grid, widget_class=QLineEdit, text="postgres", row=row, col=1)
        row += 1

        # 创建db_password部件
        build_widget(grid=self.grid, widget_class=QLabel, text="db_password", row=row, col=0)
        self.le_dbpasswd = build_widget(grid=self.grid, widget_class=QLineEdit, text="postgres", row=row, col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

    def _commit(self):
        try:
            db_host = self.cb_host.currentText()
            db_port = int(self.le_port.text())
            db = self.cb_db.currentText()
            db_user = self.le_dbuser.text()
            db_passwd = self.le_dbpasswd.text()
            pgpass = f"{db_host}:{db_port}:{db}:{db_user}:{db_passwd}"

            if self._host:
                result = write_remote_pgpass(self._host, self._port, self._user, self._password, pgpass)
            else:
                result = write_local_pgpass(pgpass)

            if result.status:
                QMessageBox.about(None, "success", result.msg)
                self.close()
            else:
                QMessageBox.warning(None, "failed", result.msg)
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class ServerConfWindow(BaseWindow):
    '''远程服务器配置窗口'''

    def __init__(self):
        super().__init__(title="远程服务器配置窗口")

    def ui_init(self):
        row = 0

        # 创建host部件
        build_widget(grid=self.grid, widget_class=QLabel, text="host:", row=row, col=0)
        self.le_host = build_widget(grid=self.grid, widget_class=QLineEdit, text=settings.REMOTE_HOST, row=row, col=1)
        row += 1

        # 创建port部件
        build_widget(grid=self.grid, widget_class=QLabel, text="port:", row=row, col=0)
        self.le_port = build_widget(grid=self.grid, widget_class=QLineEdit, text=str(settings.REMOTE_PORT), row=row,
                                    col=1)
        row += 1

        # 创建user部件
        build_widget(grid=self.grid, widget_class=QLabel, text="user:", row=row, col=0)
        self.le_user = build_widget(grid=self.grid, widget_class=QLineEdit, text=settings.REMOTE_USER, row=row, col=1)
        row += 1

        # 创建password部件
        build_widget(grid=self.grid, widget_class=QLabel, text="password:", row=row, col=0)
        self.le_passwd = build_widget(grid=self.grid, widget_class=QLineEdit, text=settings.REMOTE_PASSWORD, row=row,
                                      col=1)
        row += 1

        # 创建提交部件
        bt_commit = build_widget(grid=self.grid, widget_class=QPushButton, text="提交", row=row, col=0)
        bt_commit.clicked.connect(self._commit)

        # 创建取消部件
        bt_cancel = build_widget(grid=self.grid, widget_class=QPushButton, text="取消", row=row, col=1)
        bt_cancel.clicked.connect(self.close)

    def _commit(self):
        try:
            settings.REMOTE_HOST = self.le_host.text()
            settings.REMOTE_PORT = int(self.le_port.text())
            settings.REMOTE_USER = self.le_user.text()
            settings.REMOTE_PASSWORD = self.le_passwd.text()
            QMessageBox.about(None, "success", "配置成功")
            self.close()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ServerConfWindow()
    ex.show()
    sys.exit(app.exec_())
