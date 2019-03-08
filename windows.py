import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QGridLayout, QMessageBox

from backup import LocalBackup, RemoteBackup
from mixins.lineEdit import PortLineEditMixin, BkPathLineEditMixin, DataPathLineEditMixin, TableLineEditMixin, \
    UserLineEditMixin, PasswdLineEditMixin, HostLineEditMixin
from mixins.comboBox import HostComboxMixin, DbComboBoxMixin, PgpassComboBoxMinxin
from mixins.pushButton import CommitPushButtonMixin, CancelPushButtonMixin
from mixins.checkBox import DbCheckBoxMixin
from utils.common import add_local_pgpass, add_remote_pgpass, check_remote_server, set_remote_server, get_local_pgpass, \
    get_remote_pgpass, remove_local_pgpass, remove_remote_pgpass
import settings


class GenericsWindow(QWidget):
    def __init__(self, title, *args, **kwargs):
        super().__init__()
        self._row = 0
        self.tile = title
        self.dbs = set()
        self._grid_init(*args, **kwargs)

    def _grid_init(self, *args, **kwargs):
        '''布局初始化'''
        self._grid = QGridLayout()
        self._grid.setSpacing(10)
        self._ui_init(*args, **kwargs)
        self.setLayout(self._grid)
        self.setWindowTitle(self.tile)
        self._center()

    def _ui_init(self, *args, **kwargs):
        '''部件初始化'''
        self.cb_host = self.create_host_ComboBox(*args, **kwargs)
        self.le_host = self.create_host_LineEdit(*args, **kwargs)

        self.le_port = self.create_port_LineEdit(*args, **kwargs)

        self.ck_db = self.create_db_CheckBox(*args, **kwargs)
        self.cb_db = self.create_db_ComboBox(*args, **kwargs)

        self.le_table = self.create_table_LineEdit(*args, **kwargs)

        self.le_user = self.create_user_LineEdit(*args, **kwargs)
        self.le_passwd = self.create_passwd_LineEdit(*args, **kwargs)

        self.le_bk_path = self.create_BkPath_LineEdit(*args, **kwargs)
        self.le_data_path = self.create_DataPath_LineEdit(*args, **kwargs)

        self.cb_pgpass = self.create_pgpass_ComboBox(*args, **kwargs)

        self.bt_commit = self.create_commit_PushButton(*args, **kwargs)
        self.bt_cancel = self.create_cancel_PushButton(*args, **kwargs)

        self.after_init()

    def after_init(self):
        '''为部件添加一些额外的功能'''
        pass

    def add_widget(self, widget, col):
        self._grid.addWidget(widget, self._row, col)

    def add_row(self, num=1):
        self._row += num

    def get_grid(self):
        return self._grid

    def get_row(self):
        return self._row

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def commit(self):
        pass

    def cancel(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def create_host_ComboBox(self, *args, **kwargs):
        '''创建host ComboBox部件'''
        pass

    def create_port_LineEdit(self, *args, **kwargs):
        '''创建port LineEdit部件'''
        pass

    def create_db_CheckBox(self, *args, **kwargs):
        '''创建db CheckBox部件'''
        pass

    def create_BkPath_LineEdit(self, *args, **kwargs):
        '''创建bk_path LineEdit部件'''
        pass

    def create_commit_PushButton(self, *args, **kwargs):
        '''创建commit PushButton部件'''
        pass

    def create_DataPath_LineEdit(self, *args, **kwargs):
        '''创建data_path LineEdit部件'''
        pass

    def create_table_LineEdit(self, *args, **kwargs):
        '''创建table LineEdit部件'''
        pass

    def create_db_ComboBox(self, *args, **kwargs):
        '''创建db ComboBox部件'''
        pass

    def create_cancel_PushButton(self, *args, **kwargs):
        '''创建cancel PushButton部件'''
        pass

    def create_user_LineEdit(self, *args, **kwargs):
        '''创建user LineEdit部件'''
        pass

    def create_passwd_LineEdit(self, *args, **kwargs):
        '''创建password LineEdit部件'''
        pass

    def create_host_LineEdit(self, *args, **kwargs):
        '''创建host LineEdit部件'''
        pass

    def create_pgpass_ComboBox(self, *args, **kwargs):
        '''创建pgpass ComboBox部件'''
        pass


class BackupWindow(HostComboxMixin, PortLineEditMixin, DbCheckBoxMixin, BkPathLineEditMixin, CommitPushButtonMixin,
                   GenericsWindow):
    '''数据库备份窗口'''

    def __init__(self):
        super().__init__(title="数据库备份窗口")

    def commit(self):
        try:
            host = self.cb_host.currentText()
            port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()
            local_bk = LocalBackup(host, port, self.dbs, bk_path)
            local_bk.db_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class RestoreWindow(PortLineEditMixin, DbCheckBoxMixin, DataPathLineEditMixin, CommitPushButtonMixin, GenericsWindow):
    '''数据库恢复窗口'''

    def __init__(self):
        super().__init__(title="数据库恢复窗口")

    def commit(self):
        try:
            port = int(self.le_port.text())
            data_path = self.le_data_path.text()
            local_bk = LocalBackup("127.0.0.1", port, self.dbs)
            local_bk.db_restore(data_path)
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class StructBackupWindow(HostComboxMixin, PortLineEditMixin, DbCheckBoxMixin, BkPathLineEditMixin,
                         CommitPushButtonMixin, GenericsWindow):
    '''数据库结构备份窗口'''

    def __init__(self):
        super().__init__(title="数据库结构备份窗口")

    def commit(self):
        try:
            host = self.cb_host.currentText()
            port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()
            local_bk = LocalBackup(host, port, self.dbs, bk_path)
            local_bk.table_struct_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class DataBackupWindow(HostComboxMixin, PortLineEditMixin, DbCheckBoxMixin, BkPathLineEditMixin, CommitPushButtonMixin,
                       GenericsWindow):
    '''数据库数据备份窗口'''

    def __init__(self):
        super().__init__(title="数据库数据备份窗口")

    def commit(self):
        try:
            host = self.cb_host.currentText()
            port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()
            local_bk = LocalBackup(host, port, self.dbs, bk_path)
            local_bk.table_data_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class SingleBackupWindow(HostComboxMixin, PortLineEditMixin, DbComboBoxMixin, TableLineEditMixin, BkPathLineEditMixin,
                         CommitPushButtonMixin, GenericsWindow):
    '''数据库单表备份窗口'''

    def __init__(self, operation="all"):
        super().__init__(title="数据库单表备份窗口")
        self._operation = operation

    def commit(self):
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


class RemoteBackupWindow(HostComboxMixin, PortLineEditMixin, DbCheckBoxMixin, BkPathLineEditMixin,
                         CommitPushButtonMixin, GenericsWindow):
    '''数据库远程备份窗口'''

    def __init__(self):
        super().__init__(title="数据库远程备份窗口")

    def commit(self):
        try:
            result = check_remote_server()
            if not result.status:
                QMessageBox.warning(self, "warning", result.msg)
                return

            bk_host = self.cb_host.currentText()
            bk_port = int(self.le_port.text())
            bk_path = self.le_bk_path.text()

            remote_bk = RemoteBackup(bk_host, bk_port, self.dbs, bk_path)
            remote_bk.init_remove_server(settings.REMOTE_HOST, settings.REMOTE_PORT, settings.REMOTE_USER,
                                         settings.REMOTE_PASSWORD)
            remote_bk.db_backup()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class AddPgpassWindow(HostComboxMixin, PortLineEditMixin, DbComboBoxMixin, UserLineEditMixin, PasswdLineEditMixin,
                      CommitPushButtonMixin, GenericsWindow):
    '''pgpass配置文件窗口'''

    def __init__(self, is_remote):
        self._is_remote = is_remote
        super().__init__(title="pgpass配置文件窗口")

    def after_init(self):
        self.cb_db.insertItem(0, "*")

    def commit(self):
        try:
            db_host = self.cb_host.currentText()
            db_port = int(self.le_port.text())
            db = self.cb_db.currentText()
            db_user = self.le_user.text()
            db_passwd = self.le_passwd.text()
            pgpass = f"{db_host}:{db_port}:{db}:{db_user}:{db_passwd}"

            if self._is_remote:
                result = add_remote_pgpass(pgpass)
            else:
                result = add_local_pgpass(pgpass)

            if result.status:
                QMessageBox.about(None, "success", result.msg)
                self.close()
            else:
                QMessageBox.warning(None, "failed", result.msg)
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))


