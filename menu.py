import sys

from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QMenu, QTextEdit, QMessageBox, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from windows import BackupWindow, RestoreWindow, StructBackupWindow, DataBackupWindow, SingleBackupWindow, \
    RemoteBackupWindow, ServerConfWindow, AddPgpassWindow, DelPgpassWindow
import settings
from utils.common import get_local_pgpass, get_remote_pgpass


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_init()

    def ui_init(self):
        menubar = self.menuBar()

        self.text_widget = QTextEdit()
        self.text_widget.setReadOnly(True)
        font = QFont()
        font.setPointSize(14)
        self.text_widget.setFont(font)
        self.setCentralWidget(self.text_widget)

        # 配置菜单
        configure_menu = menubar.addMenu("配置")
        self.configure_menu_init(menu=configure_menu)

        # 运行菜单
        run_menu = menubar.addMenu("运行")
        self.run_menu_init(menu=run_menu)

        self.resize(700, 500)
        self._center()
        self.setWindowTitle('postgresql数据库备份工具')
        self.show()

    def configure_menu_init(self, menu):
        remote_server_menu = QMenu("远程服务器", self)
        menu.addMenu(remote_server_menu)
        checkAct = QAction("查看", self)
        checkAct.triggered.connect(self.show_remote_server)
        remote_server_menu.addAction(checkAct)

        configureAct = QAction("配置", self)
        configureAct.triggered.connect(self.config_remote_server)
        remote_server_menu.addAction(configureAct)

        menu.addSeparator()

        local_pgpass_menu = QMenu("本地pgpass", self)
        menu.addMenu(local_pgpass_menu)
        checkAct = QAction("查看", self)
        checkAct.triggered.connect(lambda: self.show_pgpass(is_remote=False))
        local_pgpass_menu.addAction(checkAct)

        addAct = QAction("添加", self)
        addAct.triggered.connect(lambda: self.add_pgpass(is_remote=False))
        local_pgpass_menu.addAction(addAct)

        delAct = QAction("删除", self)
        delAct.triggered.connect(lambda: self.del_pgpass(is_remote=False))
        local_pgpass_menu.addAction(delAct)

        remote_pgpass_menu = QMenu("远程pgpass", self)
        menu.addMenu(remote_pgpass_menu)
        checkAct = QAction("查看", self)
        checkAct.triggered.connect(lambda: self.show_pgpass(is_remote=True))
        remote_pgpass_menu.addAction(checkAct)

        addAct = QAction("添加", self)
        addAct.triggered.connect(lambda: self.add_pgpass(is_remote=True))
        remote_pgpass_menu.addAction(addAct)

        delAct = QAction("删除", self)
        delAct.triggered.connect(lambda: self.del_pgpass(is_remote=True))
        remote_pgpass_menu.addAction(delAct)

    def run_menu_init(self, menu):
        backupAct = QAction("数据库备份", self)
        backupAct.triggered.connect(self.db_backup)
        menu.addAction(backupAct)

        restoreAct = QAction("数据库恢复", self)
        restoreAct.triggered.connect(self.db_restore)
        menu.addAction(restoreAct)

        menu.addSeparator()

        remoteBkAct = QAction("远程备份", self)
        remoteBkAct.triggered.connect(self.remote_backup)
        menu.addAction(remoteBkAct)

        menu.addSeparator()

        structAct = QAction("结构备份", self)
        structAct.triggered.connect(self.db_struct_backup)
        menu.addAction(structAct)

        datasAct = QAction("数据备份", self)
        datasAct.triggered.connect(self.db_data_backup)
        menu.addAction(datasAct)

        menu.addSeparator()

        tableMenu = QMenu("单表备份", self)
        menu.addMenu(tableMenu)

        tableAct = QAction("表备份", self)
        tableAct.triggered.connect(self.table_backup)
        tableMenu.addAction(tableAct)

        tableStructAct = QAction("结构备份", self)
        tableStructAct.triggered.connect(self.table_struct_backup)
        tableMenu.addAction(tableStructAct)

        tableDataAct = QAction("数据备份", self)
        tableDataAct.triggered.connect(self.table_data_bcakup)
        tableMenu.addAction(tableDataAct)

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_remote_server(self):
        '''显示远程服务器'''
        host = f"主机: {settings.REMOTE_HOST}"
        port = f"端口: {settings.REMOTE_PORT}"
        user = f"用户名: {settings.REMOTE_USER}"
        password = f"密码: {settings.REMOTE_PASSWORD}"
        text = "\n".join([host, port, user, password])
        self.text_widget.setText(text)

    def config_remote_server(self):
        '''配置远程服务器'''
        try:
            self.remoteSvrConfUI = ServerConfWindow()
            self.remoteSvrConfUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def show_pgpass(self, is_remote=False):
        '''显示pgpass文件'''
        try:
            if is_remote:
                result = get_remote_pgpass()
            else:
                result = get_local_pgpass()

            if result.status:
                self.text_widget.setText(result.msg)
            else:
                QMessageBox.warning(self, "warning", result.msg)
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def add_pgpass(self, is_remote=False):
        '''添加pgpass记录'''
        try:
            self.addPgpassUI = AddPgpassWindow(is_remote=is_remote)
            self.addPgpassUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def del_pgpass(self, is_remote=False):
        '''删除pgpass记录'''
        try:
            self.delPgpassUI = DelPgpassWindow(is_remote=is_remote)
            self.delPgpassUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def db_backup(self):
        '''数据库备份'''
        try:
            self.bkUI = BackupWindow()
            self.bkUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def db_restore(self):
        '''数据库恢复'''
        try:
            self.restoreUI = RestoreWindow()
            self.restoreUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def remote_backup(self):
        '''远程备份'''
        try:
            self.remoteBkUI = RemoteBackupWindow()
            self.remoteBkUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def db_struct_backup(self):
        '''数据库结构备份'''
        try:
            self.structBkUI = StructBackupWindow()
            self.structBkUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def db_data_backup(self):
        '''数据库数据备份'''
        try:
            self.dataBkUI = DataBackupWindow()
            self.dataBkUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def table_backup(self):
        '''数据库表备份'''
        try:
            self.tableBkUI = SingleBackupWindow(operation="all")
            self.tableBkUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def table_struct_backup(self):
        '''数据库表结构备份'''
        try:
            self.tableStructBkUI = SingleBackupWindow(operation="struct")
            self.tableStructBkUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def table_data_bcakup(self):
        '''数据库表数据备份'''
        try:
            self.tableDataBkUI = SingleBackupWindow(operation="data")
            self.tableDataBkUI.show()
        except Exception as e:
            QMessageBox.warning(self, "warning", str(e))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    sys.exit(app.exec_())
