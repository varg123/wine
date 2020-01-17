from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import csv
from collections import namedtuple

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

year_of_creation = datetime.datetime(year=1920, month=1, day=1)
age = datetime.datetime.now() - year_of_creation

Wine_Record = namedtuple('Wine_Record', 'name type price image_src category discount')
def get_wine_record():
    with open('wine.csv', 'r', encoding="utf8") as wine_file:
        reader = csv.DictReader(wine_file, delimiter=';')
        for record in reader:
            discount = False
            if record['Выгодное предложение'].strip().lower() == 'Да':
                discount = True
            yield  Wine_Record(
                record['Название'],
                record['Сорт'],
                record['Цена'],
                record['Картинка'],
                record['Категория'],
                discount,
            )


wines = list(get_wine_record())
rendered_page = template.render(
    age=int(age.days / 365.25),
    wines=wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
