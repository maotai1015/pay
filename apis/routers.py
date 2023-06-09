from apis.api import SuppliesOpt, UserRegistration, Login, TokenRefresh, RecordOpt
from app.app import api_restful

api_restful.add_resource(SuppliesOpt, '/supply')    # 物品管理  get查询   put编辑  post新加 delete删除
api_restful.add_resource(UserRegistration, '/register')     # 注册
api_restful.add_resource(Login, '/login')       # 登陆
api_restful.add_resource(TokenRefresh, '/tokenRefresh')     # 刷新token
api_restful.add_resource(RecordOpt, '/opt')     # 出入库操作


