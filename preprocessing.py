import string
# import pandas as pd
from nltk import download
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer

def download_packages():
  download('stopwords')
  download('punkt')
  download('wordnet')

# LEMMATIZATION
def lemmatization(sentence):
  lemmatizer = WordNetLemmatizer()
  # Tokenize: Split the sentence into words
  word_list = word_tokenize(sentence)
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

# GENERAL FUNCTIONS
def separate_sentence_and_class(all_sentences):
  sentences_list = []
  classes_list = []
  for sentence in all_sentences:
    sentences_list.append(sentence[:-1])
    classes_list.append(sentence[-1])
  
  return [sentences_list, classes_list]

def apply_filters_to_sentences(sentences_list, filters):
  if('stop_words' in filters):
    sentences_list = remove_stop_words_from_text(sentences_list)
  
  if('freq_1' in filters):
    sentences_list = remove_words_freq_1(sentences_list)

  if('lemmatization' in filters):
    sentences_list = add_lemmatization(sentences_list)
  
  return sentences_list

# FILE MANIPULATION
def get_sentences_without_punctuation(input_filename):
  file = open(input_filename, "r")
  all_sentences = []
  for sentence in file:
    sentence_without_new_line = sentence.replace('\n', '')
    processed_sentence = ''.join([i for i in sentence_without_new_line if i not in string.punctuation]).lower()
    all_sentences.append(processed_sentence)
  
  return all_sentences

def write_to_file(output_filename, sentences_list, classes_list):
  file = open(output_filename, "w")
  for index in range(len(sentences_list)):
    file.write(sentences_list[index] + ' ' + classes_list[index] + '\n')
  file.close()

# MAIN
if __name__ == '__main__':
  input_filename = 'reviews.txt'
  output_filename = "processed_test.txt"
  filters = ['stop_words', 'freq_1', 'lemmatization']

  download_packages()
  all_sentences = get_sentences_without_punctuation(input_filename=input_filename)
  [sentences_list, classes_list] = separate_sentence_and_class(all_sentences=all_sentences)
  sentences_list = apply_filters_to_sentences(sentences_list=sentences_list, filters=filters)
  write_to_file(output_filename, sentences_list, classes_list)