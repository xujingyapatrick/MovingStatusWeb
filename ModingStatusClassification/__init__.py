import os
from flask import Flask

def create_app(cfg=None):
    app = Flask(__name__,static_url_path='')
#     load_config(app, cfg)
    from ModingStatusClassification.views import blah_bp
    app.register_blueprint(blah_bp)
    return app

