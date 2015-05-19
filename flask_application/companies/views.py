from flask import current_app, render_template

from flask_application.companies.controllers import CompanyView

app.add_url_rule('/companies/', view_func=CompanyView.as_view('company', template_name='company.html'))

