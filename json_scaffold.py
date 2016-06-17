import json
import sys
from uuid import uuid4
from datetime import timedelta, datetime
import time
import random
from loremipsum import get_paragraphs, Generator
import loremipsum
import nltk
import pickle

'''
corpera = {}

with open('corpera.pickle', 'w') as f:
  corpus_news = nltk.corpus.conll2002.sents('ned.train')[1000:]
  corpera['news'] = [" ".join(sent) for sent in corpus_news if len(sent) > 5]

  with open('mock_corpera/corpus_address.txt', 'r') as a:
    corpera['adress'] = [",".join(sent.split(",")[:2]) for sent in a.readlines()]
  pickle.dump(corpera, f)
'''



with open('mock_corpera/corpera.pickle', 'r') as f:
  corpera = pickle.load(f)

cats = {}
with open('mock_corpera/catnames_male.txt') as f:
  cats['male'] = [c for c in [cat.strip(' \t\n\r') for cat in f.readlines()] if len(c)]

with open('mock_corpera/catnames_female.txt') as f:
  cats['female'] = [c for c in [cat.strip(' \t\n\r') for cat in f.readlines()] if len(c)]


male_female = ['male', 'female']
all_cat_traits = ['playful', 'fierce', 'happy', 'silent', 'calm', 'cute', 'loving', 'bold', 'heroic', 'cunning', 'sweet', 'active', 'outgoing']


latlong_bounds = (51.939979,51.96225, 5.20061,5.244298)
gen_num = 0
current_dict = {}
def date(daysback=365, daysahead=0):
    start = datetime.now() - timedelta(days=abs(int(daysback)))
    end = datetime.now() + timedelta(days=int(daysahead))
    rand_date = (start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))))
    return int(time.mktime(rand_date.timetuple()))

def empty():
  return ""

def uuid():
  return str(uuid4())

def corpus_sent(corpus="news"): #  news | adress
  return random.choice(corpera[corpus])

def lipsum(paragraphs=2):
  return "\n".join(get_paragraphs(int(paragraphs)))

def lipsum_words(between_start=3, between_end=9):
  words = random.randint(int(between_start), int(between_end))

  return " ".join(" ".join(loremipsum.get_paragraphs(2)).split()[:words])

def value(v=""):
  return v

def array():
  return []

def object(elems=""):
  ret = {}

  keys = elems.split(",")
  for x in keys:
    ret[x] = ""

  return ret

def catname():
  cat = random.choice(cats[current_dict['gender']])
  cats[current_dict['gender']].remove(cat)
  return cat

def cat_traits():
  return random.sample(all_cat_traits, 2)

def randomnumber(start=100, end=1500):
  return random.randint(int(start), int(end))

def placekitten(width=250, height=250):
 
  width += gen_num
  height += gen_num
  return "http://placekitten.com/%i/%i" % (width, height)


def image(dim="300x300", cat="netherlands"):
  random.seed(time.time())
  rand_num = random.randint(100000, 999999)
  return "http://loremflickr.com/%s/%s?bust=%i" % (dim.replace("x", "/"), cat, rand_num) 

def gender():
  return random.choice(male_female)

def latlong():
  return {'latitude': random.uniform(*latlong_bounds[:2]), 'longitude': random.uniform(*latlong_bounds[2:])}

def generate(num, args):
  json_list = []

  for x in range(0, int(num)):
    global gen_num
    gen_num = x
    json_dict = {}
    global current_dict
    for a in args:

      vals = a.split(":")
      generator = 'uuid' if len(vals) == 1 else vals[1]

      gen_args = []
      if(len(vals) > 1):    
        gen_args = vals[2:]

      json_dict[vals[0]] = globals()[generator](*gen_args)

      current_dict = json_dict
     


    json_list.append(json_dict)

  return json.dumps(json_list,  indent=2, sort_keys=True)



def main():
  print generate(sys.argv[1], [a for a in sys.argv[2:]])


if __name__ == "__main__":
  main()
