#What this script do is 
#1. add a title and headline at the very beginning of each html file, for friendly reading
#2. prepend each img url with pressplay base_url, for online fetch
#3. replace each outlink href url with local articleId.html, for local browsing
#4. after processed, write to file

from bs4 import BeautifulSoup

def process_html():
    filename = "id_title.csv"

    with open(filename, mode='r', encoding='utf-8') as file:
        for line in file:
            id = line.rstrip().split(',')[0]
            title = line.rstrip().split(',')[1]

            filename = id + '.html'
            html = open(filename).read()
            soup = BeautifulSoup(html, 'html.parser')

            #1. add a title and headline at the very beginning of each html file
            #from observation, first line with p tags, 
            tag = soup.p 
            new_headline = soup.new_tag("h1")
            new_headline.string = title

            new_title = soup.new_tag("title")
            new_title.string = title

            tag.insert_before(new_title)
            tag.insert_before(new_headline)

            #2. prepend each img url with pressplay base_url, for online fetch
            prepend_img_url = 'https://www.pressplay.cc'
            images = soup.findAll('img')
            for image in images:
                img_url = image['src']
                if "https:" not in img_url:
                    image['src'] = prepend_img_url + image['src']

            #3. replace each outlink href url with local articleId.html
            hrefs = soup.findAll('a')
            for href in hrefs:
                web_url = href['href']
                if "https://www.pressplay.cc/" in web_url:
                    parse_id = web_url.split('/')[-1]
                    href['href'] = parse_id + '.html'

            #4. after processed, write to file
            html = str(soup)
            with open(filename, "w") as file:
                file.write(html)

# process_html()
