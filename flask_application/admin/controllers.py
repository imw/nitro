from flask import Blueprint, current_app

from flask.ext.security import login_required

from flask_application.controllers import TemplateView

admin = Blueprint('admin', __name__, url_prefix='/admin')


class AdminView(TemplateView):
    blueprint = admin
    route = '/'
    route_name = 'admin'
    template_name = 'admin/admin.html'
    decorators = [login_required]
#    decorators = [roles_required('admin')]

    def get_context_data(self, *args, **kwargs):
        return {
            'content': 'This is the Admin Page'
        }
