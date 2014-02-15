frequency_dir = "frequencies/"

# Some hard coded stats about the corpus frequency files
frequency_stats = {
    "en": {
        "total_documents": 106828
    }
}


class Frequencies:
    def __init__(self, language):
        self.language = language
        self.frequencies = {}
        self.stats = frequency_stats[self.language]
        self.load_corpus_frequency(frequency_dir + self.language + ".txt")

    def get(self, word):
        return abs(self.frequencies.get(word, 1))

    def load_corpus_frequency(self, file_name):
        """
        Loads frequency list into memory
        List from http://invokeit.wordpress.com/frequency-word-lists/
        """
        with open(file_name, 'r') as f:
            read_data = f.read()
            lines = read_data.decode("utf-8").split(u"\n")
            for line in lines:
                entry = line.split(u" ")
                if len(entry) == 2:
                    self.frequencies[entry[0].strip()] = int(entry[1].strip())
