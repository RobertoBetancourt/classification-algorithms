import csv
import random
import string
import math
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

def classify_sentence(sentences_freq, words_freq, text):
  list_of_words = text.split()
  number = int(list_of_words.pop(len(list_of_words) - 1))
  if number == 0:
    sentences_freq['neg'] += 1
  else:
    sentences_freq['pos'] += 1

  for word in list_of_words:
    if words_freq.get(word, -1) == -1:
      words_freq[word] = {
        'pos': 0,
        'neg': 0
      }

    if number == 0:
      words_freq[word]['neg'] += 1
    else:
      words_freq[word]['pos'] += 1

  return [sentences_freq, words_freq]

def evaluate_sentences(test_sentences, words_prob, positive_prob, negative_prob):
  # output = [['Instancia', 'LogPos', 'LogNeg', 'Clase', 'ClaseReal']]

  index = 1
  test_classes = []
  real_classes = []
  for current_sentence in test_sentences:
    test_sentence = ''.join([i for i in current_sentence if i not in string.punctuation]).lower()
    processed_sentence, real_class = test_sentence[:-1], test_sentence[-1]

    test_word_to_list = processed_sentence.split()
    pos_sum_log = 0
    neg_sum_log = 0
    for word in test_word_to_list:
      if words_prob.get(word, -1) != -1:
        pos_sum_log += words_prob[word]['pos']
        neg_sum_log += words_prob[word]['neg']
    pos_sum_log += positive_prob
    neg_sum_log += negative_prob

    projected_class = 1 if pos_sum_log > neg_sum_log else 0
    # output.append([index, pos_sum_log, neg_sum_log, projected_class, real_class])
    test_classes.append(int(projected_class))
    real_classes.append(int(real_class))

    index += 1
  
  # with open('classification.csv', 'w', newline='') as file:
  #   writer = csv.writer(file)
  #   writer.writerows(output)
  
  return [test_classes, real_classes]

def generate_vocabulary_csv(sentences_freq, positive_prob, negative_prob, words_freq, words_prob):
  output = [['Palabra/Clase', 'FrecPos', 'FrecNeg', 'LogPos', 'LogNeg'],
            ['CLASE', sentences_freq['pos'], sentences_freq['neg'], positive_prob, negative_prob]]
    
  for key in words_freq:
    output.append([key, words_freq[key]['pos'], words_freq[key]['neg'], words_prob[key]['pos'], words_prob[key]['neg']])
  
  with open('model.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)

def count_and_classify_words(words_freq):
  total_positive_words = 0
  total_negative_words = 0
  for key in words_freq:
    total_positive_words += words_freq[key]['pos']
    total_negative_words += words_freq[key]['neg']
  return [total_positive_words, total_negative_words]  

def get_probabilities(words_freq):
  vocabulary = len(words_freq.keys())
  total_positive_words = 0
  total_negative_words = 0
  for key in words_freq:
    total_positive_words += words_freq[key]['pos']
    total_negative_words += words_freq[key]['neg']
  
  words_prob = {}
  for key in words_freq:
    pos_prob = math.log10((words_freq[key]['pos'] + 1) / (total_positive_words + vocabulary))
    neg_prob = math.log10((words_freq[key]['neg'] + 1) / (total_negative_words + vocabulary))
    words_prob[key] = {
      'pos': pos_prob,
      'neg': neg_prob
    }
  
  return words_prob

if __name__ == '__main__':
  sentences_freq = {
    'pos': 0,
    'neg': 0
  }

  words_freq = {}
  
  test_sample = random.sample(range(0, 2999), 300)

  test_sentences = []
  for index in range(3000):
    if index in test_sample:
      test_sentence = input()
      test_sentences.append(test_sentence)
    else:
      text = input()
      [sentences_freq, words_freq] = classify_sentence(sentences_freq=sentences_freq, words_freq=words_freq, text=text)
  
  
  positive_prob = math.log10(sentences_freq['pos'] / 900)
  negative_prob = math.log10(sentences_freq['neg'] / 900)  
  words_prob = get_probabilities(words_freq)  
  # generate_vocabulary_csv(sentences_freq, positive_prob, negative_prob, words_freq, words_prob)
  [test_classes, real_classes] = evaluate_sentences(test_sentences, words_prob, positive_prob, negative_prob)
  print('ClasesTest:', test_classes)
  print('ClasesRecuperadas', real_classes)

  Matriz = confusion_matrix(test_classes, real_classes)
  # tn, fp, fn, tp = confusion_matrix(test_classes, real_classes).ravel()
  print('Confusion matrix:')
  print(Matriz)

  precision, recall, fscore, _ = precision_recall_fscore_support(test_classes, real_classes, average='micro')
  print('Precision: ', precision, '\nRecall: ', recall, '\nF-score', fscore)
