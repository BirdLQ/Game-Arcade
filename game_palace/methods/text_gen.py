import numpy as np
import random
import re
from collections import defaultdict
#import os

#cur_path = os.path.dirname(__file__)

#path = os.path.relpath('..\\data\\words.txt', cur_path)

with open('data/words.txt') as f:
  text = f.read()
tokenized_text = [
    word
    for word in re.split('\W+', text)
    if word != ''
]
 
# Create graph.
markov_graph = defaultdict(lambda: defaultdict(int))

last_word = tokenized_text[0].lower()
for word in tokenized_text[1:]:
  word = word.lower()
  markov_graph[last_word][word] += 1
  last_word = word
    
def walk_graph(graph, distance=5, start_node=None):
  """Returns a list of words from a randomly weighted walk."""
  if distance <= 0:
    return []
  
  # If not given, pick a start node at random.
  if not start_node:
    start_node = random.choice(list(graph.keys()))
  
  weights = np.array(
      list(markov_graph[start_node].values()),
      dtype=np.float64)
  # Normalize word counts to sum to 1.
  weights /= weights.sum()

  # Pick a destination using weighted distribution.
  choices = list(markov_graph[start_node].keys())
  try:
    chosen_word = np.random.choice(choices, None, p=weights)
  except:
    chosen_word = 'a'
  
  return [chosen_word] + walk_graph(
      graph, distance=distance-1,
      start_node=chosen_word)

def words_sentence():
    result = str()
    for i in range(30):
      result+= ' '.join(walk_graph(
          markov_graph, distance=12))
    return result