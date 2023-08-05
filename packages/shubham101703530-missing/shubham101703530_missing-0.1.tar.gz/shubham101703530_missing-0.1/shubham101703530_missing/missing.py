#!/usr/bin/env python
# coding: utf-8

# In[87]:
import pandas as pd
import numpy as np
import datawig
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from os import path


class MError(Exception): 
  
    # Constructor or Initializer 
    def __init__(self, value): 
        self.value = value 
  
    # __str__ is to print() the value 
    def __str__(self): 
        return(repr(self.value))




# In[57]:


def missingdata(dataset):
    if (dataset.shape[0]==0):
        return print("No data value in the dataset")
    nullclmns= dataset.columns[dataset.isnull().any()]
    #values to be replaced in place of the NaN
    filldata=pd.DataFrame(0,index=np.arange(len(dataset)),columns=nullclmns)
    
    for target in nullclmns:
      cells_with_null=dataset[target].isnull()
      cells_without_null=dataset[target].notnull()
      
      imputer=datawig.SimpleImputer(
              #columns containing information about the column we want to impute
              input_columns=dataset.columns[dataset.columns!=target],
              #column  for which we have to impute the values 
              output_column=target,
              #stores model data and its metrics
              output_path='imputer_model' 
              )
      #fitting the imputer model with non null columns 
      imputer.fit(train_df=dataset[cells_without_null],num_epochs=15)
      #predicting from the imputer model for the columns with null values 
      predicted=imputer.predict(dataset[cells_with_null])
      
      filldata[target]=predicted[target+'_imputed']
     
    
        
    #appending the dataset by replacing the NaN values with the values computed with the help of the imputer model 
    dataset=dataset.fillna(filldata)
    
    print("number of missing values replaced: ",filldata.notnull().sum().sum())
    
    return dataset


# In[64]:


def m_m_m(dataset,f):
    fill = dataset.isnull().sum().sum()
    for i in range(len(f)):
        if f[i]=='n':
            dataset.iloc[:,i].fillna(dataset.iloc[:,i].mean(),inplace=True)
        elif f[i]=='c':
            dataset.iloc[:,i].fillna(dataset.iloc[:,i].mode()[0],inplace=True)
        else:
            print('Wrong value in feature type')
    print("number of missing values replaced: ",fill)
    print(dataset)
    return dataset


# In[77]:


def drop_all(dataset):
    fill = dataset.isnull().sum().sum()
    dataset.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
    print("number of missing values replaced: ",fill)
    return dataset


# In[40]:


from sklearn.neighbors import KNeighborsClassifier

# In[102]:


def testing(d,f):
    score=[]
    for i in d:
        
        X_train, X_test, Y_train, Y_test = train_test_split(i.iloc[:,:-1], i.iloc[:,-1], test_size = 0.4)

        if f[-1]=='c':
          clf = KNeighborsClassifier()
          clf.fit(X_train,Y_train)
          score.append(clf.score(X_test, Y_test))
        elif f[-1]=='n':
          clf = LinearRegression()
          clf.fit(i.iloc[:,:-1], i.iloc[:,-1])
          score.append(clf.score(i.iloc[:,:-1], i.iloc[:,-1]))
    best_i = max(score[0],score[1],score[2])
    ind = score.index(best_i)
    h = ['dropna','mean/mode','impute']
    for i in range(3):
      print('score',str(h[i]),":",score[i])
    return d[ind]


# In[104]:


if len(sys.argv)!=4:
  print("Incorrect parameters...Input format:- python <Program_name> <Inputdatafile> <Outputdatafile> <comma separated feature types of each column, n for numerical and c for categorical>")
  exit(1)
f = sys.argv[3].split(',')
for i in f:
  if i not in ['n','c']:
    print("Enter type of feature correctly, only n or c")
    exit(1)
fname = sys.argv[1]
if not(path.exists(fname)):
  print('input directory doesn;t exists')
  exit(1)
dname = sys.argv[2]
if dname[-4:]!='.csv':
  print('output file is not of csv type')
else:
  dataset=pd.read_csv(sys.argv[1])
  print(len(dataset.columns))
  data1 = dataset.copy()
  data2 = dataset.copy()
  data3 = dataset.copy()
  f = sys.argv[3].split(',')
  print(f)
  dtstdrop = drop_all(data1)
  dtstmean_mode = m_m_m(data2,f)
  dtstimpute=missingdata(data3)

  d = [dtstdrop,dtstmean_mode,dtstimpute]
  df = testing(d,f)
  df.to_csv(sys.argv[2])


