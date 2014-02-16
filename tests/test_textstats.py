from textstats.frequencies import Frequencies
from textstats.textstats import TextStats
from mock import MagicMock

corpus = Frequencies("en")
corpus.stats = {
    "total_documents": 100
}

class TestTextStats:
    def setup(self):
        self.stats = TextStats("en", corpus)

    def test_tf(self):
        self.stats.document = ["hello", "world"]
        assert(self.stats.tf(1) == 0.5)

    def test_idf(self):
        word = "hello"
        expected = 3.258096538021482
        corpus.get = MagicMock(return_value=3)

        result = self.stats.idf(word)
        corpus.get.assert_called_with(word)
        assert(result == expected)

    def test_get_z_score(self):
        expected = 11.75
        score = self.stats.get_z_score(50.0, 4.0, 97.0)
        assert(score == expected)

    def test_add_node(self):
        content = "text to test the test content of this text test"
        self.stats.add_node(content)
        assert(self.stats.document_counts["test"] == 3)
        assert(len(self.stats.nodes) == 1)

        # Document counts should increment
        content = "text to test the test content of this text test"
        self.stats.add_node(content)
        assert(self.stats.document_counts["test"] == 6)
        assert(len(self.stats.nodes) == 2)

        # Check weighting works and capitals are handled
        content = "Some New Content"
        assert(self.stats.document_counts["content"] == 2)
        self.stats.add_node(content,2)
        assert(self.stats.document_counts["content"] == 4)
        assert(len(self.stats.nodes) == 3)
