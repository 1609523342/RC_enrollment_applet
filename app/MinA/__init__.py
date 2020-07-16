from flask import Blueprint

MinAs = Blueprint('MinAs', __name__)
from app.MinA import information
from app.MinA import user
from app.MinA import switch

