from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
 

# Create your views here.
#Adding url of the website to scrapp and opening a dict after query so it can be dinamically 
# generated for every search result
CRAIGLIST_URL = 'https://sfbay.craigslist.org/search/?query={}' 
IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search') #Pulling data out of the search bar
    models.Search.objects.create(search=search)
    final_url = CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,features= 'html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []


    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'


        final_postings.append ((post_title,post_url,post_price,post_image_url))
    frontend_content = { 
        #passing dictionary from views.py to html content
        'search':search,
        'final_postings' : final_postings
    
    }
    return render(request,'new_search.html',frontend_content)