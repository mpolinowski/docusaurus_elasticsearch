import requests
import re
from bs4 import BeautifulSoup

# add some infos that are not on the page

camera_series = '["PLACEHOLDER"]'
article_type = 'PLACEHOLDER'
chapter = 'PLACEHOLDER'
tags = '["PLACEHOLDER"]'
image = 'PLACEHOLDER'
imagesquare = 'PLACEHOLDER'


# read in list of page urls

pages = open('pages/sideLinkscopy.txt', 'r')

# loop over urls and request content

for line in pages:
    page = line.split()[0]
    # print(page[0])
    # exit()
    # use page url to fetch/parse content
    response = requests.get(page)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # find in content

    ## get article title from meta tag
    article_title = (soup.find("meta", property="og:title"))["content"]
    ## get article description from meta tag
    article_description = (soup.find("meta", property="og:description"))["content"]
    ## get article description from meta tag
    article_content = soup.find('main', attrs={'class': 'docMainContainer_gTbr'}).text
    ## replace quotation marks
    jsonfied_content = article_content.replace('"', ' ')
    ## strip multiple-space character
    single_space = re.sub('\s+',' ',jsonfied_content)

    # create json object from results

    json_template = """{
        "title": "ARTICLE_TITLE",
        "series": ARTICLE_SERIES,
        "type": "ARTICLE_TYPE",
        "description": "ARTICLE_BODY",
        "sublink1": "ARTICLE_URL",
        "chapter": "ARTICLE_CHAPTER",
        "tags": ARTICLE_TAGS,
        "image": "ARTICLE_THUMB",
        "imagesquare": "ARTICLE_SQUAREIMAGE",
        "short": "ARTICLE_SHORT",
        "abstract": "ARTICLE_ABSTRACT"
    }"""


    add_body = json_template.replace('ARTICLE_BODY', single_space)
    add_title = add_body.replace('ARTICLE_TITLE', article_title)
    add_series = add_title.replace('ARTICLE_SERIES', camera_series)
    add_type = add_series.replace('ARTICLE_TYPE', article_type)
    add_url = add_type.replace('ARTICLE_URL', page[29:])
    add_chapter = add_url.replace('ARTICLE_CHAPTER', chapter)
    add_tags = add_chapter.replace('ARTICLE_TAGS', tags)
    add_image = add_tags.replace('ARTICLE_THUMB', image)
    add_imagesquare = add_image.replace('ARTICLE_SQUAREIMAGE', imagesquare)
    add_short = add_imagesquare.replace('ARTICLE_SHORT', article_description)
    add_abstract = add_short.replace('ARTICLE_ABSTRACT', article_description)

    with open('pages/articles.json', 'a') as file:
        file.write(add_abstract)

pages.close()