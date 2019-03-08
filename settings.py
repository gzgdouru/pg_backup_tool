#配置文件路径
CONFIG_FILE = "config.json"

#基本设置
BK_THREAD_NUM = 5  #并发线程数量

#默认的远程服务器配置
REMOTE_HOST = "127.0.0.1"
REMOTE_PORT = 22
REMOTE_USER = ""
REMOTE_PASSWORD = ""

#日志设置
LOG_NAME = "database_backup"
LOG_LEVEL = "INFO"
LOG_FORMATTER = "[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s"
