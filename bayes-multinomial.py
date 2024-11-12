# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UfupdYcH8Zcw2O5Sb-_yzcTkoMUz2cuj
"""

import kagglehub
import pandas as pd
import os
import re
from collections import defaultdict
from math import log
from typing import List
from collections import Counter


path = kagglehub.dataset_download("akash14/news-category-dataset")
print("Path to dataset files:", path)

file_path1 = os.path.join(path, 'Data_Train.csv')
file_path2= os.path.join(path, 'Data_Test.csv')

train_data = pd.read_csv(file_path1, encoding='latin-1')
test_data = pd.read_csv(file_path2, encoding='latin-1')

x_train = train_data['STORY']
y_train = train_data['SECTION']

x_test = test_data['STORY']
x_train, y_train

total_samples = len(x_train)
subset_size = int(0.8 * total_samples)
test_size = int(0.2 * total_samples)

# x = first col, y = second col
x_train_subset = x_train[:subset_size]
y_train_subset = y_train[:subset_size]
x_test_subset = x_train[:subset_size]
y_test_subset = y_train[:subset_size]

x_train_subset, y_train_subset


def probabilities(y_train_subset) -> dict[str, float]:
    n = len(y_train_subset)
    result = {"0": 0, "1": 0, "2": 0, "3": 0}

    for row in y_train_subset:
      result[str(row)] += 1

    for key in result.keys():
        result[key] /= n

    return result

a_priori_probs = probabilities(y_train_subset)

a_priori_probs

import re
from collections import defaultdict
from math import log
stop_words = {
    "the", "and", "or", "an", "a", "in", "of", "to", "for", "with", "on",
    "at", "by", "from", "about", "as", "if", "is", "it", "this", "that",
    "these", "those", "but", "not", "so", "such", "than", "too", "very",
    "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "no", "nor", "my", "your", "his", "her", "its", "our", "their", "just",
    "then", "there", "when", "where", "while", "which", "who", "whom",
    "above", "below", "because", "before", "after", "once", "here", "now",
    "out", "up", "down", "again", "back", "off", "over", "under", "same",
    "next", "until", "since", "during", "will", "can", "could", "would",
    "should", "might", "must", "may", "let", "has", "have", "had", "does",
    "did", "do", "don't", "doesn't", "didn't", "haven't", "hasn't", "was",
    "were", "be", "being", "been", "am", "are", "ain't", "aren't", "wasn't",
    "weren't", "i", "me", "myself", "mine", "we", "us", "ourselves", "ours",
    "you", "yourself", "yourselves", "yours", "he", "him", "himself",
    "she", "herself", "hers", "they", "them", "themselves", "their",
    "itself", "each", "someone", "everyone", "anyone", "nobody", "none",
    "such", "much", "many", "several", "anybody", "everybody", "everything",
    "somebody", "something", "nobody", "nothing", "whatever", "whichever",
    "whoever", "whomever", "mine", "yours", "ours", "hers", "theirs",
    "own", "till", "unto", "per", "within", "without", "via", "through",
    "toward", "towards", "thus", "whence", "whither", "whomsoever",
    "whenever", "wherein", "every", "such", "another", "one", "two",
    "three", "four", "five", "first", "second", "third", "however",
    "always", "often", "usually", "sometimes", "seldom", "rarely",
    "never", "together", "apart", "around", "among", "amongst", "besides",
    "furthermore", "moreover", "likewise", "thus", "therefore", "hereby",
    "hence", "forth", "hither", "thither", "yonder", "again", "albeit",
    "although", "though", "either", "neither", "henceforth", "heretofore",
    "inasmuch", "lest", "nonetheless", "nevertheless", "notwithstanding",
    "perhaps", "possibly", "probably", "certainly", "definitely", "surely",
    "undoubtedly", "indeed", "especially", "particularly", "specifically",
    "generally", "typically", "usually", "frequently", "commonly",
    "commonly", "rarely", "sometimes", "seldom", "never", "nowadays",
    "whilst", "already", "soon", "yet", "still", "even", "otherwise",
    "somewhat", "anyways", "anyhow", "further", "eventually", "meanwhile",
    "afterwards", "formerly", "previously", "later", "subsequently",
    "currently", "right", "left", "inside", "outside", "downwards",
    "upwards", "forwards", "backwards", "inwards", "outwards", "sideways",
    "upward", "downward", "forward", "backward", "anywhere", "nowhere",
    "somewhere", "everywhere", "anyplace", "someplace", "everyplace",
    "noone", "someone", "whomever", "anyhow", "anyway", "seriously",
    "mostly", "likely", "quite", "rather", "just", "everybody", "nobody",
    "whosoever", "whomsoever", "likewise", "nonetheless", "overall",
    "forthwith", "henceforth", "whenever", "sometimes", "perhaps",
    "probably", "certainly", "undoubtedly", "indubitably", "unquestionably",
    "actually", "already", "briefly", "sooner", "shortly", "whenever",
    "sometimes", "oftentimes", "whenever", "forever", "eternally",
    "permanently", "everlastingly", "always", "continuously", "repeatedly",
    "constantly", "again", "henceforward", "aforementioned", "wherefore",
    "whereas", "whereby", "wherein", "whereupon", "herewith", "hereto",
    "hereof", "herein", "hereby", "hereafter", "hereunder", "hitherto",
    "likewise", "moreover", "furthermore", "meanwhile", "therefore",
    "wherefore", "whereas", "whereby", "wherein", "whereupon", "whether",
    "while", "after", "before", "soon", "just", "since", "until",
    "despite", "toward", "towards", "except", "besides", "along", "aside",
    "between", "beyond", "amid", "among", "above", "beneath", "across",
    "inside", "near", "far", "due", "owing", "pending", "regarding",
    "concerning", "including", "excluding", "concerning", "regarding", "s"
}

def tokenize(text):

    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    words = set(word for word in text.split() if word not in stop_words)
    return list(words)

def parse_data(X_train_subset, y_train_subset):
    categories = {0: [], 1: [], 2: [], 3: []}
    for text, label in zip(x_train_subset, y_train_subset):
        tokenized_words = tokenize(text)
        categories[label].append(tokenized_words)
    return categories

data=parse_data(x_train_subset, y_train_subset)
# data

def top_k_frequent_words(paragraphs: List[List[str]], k: int) -> List[tuple[str, int]]:
    word_count = Counter()

    for paragraph in paragraphs:
        words = set(paragraph)
        word_count.update(words)

    number=(k/100)*len(word_count)

    top_k_words = word_count.most_common(int(number))

    return top_k_words


def combine_results(results: List[List[tuple[str, int]]]) -> List[tuple[str, int]]:
    combined_counter = Counter()
    for result in results:
        combined_counter.update(dict(result))
    return list(combined_counter.items())


top_words = []
for key in data:

  res = top_k_frequent_words(data[key], 5)
  top_words.append(res)
top_words = combine_results(top_words)

# top_words

def find_probabilities_for_top_words(data: dict[int, List[List[str]]], top_words : List[tuple[str, int]]) -> dict[str, dict[str, float]]:
    # Returns the probability of a word appearing in a category
    # The probability is calculated as the number of paragraphs containing the word divided by the total number of paragraphs in the category

    d_res = {}
    total_paragraphs = sum(len(paragraphs) for paragraphs in data.values())

    for word, count in top_words:
      # +1 Offset to avoid  0%
        d_res[word] = {"0": 1, "1": 1, "2": 1, "3": 1, "total": 1}
        for key in data.keys():
            for paragraph in data[int(key)]:
                if word in paragraph:
                    d_res[word][str(key)] += 1
                    d_res[word]["total"] += 1

    for word in d_res.keys():
        for key in d_res[word].keys():
            if key != "total":
                d_res[word][str(key)] /= len(data[int(key)])
            else:
                d_res[word][str(key)] /= total_paragraphs

    return d_res

d_res = find_probabilities_for_top_words(data, top_words)
d_res

for word in d_res.keys():
  for key in d_res[word].keys():
    if d_res[word][key] == 0:
      print(word, key, d_res[word][key])
# We don't have any 0% words. This should print nothing

def calculate_bayes(a_priori_probs: dict[str, float] , probabilities: dict[str, dict[str, float]], paragraph: List[str]) -> str:
    # Returns the probability of a category given a word
    # The probability is calculated using Bayes' theorem

    p0, p1, p2, p3 = a_priori_probs["0"], a_priori_probs["1"], a_priori_probs["2"], a_priori_probs["3"]

    for word in paragraph:
        if word not in probabilities.keys():
            continue

        p0_given_word = probabilities[word]["0"]
        p1_given_word = probabilities[word]["1"]
        p2_given_word = probabilities[word]["2"]
        p3_given_word = probabilities[word]["3"]

        p_word = probabilities[word]["total"]

        p0 = p0_given_word * p0 / p_word
        p1 = p1_given_word * p1 / p_word
        p2 = p2_given_word * p2 / p_word
        p3 = p3_given_word * p3 / p_word

    probs = [(p0, "0"), (p1, "1"), (p2, "2"), (p3, "3")]
    probs = sorted(probs, reverse=True)
    return probs[0][1]

bayes_categories = []
for text in x_test_subset:
  tokenized_words = tokenize(text)
  bayes_category = calculate_bayes(a_priori_probs, d_res, tokenized_words)
  bayes_categories.append(bayes_category)

correct_predictions = 0
for i in range(len(y_test_subset)):
  if str(y_test_subset.iloc[i]) == bayes_categories[i]:
    correct_predictions += 1

accuracy = correct_predictions / len(y_test_subset)
print("Accuracy:", accuracy)