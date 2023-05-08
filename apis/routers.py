from flask import Response

from apis import index
from app import app


# 健康检查
app.add_url_rule(
    '/hs', view_func=lambda: Response('OK', mimetype='text/plain')
)

# 首页
app.add_url_rule("/index", view_func=index, methods="GET")

