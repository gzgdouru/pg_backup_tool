import os
import getpass
from collections import namedtuple
import abc
from concurrent.futures import ThreadPoolExecutor, as_completed

from remote import RemoteServer
from core import get_logger
from utils.common import exec_command
import settings

logger = get_logger()
Pgpass = namedtuple("Pgpass", ["host", "port", "db", "user", "password"])


class DbBackup(metaclass=abc.ABCMeta):
    def __init__(self, host="127.0.0.1", port=5432, dbs=None, bk_path="."):
        self._host = host
        self._port = port
        self._dbs = dbs
        self._bk_path = f"{bk_path.strip('/')}/{host}"

    @abc.abstractmethod
    def make_bkdir(self):
        pass

    @abc.abstractmethod
    def check_pgpass(self):
        pass

    @abc.abstractmethod
    def db_backup(self):
        pass


class LocalBackup(DbBackup):
    def __init__(self, host="127.0.0.1", port=5432, dbs=None, bk_path="."):
        super().__init__(host, port, dbs, bk_path)
        self.make_bkdir()

    def make_bkdir(self):
        '''检查备份目录, 不存在时则创建'''
        if not os.path.exists(self._bk_path):
            os.makedirs(self._bk_path)

    def check_pgpass(self):
        '''检查需要备份的数据库是否配置到pgpass文件'''
        user = getpass.getuser()
        file = f"C:/Users/{user}/AppData/Roaming/postgresql/pgpass.conf"
        if not os.path.exists(file):
            logger.error(f"文件[{file}]不存在!")
            return False
        records = open(file, "r").read()
        dbs = set()

        for line in records.split("\n"):
            if not line:
                continue
            pgpass = Pgpass(*line.split(":"))
            if self._host == pgpass.host and self._port == int(pgpass.port) and "postgres" == pgpass.user:
                dbs.add(pgpass.db)

        if "*" in dbs:
            return True

        results = [db in dbs for db in self._dbs]
        return all(results)

    def single_db_backup(self, db_name):
        '''备份单个数据库'''
        cmd = f"pg_dump -h {self._host} -p {self._port} -U postgres -c {db_name} | gzip > {self._bk_path}/{db_name}.gz"
        logger.info(f"备份数据库[{db_name}]开始, 请等待完成...")
        result = exec_command(cmd)
        if not result.status:
            logger.error(result.msg)
        else:
            logger.info(f"备份数据库[{db_name}]成功.")

    def single_db_data_backup(self, db_name):
        '''备份单个数据库中的数据'''
        cmd = f"pg_dump -h {self._host} -p {self._port} -U postgres -a {db_name} > {self._bk_path}/{db_name}_data.sql"
        logger.info(f"备份数据库[{db_name}]数据开始, 请等待完成...")
        result = exec_command(cmd)
        if not result.status:
            logger.error(result.msg)
        else:
            logger.info(f"备份数据库[{db_name}]数据成功.")

    def db_backup(self):
        '''数据库备份'''
        if not self._dbs:
            logger.error("请选择需要进行备份的数据库!")
            return

        # 检查pgpass文件配置
        if not self.check_pgpass():
            logger.error("请检查pgpass文件, 确保需要备份的数据库已配置到了pgpass文件")
            return

        logger.info(f"开始进行数据库{self._dbs}备份, 请等到完成...")
        with ThreadPoolExecutor(max_workers=settings.BK_THREAD_NUM) as executor:
            tasks = [executor.submit(self.single_db_backup, db) for db in self._dbs]
            for task in as_completed(tasks):
                exception = task.exception()
                if exception:
                    logger.error(exception)
        logger.info("数据库备份已全部完毕.")

    def db_restore(self, path):
        '''数据库恢复(慎用, 未通过测试)'''
        if not self._dbs:
            logger.error("请选择需要进行恢复的数据库!")
            return

        # 检查pgpass文件配置
        if not self.check_pgpass():
            logger.error("请检查pgpass文件, 确保需要备份的数据库已配置到了pgpass文件!")
            return

        # 恢复前检查
        if not self.restore_check(path):
            logger.error("请检查数据目录, 确保需要恢复的数据库对应的文件都存在!")
            return False

        logger.info(f"开始进行数据库{self._dbs}恢复, 请等到完成...")
        for loop in self._dbs:
            cmd = f"cat {path}/{loop}.gz | gunzip | psql -p {self._port} -h {self._host} -U postgres {loop}"
            result = exec_command(cmd)
            if not result.status:
                logger.error(result.msg)
        logger.info("数据库恢复完成.")

    def restore_check(self, path):
        '''数据库恢复检查'''
        if not os.path.exists(path):
            logger.error(f"数据目录:{path}不存在!")
            return False

        for db in self._dbs:
            file = os.path.join(path, f"{db}.gz")
            if not os.path.exists(file):
                logger.error(f"文件:{file}不存在!")
                return False
        return True

    def table_data_backup(self):
        '''表数据备份'''
        if not self._dbs:
            logger.error("请选择需要进行表数据备份的数据库!")
            return

        # 检查pgpass文件配置
        if not self.check_pgpass():
            logger.error("请检查pgpass文件, 确保需要备份的数据库已配置到了pgpass文件")
            return

        logger.info(f"开始进行数据库{self._dbs}表数据备份, 请等待完成...")
        with ThreadPoolExecutor(max_workers=settings.BK_THREAD_NUM) as executor:
            tasks = [executor.submit(self.single_db_data_backup, db) for db in self._dbs]
            for task in as_completed(tasks):
                exception = task.exception()
                if exception:
                    logger.error(exception)
        logger.info("数据库数据备份已完成.")

    def table_struct_backup(self):
        '''表结构备份'''
        if not self._dbs:
            logger.error("请选择需要进行表结构备份的数据库!")
            return

        # 检查pgpass文件配置
        if not self.check_pgpass():
            logger.error("请检查pgpass文件, 确保需要备份的数据库已配置到了pgpass文件")
            return

        logger.info(f"开始进行数据库[{self._dbs}]表结构备份, 请等待完成...")
        for loop in self._dbs:
            cmd = f"pg_dump -p {self._port} -h {self._host} -U postgres -s {loop} > {self._bk_path}/{loop}_struct.sql"
            result = exec_command(cmd)
            if not result.status:
                logger.error(result.msg)
            else:
                logger.info(f"备份数据库[{loop}]表结构成功.")
        logger.info("备份数据库表结构已完成")

    def single_table_backup(self, db, table, operation):
        '''单表备份'''
        if not db:
            logger.error("请选择需要单表备份的数据库!")
            return

        if not table:
            logger.error("请选择需要单表备份的数据表!")
            return

        if not operation:
            logger.error("请选择需要单表备份的操作!")
            return

        # 检查pgpass文件配置
        if not self.check_pgpass():
            logger.error("请检查pgpass文件, 确保需要备份的数据库已配置到了pgpass文件")
            return

        logger.info(f"开始进行数据库[{db}]的[{table}]表备份, 请等待完成...")
        if operation == "data":
            cmd = f"pg_dump -p {self._port} -h {self._host} -U postgres -t {table} -a {db}> {self._bk_path}/{table}_data.sql"
        elif operation == "struct":
            cmd = f"pg_dump -p {self._port} -h {self._host} -U postgres -t {table} -s {db}> {self._bk_path}/{table}_struct.sql"
        elif operation == "all":
            cmd = f"pg_dump -p {self._port} -h {self._host} -U postgres -t {table} {db}> {self._bk_path}/{table}.sql"
        else:
            logger.error(f"不支持的操作:{operation}")
            return

        result = exec_command(cmd)
        if not result.status:
            logger.error(result.msg)
        else:
            logger.info(f"备份数据库[{db}]的[{table}]成功.")


