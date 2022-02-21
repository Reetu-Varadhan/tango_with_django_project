import os

from django import views
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():

    python_pages = [
        {'title': 'Official Python Tutorial',
        'url': 'http://docs.python.org/3/tutorial/',
        'views': 29},
        {'title': 'How to Think like a Computer Scientist',
        'url': 'http://www.greenteapress.com/thinkpython/',
        'views': 10},
        {'title': 'Learn Python in 10 Minutes',
        'url': 'http://www.korokithakis.net/tutorials/python/',
        'views': 45}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
        'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01',
        'views': 38},
        {'title': 'Django Rocks',
        'url': 'http://www.djangorocks.com/',
        'views': 42},
        {'title': 'How to Tango with Django',
        'url': 'http://www.tangowithdjango.com/',
        'views': 22}
    ]

    other_pages = [
        {'title': 'Bottle',
        'url': 'http://bottlepy.org/docs/dev/',
        'views': 8},
        {'title': 'Flask',
        'url': 'http://flask.pocoo.org',
        'views': 80}
    ]

    cats = [{'name': 'Python', 'pages': python_pages, 'views': 128, 'likes': 64},
            {'name': 'Django', 'pages': django_pages, 'views': 64, 'likes': 32},
            {'name': 'Other Frameworks', 'pages': other_pages, 'views': 32, 'likes': 16}]

    # add more categories or pages, add to the dictionaries above

    # adds each category and associated pages
    for cat_data in cats:
        c = add_cat(cat_data['name'], cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])
    
    # print out the categories that have been added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

#Start execution
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
