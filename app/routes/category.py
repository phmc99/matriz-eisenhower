from flask import Blueprint
from app.controllers.category import *

bp_category = Blueprint("category", __name__, url_prefix="/category")
bp_category.post("")(create_category)
bp_category.patch("/<int:category_id>")(update_category)
bp_category.delete("/<int:category_id>")(delete_category)