import paramiko

from utils.declare import Status


class RemoteServer:
    def __init__(self, host, port, user, password):
        self._host = host
        self._port = port
        self._user = user
        self._password = password

        self.init_server_connect()

    def init_server_connect(self):
        trans = paramiko.Transport((self._host, self._port))
        trans.connect(username=self._user, password=self._password)
        self.ssh = paramiko.SSHClient()
        self.ssh._transport = trans

    def check_dir(self, path):
        return self.exec_command(f"ls {path}")

    def exec_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        err = stderr.read()
        if err:
            return Status(status=False, msg=err)
        return Status(status=True, msg=stdout.read())

    def __del__(self):
        self.ssh.close()


if __name__ == "__main__":
    remote_server = RemoteServer("192.168.34.203", 22, "postgres", "postgres")
    result = remote_server.exec_command("pwd")
    print(result.msg)
