from datetime import datetime, date, timedelta
import json

from flask import Blueprint, current_app

from flask_application.controllers import TemplateView
from flask_application.api import PollAPI

from flask_application.companies.models import Company, Price

public = Blueprint('public', __name__, url_prefix='/')


class IndexView(TemplateView):
    blueprint = public
    route = '/'
    route_name = 'home'
    template_name = 'home/index.html'

 
    def get_context_data(self, *args, **kwargs):
        PollAPI.poll()

        last = Price.objects.order_by('-date')[0].date
        first = last - timedelta(days=90)

        total_prices = []
        for i in range (0, 90):
            day = last - timedelta(days=i)
            if Price.objects(date=day).count() >= 193:
                total_prices.append(Price.objects(date=day).sum('price'))

        total_prices.reverse()

        chartID = 'chart_ID'
        chart_type = 'line'
        chart_height = 500
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
        series = [{"name": 'Total Price (All Securities)', "pointStart": (int(first.strftime('%s')) * 1000), "pointInterval": (24 * 3600 * 1000), "data": total_prices}]
        title = {"text": 'Stocksplosion Exchange'}
        xAxis = {"title": {"text": 'Date'}, "type": 'datetime', "dateTimeLabelFormats": { "month": '%b %Y', "day": '%b %e, %Y'}}
        yAxis = {"title": {"text": 'Price'}}
        tooltip = {"xDateFormat": '%b %e, %Y'}

        return {
            'chartID': chartID,
            'chart': chart,
            'series': series,
            'title': title,
            'xAxis': xAxis,
            'yAxis': yAxis,
            'tooltip': tooltip,
            'config': current_app.config
        }
