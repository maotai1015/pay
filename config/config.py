import os
from datetime import timedelta

ENV = os.environ.get('ENV')


class BaseConfig:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    basedir = os.path.abspath(os.path.dirname(__file__))

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 防止超时无操作导致连接失效
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True, 'pool_recycle': 120, 'pool_size': 20}

    DB_CREATEALL = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'mysql+pymysql://{self.user}:{self.password}@{self.address}:{self.port}/{self.database}'


# 本地测试
class LocalConfig(BaseConfig):
    user = 'root'
    password = '20220620'
    database = 'tong'
    address = "124.221.75.228"
    port = 3306
    DB_CREATEALL = True


# 正式环境
class ProConfig(BaseConfig):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = '20220620'
    database = 'tong'
    address = "124.221.75.228"
    port = 3306

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False

    # 禁止自动提交数据处理
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False


configs = {
    'local': LocalConfig(),
    'pro': ProConfig(),
}
config = configs.get(ENV or 'local')