class ServerConfWindow(HostLineEditMixin, PortLineEditMixin, UserLineEditMixin, PasswdLineEditMixin,
                       CommitPushButtonMixin, CancelPushButtonMixin, GenericsWindow):
    '''远程服务器配置窗口'''

    def __init__(self):
        super().__init__(title="远程服务器配置窗口", host=settings.REMOTE_HOST, port=settings.REMOTE_PORT,
                         user=settings.REMOTE_USER, password=settings.REMOTE_PASSWORD)

    def commit(self):
        try:
            host = self.le_host.text()
            port = int(self.le_port.text())
            user = self.le_user.text()
            password = self.le_passwd.text()
            set_remote_server(host, port, user, password)
            QMessageBox.about(None, "success", "配置成功")
            self.close()
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))

    def cancel(self):
        self.close()


class DelPgpassWindow(PgpassComboBoxMinxin, CommitPushButtonMixin, CancelPushButtonMixin, GenericsWindow):
    '''pgpass记录删除窗口'''

    def __init__(self, is_remote=False):
        self._is_remote = is_remote
        if self._is_remote:
            result = get_remote_pgpass()
        else:
            result = get_local_pgpass()

        if not result.status:
            raise RuntimeError(result.msg)

        records = set([record.strip() for record in result.msg.split("\n") if record.strip()])
        super().__init__(title="pgpass记录删除窗口", commit_label="删除", pgpass_records=records)

    def commit(self):
        try:
            pgpass = self.cb_pgpass.currentText()
            if self._is_remote:
                result = remove_remote_pgpass(pgpass)
            else:
                result = remove_local_pgpass(pgpass)

            if result.status:
                QMessageBox.about(self, "success", "删除记录成功")
                self.close()
            else:
                QMessageBox.warning(self, "warning", f"删除记录失败, 原因:{result.msg}")
        except Exception as e:
            QMessageBox.warning(None, "warning", str(e))

    def cancel(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DelPgpassWindow(is_remote=True)
    ex.show()
    sys.exit(app.exec_())
