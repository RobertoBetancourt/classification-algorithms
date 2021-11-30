from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk
import string
import pandas as pd
from nltk.stem import WordNetLemmatizer

def download_packages():
  nltk.download('stopwords')
  nltk.download('punkt')
  nltk.download('wordnet')

# LEMMATIZATION
def lemmatization(sentence):
  lemmatizer = WordNetLemmatizer()

  # Tokenize: Split the sentence into words
  word_list = nltk.word_tokenize(sentence)

  # Lemmatize list of words and join
  lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
  return lemmatized_output

def add_lemmatization(all_sentences):
  new_sentences = []
  for sentence in all_sentences:
    new_sentence = lemmatization(sentence)
    new_sentences.append(new_sentence)
  
  return new_sentences

# STOP WORDS
def remove_stop_words_from_sentence(sentence):  
  stop_words = set(stopwords.words('english'))
  word_tokens = word_tokenize(sentence)
  
  filtered_sentence = []
  for w in word_tokens:
      if w not in stop_words:
          filtered_sentence.append(w)
  
  string_without_stop_words = ' '.join(filtered_sentence)
  return string_without_stop_words

def remove_stop_words_from_text(all_sentences):
  sentences_without_stop_words = []
  for sentence in all_sentences:
    new_sentence = remove_stop_words_from_sentence(sentence)
    sentences_without_stop_words.append(new_sentence)
  
  return sentences_without_stop_words

# FREQUENCY 1
def filter_text(text):
  words = word_tokenize(text)
  fdist = FreqDist(words) 
  result = filter(lambda x: fdist[x] < 2, fdist)
  list_of_words = []
  for element in result:
    list_of_words.append(element)
  
  return list_of_words

def remove_words_freq_1(all_sentences):
  text = ''
  for sentence in all_sentences:
    text += sentence + ' '
  
  word_dictionary = filter_text(text)
  
  sentences_without_freq_1 = []
  for sentence in all_sentences:
    sentence_in_list = sentence.split()
    new_words = [word for word in sentence_in_list if word not in word_dictionary]
    sentences_without_freq_1.append(' '.join(new_words))
  
  return sentences_without_freq_1

# REMOVE PUNCTUATION
def remove_punctuation_from_text(all_sentences):
  sentences_without_punctuation = []
  for sentence in all_sentences:
    temp_sentence = sentence.replace('.', ' ').replace('\n', '')
    new_sentence = ''.join([i for i in temp_sentence if i not in string.punctuation]).lower()
    sentences_without_punctuation.append(new_sentence)
  
  return sentences_without_punctuation

if __name__ == '__main__':
  filename = 'reviews.txt'
  file = open(filename, "r")

  filters = ['remove_punctuation', 'stop_words', 'freq_1', 'lemmatization']
  # Primera representación: filtro a y filtro c
  # Segunda representación: filtro b y filtro a
  all_sentences = []
  for sentence in file:
    all_sentences.append(sentence)

  if('remove_punctuation' in filters):
    all_sentences = remove_punctuation_from_text(all_sentences)
  
  sentence_list = []
  class_list = []
  for sentence in all_sentences:
    sentence_list.append(sentence[:-1])
    class_list.append(sentence[-1])

  if('stop_words' in filters):
    sentence_list = remove_stop_words_from_text(sentence_list)
  
  if('freq_1' in filters):
    sentence_list = remove_words_freq_1(sentence_list)

  if('lemmatization' in filters):
    sentence_list = add_lemmatization(sentence_list)
  
  file = open("processed_test.txt", "w")
  for index in range(len(sentence_list)):
    file.write(sentence_list[index] + ' ' + class_list[index] + '\n')
  file.close()

  