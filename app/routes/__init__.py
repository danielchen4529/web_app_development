from flask import Flask

def register_routes(app: Flask):
    """
    註冊所有的 Flask Blueprints 路由到應用程式中
    """
    from .recipe import recipe_bp
    app.register_blueprint(recipe_bp)
