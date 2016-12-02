
#!/usr/bin/env python
'''
 get_posts.py
 Gets post data from csv files in this directory.
 Python 2.7 compatible.
'''

from __future__ import unicode_literals
import os, csv, re, io
from collections import defaultdict

###############################################################################
## Utility Functions ##########################################################
###############################################################################

def getAttrLists(attr):
    """
    Processes all csv files within the current directory and returns the columns
    associated with the attribute attr.
    Assumption: this python program is in the same directory as the training files.
    """
    columns = defaultdict(list) # each value in each column is appended to a list

    # iterate through all the files in the current directory
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            with open(filename, 'rb') as f:
                reader = csv.DictReader(f)   # read rows into as dict (col:val)
                for row in reader:
                    for (k,v) in row.items(): 
                        if k == attr:
                            v = v.decode('utf-8', errors='replace')
                            columns[k].append(v)

    return columns[attr]


###############################################################################
## Program Entry Point ########################################################
###############################################################################
if __name__ == '__main__':
    with io.open("post_compilation", "w", encoding='utf-8') as output:
            posts = getAttrLists('status_message')
            for post in posts:
                if len(post) > 0:
                    # To deal with page quote prevalence
                    if not re.match(r'^.* .* .*:', post) \
                        and not re.search(r'The Great Gatsby by F. Scott Fitzgerald', post) \
                        and not re.search(r'The Meme Games', post) \
                        and not re.search(r'Surface Reality', post) \
                        and not re.search(r'The Epic Department', post) \
                        and not re.search(r'The Content Zone', post) \
                        and not re.search(r'Kevin 3', post) \
                        and not re.search(r'The Needle Drop', post):
                            # To deal with non-punctuated post ends we insert
                            # a special unicode marker
                            for line in post.split('\n'):
                                output.write(line + u'\U0000FFFF\n')
