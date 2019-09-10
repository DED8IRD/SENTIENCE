# PLAN

Refactor S E N T I E N C E into Django 2.0 web app with DRF API for Inferno.js frontend.

## TASKS
1. Update scraper + post_compilation
	- Only generate post_compilation text file with new data
	- Make scraper more efficient
	- Delete CSV content (except row for latest entry)
	- Split post_comp into 10mb files 

2. (a) Either improve model generator and Markov chain generator... 
	- Caching?
	- Steal features of Markovify's generator

   (b) ... or scrap for Markovify entirely
   	- Replace ngram_generator with Markovify extension class
   		- Customize sentence splitter
   		- Play with state size
   		- Maybe integrate POS model using Spacy

3. Convert Django 1.0 > 2.0 
	- Convert modules from python 2.7 to 3.6
	- Possibly just rebuild from scratch (better idea)

4. Set up DRF API endpoints

5. Create new features:
	- Automatic posting to FB
	- User management system
		- Maybe integrate FB + Google OAuth
		- Maybe create paid user group to allow them to generate their own shitposts?
	- Submission form for source images
		- Require moderator to accept first 
	- Shitpost model has many to many field for source images 
		- Create view to filter shitposts by src img 
		- Maybe allow shitposts to be tagged by these src images?
	- Big ol donate button 


# Playing with Markovify
```py 
import markovify
import re
import spacy
from datetime import datetime

nlp = spacy.load("en")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]
    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


# with open('post_compilation_shuffled.txt', 'rb') as f:
#     start = datetime.now()
#     pos_model_ro = POSifiedText(str(f.read()), retain_original=False)
#     finish = datetime.now()
#     print(f'RETAIN_ORIGINAL POSified MODEL CREATED IN {finish-start}')


with open('post_compilation_shuffled.txt', 'rb') as f:
    corpus = f.read()

start = datetime.now()
pos_model = POSifiedText(str(corpus), state_size=3)
finish = datetime.now()
print(f'POSified MODEL CREATED IN {finish-start}')

start = datetime.now()
reg_model = markovify.Text(str(corpus), state_size=3)
finish = datetime.now()
print(f'REGULAR MODEL CREATED IN {finish-start}')
```