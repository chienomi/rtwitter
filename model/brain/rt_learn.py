# -*- coding: utf-8 -*-
import tensorflow as tf
from keras.layers import Input, Dense, Embedding, Convolution2D, Conv2D, MaxPooling2D, BatchNormalization, Dropout, Reshape, Flatten, concatenate, merge
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler, EarlyStopping, ModelCheckpoint, TensorBoard
from keras.models import Model, load_model
import numpy as np
import json

# include all files in the working directory
import os
import sys
try:
  sys.path.append(os.getcwd())
except:
  pass

from model.generator.generate_data import *
from model.param.rtwitter import *

def rtwitter_model(dim_emb=EMBEDDING_DIMENTION, input_length=INPUT_LENGTH, filter_sizes=(2, 3, 4, 5, 6), n_filter=NUMBER_OF_FILTERS, category_size=CATEGORY_SIZE, char_cutoff_dim=CHAR_CUTOFF_DIM):
  """ detect the categories of data """
  x = Input(shape=(input_length,)) # Input data of fixed length
  emb_0 = Embedding(CHAR_CUTOFF_DIM, dim_emb)(x)
  emb_1 = Reshape((input_length, dim_emb, 1))(emb_0)
  conv_layers = []
  array_conv_2 = []
  # learn by convolutions
  for dim_k in filter_sizes:
    conv_0 = Convolution2D(n_filter, dim_k, dim_emb, activation="relu")(emb_1)
    conv_1 = MaxPooling2D(pool_size=(input_length - dim_k + 1, 1))(conv_0)
    conv_layers.append(conv_1)
  conv_concat = concatenate(conv_layers)
  middle = Reshape((n_filter * len(filter_sizes),))(conv_concat)
  middle = BatchNormalization()(middle)
  middle = Dropout(DROPOUT_RATE)(middle)
  middle = Dense(dim_emb, activation="relu")(middle)
  middle = BatchNormalization()(middle)
  middle = Dropout(DROPOUT_RATE)(middle)
  final = Dense(category_size, activation='sigmoid')(middle)
  model = Model(input=x, output=final)
  return model

def train(x_array, y_array, batch_size=300, epoch_size=100, nu=LEARNING_RATE, model_path=MODEL_PATH, model_checkpoint_path=MODEL_CHECKPOINT_PATH):
  """ train the model defined above """
  # coordinate the learning rate
  nu_array = np.linspace(nu, LEARNING_RATE * nu, epoch_size)
  # create a model to learn
  model = rtwitter_model()
  optimizer = Adam(lr=nu)
  model.summary()
  model.compile(
    loss='binary_crossentropy',
    optimizer=optimizer,
    metrics=['accuracy']
  )
  # start learning
  model.fit(
    x_array, y_array,
    epochs=epoch_size, batch_size=batch_size, verbose=1,
    validation_split=0.1, shuffle=True,
    callbacks=[
      LearningRateScheduler(lambda epoch: nu_array[epoch]),
      EarlyStopping(monitor='val_loss', patience=LEARNING_PATIENCE, verbose=1, mode='auto'),
      ModelCheckpoint(filepath=model_checkpoint_path, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
      ]
  )
  model.save(model_path)

if __name__ == "__main__":
  ml_data = generate_ml_data(base_folder="ml_data", index_folder="rt_predictor")
  x_array = []; y_array = []
  for x, y in ml_data:
    x_array.append(x); y_array.append(y)
  x_array = np.array(x_array); y_array = np.array(y_array); y_array = one_hot(y_array, CATEGORY_SIZE)
  train(x_array, y_array)
