from flask import Flask

def create_app():
    app = Flask(__name__)
    from .routes import main  # ✅ import your Blueprint
    app.register_blueprint(main)  # ✅ register it
    return app
