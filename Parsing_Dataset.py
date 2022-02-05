import numpy as np
import pandas as pd
import re


answers = pd.read_csv('posts_answers.csv')
questions = pd.read_csv('posts_questions.csv')
cdata = questions[['id', 'title', 'body', 'tags']]
cdata['tags'] = data['tags'].astype('str')
cdata.head()
mltags = '''
tensorflow

tensorflow2.0

tensorflow-gpu

tensorflow2.x

tensorflow1.15

tensorflow2

tensorflow-layers

tensorflow1.12

torch

pytorch

torchvision

torchtext

pytorch-dataloader

gpytorch

torchaudio

pytorch3d

keras

keras-2

keras-metrics

keras-rl

keras-vggface

keras-lambda

tf.keras

keras-layer

datascience

data science

ml'''
mltags = mltags.split('\n')
mltags = [tag for tag in mltags if tag != '']
mltags, len(mltags)
mask = pd.Series(-1, np.arange(len(cdata)))
for tag in mltags:
    mask = mask + cdata['tags'].str.find(tag) + 1
mask[mask >= 0] = 1
mask[mask < 0] = 0
mask = mask.astype('bool')
mldata = cdata[mask]
questions.drop(columns=["parent_id"], inplace=True)
questions.rename(columns={"id" : "parent_id", "body" : "questions"}, inplace=True)
answers.rename(columns={"body" : "answers"}, inplace=True)
qa = questions.merge(answers, on=['parent_id'])
col = qa.columns
for i in col:
  if i != "answers" and i != "questions":
    qa.drop(columns=i, inplace=True)
col = qa.columns
for j in col:
  for i in range(len(qa[j])):
    killmentions = re.compile('^@[A-Za-z]+|.+ @[A-Za-z]+')
    clear_text_1 = killmentions.sub('', qa[j][i])
    killtags = re.compile('<.*?>')  
    clear_text_2 = killtags.sub('', clear_text_1)
    killslashn = re.compile('\n')
    qa[j][i] = killslashn.sub('', clear_text_2)
qa.to_csv('dataset.csv')