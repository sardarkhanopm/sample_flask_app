from celery import Celery, Task
import logging
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, FLASK_APP, FLASK_ENV
from flask import Flask
db = SQLAlchemy()

# Logging setup

logger = logging.getLogger(__name__)
logging_format = logging.Formatter(
    '[%(asctime)s] %(levelname)s %(filename)s:%(lineno)s %(funcName)s: %(message)s')
file_handler = logging.handlers.TimedRotatingFileHandler(
    'logs/app.log', backupCount=5, when='midnight')
file_handler.setFormatter(logging_format)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def create_app() -> Flask:
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="amqp://guest@localhost//",
            task_ignore_result=True,
            include="app.tasks",
            queue="long_running_queue"
        ),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['FLASK_APP'] = FLASK_APP
    app.config['FLASK_ENV'] = FLASK_ENV
    db.init_app(app)
    celery_init_app(app)
    with app.app_context():
        from . import views  # noqa
        db.create_all()
        return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask, broker="amqp://guest@localhost//",
                        include='app.tasks')
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
