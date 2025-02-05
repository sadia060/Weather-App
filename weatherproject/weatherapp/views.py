from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'dhaka'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='
    PARAMS = {'units': 'metric'}
    
    API_KEY =  ''
    SEARCH_ENGINE_ID = ''
     
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        data = requests.get(city_url).json()
        search_items = data.get("items")
        if search_items and len(search_items) > 1:
            image_url = search_items[1]['link']
        else:
            image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'  # Default image URL
    except (KeyError, IndexError):
        image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'  # Default image URL

    try: 
        response = requests.get(url, params=PARAMS)
        data = response.json()
        
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })
    
    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'dhaka',
            'exception_occurred': exception_occurred,
            'image_url': image_url  
        })