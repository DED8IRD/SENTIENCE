"""
get_page_names.py

Gets page ids from csvs.
"""    

import os

if __name__ == '__main__':
    output = open("page_names", "w")
    # iterate through all the files in the current directory
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            output.write('\n'.join(str(filename.split('_')[0])))
