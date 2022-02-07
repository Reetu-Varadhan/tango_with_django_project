from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Page, Category

def index(request):
    # Query database for all categories currently stored, order them by # likes in descending order
    # retrieve top 5 only
    # place in context_dict
    # constructing a dictionary to pass to the template engine as its context
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list


    # return a rendered httpresponse to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Reetu V'}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        #Tries to find a category name slug with the given name
        # if DNE, the .get() method raises a DNE exception
        category = Category.objects.get(slug=category_name_slug)

        #Retrieve all associated pages
        #Filater() returns a list of page objects, or an empty list
        pages = Page.objects.filter(category=category)

        #Adds results list to the template context
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

