from datetime import datetime
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
        latest = PollAPI.poll()

        chartID = 'chart_ID'
        chart_type = 'line'
        chart_height = 500
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
        series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
        title = {"text": 'Stocksplosion Exchange'}
        xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
        yAxis = {"title": {"text": 'yAxis Label'}}

        return {
            'chartID': chartID,
            'chart': chart,
            'series': series,
            'title': title,
            'xAxis': xAxis,
            'yAxis': yAxis,
            'config': current_app.config,
            'latest': 'test',
            'market': len(Company.objects()),
            'count': len(Price.objects())
        }
