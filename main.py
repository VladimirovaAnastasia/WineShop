from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas
from collections import defaultdict

import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='The source of file and name')
    parser.add_argument('file_path', help='The source of file', default='wine.xlsx')

    return parser

parser = create_parser()
args = parser.parse_args()
file_path = args.file_path

excel_data_df = pandas.read_excel(file_path,
                                  usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
                                  na_values='nan',
                                  keep_default_na=False)
products = excel_data_df.to_dict(orient='record')
structured_products = defaultdict(list)
for product in products:
    structured_products[product['Категория']].append(product)



now_year = datetime.datetime.now().year
burn_year = 1920

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


rendered_page = template.render(
    working_years=(now_year - burn_year),
    structured_products=structured_products
)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()