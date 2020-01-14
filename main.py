from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

from collections import namedtuple

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

year_of_creation = datetime.datetime(year=1920, month=1, day=1)
age = datetime.datetime.now() - year_of_creation


#TODO: сделать нормальные названия
Parts = namedtuple('Parts', 'name type price image_src')
with open('wine.txt', 'r', encoding="utf8") as file:
    wines_info = file.read().replace('\ufeff', '').split('\n\n')
wines = []
for wine_info in wines_info:
    list1 = []
    for item in wine_info.split('\n'):
        list1.append(item.split(': ')[1])
    wines.append(Parts(*list1))


rendered_page = template.render(
    age=int(age.days / 365.25),
    wines=wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
