from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import csv
from collections import namedtuple
import pendulum

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

year_of_creation = pendulum.datetime(1920, 1, 1)
age = (pendulum.now() - year_of_creation).years
Wine_Record = namedtuple('Wine_Record', 'name type price image_src category discount')


def get_wine_record():
    with open('wine.csv', 'r', encoding="utf8") as wine_file:
        reader = csv.DictReader(wine_file, delimiter=';')
        for record in reader:
            discount = False
            if record['Выгодное предложение'].strip().lower() == 'да':
                discount = True
            yield Wine_Record(
                record['Название'],
                record['Сорт'],
                record['Цена'],
                record['Картинка'],
                record['Категория'],
                discount,
            )


wines = list(get_wine_record())
print(wines)
rendered_page = template.render(
    age=age,
    wines=wines
)

with open('index.html', 'w', encoding="utf8") as index_file:
    index_file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
