import sys
import os


class TfIdf():
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def add_document(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.0) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0
        
        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])


    
    def similarities(self, list_of_words):
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) \
                    + (doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])

        return sims



if __name__ == '__main__':
    table = TfIdf()
    table.add_document("foo", ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"])
    table.add_document("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
    table.add_document("baz", ["kilo", "lima", "mike", "november"])
    print(table.similarities(["alpha", "bravo", "charlie"]))
    # [['foo', 0.6875], ['bar', 0.75], ['baz', 0.0]]