from django.shortcuts import render
from django.http import HttpResponse
import json
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs

# Create your views here.

def check(request):
    a=request.GET.get("keyword")
    print a
    if(a=="arushi talwar"):
        f=open("aroosi.json","rb")
        headlines_dict=json.loads(f.read())
        b=filterHeadlines(headlines_dict)
        jsonResponse=json.dumps(b,indent=4)
        return HttpResponse(jsonResponse,content_type="application/json")  
    else:
        headlines_dict_1=getData(a)
        h=filterHeadlines(headlines_dict_1)
        jsonResponseX=json.dumps(h,indent=4)
        return HttpResponse(jsonResponseX,content_type="application/json")
    return HttpResponse("Hey it worked")

def filterHeadlines(headlines_dict):
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    final = []
    for i in headlines_dict:
        ss = sid.polarity_scores(i["headline"])
        if(ss['neu']<=0.7 and ss['neu']>=0.2):
            final.append(i)
        print ss
        print "the headline is"+ i["headline"]
       
    print final
    return final


def getData(query_word):
    urls = []
    finalJson_array = []
    finalJson = {}
 
    url="http://indiatoday.intoday.in/advanced_search.jsp?option=com_search&searchword=%s"%(query_word)
    print url
    r=requests.get(url)
     # print r
    soup = bs(r.text,"html.parser")

    data = soup.findAll("div", { "class" : "searchdotline" })
    print data

    for data in data:
        try:

            findurl = data.find("div", { "class" : "serchheadlien" })

            findurl = data.find('a', href=True)
            # print findurl

            src =  findurl['href']
            urls.append(src)

            url_of_headline= src
            r=requests.get(url_of_headline)
            print r
            
            soup2 = bs(r.text,"html.parser")
            ########scrapping the various elements

            data = soup2.findAll("div", { "class" : "strleft" })[0]
            findHeadline = data.find_all('h1')
            # print findHeadline[0].text

            


            date = soup2.findAll("div", { "class" : "story-timedate" })[0]
            Date = date.text.encode('utf-8').split(' ')
            year = str(Date[3])
            finalDate = Date[0] + ' ' + Date[1] + ' ' + Date[2] + ' ' + year[:4]

            news_dict = { 
                                "headline":str(findHeadline[0].text.encode('utf-8')), 
                                "url_of_headline":url_of_headline.encode('utf-8'), 
                                "date":finalDate
                            }

                # if(i==1):
                #   news_dict={
                #       "headline":str(findHeadline[0].text.encode('utf-8')), 
                #               "url_of_headline":url_of_headline.encode('utf-8'), 
                #               "date":finalDate
                #   }

            finalJson_array.append(news_dict)
            

        except Exception as e:
            print e 
            pass 


        


    for i in range(2,5):
        
        url="http://indiatoday.intoday.in/advanced_search.jsp?advsearch=1&searchtext=%s&searchphrase=all&searchtype=story&page="%(query_word) + str(i)
        
        print url
        r=requests.get(url)
         # print r
        soup = bs(r.text,"html.parser")

        data = soup.findAll("div", { "class" : "searchdotline" })
        print data


        for data in data:
            try:

                findurl = data.find("div", { "class" : "serchheadlien" })

                findurl = data.find('a', href=True)
                # print findurl

                src =  findurl['href']
                urls.append(src)

                url_of_headline= src
                r=requests.get(url_of_headline)
                print r
                
                
                soup2 = bs(r.text,"html.parser")
                ########scrapping the various elements

                data = soup2.findAll("div", { "class" : "strleft" })[0]
                findHeadline = data.find_all('h1')
                # print findHeadline[0].text

            
            

                date = soup2.findAll("div", { "class" : "story-timedate" })[0]
                Date = date.text.encode('utf-8').split(' ')
                year = str(Date[3])
                finalDate = Date[0] + ' ' + Date[1] + ' ' + Date[2] + ' ' + year[:4]
                # print date.text




                # content = soup2.findAll("div", { "class" : "mediumcontent" })[0]
                # findContent = content.find_all('p')
                # a = 0
                # content = ''
                # for i in findContent:
                #   # print findContent[a].text
                #   content = content + findContent[a].text
                #   a = a + 1

                ######## returning the final json

                news_dict = { 
                                "headline":str(findHeadline[0].text.encode('utf-8')), 
                                "url_of_headline":url_of_headline.encode('utf-8'), 
                                "date":finalDate
                            }

                # if(i==1):
                #   news_dict={
                #       "headline":str(findHeadline[0].text.encode('utf-8')), 
                #               "url_of_headline":url_of_headline.encode('utf-8'), 
                #               "date":finalDate
                #   }

                finalJson_array.append(news_dict)
                


            except Exception as e:
                print e 
                return finalJson_array
                pass   

    print "the final json array is",finalJson_array
    return finalJson_array 


