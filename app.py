from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_content(url, content_type):
    """Helper function to fetch and extract content based on content_type."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if content_type == 'text':
            # Extract all text from the HTML
            text = soup.get_text()
            return {'text': text}
        
        elif content_type == 'images':
            # Extract all image URLs
            images = []
            for img in soup.find_all('img'):
                img_url = img.get('src')
                if img_url:
                    if not img_url.startswith(('http://', 'https://')):
                        img_url = requests.compat.urljoin(url, img_url)
                    images.append(img_url)
            return {'images': images}
        
        elif content_type == 'videos':
            # Extract all video URLs
            videos = []
            for video in soup.find_all('video'):
                video_url = video.get('src')
                if video_url:
                    if not video_url.startswith(('http://', 'https://')):
                        video_url = requests.compat.urljoin(url, video_url)
                    videos.append(video_url)
            return {'videos': videos}
        
        elif content_type == 'source':
            # Extract source code of the webpage
            return {'source': response.text}

        else:
            # Extract all content
            text = soup.get_text()
            images = []
            videos = []
            for img in soup.find_all('img'):
                img_url = img.get('src')
                if img_url:
                    if not img_url.startswith(('http://', 'https://')):
                        img_url = requests.compat.urljoin(url, img_url)
                    images.append(img_url)
            for video in soup.find_all('video'):
                video_url = video.get('src')
                if video_url:
                    if not video_url.startswith(('http://', 'https://')):
                        video_url = requests.compat.urljoin(url, video_url)
                    videos.append(video_url)
            return {'text': text, 'images': images, 'videos': videos}
    
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        result = fetch_content(url, 'all')
        return render_template('index.html', **result, url=url)
    return render_template('index.html')

@app.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        url = request.form.get('url')
        result = fetch_content(url, 'text')
        return render_template('index.html', **result, url=url)
    return render_template('index.html')

@app.route('/images', methods=['GET', 'POST'])
def images():
    if request.method == 'POST':
        url = request.form.get('url')
        result = fetch_content(url, 'images')
        return render_template('index.html', **result, url=url)
    return render_template('index.html')

@app.route('/videos', methods=['GET', 'POST'])
def videos():
    if request.method == 'POST':
        url = request.form.get('url')
        result = fetch_content(url, 'videos')
        return render_template('index.html', **result, url=url)
    return render_template('index.html')

@app.route('/source', methods=['GET', 'POST'])
def source():
    if request.method == 'POST':
        url = request.form.get('url')
        result = fetch_content(url, 'source')
        return render_template('index.html', **result, url=url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
