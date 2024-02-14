# -*- coding: utf-8 -*-
"""Voc.ipynb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rotbjyC_1EfYg3H9aKsJAJ0vJPbbAciY
"""

import time
import numpy as np
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup
from google.colab import files

# ToDict Port
def data_search(word: str): #dict
  word = word.lower()
  url = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/" + word
  headers = {
    "content-type": "text/html; charset=UTF-8",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
  content = rq.get(url, headers=headers).text
  soup = BeautifulSoup(content, "html.parser")
  if word.count(" "): # phrase
    divSet = soup.find_all("div", {"class": "pv-block"})
  else: # voc
    divSet = soup.find_all("div", {"class": "pr entry-body__el"})

  data = {}
  for div in divSet:
    POS = div.find("span", {"class": "pos dpos"}).string
    meanSet = div.find_all("span", {"class": "trans dtrans dtrans-se break-cj"})
    meanSet = [mean.text.replace(";", "，").split("，") for mean in meanSet]
    for mean in meanSet:
      data.setdefault(POS, []).extend(mean)

  #idiom
  divSet = soup.find_all("div", {"class": "pr idiom-block"})
  for div in divSet:
    POS = "idiom"
    meanSet = div.find_all("span", {"class": "trans dtrans dtrans-se break-cj"})
    meanSet = [mean.string.replace(";", "，").split("，") for mean in meanSet]
    for mean in meanSet:
      data.setdefault(POS, []).extend(mean)
  return data

def user_search(word: str): #void
  data = data_search(word)
  for POS, MeanSet in data.items():
    print(f"  {POS}")
    print(f"    {' / '.join(MeanSet)}")

# ToInput Port
class Voc:
  def __init__(self, word: str, pos: str, mean: str):
    self.word = word
    self.pos = pos
    self.mean = mean

  def show(self):
    print(f"{self.word}: <{self.pos}>\n\t {self.mean}")

  def toList(self): #list
    return [self.word, self.pos, self.mean]

def dismantle(word: str): #list<Voc>
  result = []
  curVoc = data_search(word)
  leng = len(curVoc);
  for pos, mean in curVoc.items():
    result.append(Voc(word, pos, "/".join(mean)))
  return result

def selection(mean: str): #str
  result = []
  meanSet = mean.split("/")
  if len(meanSet) < 5: return mean
  theKept = input()
  for idx in range(len(meanSet)):
    try:
      if theKept[idx] == "0": continue
      result.append(meanSet[idx])
    except:
      result.append(meanSet[idx])
  return "/".join(result)

def typein(): #list<Voc>
  vocSet = []
  error = []
  while True:
    try:
      order = input().lower()
      if order == "!": break
      if order == "<": vocSet.pop()
      vocData = dismantle(order)
      if vocData == []: error.append(order)
      vocSet.extend(vocData)
    except:
      break
  if error != []: print(error)
  return vocSet

#To DataBase Port
def csvMake(data: list): #DataFrame
  columns = ["word", "pos", "mean"]
  df = pd.DataFrame()
  for voc in data:
    df = df.append([voc.toList()], ignore_index=True)
  df.columns=columns
  return df

def output(data, filename: str): #.csv
  data.to_csv(filename)
  files.download(filename)

def paste(fileList: list): #Dateframe
  main = pd.DataFrame()
  dfList = []
  for filename in fileList:
    dfTmp = pd.read_csv(filename, index_col=[0])
    dfList.append(dfTmp)
  main = pd.concat(dfList, ignore_index=True)
  main.sort_values(by=["word", "pos"], inplace=True)
  main.drop_duplicates(subset=["word", "pos"], keep="first", inplace=True)
  main.reset_index(drop=True)
  return main

# ToUser Port
def randomVoc(number: int, filename: str): #DataFrame
  data = pd.read_csv(filename, index_col=[0])
  selected = pd.DataFrame()
  size = len(data)
  for i in range(number):
    idx = np.random.randint(0, size-1)
    selected = selected.append(data.loc[idx])
  return selected

def modify(filename: str): #DataFrame
  data = pd.read_csv(filename, index_col=[0])
  size = len(data)
  for idx in range(size):
    theVoc = data.loc[idx:idx, "word":"mean"]
    word = theVoc.loc[idx]["word"]
    Voc(word, theVoc.loc[idx]["pos"], theVoc.loc[idx]["mean"]).show()
    data.loc[idx]["mean"] = selection(theVoc.loc[idx]["mean"])
  return data

output(csvMake(typein()), "sample.csv")