import ivtff
import voynich
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# File reading and word counting (unchanged)
file = open('voynich/ZL_ivtff_3a.txt', 'r').read()
booktext = ivtff.parse_transliteration(file)
pages = {}
lines = []
for key, value in booktext.items():
    pagelines = value.split('\n')
    pages[key] = pagelines
    lines += pagelines

words = []
for line in lines:
    words += line.split(' ')
unique_words = set(words)

# Count occurrences of each word
word_counts = Counter(words)

print("Total word count:", len(words))
print("Unique word count:", len(unique_words))

# Plotting
def plot_word_frequency_distribution(word_counts, bins=None):
    frequencies = list(word_counts.values())
    max_freq = max(frequencies)
    
    # Define default bins if not provided
    if bins is None:
        bins = [1, 2, 3, 4, 5, 10, 20, 50, 100, 200, 500, 1000]
    
    # Ensure bins are appropriate for the data
    bins = [b for b in bins if b <= max_freq]
    if bins[-1] < max_freq:
        bins.append(max_freq + 1)
    
    # Count words in each bin
    hist, bin_edges = np.histogram(frequencies, bins=bins)
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(hist)), hist, align='center')
    plt.title('Distribution of Word Frequencies in Voynich Manuscript')
    plt.xlabel('Word Frequency Bins')
    plt.ylabel('Number of Words')
    
    # Set x-axis labels
    bin_labels = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins)-1)]
    bin_labels[-1] = f'{bins[-2]}+'
    plt.xticks(range(len(hist)), bin_labels, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()

def plot_unique_word_length_distribution(unique_words):
    # Calculate word lengths
    word_lengths = [len(word) for word in unique_words]
    
    # Count occurrences of each length
    length_counts = Counter(word_lengths)
    
    # Sort the lengths
    sorted_lengths = sorted(length_counts.keys())
    
    # Prepare data for plotting
    lengths = sorted_lengths
    counts = [length_counts[length] for length in lengths]
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(lengths, counts, align='center')
    plt.title('Distribution of Unique Word Lengths in Voynich Manuscript')
    plt.xlabel('Word Length')
    plt.ylabel('Number of Unique Words')
    
    # Set x-axis ticks
    plt.xticks(lengths)
    
    plt.tight_layout()
    plt.show()

def print_n_most_frequent(n):
    print(f"\nTop {n} Most Frequent Words:")
    for word, count in word_counts.most_common(n):
        print(f"{word}: {count}")

def plot_top_words(word_counts, n=20):
    plt.figure(figsize=(12, 6))
    top_words = word_counts.most_common(n)
    words, counts = zip(*top_words)
    
    plt.bar(words, counts)
    plt.title(f'Top {n} Most Common Words in Voynich Manuscript')
    plt.xlabel('Words')
    plt.ylabel('Occurrences')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plt.show()

plot_unique_word_length_distribution(unique_words)