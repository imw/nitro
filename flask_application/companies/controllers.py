from flask import Blueprint, current_app, render_template

from flask.ext.security import login_required

from flask_application.controllers import TemplateView

companies = Blueprint('companies', __name__, url_prefix='/companies')


class CompanyView(TemplateView):
    blueprint = companies
    route = '/'
    route_name = 'companies'
    template_name = 'companies/company.html'
    decorators = [login_required]
    ticker = None

    def get_context_data(self, *args, **kwargs):
        return {
            'ticker' : 'none'
        }
    
@companies.route('/<ticker>')
def show_company(ticker):
    return render_template('companies/company.html', ticker=ticker)

#company_view = CompanyView.as_view('company')

#companies.add_url_rule('/companies/', defaults={'ticker': None}, view_func=company_view, methods=['GET',])

#companies.add_url_rule('/companies/<ticker>', view_func=company_view, methods=['GET',])
