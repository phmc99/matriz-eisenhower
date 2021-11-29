from flask import Blueprint
from app.routes.category import bp_category
from app.routes.task import bp_task
from app.controllers.task_category import get_all

            
bp_api = Blueprint("bp_api", __name__, url_prefix="/api")
bp_api.register_blueprint(bp_category)
bp_api.register_blueprint(bp_task)
bp_api.get("")(get_all)