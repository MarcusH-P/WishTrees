from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from models import User, Donation, Security, SecurityError
from app import requires_roles, db_add_commit, db
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


def view_donations():
    return


@admin_blueprint.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('admin.html')


@admin_blueprint.route('/view_users', methods=['POST'])
@login_required
@requires_roles('admin')
def view_users():
    return render_template('admin.html', all_users=User.query.all())


@admin_blueprint.route('/view_security', methods=['POST'])
@login_required
@requires_roles('admin')
def view_security():
    return render_template('admin.html', all_events=Security.query.all())


@admin_blueprint.route('/view_donations', methods=['POST'])
@login_required
@requires_roles('admin')
def view_donations():
    return render_template('admin.html', all_donations=Donation.query.all())


@admin_blueprint.route('/delete_user', methods=['POST'])
@login_required
@requires_roles('admin')
def delete_user():
    email = request.form.get('email')
    user_to_go = User.query.filter_by(email=email).first()

    if user_to_go:
        db.session.delete(user_to_go)
        db.session.commit()
        flash('Success!')
    else:
        flash("User likely doesn't exist")
    return admin()


@admin_blueprint.route('/view_security_errors', methods=['POST'])
@login_required
@requires_roles('admin')
def view_security_errors():
    return render_template('admin.html', all_errors=SecurityError.query.all())


