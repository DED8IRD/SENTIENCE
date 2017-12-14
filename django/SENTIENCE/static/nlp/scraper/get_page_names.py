"""
get_page_names.py

Gets page ids from csvs.
"""    

import os

if __name__ == '__main__':
    mydir = os.path.abspath(os.path.dirname(__file__))
    output = open(os.path.join(mydir, "page_names"), 'w')
    inactive_pages = open(os.path.join(mydir, "rip_pages"), 'r').read()
    # iterate through all the files in the current directory
    for filename in os.listdir(mydir):
        if filename.endswith('.csv'):
            page = str(filename.split('_')[0])
            if page not in inactive_pages:
                output.write(page + '\n')
