from flask import Blueprint,render_template
from flask_login import current_user, login_required
from models import User
admin = Blueprint('admin', __name__, template_folder='templates')


def view_donations():



@admin.route('/view_all_users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_all_users():
        return render_template('admin.html', name=current_user.firstname,
                               current_users=User.query.filter_by(role='user').all())
