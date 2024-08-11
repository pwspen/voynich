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
def plot_word_frequency_distribution(word_counts):
    frequencies = list(word_counts.values())
    
    # Define bins
    max_freq = max(frequencies)
    bins = [5, 10, 20, 50, 100, 200, 500, 1000]
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

    # Print bin information
    print("\nWord Frequency Distribution:")
    for i, count in enumerate(hist):
        print(f"{bin_labels[i]}: {count} words")

# Plot word frequency distribution
plot_word_frequency_distribution(word_counts)

# Print top 20 most frequent words
print("\nTop 20 Most Frequent Words:")
for word, count in word_counts.most_common(20):
    print(f"{word}: {count}")