# -*- coding: utf-8 -*-
"""evaluate.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YGfu4LT9Uy3uxDOFewP8-vbWdJC9_N4T
"""

from sklearn.svm import OneClassSVM
#import time
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import seaborn as sns
#import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons, make_blobs
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from pyod.models.knn import KNN
from pyod.models.abod import ABOD
from pyod.models.hbos import HBOS
import tensorflow as tf
import keras
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers
from sklearn.preprocessing import  StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score,confusion_matrix

def plot_var_in_out(X,y,var1,var2,var3,var4):
  x1 = X[:,var1]
  x2 = X[:,var2]
  x3 = X[:,var3]
  x4 = X[:,var4]

  fig = plt.figure(figsize=(20,18))

  ax0 = fig.add_subplot(5,3,1)
  ax0.scatter(x1, x2, alpha=0.7, c=y)
  ax0.set_title('Représentation des données selon les variables ' +str(var1)+ ' et '+ str(var2))
  ax0.set_xlabel('variable '+str(var1)) 
  ax0.set_ylabel('variable '+str(var2)) 

  ax1 = fig.add_subplot(5,3,2)
  ax1.scatter(x1, x3, alpha=0.7,  c=y)
  ax1.set_title('Représentation des données selon les variables ' +str(var1)+ ' et '+ str(var3))
  ax1.set_xlabel('variable '+str(var1))
  ax1.set_ylabel('variable '+str(var3))

  ax2 = fig.add_subplot(5,3,3)
  ax2.scatter(x1, x4, alpha=0.7,  c=y)
  ax2.set_title('Représentation des données selon les variables ' +str(var1)+ ' et '+ str(var4))
  ax2.set_xlabel('variable '+str(var1))
  ax2.set_ylabel('variable '+str(var4))

  plt.tight_layout()
  plt.show()

def evaluation_detection(X_test,ytrue,ypred, var1 = 10, var2 = 20):
    
  ind_col = np.zeros(len(ytrue))
  ytrue = np.squeeze(np.asarray(ytrue))
  ind_col[(ytrue == -1)&(ypred == -1)] = 1
  ind_col[(ytrue == 1)&(ypred == -1)] = 2
  ind_col[(ytrue == -1)&(ypred == 1)] = 3

  classes = ['Inlier en test et en prediction','Outlier en test et en prediction','Inlier manqué par le modèle','Outlier manqué par le modèle']
  col = ['yellow','green','blue','red']

  fig = plt.figure(figsize=(14,18))

  ax0 = fig.add_subplot(5,2,1)
  data = confusion_matrix(ytrue, ypred)
  # labels = ['Outlier', 'Inliers']
  labels = ['Inliers', 'Outliers'] #inlier = -1, outlier = 1
  sns.heatmap(data, xticklabels = labels, yticklabels = labels, annot = True, fmt='d', cmap="Reds", ax=ax0) 
  ax0.set_title('Matrice de confusion')

  ax1 = fig.add_subplot(5,2,2)
  base = X_test[np.where(ind_col == 0)]
  x1 = base[:,var1]
  x2 = base[:,var2]
  ax1.scatter(x1, x2, alpha = 0.7,c=col[0], label = classes[0])
  base = X_test[np.where(ind_col == 1)]
  x1 = base[:,var1]
  x2 = base[:,var2]
  ax1.scatter(x1, x2, alpha = 0.7,c=col[1], label = classes[1])
  base = X_test[np.where(ind_col == 2)]
  x1 = base[:,var1]
  x2 = base[:,var2]
  ax1.scatter(x1, x2, alpha = 0.7,c=col[2], label = classes[2])
  base = X_test[np.where(ind_col == 3)]
  x1 = base[:,var1]
  x2 = base[:,var2]
  ax1.scatter(x1, x2, alpha = 0.7,c=col[3], label = classes[3])
  ax1.set_title('Représentation des données selon la différence entre le vrai label et la prévision')
  ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Catégorie")
  ax1.set_xlabel('x1') 
  ax1.set_ylabel('x2') 

  plt.tight_layout()
  plt.show()

def deep_predict(model,X_test_scaled,outlier_prop,y_test):
  ypred = model.predict(X_test_scaled)
  mse = np.mean(np.power(X_test_scaled - ypred, 2), axis=1)
  df_error = pd.DataFrame({'reconstruction_error': mse})
  outliers = df_error.index[df_error.reconstruction_error > outlier_prop].tolist()
  y_pred = np.ones(len(y_test))
  y_pred[outliers] = -1
  return y_pred

def evaluate(ytrue,ypred):
  
    CM = confusion_matrix(ytrue, ypred)
    # # TN = CM[0][0]
    # # FN = CM[1][0]
    # # TP = CM[1][1]
    # # FP = CM[0][1]
    # outlier = 1, inlier = -1
    TN = CM[1][0]
    FN = CM[0][1]
    TP = CM[0][0]
    FP = CM[1][0]

    # round metrics
    metrics = pd.DataFrame([],columns=['accuracy','recall','True negative rate','False discovery rate'])
    metrics['accuracy'] = [np.round(accuracy_score(ytrue,ypred),3)]
    metrics['recall'] = [np.round(recall_score(ytrue,ypred,average='macro'))]
    metrics['True negative rate'] = [np.round(FN/(TP+FN))]
    metrics['False discovery rate'] = [np.round(FP/(TP+FP))]

    return metrics


    
    
    
    
    
    
    
    



