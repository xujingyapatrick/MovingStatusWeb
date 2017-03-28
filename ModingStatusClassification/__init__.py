import os
from flask import Flask

def create_app(cfg=None):
    app = Flask(__name__)
#     load_config(app, cfg)
    from ModingStatusClassification.views import blah_bp
    app.register_blueprint(blah_bp)
    return app