class RemoteBackup(DbBackup):
    def __init__(self, host, port, dbs, bk_path="."):
        super().__init__(host, port, dbs, bk_path)
        self._remote_server = None

    def init_remove_server(self, host, port, user, password):
        self._remote_server = RemoteServer(host, port, user, password)

    def make_bkdir(self):
        '''创建备份目录'''
        if not self._remote_server:
            logger.error("请先设置远程服务器!")
            return

        result = self._remote_server.check_dir(self._bk_path)
        if not result.status:
            self._remote_server.exec_command(f"mkdir -p {self._bk_path}")

    def check_pgpass(self):
        '''检查pgpass配置文件'''
        if not self._remote_server:
            logger.error("请先设置远程服务器!")
            return False

        result = self._remote_server.exec_command(f"cat .pgpass")
        if not result.status:
            logger.error(result.msg)
            return False

        dbs = set()
        for line in result.msg.split("\n"):
            if not line:
                continue
            pgpass = Pgpass(*line.split(":"))
            if self._host == pgpass.host and self._port == int(pgpass.port) and "postgres" == pgpass.user:
                dbs.add(pgpass.db)

        if "*" in dbs:
            return True

        results = [db in dbs for db in self._dbs]
        return all(results)

    def _single_db_backup(self, db_name):
        '''单个数据库备份'''
        logger.info(f"开始备份数据库[{db_name}], 请等待完成...")
        cmd = f"pg_dump -h {self._host} -p {self._port} -U postgres -c {db_name} | gzip > {self._bk_path}/{db_name}.gz"
        result = self._remote_server.exec_command(cmd)
        if not result.status:
            logger.error(result.msg)
        else:
            logger.info(f"数据库[{db_name}]备份完成.")

    def db_backup(self):
        '''数据库备份'''
        if not self._dbs:
            logger.error("请选择需要进行表结构备份的数据库!")
            return

        if not self._remote_server:
            logger.error("请先设置远程服务器!")
            return

        if not self.check_pgpass():
            logger.error("请检查.pgpass文件, 确保需要备份的数据库都配置到了.pgpass文件!")
            return

        self.make_bkdir()
        logger.info(f"开始对数据库{self._dbs}进行备份, 请等到完成...")
        with ThreadPoolExecutor(max_workers=settings.BK_THREAD_NUM) as executor:
            tasks = [executor.submit(self._single_db_backup, db) for db in self._dbs]
            for task in as_completed(tasks):
                err = task.exception()
                if err:
                    logger.error(err)
        logger.info("数据库备份已全部完毕.")


if __name__ == "__main__":
    local_bk = LocalBackup(host="127.0.0.1", port=5432, dbs=["ouru", "postgres"])
    local_bk.single_table_backup("ouru", "test", "all2")

    # remote_bk = RemoteBackup(host="127.0.0.1", port=5432, dbs=["rtsp", "rtp"])
    # remote_bk.init_remove_server("172.16.33.6", 22, "postgres", "postgres")
    # remote_bk.db_backup()
