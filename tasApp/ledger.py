from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tasApp.auth import login_required
from tasApp.db import get_db

bp = Blueprint('ledger', __name__)

@bp.route('/')
def index():
    template('index.html')