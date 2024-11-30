from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Activity

bp = Blueprint('carbon', __name__, url_prefix='/carbon')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('carbon/dashboard.html')
