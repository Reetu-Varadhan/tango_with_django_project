from re import L
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Page, Category
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

    visitor_cookie_handler(request)


    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Reetu V'}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

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
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # http post
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # is the form valid?
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect('/rango/')
        else: # if there are errors
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))
    
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                kwargs={'category_name_slug':
                                        category_name_slug}))
        
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context = context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # hash password
            user.set_password(user.password)
            user.save()

            #now the profile
            profile = profile_form.save(commit=False)
            profile.user = user

            #profile pic
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # successful registration
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else: # not an http post
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                    'rango/register.html',
                    context = {'user_form': user_form,
                                'profile_form': profile_form,
                                'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits




