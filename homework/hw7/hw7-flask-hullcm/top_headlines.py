'''
Name: Chloe Hull
Uniqname: hullcm@umich.edu
'''

from flask import Flask, render_template
import secrets
import requests

app = Flask(__name__)
API_KEY = secrets.api_key

@app.route('/')
def index():
    return '<h1>Welcome!</h1>'

@app.route('/name/<name>')
def hello_name(name):
    return render_template('name.html',
    name = name)

@app.route('/headlines/<name>')
def get_news(name):
    BASE_URL = "https://api.nytimes.com/svc/topstories/v2/technology.json"
    params = {'api-key':API_KEY}
    results = requests.get(BASE_URL, params=params).json()
    article_details = results['results']
    headlines = []
    for item in article_details:
        for key, value in item.items():
            if key == 'section' and value != 'technology':
                break      
            if key == 'title':
                title = value
                headlines.append(title)
    print(headlines)
    return render_template('headlines.html',
    name=name, headline=headlines)

@app.route('/links/<name>')
def get_links(name):
    BASE_URL = "https://api.nytimes.com/svc/topstories/v2/technology.json"
    params = {'api-key':API_KEY}
    results = requests.get(BASE_URL, params=params).json()
    article_details = results['results']
    headlines = []
    urls = []
    for item in article_details:
        for key, value in item.items():
            if key == 'section' and value != 'technology':
                break
            if key == 'title':
                title = value
                headlines.append(title)
            if key == 'url':
                url = value
                urls.append(url)
    print(urls)
    return render_template('links.html',
    name=name, link=urls, headline=headlines)

@app.route('/images/<name>')
def get_images(name):
    BASE_URL = "https://api.nytimes.com/svc/topstories/v2/technology.json"
    params = {'api-key':API_KEY}
    results = requests.get(BASE_URL, params=params).json()
    article_details = results['results']
    headlines = []
    urls = []
    images = []
    for item in article_details:
        for key, value in item.items():
            if key == 'section' and value != 'technology':
                break
            if key == 'title':
                title = value
                headlines.append(title)
            if key == 'url':
                url = value
                urls.append(url)
            if key == 'multimedia':
                image = value[0]['url']
                images.append(image)
    return render_template('images.html',
    name=name, link=urls, headline=headlines,images=images)


if __name__ == '__main__':  
   print('starting Flask app', app.name)  
   app.run(debug=True)