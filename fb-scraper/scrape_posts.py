'''  
scrape_posts.py

Scrapes Facebook pages from page_names (pre-approved text list of public pages
that expressed permission to use their content) for only text content.

Modified from Minimaxir's Facebook page scraper. 
Python 2.7 compatible.
'''

from __future__ import unicode_literals
from util import keys
import requests, json, datetime, csv, time, os, tempfile, shutil

app_id = keys.APP_ID
app_secret = keys.APP_SECRET
access_token = app_id + "|" + app_secret
pages = [line.strip() for line in open("page_names", 'r')]

def request_until_succeed(url):
    r = requests.get(url)
    success = False
    while success is False:
        try: 
            r = requests.get(url)
            if r.status_code == 200:
                success = True
        except Exception as e:
            print (e)
            time.sleep(5)

            print ("Error for URL %s: %s" % (url, datetime.datetime.now()))
            print ("Retrying.")

    return r.text


# Needed to write tricky unicode correctly to csv
def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, \
                            0x201D:0x22, 0xa0:0x20 }).encode('utf-8')


# Checks if post already in existing csv
def check_existing_post(post_id, csv_file):
    for row in csv_file:
         if post_id in row[0]:
            return True

# Creates tempfile copy of existing csv
def create_temp_copy(path):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'temp_csv')
    shutil.copy2(path, temp_path)
    return temp_path


def getFacebookPageFeedData(page_id, access_token, num_statuses):

    # Construct the URL string
    base = "https://graph.facebook.com/v2.6"
    node = "/%s/posts" % page_id 
    fields = "/?fields=message,link,created_time,type,name,id," + \
            "comments.limit(0).summary(true),shares,reactions" + \
            ".limit(0).summary(true)"
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = "%s%s%s%s" % (base, node, fields, parameters)
    
    # retrieve getFacebookPageFeedData
    data = json.loads(request_until_succeed(url))

    return data


def processFacebookPageFeedStatus(status, access_token):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id       = status['id']
    status_message  = '' if 'message' not in status.keys() \
                         else unicode_normalize(status['message'])
    link_name       = '' if 'name' not in status.keys() \
                         else unicode_normalize(status['name'])
    status_type     = status['type']
    status_link     = '' if 'link' not in status.keys() \
                         else unicode_normalize(status['link'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(
            status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + \
            datetime.timedelta(hours=-5) # EST
    status_published = status_published.strftime(
            '%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs

    # Return a tuple of all processed data
    return (status_id, status_message, link_name, status_type, status_link,
            status_published)


def scrapeFacebookPageFeedStatus(page_id, access_token):
    filename = page_id + '_facebook_statuses.csv'
    existing = None
    try:
        existing = create_temp_copy(filename)
        with open(existing, 'rb') as original: 
            temp = list(csv.reader(original))
    except IOError, OSError:
        pass

    with open(filename, 'wb') as file: 
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "link_name", \
                    "status_type", "status_link", "status_published"])

        has_existing_post = False
        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()

        print ("Scraping %s Facebook Page: %s\n" % (page_id, \
                scrape_starttime))

        statuses = getFacebookPageFeedData(page_id, access_token, 100)

        while has_next_page and not has_existing_post:
            for status in statuses['data']:
                if existing != None and \
                    check_existing_post(status['id'], temp): 
                        has_existing_post = True
                        break 

                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    w.writerow(processFacebookPageFeedStatus(status,
                        access_token))

                # output progress occasionally to make sure code is not
                # stalling
                num_processed += 1
                if num_processed % 100 == 0:
                    print ("%s Statuses Processed: %s" % \
                        (num_processed, datetime.datetime.now()))

            # if there is no next page, we're done.
            if 'paging' in statuses.keys():
                statuses = json.loads(request_until_succeed(
                                        statuses['paging']['next']))
            else:
                has_next_page = False

        print ("\nDone!\n%s Statuses Processed in %s" % \
                (num_processed, datetime.datetime.now() - scrape_starttime))
    
        if existing:
            with open(existing, 'r') as existing:
                existing = csv.reader(existing)
                for row in existing:
                    if row != ["status_id", "status_message", "link_name", \
                         "status_type", "status_link", "status_published"]:
                            w.writerow(row)


if __name__ == '__main__':
	for page_id in pages:
	    scrapeFacebookPageFeedStatus(page_id, access_token)
