import os
import subprocess
import tempfile
import getpass

from remote import RemoteServer
from utils.declare import Status
import settings


def exec_command(cmd):
    '''执行shell命令'''
    stderr_temp = tempfile.TemporaryFile()
    stdout_temp = tempfile.TemporaryFile()
    result = subprocess.Popen(cmd, stdout=stdout_temp.fileno(), stderr=stderr_temp.fileno(), shell=True)
    result.wait()

    stderr_temp.seek(0)
    stderr = stderr_temp.read()
    if stderr:
        return Status(status=False, msg=stderr.decode("gbk"))
    stdout_temp.seek(0)
    return Status(status=True, msg=stdout_temp.read().decode("gbk"))


def set_remote_server(host, port, user, password):
    settings.REMOTE_HOST = host
    settings.REMOTE_PORT = port
    settings.REMOTE_USER = user
    settings.REMOTE_PASSWORD = password


def check_remote_server():
    '''检查远程服务器配置'''
    if not settings.REMOTE_HOST or settings.REMOTE_HOST in ("localhost", "127.0.0.1"):
        return Status(status=False, msg="主机不能为空/localhost/127.0.0.0!")
    if not settings.REMOTE_PORT:
        return Status(status=False, msg="端口不能为空!")
    if not settings.REMOTE_USER:
        return Status(status=False, msg="用户名不能为空!")
    if not settings.REMOTE_PASSWORD:
        return Status(status=False, msg="密码不能为空!")
    return Status(status=True, msg="检查通过")


def check_pgpass(pgpass):
    '''检查pgpass记录是否合法'''
    pgpass = pgpass.strip()
    fields = pgpass.split(":")
    fields = [field for field in fields if field]
    if len(fields) != 5:
        return Status(status=False, msg="pgpass记录格式错误, 请参照以下格式[host:port:db:user:password]")
    return Status(status=True, msg="检查通过")


def get_local_pgpass():
    '''读取本地的pgpass记录'''
    user = getpass.getuser()
    file = f"C:/Users/{user}/AppData/Roaming/postgresql/pgpass.conf"
    if not os.path.exists(file):
        return Status(status=False, msg="pgpass文件不存在!")

    records = set([line.strip() for line in open(file, "r") if line.strip()])
    return Status(status=True, msg="\n".join(records))


def save_local_pgpass(records):
    '''写入记录到本地的pgpass文件'''
    user = getpass.getuser()
    file = f"C:/Users/{user}/AppData/Roaming/postgresql/pgpass.conf"

    # 添加pgpass记录
    with open(file, "w") as f:
        for record in records:
            f.write(f"{record}\n")
    return Status(status=True, msg="添加记录成功.")


def add_local_pgpass(pgpass):
    '''添加本地pgpass记录'''
    result = get_local_pgpass()
    if not result.status:
        return Status(status=False, msg="添加记录失败, 原因:{}".format(result.msg))

    records = set([record.strip() for record in result.msg.split("\n") if record.strip()])
    result = check_pgpass(pgpass)
    if not result.status:
        return Status(status=False, msg="添加记录失败, 原因:{}".format(result.msg))

    if pgpass in records:
        return Status(status=False, msg="添加记录失败, 原因:记录已存在")

    records.add(pgpass)
    result = save_local_pgpass(records)
    if not result:
        return Status(status=False, msg="添加记录失败, 原因:{}".format(result.msg))
    else:
        return Status(status=True, msg="添加记录成功")


def remove_local_pgpass(pgpass):
    '''删除本地pgpass记录'''
    result = get_local_pgpass()
    if not result:
        return Status(status=False, msg="删除记录失败, 原因:{}".format(result.msg))

    pgpass = pgpass.strip()
    records = set(result.msg.split("\n"))
    if pgpass in records:
        records.remove(pgpass)
        user = getpass.getuser()
        file = f"C:/Users/{user}/AppData/Roaming/postgresql/pgpass.conf"
        with open(file, "w") as f:
            for record in records:
                f.write(f"{record}\n")
        return Status(status=True, msg="删除记录成功.")
    else:
        return Status(status=False, msg="删除记录失败, 原因:记录不存在!")


def get_remote_pgpass():
    '''读取远程服务器记录'''
    result = check_remote_server()
    if not result.status:
        return result

    server = RemoteServer(settings.REMOTE_HOST, settings.REMOTE_PORT, settings.REMOTE_USER, settings.REMOTE_PASSWORD)
    result = server.exec_command("cat .pgpass")
    return Status(status=result.status, msg=result.msg)


def save_remote_pgpass(records):
    '''写入记录到远程pgpass文件'''
    result = check_remote_server()
    if not result.status:
        return result

    server = RemoteServer(settings.REMOTE_HOST, settings.REMOTE_PORT, settings.REMOTE_USER, settings.REMOTE_PASSWORD)
    content = "\n".join(records)
    result = server.exec_command(f"echo '{content}' > .pgpass")
    if not result.status:
        return Status(status=False, msg=result.msg)
    return Status(status=True, msg="添加记录成功.")


def add_remote_pgpass(pgpass):
    '''添加远程pgpass记录'''
    pgpass = pgpass.strip()

    result = check_remote_server()
    if not result.status:
        return Status(status=False, msg="添加记录失败, 原因:{}".format(result.msg))

    result = get_remote_pgpass()
    if not result.status:
        return Status(status=False, msg="添加记录失败, 原因:{}".format(result.msg))

    records = set([record.strip() for record in result.msg.split("\n") if record.strip()])
    result = check_pgpass(pgpass)
    if not result.status:
        return Status(status=False, msg="添加记录失败, 原因:{}".format(result.msg))

    if pgpass in records:
        return Status(status=False, msg="添加记录失败, 原因:记录已存在")

    records.add(pgpass)
    result = save_remote_pgpass(records)
    if not result.status:
        return Status(status=False, msg="添加记录失败, 原因:{}".format(result.msg))
    else:
        return Status(status=True, msg="添加记录成功")


def remove_remote_pgpass(pgpass):
    '''移除远程pgpass记录'''
    pgpass = pgpass.strip()

    result = check_remote_server()
    if not result.status:
        return Status(status=False, msg="删除记录失败, 原因:{}".format(result.msg))

    result = get_remote_pgpass()
    if not result.status:
        return Status(status=False, msg="删除记录失败, 原因:{}".format(result.msg))

    records = result.msg.split("\n")
    if pgpass not in records:
        return Status(status=False, msg="删除记录失败, 原因:记录不存在")

    records.remove(pgpass)
    result = save_remote_pgpass(records)
    if not result.status:
        return Status(status=False, msg="删除记录失败, 原因:{}".format(result.msg))
    else:
        return Status(status=True, msg="删除记录成功")


if __name__ == "__main__":
    pgpass = "127.0.0.1:5432:ouru:ouru:5201314ouru11"
    # set_remote_server("192.168.34.203", 22, "postgres", "postgres")
    print(add_local_pgpass(pgpass))
