from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import csv
from collections import namedtuple
import pendulum
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--wine_file', help='File with information about wines', default='wine.csv')
args = parser.parse_args()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

year_of_creation = pendulum.datetime(1920, 1, 1)
age = (pendulum.now() - year_of_creation).years
Wine_Record = namedtuple('Wine_Record', 'name type price image_src category discount')


def get_wine_record():
    with open(args.wine_file, 'r', encoding="utf8") as wine_file:
        reader = csv.DictReader(wine_file, delimiter=';')
        for record in reader:
            discount = record['Выгодное предложение'].strip().lower() == 'да'
            yield Wine_Record(
                record['Название'],
                record['Сорт'],
                record['Цена'],
                record['Картинка'],
                record['Категория'],
                discount,
            )


try:
    wines = list(get_wine_record())
except FileNotFoundError:
    exit('Ошибка: Ненайден файл с информацией об винах')

rendered_page = template.render(
    age=age,
    wines=wines
)

with open('index.html', 'w', encoding="utf8") as index_file:
    index_file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
