
#!/usr/bin/env python
'''
 get_posts.py
 Gets post data from csv files in this directory.
'''

import zipfile, argparse, os, csv, re
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
            with open(filename, encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)          # read rows into a dictionary format
                for row in reader:                  # read a row as {col1: val1, col2: val2, ..}
                    for (k,v) in row.items():       # go over each column name and value 
                        if k == attr:               # if the column is the desired attribute
                            columns[k].append(v)    # append the values to the column[attr]

    return columns[attr]


###############################################################################
## Program Entry Point ########################################################
###############################################################################
if __name__ == '__main__':
    with open("post_compilation.txt", "w", encoding='utf-8') as output:
            posts = getAttrLists('status_message')
            for post in posts:
                if len(post) > 0:
                    # To deal with page quote prevalence
                    if not re.match(r'^.* .* .*:', post) \
                        and not re.search(r'The Meme Games', post) \
                        and not re.search(r'Surface Reality', post) \
                        and not re.search(r'The Epic Department', post) \
                        and not re.search(r'The Content Zone', post) \
                        and not re.search(r'Kevin 3', post) \
                        and not re.search(r'The Needle Drop', post):
                        output.write(post + '\n\n')
