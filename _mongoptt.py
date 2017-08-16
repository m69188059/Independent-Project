import _ptool
import sys
import os
from threading import Thread, Lock
from pymongo import MongoClient

url='https://www.ptt.cc/bbs/Gossiping/index.html'
pagefornum = _ptool.get_web(url)
docfornum = _ptool.get_doc(pagefornum)

num = _ptool.get_index(docfornum) + 1
data_n = 1

client = MongoClient()
db = client.ptt
postin = db.gossiping


print('home page is :%d'%(num))
print('====================================================================')

def mul_ptt(tid,keyword,lock):
    while True:

      with lock:
           global num
           if num>0:              
     
              ptt_url = 'https://www.ptt.cc/bbs/Gossiping/index' + str(num) + '.html'          
              page_num = num
              num = num - 1           

              print('thread id %d at link : %s'%(tid,ptt_url))

              web = []            
              page = _ptool.get_web(ptt_url)
              html = _ptool.get_doc(page)
              web = _ptool.get_articles(keyword,html)                                 #find the all articles that match keyword
              
              
              try:
                for match_article in web:                  
                    global data_n
                    data = data_n                                     
                    data_n = data_n + 1
                    
                    article_page = _ptool.get_web(match_article['link'])
                    article_html = _ptool.get_doc(article_page)
                    article_push = _ptool.get_push(article_html)

                    _dict = _ptool.get_in_article(article_html)
                    _detail = _ptool.get_detail(match_article['title'],_dict['time'])
 


               
                    post = {
                      "Tid":tid,
                      "_id":data,
                      "Keyword":keyword,

                      "Kind":_detail['Kind'],
                      "Isre":_detail['Isre'],
                      "Title":match_article['title'],
                      "Author":match_article['author'],

                      "Week":_detail['Week'],
                      "Month":_detail['Month'],
                      "Date":_detail['Date'],
                      "Time":_detail['Time'],
                      "Year":_detail['Year'],

                      
                      "Link":match_article['link'],
                      
                      "Push":article_push[0],
                      "Re":article_push[1],
                      "Fuck":article_push[2],

                      "Text":_dict['text'],
                      "Retext":_dict['retext'],

                      "Postive":0,
                      "Negative":0,
                      "Score":0
                    }
                    
                    global postin
                    postin.insert_one(post)
                   # print("Thread %d post in database"%tid)

              except TypeError as e:
                   pass
                        
           elif num==0:
                print("Thread %d done"%tid)
                break
       


tnum = int(sys.argv[2])
kword = sys.argv[1]


if tnum is 0:
   tnum = 100 #defult thread_num


for i in range(tnum):
    t = Thread(target=mul_ptt, args=(i,kword,Lock()))
    t.start()

