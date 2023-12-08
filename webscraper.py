import requests
import lxml
import json
import time
import tldextract
import codecs
from datetime import date
from bs4 import BeautifulSoup

date = date.today()

# Specify User Agent
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

list_of_keywords = [
    'zero sugar candy',
    'zero sugar lollipops', 
    'sugar-free lollipops'

]
num_of_times = 5
result_dict = {}

for keyword in list_of_keywords:
    company_list = []
    num_top_ads = 0
    num_bottom_ads = 0
    result_dict[keyword] = {}
    absolute_top = 0

    print(keyword)

    for _ in range(num_of_times):
        payload = {'q': keyword}
        html = requests.get('https://www.google.com/search?q=',
                            params=payload, headers=headers)
        status_code = html.status_code

        if status_code == 200:
            response = html.text
            soup = BeautifulSoup(response, 'lxml')

            print('-------------------Top Ads-------------------')
            top_ads = soup.find(id='tvcap')
            if (top_ads):
                if len(top_ads.findAll('div', class_='uEierd')) > 0:
                    num_top_ads += 1
                absolute_top = 0
                for container in top_ads.findAll('div', class_='uEierd'):
                    try:
                        ad_headline = container.find(
                            'div', class_='CCgQ5 vCa9Yd QfkTvb N8QANc MUxGbd v0nnCb').span.text
                    except:
                        ad_headline = 'n/a'

                company = container.find('div', class_='v5yQqb').find(
                    'span', class_='x2VHCd OSrXXb ob9lvb').text

                if company not in company_list:
                    company_list.append(company)
                    if absolute_top == 0:
                        result_dict[keyword][company] = {
                            'absolute-top': 1, 'top': 0, 'bottom': 0}
                    else:
                        result_dict[keyword][company] = {
                            'absolute-top': 0, 'top': 1, 'bottom': 0}
                else:
                    if absolute_top == 0:
                        result_dict[keyword][company]['absolute-top'] += 1
                    else:
                        result_dict[keyword][company]['top'] += 1

                ad_description = container.find(
                    'div', class_='MUxGbd yDYNvb lyLwlc').text

                print(f'Company: {company}')
                print(f'Headline: {ad_headline}')
                print(f'Desc: {ad_description}')
                print()
                absolute_top += 1

            print('-------------------Bottom Ads-------------------')

            bottom_ads = soup.find(id='bottomads')
            if (bottom_ads):
                if len(bottom_ads.findAll('div', class_='uEierd')) > 0:
                    num_bottom_ads += 1
                for container in bottom_ads.findAll('div', class_='uEierd'):
                    try:
                        ad_headline = container.find(
                            'div', class_='CCgQ5 vCa9Yd QfkTvb N8QANc MUxGbd v0nnCb').span.text
                    except:
                        ad_headline = 'n/a'

                company = container.find('div', class_='v5yQqb').find(
                    'span', class_='x2VHCd OSrXXb ob9lvb').text

                if company not in company_list:
                    company_list.append(company)
                    result_dict[keyword][company] = {
                        'absolute-top': 0, 'top': 0, 'bottom': 1}
                else:
                    result_dict[keyword][company]['bottom'] += 1

                ad_description = container.find(
                    'div', class_='MUxGbd yDYNvb lyLwlc').text

                print(f'Company: {company}')
                print(f'Headline: {ad_headline}')
                print(f'Desc: {ad_description}')
                print()

    keys = list(result_dict[keyword].keys())
    for name in ['bottom', 'top', 'absolute-top']:
        keys.sort(key=lambda k: result_dict[keyword][k][name], reverse=True)

    result_dict[keyword]['top performers'] = keys
    result_dict[keyword]['total top ads'] = num_top_ads
    result_dict[keyword]['total bottom ads'] = num_bottom_ads
    print(json.dumps(result_dict, indent=4))

file = codecs.open(f'output_for_{date}.txt', 'w', 'utf-8')