# webscrapernews.py
# Data Scraper: Hacker News Y-Combinator
# Organizing Hacker News YC news by: 1) Title 2) Title link 3) 100+ community votes


#importing libraries to: request access to page; scrape data; organize results
import requests
from bs4 import BeautifulSoup
import pprint


# request access to pages; obtaining read only text, links to titles, and number of votes
res = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links = soup.select('.titleline > a')
links2 = soup2.select('.titleline > a')
subtext = soup.select('.subtext')
subtext2 = soup2.select('.subtext')

# linking page 1 and page 2 search results
mega_links = links + links2
mega_subtext = subtext + subtext2


# sorting hnlist from high to low(reverse). Sorting w/ key 'votes'
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

# create list for data scrape results
def create_custom_hn(links, subtext):
    hn = []
    
    # Loop through index of title, link, votes
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        
        # obtain numerical value only of votes; if >99 votes -> append to hn list
        if len(vote):
            points = int(vote[0].getText().replace(' points', ""))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
   
   return sort_stories_by_votes(hn)
