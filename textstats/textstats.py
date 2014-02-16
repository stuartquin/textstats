# -*- coding: utf-8 -*-

from collections import defaultdict
import math
import numpy
import stopwords
strip_list = u"\",.;:?()[]{}'!-"

class TextStats:

    def __init__(self, language, corpus):
        self.corpus = corpus
        self.language = language
        # This is composed using 'process_block'
        self.stats = {}

        # Each node is a tupple containing a list of words and a weighting
        self.nodes = []

        # A complete document
        self.document = [] 

        # Maps from word to weighted frequency
        self.document_counts = defaultdict(int)

        self.meta = {
            "min_z_score": 0.0,
            "max_z_score": 0.0,
        }

    def tf(self, doc_frequency):
        """
        Calculate the term frequency for single word, multiplied by weighting
        """
        return doc_frequency / float(len(self.document))

    def idf(self, word):
        return math.log(self.corpus.stats["total_documents"] /
               float(self.corpus.get(word) + 1.0) + 1.0)

    def get_z_score(self, mean, std, score):
        """ Calculates and returns Z-score """
        return float((score - mean) / std)

    def attach_z_scores(self, stats, scores):
        """
        Takes a dict representing word stats and attaches z-score
        """
        mean = numpy.mean(scores)
        std = numpy.std(scores)
        z_min_score = self.meta["min_z_score"]
        z_max_score = self.meta["max_z_score"]

        for word in stats:
            score = self.get_z_score(mean, std, stats[word]["score"]) 
            stats[word]["z_score"] = score

            if score < z_min_score or z_min_score == 0.0:
                z_min_score = score

            if score > z_max_score:
                z_max_score = score

        self.meta["min_z_score"] = z_min_score
        self.meta["max_z_score"] = z_max_score

        return stats

    def add_node(self, text, weighting=1):
        """
        Adds a single node of content to the document, preserves the nodes
        weighting along with each token
        """
        words = text.lower().split(u" ")
        cleaned_words = [w.strip(strip_list) for w in words]

        self.nodes.append((cleaned_words, weighting))
        self.document.extend(cleaned_words)

        for word in cleaned_words:
            word = word.strip(strip_list)
            self.document_counts[word] += (1 * weighting)
    
    def calculate_scores(self):
        """
        Takes a block of text and runs scoring on it, returns a dict containing
        'words' and 'meta'
        weighting is used to influence the term frequency, defaults to 1
        """
        stats = {}
        meta = {}
        words = []

        # Keep a list of scores for mean/SD
        scores = []

        for node in self.nodes:
            for word in node[0]:
                if word and word not in stats:
                    word = word.strip(strip_list)
                    is_stop = word in stopwords.stopwords[self.language]
                    tf = self.tf(self.document_counts[word])
                    idf = self.idf(word)
                    score = tf * math.sqrt(idf)

                    if is_stop:
                        score = 0.0

                    scores.append(score)

                    stats[word] = {
                        "is_stop": is_stop,
                        "word": word,
                        "tf": tf,
                        "idf": idf,
                        "score": score,
                        "corpus_frequency": self.corpus.get(word),
                        "weighted_frequency": self.document_counts[word]
                    }

        self.stats = self.attach_z_scores(stats, scores)
        return self.stats
