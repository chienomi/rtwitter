from model.param.rtwitter import *
import numpy as np
import MeCab
try:
  mecab = MeCab.Tagger('-Ochasen -d /root/local/lib/mecab/dic/mecab-ipadic-neologd')
except:
  mecab = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def generate_ml_data(base_folder, index_folder, max_length=INPUT_LENGTH, category_size=CATEGORY_SIZE):
  # generate data for CNN
  ml_data = []
  for y in range(category_size):
    filepath = base_folder + "/" + index_folder + "/" + str(y)
    with open(filepath) as f:
      for l in f:
        l = l.strip()
        x = phrase_to_numpy_array(l, max_length=max_length)
        ml_data.append([x, y])
  return ml_data

def phrase_to_numpy_array(l, max_length=INPUT_LENGTH, cutoff_dim=CHAR_CUTOFF_DIM, cutoff_mode="cut_tail", will_append_space=False, will_katakanize=True):
  x = []
  # ignore charactors whose ascii index is over cutoff_dim
  l = l.strip()
  if will_katakanize == True:
    l = katakanize(l)
  print("l: ", l)
  if will_append_space == True:
    l += " "
  for x_word in l:
    if will_katakanize == True and 1.2*10**4 < ord(x_word) < 1.3*10**4: # range of hiragana & katakana
      x_word = chr(ord(x_word)%1000 - 200)
    if ord(x_word) <= cutoff_dim:
      x.append(ord(x_word))
    else:
      x.append(42)
  # if length is over max_length, you can dump/cut_tail
  if len(x) > max_length:
    if cutoff_mode == "dump":
      return np.array([])
    elif cutoff_mode == "cut_tail":
      # cutoff element whose index is over or equal to max_length
      x = x[:max_length]
  if len(x) < max_length:
    # 0 padding
    x = x + ([0] * (max_length - len(x)))
  x = np.array(x)
  return x

def katakanize(text):
  mecab_array = mecab.parse(text).split("\n")
  mecab_array = [y.split("\t")[1] for y in mecab_array if len(y.split("\t"))>1]
  katakanized_text = " ".join(mecab_array)
  return katakanized_text

def prepare_dataset():
  ml_data = generate_ml_data(
    base_folder="ml_data",
    index_folder="rt_predictor",
    max_length=140,
    category_size=3
  )
  x_array = []
  y_array = []
  for x, y in ml_data:
    x_array.append(x)
    y_array.append(y)
  x_array = np.array(x_array)
  y_array = np.array(y_array)
  y_array = one_hot(y_array, 2)

def one_hot(y, category_size=2):
  # numpy array を one-hot ベクトルへ変換
  row_size = y.shape[0]
  one_hot_vector = np.zeros([row_size, category_size])
  for i in range(row_size):
    one_hot_vector[i][y[i]] = 1
  return one_hot_vector
