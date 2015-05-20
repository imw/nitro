from flask import Blueprint, current_app, render_template
from flask.ext.security import login_required

from datetime import datetime, date, timedelta
from flask_application.controllers import TemplateView
from flask_application.companies.models import Company, Price
from flask_application.forms import LookupForm

import numpy

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

def movingaverage(interval, window_size):
    window = numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'valid')
    
@companies.route('/<ticker>')
@login_required
def show_company(ticker):
    try:
        company_obj = Company.objects(symbol=ticker)[0]
    except:
        return render_template('companies/lookup.html')

    last = Price.objects(company=company_obj).order_by('-date')[0].date
    first = last - timedelta(days=90)

    prices = []
    for i in range (0, 90):
        day = last - timedelta(days=i)
        prices.append(Price.objects(company=company_obj,date=day)[0].price)

    prices.reverse()

    chartID = 'chart_ID'
    chart_type = 'line'
    chart_height = 500
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": str(company_obj.symbol), "pointStart": (int(first.strftime('%s')) * 1000), "pointInterval": (24 * 3600 * 1000), "data": prices}]
    title = {"text": str(company_obj.name)}
    xAxis = {"title": {"text": 'Date'}, "type": 'datetime', "dateTimeLabelFormats": { "month": '%b %Y', "day": '%b %e, %Y'}}
    yAxis = {"title": {"text": 'Price'}}
    tooltip = {"xDateFormat": '%b %e, %Y'}
    

    moving_averages = movingaverage(prices, 14)
    derivative = moving_averages[len(moving_averages)-1] - moving_averages[len(moving_averages)-2]
    directive = 'Wait'
    if derivative > .5:
        directive = 'Buy'
    elif derivative < -.5:
        directive = 'Sell'
    else:
        pass

    price = prices[len(prices)-1]
    updated = company_obj.updated
    listed = company_obj.created

    return render_template('companies/company.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, tooltip=tooltip, directive=directive, ticker=ticker, price=price, updated=updated, listed=listed)

@companies.route('/lookup')
@login_required
def lookup():
    form = LookupForm()
    return render_template('companies/lookup.html',form=form)

@companies.route('/leaderboard')
@login_required
def leaderboard():
    companies = Company.objects()
    movement = []
    for company_obj in companies:
       difference = Price.objects(company=company_obj).order_by('-date')[0].price - Price.objects(company=company_obj).order_by('-date')[1].price
       company_tuple = [company_obj.name, company_obj.symbol, difference]
       movement.append(company_tuple)
    
    movement.sort(key=lambda x: x[2], reverse=True)
    movement = movement[0:10]
    return render_template('companies/leaderboard.html',movement=movement)
