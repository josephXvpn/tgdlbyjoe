import re
import requests
from bs4 import BeautifulSoup


def get_absolute_video_url(url):
    video_url = None
    pattern = r"/reel/(.*?)(/|$)"
    pattern2 = r"/p/(.*?)(/|$)"
    match = re.search(pattern, url)
    match2 = re.search(pattern2, url)

    if match:
        video_url = match.group(1)
    elif match2:
        video_url = match2.group(1)

    if video_url:
        absolute_video_url = "https://www.ddinstagram.com/videos/" + video_url + "/1"
        return absolute_video_url, video_url
    else:
        print("can't find video url")
        return None, None


def get_title_and_author_name(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    title_tag = soup.find('meta', attrs={'name': 'twitter:title'})
    title = title_tag['content'] if title_tag else 'Title not found'

    oembed_url_tag = soup.find('link', attrs={'rel': 'alternate', 'type': 'application/json+oembed'})
    if oembed_url_tag:
        oembed_url = oembed_url_tag['href']
        oembed_response = requests.get(oembed_url)
        if oembed_response.status_code == 200 and oembed_response.headers['content-type'] == 'application/json':
            oembed_data = oembed_response.json()
            author_name = oembed_data.get('author_name', 'Author Name not found')
        else:
            author_name = 'Author Name not found'
    else:
        author_name = 'Description not found'

    caption = title + "\n" + author_name
    return caption
