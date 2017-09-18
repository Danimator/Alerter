from bs4 import BeautifulSoup
from urlparse import urljoin
from datetime import datetime
from dateutil import parser
import requests
import training
import pytz

urls = {
    "reddit": "https://www.reddit.com/r/popular/",
    "cbc": "http://www.cbc.ca/news/world",
    "national-post": "http://nationalpost.com/category/news/world",
    "globe-and-mail": "https://beta.theglobeandmail.com/world/",
    "globe-and-mail-canada": " https://beta.theglobeandmail.com/canada/"
}

sources = {
    "reddit": "Reddit",
    "cbc": "CBC",
    "national-post": "National Post",
    "globe-and-mail": "Globe and Mail",
    "globe-and-mail-canada": "Globe and Mail Canada"
}

headers = {
    'User-Agent': 'Chrome/60.0.3112.113'
}

indicator_word_scores = {
    "found": 1,
    "shot": 3,
    "dead": 4,
    "deceased": 4,
    "alive": 4,
    "discovered": 2,
    "missing": 3,
    "hurricane": 5,
    "disaster": 5,
    "miracle": 3,
    "solved": 2,
    "tornado": 3,
    "assault": 4,
    "bloody": 2,
    "blood": 2,
    "derail": 4,
    "abuse": 3,
    "abuser": 3,
    "abusing": 3,
    "revelation": 2,
    "amber": 4,
    "just": 1,
    "lost": 3,
    "accuses": 3,
    "accused": 3,
    "accuse": 3,
    "accusing": 3,
    "condemn": 2,
    "condemns": 2,
    "mysterious": 2,
    "attack": 3,
    "attacks": 3,
    "breach": 4,
    "protest": 2,
    "protests": 2,
    "death": 4,
    "unexpected": 3,
    "dies": 4,
    "prevent": 3,
    "relief": 1,
    "since": 1,
    "nuclear": 4,
    "destruction": 4,
    "mass": 1,
    "pay": 1,
    "ordered": 1,
    "damages": 2,
    "damaged": 2,
    "appeal": 2,
    "accident": 3,
    "battle": 3,
    "unclear": 1,
    "executing": 3,
    "execute": 3,
    "hit": 3,
    "emergency": 3,
    "tsunami": 4,
    "earthquake": 4,
    "quake": 4,
    "missile": 3,
    "update": 2,
    "breaking": 5,
    "unidentified": 2,
    "arson": 5,
    "burning": 3,
    "radiation": 4,
    "debt": 1,
    "destroyed": 3,
    "military": 1,

}

alert_threshold = 4

def getTitleScore(title):
    keyword_score = 0
    # bag of words approach
    stripped_title = "".join([c if (c.isalnum() or c==" ") else "" for c in title]).lower().split()
    for word in stripped_title:
        if word in indicator_word_scores:
            keyword_score += indicator_word_scores[word]
    naive_bayes_score = training.get_score(title)
    return keyword_score+naive_bayes_score

def get_site_feed(site, keywords, urgency):
    results = []
    url = urls[site]
    response = requests.get(url, headers=headers)
    htmlSoup = BeautifulSoup(response.content, "html.parser")

    if site == "reddit":
        stories = htmlSoup.find_all("div", "thing")
        for story in stories:
            story_title =  story.find("a", "title").get_text().encode("utf-8")
            story_url = urljoin(url, story.find("a", "title").get('href')) #fix relative links

            #storyResponse = requests.get(story_url, headers=headers)
            #storySoup = BeautifulSoup(storyResponse.content, "html.parser")

            story_datetime = parser.parse(story.find("time").get("datetime")).replace(tzinfo=pytz.UTC)
            print story_datetime
            print story_title
            print story_url

            story_score = getTitleScore(story_title)
            story_score += 0 if passesKeywordCheck(story_title, keywords, urgency) else -100
            if story_score >= alert_threshold:
                results.append({
                    "title": story_title,
                    "time": story_datetime,
                    "url": story_url,
                    "score": story_score,
                    "source": sources[site]
                })
    elif site == "cbc":
        stories = htmlSoup.find_all("a", "pinnableHeadline")
        for story in stories:
            story_title = story.get_text()
            story_url =  urljoin(url, story.get('href'))

            storyResponse = requests.get(story_url, headers=headers)
            storySoup = BeautifulSoup(storyResponse.content, "html.parser")

            story_datetime = storySoup.find("span", "delimited").get_text()[8:]
            story_datetime = parser.parse(story_datetime).replace(tzinfo=pytz.UTC)
            print story_datetime

            story_score = getTitleScore(story_title)
            story_score += 0 if passesKeywordCheck(story_title, keywords, urgency) else -100
            if story_score >= alert_threshold:
                results.append({
                    "title": story_title,
                    "time": story_datetime,
                    "url": story_url,
                    "score": story_score,
                    "source": sources[site]
                })
    elif site == "globe-and-mail" or site == "globe-and-mail-canada":
        stories = htmlSoup.find_all("div", "o-card")
        for story in stories:
            story_title =  story.find("span", "o-card__content-text").get_text().encode("utf-8")
            story_url = "https://beta.theglobeandmail.com" + story.find("a").get('href') #fix relative links
            print "STORY URL:  ", story_url
            print url
            print story.find("a").get('href')
            try:
                story_datetime = parser.parse(story.find("time").get("datetime")).replace(tzinfo=pytz.UTC)
                print story_datetime
                print story_title
                print story_url 

                story_score = getTitleScore(story_title)
                story_score += 0 if passesKeywordCheck(story_title, keywords, urgency) else -100
                if story_score >= alert_threshold:
                    results.append({
                        "title": story_title,
                        "time": story_datetime,
                        "url": story_url,
                        "score": story_score,
                        "source": sources[site]
                    })
            except:
                pass
    return results
    '''elif site == "national-post":
        stories = htmlSoup.find_all("h2", "entry-title").extend(htmlSoup.find_all("h4", "entry-title"))
        print htmlSoup
        for story in stories:
            story_title = story.find("a").get_text()
            story_url =  urljoin(url, story.find("a").get('href'))
            
            storyResponse = requests.get(story_url, headers=headers)
            storySoup = BeautifulSoup(storyResponse.content, "html.parser")

            story_datetime = storySoup.find("time").get("datetime")

            print story_datetime
            print story_title
            print story_url'''

def passesKeywordCheck(title, keywords, urgency):
    if keywords == []:
        return True
    stripped_title = stripped_title = "".join([c if (c.isalnum() or c==" " or c=="-") else "" for c in title]).lower().split()
    if urgency == 1:
        for word in stripped_title:
            if word in keywords:
                return True
        return False
    else:
        for word in stripped_title:
            if word in keywords:
                return False
        return True
