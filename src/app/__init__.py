from flask import Blueprint, Flask, render_template
from .routes import recommendation_bp
from .containers import Container

from ..client.ollama import Ollama
from ..context.context import USER_SENTIMENT

import pandas as pd

def create_app():
    app = Flask(__name__)

    cl = Ollama(USER_SENTIMENT)

    # Initialize container here
    container = Container()
    container.config.from_dict({
        'sentimentAnalyser': cl,
        "features": pd.read_csv("../Data/features.csv")
    })

    app.container = container

    # Register blueprints here
    app.register_blueprint(recommendation_bp)

    return app
