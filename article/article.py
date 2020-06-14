import networkx as nx
import numpy as np
import re

from abc import ABC, abstractmethod
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance


class Article(ABC):
    def __init__(self, url, title, summary_sentence_no=3):
        self.url = url
        self.title = title
        self.summary_sentence_no = summary_sentence_no
        self.text = self.get_article_text()
        if self.text:
            self.summary = self.summarize_text()
        else:
            self.summary = 'No summary to display (artwork article)'

    @abstractmethod
    def get_article_text(self):
        pass

    def get_clean_sentences(self):
        return [re.sub(r'[^\w\s]', '', raw_sentence).split(" ")
                for raw_sentence in re.split(r'\. |”\. |\.” |”\.|\.”', self.text)]

    def summarize_text(self):
        sentences = self.get_clean_sentences()
        np.seterr(divide='ignore', invalid='ignore')
        similarity_matrix = self.get_similarity_matrix(sentences)
        similarity_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(similarity_graph)
        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

        summary_sentences = []
        for i in range(self.summary_sentence_no):
            try:
                summary_sentences.append(" ".join(ranked_sentences[i][1]))
            except IndexError:
                continue

        return "\n".join(summary_sentences)

    @staticmethod
    def get_similarity_matrix(sentences):
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for current_idx, current_sentence in enumerate(sentences):
            for compare_idx, compare_sentence in enumerate(sentences):
                if current_idx == compare_idx:
                    continue  # no point in comparing the sentence to itself
                similarity_matrix[current_idx][compare_idx] = \
                    Article.get_sentence_similarity(current_sentence, compare_sentence)

        return similarity_matrix

    @staticmethod
    def get_sentence_similarity(s1, s2):
        stop_words = stopwords.words('english')

        s1 = [word.lower() for word in s1]
        s2 = [word.lower() for word in s2]

        all_words = list(set(s1 + s2))

        v1 = [0] * len(all_words)
        v2 = [0] * len(all_words)

        # build the vector for the first sentence
        for w in s1:
            if w in stop_words:
                continue
            v1[all_words.index(w)] += 1

        # build the vector for the second sentence
        for w in s2:
            if w in stop_words:
                continue
            v2[all_words.index(w)] += 1

        return 1 - cosine_distance(v1, v2)

    def __str__(self):
        output = '---------------------------------------\n'
        output += f'Article title: {self.title}\n\n'
        output += f'--Summary--\n{self.summary}\n\n'
        output += f'Link to full article: {self.url}\n'
        output += '---------------------------------------\n'
        return output
