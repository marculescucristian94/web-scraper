import requests

from article.el_pais_article import ElPaisArticle
from article.guardian_article import GuardianArticle
from article.bbc_article import BBCArticle
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from networkx.exception import PowerIterationFailedConvergence

ARTICLE_COUNT = 5

PAIS_URL = 'https://english.elpais.com/'
GUARDIAN_URL = 'https://www.theguardian.com/international'
BBC_URL = 'https://www.bbc.com/'


def download_pais_articles():
    page = requests.get(PAIS_URL)
    main_soup = BeautifulSoup(page.content, 'html.parser')

    coverpage_articles = main_soup.find_all('h2', class_='headline')

    for article_item in coverpage_articles[:ARTICLE_COUNT]:
        article_url = urljoin(PAIS_URL, article_item.contents[0]['href'])
        article_title = article_item.contents[0].string
        a = ElPaisArticle(article_url, article_title)
        print(a)


def download_guardian_articles():
    page = requests.get(GUARDIAN_URL)
    main_soup = BeautifulSoup(page.content, 'html.parser')

    coverpage_articles = main_soup.find_all('a', class_='fc-item__link')

    summarized_articles = []
    for article_item in coverpage_articles[:ARTICLE_COUNT]:
        article_url = article_item['href']
        if article_url in summarized_articles:
            continue
        summarized_articles.append(article_url)
        article_title = article_item.text.strip()
        try:
            a = GuardianArticle(article_url, article_title)
            print(a)
        except (PowerIterationFailedConvergence, IndexError):
            print(f'\nFailed to summarize {article_url}, skipping...\n')


def download_bbc_articles():
    page = requests.get(BBC_URL)
    main_soup = BeautifulSoup(page.content, 'html.parser')

    coverpage_articles = main_soup.find_all('a', class_='block-link__overlay-link')
    for article_item in coverpage_articles[:ARTICLE_COUNT]:
        url_fragment = article_item['href']
        if url_fragment.startswith('http://'):
            article_url = url_fragment
        else:
            article_url = urljoin(BBC_URL, url_fragment)
        article_title = article_item.text.strip()
        try:
            a = BBCArticle(article_url, article_title)
            print(a)
        except IndexError:
            print(f'\nFailed to summarize {article_url}, skipping...\n')


if __name__ == '__main__':
    download_pais_articles()
    download_guardian_articles()
    download_bbc_articles()

