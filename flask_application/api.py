from flask import current_app
from datetime import datetime, timedelta
from flask.ext.script import Command
from urllib2 import Request, urlopen
from flask_application.models import db, FlaskDocument
from flask_application.companies.models import Company, Price
import json

class PollAPI(Command):
    """Updates price information, if necessary"""
    def run(self, **kwargs):
        self.get_market()
        self.get_company_days()
        self.poll()

    @staticmethod
    def get_market():
        headers = {
        'Content-Type': 'application/json'
        }
        request = Request('http://stocksplosion.apsis.io/api/company', headers=headers)
        market_body = urlopen(request).read()
        market_dict = json.loads(market_body)

        return market_dict

    @staticmethod
    def get_company_days(ticker,start,end):
        headers = {
        'Content-Type': 'application/json'
        }
        request_string = 'http://stocksplosion.apsis.io/api/company/' + ticker + '?startdate=' + start + '&enddate=' + end
        request = Request(request_string, headers=headers)

        company_body = urlopen(request).read()
        company_dict = json.loads(company_body) 
        return company_dict

    @staticmethod
    def update_prices(ticker):
        company_record = Company.objects(symbol=ticker)[0]
        today = datetime.today()
        start = today - timedelta(days=90)
        while start < today:
            end = start + timedelta(days=30)
            try:
                company_dict = PollAPI.get_company_days(ticker, start.strftime("%Y%m%d"), end.strftime("%Y%m%d"))
                for key, value in company_dict['prices'].iteritems():
                    record_date = datetime.strptime(key, '%Y%m%d')
                    try: 
                        Price.find({company:company_record},{date:key})
                    except:
                        new_price = Price( date=record_date, price=value, company=company_record)
                        new_price.save()
            except:
                pass
            start = start + timedelta(days=30)


    @staticmethod
    def poll():
        market_dict = PollAPI.get_market()
        for company in market_dict:
            updated_at = datetime.strptime(company['updated_at'], '%Y-%m-%d %H:%M:%S')
            created_at = datetime.strptime(company['created_at'], '%Y-%m-%d %H:%M:%S')
            ticker = company['symbol']
            company_id = company['id']
            company_name = company['name']
            record_exists = False
            try:
                company_record = Company.objects(symbol=ticker)[0]
                record_exists = True
            except:
                company_record = False
           
            if record_exists:
                if updated_at > company_record.updated:
                    PollAPI.update_prices(ticker)
            else: 
                new_company = Company( updated=updated_at, created=created_at, symbol=ticker, cid=company_id, name=company_name)
                new_company.save()
                PollAPI.update_prices(ticker)
