import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links = soup.select('.titleline > a')
links2 = soup2.select('.titleline > a')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

# adding 2nd page to scrape

mega_links = links + links2
mega_subtext = subtext + subtext2
# Step 1 - get data
# get request -> HTML files from site as a string
# res.text -> get all the data (unfiltered)
# beautifulsoup used to parse(turn from string to a soup object -> manipulate/use)
# -> can pull from any HTML section of text (ex. body, content, div, a (a-tags = links), etc)
# Use cases: find_all, select
# Need CSS selectors to get data (.select - to pull from nested data)
# -> Get CLASS of titleline links + scores/votes.
# subtext used bc some don't have votes (don't have CLASS='score')

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

# sorting hnlist from high to low(reverse). Sorting w/ key 'votes'

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ""))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))

# Step 2
# loop thru index to enumerate (grabbing both link + subtext) into:
# -> title (w/ just text); href (title link); points(votes w/ removing ' points')
# idx used to make sure each result matches
# vote = check subtext if there's score -> if len score True -> add to dict.
# points >99 -> append to hackernews
# pprint = nicer format spacing
