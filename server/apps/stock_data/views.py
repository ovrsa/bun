from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View
import csv
import os


@method_decorator(cache_page(60 * 60), name='dispatch')
class NasdaqTickerListView(View):
    def _load_ticker_data(self):
        csv_path = os.path.join(os.path.dirname(__file__), 'nasdaq.csv')

        ticker_data = []
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name']
                for term in ['Class A Ordinary Shares', 'Common Stock', 'Units', 'Depositary Shares']:
                    name = name.replace(term, '')
                ticker_data.append({
                    'Symbol': row['Symbol'],
                    'Name': name.strip()
                })
        return ticker_data

    def get(self, request):
        query = request.GET.get('query', '').lower()
        ticker_data = self._load_ticker_data()

        if query:
            filtered_data = [row for row in ticker_data if row['Name'].lower().startswith(query)]
        else:
            filtered_data = ticker_data

        return JsonResponse(filtered_data, safe=False)