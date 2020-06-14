import requests

from bs4 import BeautifulSoup

from .article import Article


class GuardianArticle(Article):
    def __init__(self, url, title, summary_sentence_no=3):
        super().__init__(url, title, summary_sentence_no)

    def get_article_text(self):
        article_page = requests.get(self.url)
        article_soup = BeautifulSoup(article_page.content, 'html.parser')

        article_body = article_soup.find_all('div', class_='content__article-body')[0]
        article_text = []
        for paragraph in article_body.find_all('p'):
            if 'class' in paragraph.attrs and 'tweet-body' in paragraph['class']:
                continue
            if paragraph.text:
                article_text.append(paragraph.text)

        return ' '.join(article_text)
