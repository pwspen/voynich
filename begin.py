import ivtff
import voynich
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

class Manuscript:
    def __init__(self, filename='voynich/ZL_ivtff_3a.txt', parse_function=ivtff.parse_transliteration):
        # Parse function should take in raw text for entire MS and return
        # a dictionary: {pagenum: {'text': '...', 'metadata': {...}}}
        self.filename = filename
        self.rawtext = open(filename, 'r').read()
        self.pages = parse_function(self.rawtext)
        self.lines = []
        self.words = []
        self.pages_lines = {}
        self.pages_words = {}
        for page, data in self.pages.items():
            self.pages_lines[page] = []
            self.pages_words[page] = []

            lines = data['text'].split('\n')
            self.lines += lines
            self.pages_lines[page] += lines

            words = ' '.join(lines).split()
            self.words += words # ['word1', 'word2', ...]
            self.pages_words[page] += words # {'f1r': ['word1', 'word2', ...], ...}

        self.unique_words = set(self.words) # {'word1', 'word2', ...}
        self.word_counts = Counter(self.words) # {word: count}

    def plot_top_n_word_counts(self, n: int):
        top_n = self.word_counts.most_common(n)
        words = [word for word, count in top_n]
        counts = [count for word, count in top_n]

        plt.figure(figsize=(10, 5))
        plt.bar(words, counts)
        plt.xticks(rotation=45)
        plt.title(f'Top {n} Word Counts')
        plt.xlabel('Word')
        plt.ylabel('Count')
        plt.show()

    def single_page_words_info(self, min_length=3):
        # Dictionary to store words and the pages they appear on
        word_pages = {}
        
        # Populate word_pages dictionary
        for page, words in self.pages_words.items():
            for word in words:
                if word not in word_pages:
                    word_pages[word] = set()
                word_pages[word].add(page)
        
        # Filter words that appear on only one page and have length > min_length
        single_page_words = {}
        for word, pages in word_pages.items():
            if len(pages) == 1 and len(word) > min_length:
                page = list(pages)[0]
                frequency = self.word_counts[word]
                single_page_words[word] = {
                    'frequency': frequency,
                    'page': page
                }
        
        # Sort the dictionary by frequency in descending order
        sorted_single_page_words = dict(sorted(single_page_words.items(), 
                                            key=lambda item: item[1]['frequency'], 
                                            reverse=True))
        
        return sorted_single_page_words
    
    def multi_page_words_concentration(self, min_length=3):
        word_pages = {}
        word_page_counts = {}
        
        # Populate word_pages and word_page_counts dictionaries
        for page, words in self.pages_words.items():
            for word in words:
                if len(word) <= min_length:
                    continue
                if word not in word_pages:
                    word_pages[word] = set()
                    word_page_counts[word] = {}
                word_pages[word].add(page)
                word_page_counts[word][page] = word_page_counts[word].get(page, 0) + 1
        
        # Calculate concentration for words on multiple pages
        multi_page_words = {}
        for word, pages in word_pages.items():
            if len(pages) > 1:
                total_count = self.word_counts[word]
                max_page_count = max(word_page_counts[word].values())
                concentration = (max_page_count / total_count) * 100
                max_page = max(word_page_counts[word], key=word_page_counts[word].get)
                
                multi_page_words[word] = {
                    'total_count': total_count,
                    'max_page_count': max_page_count,
                    'concentration': concentration,
                    'max_page': max_page,
                    'num_pages': len(pages)
                }
        
        # Sort the dictionary by concentration in descending order
        sorted_multi_page_words = dict(sorted(multi_page_words.items(), 
                                            key=lambda item: item[1]['concentration'], 
                                            reverse=True))
        
        return sorted_multi_page_words

    def count_single_occurrence_words_per_page(self):
        # First, count overall word occurrences
        word_counts = Counter(self.words)
        
        # Identify single-occurrence words
        single_occurrence_words = set(word for word, count in word_counts.items() if count == 1)
        
        # Count single-occurrence words per page
        page_single_word_counts = {}
        
        for page, words in self.pages_words.items():
            single_words_on_page = [word for word in words if word in single_occurrence_words]
            page_single_word_counts[page] = len(single_words_on_page)
        
        # Sort pages by their single-occurrence word count in descending order
        sorted_pages = sorted(page_single_word_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_pages)

    def plot_word_length_distribution(self):
        word_lengths = [len(word) for word in self.unique_words]
        
        plt.figure(figsize=(10, 5))
        plt.hist(word_lengths, bins=range(min(word_lengths), max(word_lengths) + 1, 1), edgecolor='black')
        plt.title('Word Length Distribution')
        plt.xlabel('Word Length')
        plt.ylabel('Frequency')
        plt.show()
VMS = Manuscript()
result = VMS.plot_word_length_distribution()
