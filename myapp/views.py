import requests
from requests.compat import quote_plus
from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup

BASE_CRAIGLIST_URL = 'https://ahmedabad.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    # print(quote_plus(search))
    # this line will create an object of every search in models.py file
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    # this data is getting all the html of page
    data = response.text
    # print(data)
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_post = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'NAN'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            # print(post_image_url)
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://images.craigslist.org/images/peace.jpg'

        final_post.append((post_title, post_url, post_price, post_image_url))
        # print(final_post)

    # print(post_title)
    # print(post_url)
    # print(post_price)

    # print(data)
    stuff_for_frontend = {
        'search': search,
        'final_post': final_post,
    }
    return render(request, 'myapp/new_search.html', stuff_for_frontend)
