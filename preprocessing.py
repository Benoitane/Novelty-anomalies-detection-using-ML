# -*- coding: utf-8 -*-
"""preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xZNwq4_a1Rbxn2dRs-QMsIJYntIc33n8
"""

from scipy import stats
import scipy.io
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import  StandardScaler, MinMaxScaler


def upload_data(path):
  mat = scipy.io.loadmat(path)
  X, y = mat['X'], mat['y']
  y = y.astype(np.int64)
  y[y == 1] = -1
  y[y == 0] = 1
  return X,y

def split_data(split_method, X, y):
  mask = np.where(y == 1)[0][:int(len(y[y == 1])*0.80)]
  index = list(np.arange(len(y)))
  anti_mask = list(set(index).difference(set(mask)))
  if split_method == "anomalies":
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
  if split_method == "nouveautes":
    X_train, X_test, y_train, y_test = X[mask], X[anti_mask], y[mask], y[anti_mask]
  return X_train, X_test, y_train, y_test

def prepro_data(path,type_):
  X, y = upload_data(path)
  X_train, X_test, y_train, y_test = split_data(type_,X,y)
  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled  = scaler.transform(X_test)
  return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled



