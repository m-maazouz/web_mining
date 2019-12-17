# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 22:45:09 2019

@author: LENOVO
"""
"""
What is BeautifulSoup? BeautifulSoup is a third party Python library from Crummy.
The library is designed for quick turnaround projects like screen-scraping What can it do?
Beautiful Soup parses anything you give it and does the tree traversal stuff for you
"""
# installing beautifulsoup using pip
# >>>>>> pip install bs4
#"https://www.hespress.com" 

from textpros import textPros as tp
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen , Request
from datetime import date
import csv

period = 1

def month_to_number(argument):
    if argument == "يناير" :
        return 1
    if argument ==  "فبراير" :
        return 2
    if argument ==  "مارس" :
        return 3
    if argument ==  "أبريل" :
        return 4
    if argument ==  "ماي" :
        return 4
    if argument ==  "يونيو" :
        return 6
    if argument ==  "يوليوز" :
        return 7
    if argument ==  "غشت" :
        return 8
    if argument ==  "شتنبر" :
        return 9
    if argument == "أكتوبر"  :
        return 10
    if argument == "نونبر"  :
        return 11
    if argument == "دجنبر"  :
        return 12

def check_topics(topic_urls,field):
    for topic_url in topic_urls:
    
        topic_req = Request("https://www.hespress.com"+topic_url, headers={'User-Agent': 'Mozilla/5.0'})
        # opens the connection and downloads html page from url
        cnx = urlopen(topic_req)
        html_topic_page = cnx.read()
        #parse html
        soup_topic_page = soup(html_topic_page, "html.parser")
        cnx.close()    
        topic_date = soup_topic_page.find("div", {"class": "story_stamp"}).span.text.split()
        day = topic_date[1]
        mounth = month_to_number(topic_date[2])
        year = topic_date[3]
        today = date.today()
        topic_date = date(int(year), int(mounth), int(day))
        duration = today - topic_date
    
        if duration.days < period :
            
            topic_date = soup_topic_page.find("div", {"class": "story_stamp"}).span.text
            topic_titel = soup_topic_page.find("h1", {"class": "page_title"}).text
            topic_titel = topic_titel.replace('\"','')
            topic_titel = topic_titel.replace(':','')
            comments = soup_topic_page.findAll("div", {"class": "comment_holder"})
            for comment in comments :
                comment_text = comment.div.div.div.find("div", {"class": "comment_text"})
                for e in comment_text.findAll('br'):
                    e.extract()
                comment_text = comment_text.text.replace('\"','')
                comment_text = comment_text.replace(',','')
                comment_text = comment_text.replace('\n',' ')
                comment_text = comment_text.strip()
                duration_days = duration.days
                if duration_days == 0 :
                    duration_days = "today"
                else:
                    duration_days = str(duration.days) + " day ago"
                comment_date = comment.div.div.div.span.text.rstrip()
                
                if comment.div.div.div.strong is None :
                    comment_author = comment.div.div.div.div.find(text=True).split('-')[1].strip()
                else:
                    comment_author = comment.div.div.div.strong.text
                
                processing_comment_text =  tp().text_pros(comment_text)

                items = {}
                items['field'] = str(field)
                items['topic_title'] = str(topic_titel)
                items['topic_duration'] = str(duration_days)
                items['comment_author'] = str(comment_author)
                items['comment_date'] = str(comment_date)
                items['comment_text'] = str(comment_text)
                items['processing_comment_text'] = str(processing_comment_text)
                # output.write(field + ","  + topic_titel + "," + duration_days + "," + comment_author + "," + comment_date + "," + comment_text + "," + processing_comment_text +"\n")
                
                with open("topics.csv","a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f,fieldnames = ['field', 'topic_title', 'topic_duration', 'comment_author', 'comment_date', 'comment_text', 'processing_comment_text'])
                    writer.writerow(items)
                
            print("field >>>>> ",field)
            print(" ******************************************************* ")
        else :
            return 0
    return 1

def get_topics(index,field):    
    topic_urls = []
    url = 'https://www.hespress.com/'+field+'/index.'+str(index)+'.html'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    # opens the connection and downloads html page from url
    cnx = urlopen(req)
    html_page = cnx.read()

    #parse html
    soup_page = soup(html_page, "html.parser")
    #print(soup_page.h2)
    cnx.close()
    
    if field == 'videos' :
        topics = soup_page.findAll("div", {"class": "image_sawt"})
        i = 0
        for topic in topics:
            # Finds all link tags "a" from within the first div.
            if i < 20 :
                topic_urls.append(topic.select("a")[0]['href'])
                i=i+1
            else:
                break
    else:
        #grabs each topics
        headline = soup_page.find("div", {"class": "category_headline"})
        topics = soup_page.findAll("div", {"class": "short"})

        topic_urls.append(headline.p.select("a")[0]['href'])

        for topic in topics:
            # Finds all link tags "a" from within the first div.
            topic_urls.append(topic.div.p.select("a")[0]['href'])

    if check_topics(topic_urls,field) == 1:
        index = index+1
        get_topics(index,field)

# La fonction main
if __name__ == '__main__':
    
    fields = ['politique','regions','societe','economie','marocains-du-monde','medias','faits-divers','art-et-culture','tamazight','orbites','sport','videos']
    # output = open("topics.csv", "w",encoding="utf-8")
    # headers = "field,topic_title,topic_duration,comment_author,comment_date,comment_text,processing_comment_text\n"
    # output.write(headers)
    with open("topics.csv","w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames = ['field', 'topic_title', 'topic_duration', 'comment_author', 'comment_date', 'comment_text', 'processing_comment_text'])
            writer.writeheader()
    for field in fields :    
        get_topics(1,field) 
    # output.close()
    # tp.plot()




