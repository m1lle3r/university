import re
import csv
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://msk.spravker.ru/avtoservisy-avtotehcentry/"
html_content = urllib.request.urlopen(url).read().decode()

with open('html.txt', 'w', encoding='utf-8') as file:
    file.write(html_content)

pattern = (
    r'class="org-widget-header__title-link">([^<]+)</a>.*?'
    r'org-widget-header__meta--location">([^<]+)</span>.*?'
    r'<dt class="spec__index"><span class="spec__index-inner">Телефон</span></dt>.*?'
    r'<dd class="spec__value">([^<]+)</dd>.*?'
    r'<dt class="spec__index"><span class="spec__index-inner">Часы работы</span></dt>.*?'
    r'<dd class="spec__value">([^<]+)</dd>'
)

matches = re.findall(pattern, html_content, re.DOTALL)

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv.writer(csvfile).writerows([['Наименование', 'Адрес', 'Телефон', 'Часы работы']] + matches)
