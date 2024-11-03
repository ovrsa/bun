from django.http import JsonResponse
from django.views.decorators.cache import cache_page
import csv
import os

@cache_page(60 * 60)
def nasdaq_ticker_list(request):

    csv_path = os.path.join(os.path.dirname(__file__), 'nasdaq.csv')
    
    ticker_data = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ticker_data.append(row)

    # データの加工処理
    ticker_data = [{ 'Symbol': row['Symbol'], 'Name': row['Name'] } for row in ticker_data]

    for row in ticker_data:
        if 'Class A Ordinary Shares' in row['Name']:
            row['Name'] = row['Name'].replace('Class A Ordinary Shares', '')
        if 'Common Stock' in row['Name']:
            row['Name'] = row['Name'].replace('Common Stock', '')
        if 'Units' in row['Name']:
            row['Name'] = row['Name'].replace('Units', '')
        if 'Depositary Shares' in row['Name']:
            row['Name'] = row['Name'].replace('Depositary Shares', '')

    return JsonResponse(ticker_data, safe=False)