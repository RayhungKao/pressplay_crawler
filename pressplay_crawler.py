import urllib.request as requests
import json
import process_html

################################## prerequisites ##################################
#1. replace the headers with your own
headers = {
}
#2. replace here with how many pages of articles of your subscribed project
page_numbers = 39 

#3. replace here with how many pages of articles of your subscribed project
project_id = "8DB74C4CEC521004C8BF9783553ADCEB"

################################## programs ##################################
id_list = []
title_list = []

def post_all_id_and_title():
    post_url = "https://og-web.pressplay.cc/member/timelines"
    for x in range(1, page_numbers+1):
        #(optional) change body payload of post request
        body = {"date": {"end": "2022-01-31", "start": "2017-11-01"}, "reward_ids": [], "tags": [], "categories": [], "keyword": "",
        "sort_by": "newest", "page": x, "count": 12, "mode": "", "project_id": project_id}
        data =  str(json.dumps(body)).encode('utf-8')

        request = requests.Request(post_url, headers=headers, data=data)
        with requests.urlopen(request) as response:
            data = response.read().decode('utf-8')
            jdata = json.loads(data)

        for article in jdata['data']['list']:
            id = article['timeline_key']
            title = article['timeline_title']
            id_list.append(id)
            title_list.append(title)
        
            filename = "id_title.csv"
            with open(filename, mode='a', encoding='utf-8') as file:
                file.write(id + "," + title + '\n')

def get_article_content_by_id(article_id):
    base_url = "https://og-web.pressplay.cc/timeline/"
    get_url = base_url + article_id + "/info"

    request = requests.Request(get_url, headers=headers)
    with requests.urlopen(request) as response:
        data = response.read().decode('utf-8')
        jdata = json.loads(data)
        parse_content = jdata['data']['timeline_info']['timeline_desc']
        # print(parse_content)
        store_article_content(article_id, parse_content)

def store_article_content(article_id, parse_content):
    filename = article_id + ".html"
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(parse_content)
    
def get_and_store_all_articles():
    post_all_id_and_title()

    for id in id_list:
        get_article_content_by_id(id)
    

get_and_store_all_articles()
process_html.process_html()