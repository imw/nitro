from datetime import datetime
import json

from urllib2 import Request, urlopen
from flask import Blueprint, current_app

from flask_application.controllers import TemplateView

public = Blueprint('public', __name__, url_prefix='/')


class IndexView(TemplateView):
    blueprint = public
    route = '/'
    route_name = 'home'
    template_name = 'home/index.html'

    def get_context_data(self, *args, **kwargs):
        headers = {
        'Content-Type': 'application/json'
        }
        request = Request('http://stocksplosion.apsis.io/api/company', headers=headers)
        market_body = urlopen(request).read()
        market_dict = json.loads(market_body)

        latest = datetime.strptime('1970-1-1 0:0:0', '%Y-%m-%d %H:%M:%S')

        for company in market_dict:
            updated_date = datetime.strptime(company['updated_at'], '%Y-%m-%d %H:%M:%S')
            if updated_date > latest:
                latest = updated_date

        return {
            'config': current_app.config,
            'latest': latest,
            'market': market_dict,
            'count': len(market_dict)
        }
