import json
import re
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
}

def RemoveAll(parent, object, classes = ''):
    if classes != '' :
        container=parent.findAllNext(object, class_=classes)
        for item in container:
            item.decompose()
    else :
        container=parent.findAllNext(object)
        for item in container:
            item.decompose()

def ParseItem(object):
    temp = ""
    if type(object) is dict :
        if 'Txt' in object:
            return object['Txt']
    elif type(object) is list :
        for tag in object:
            temp += ParseItem(tag)
    else :
        return ""
    return temp


def NEPSZAVA(url):
    name=url.split("/")[-1]
    req = requests.get("https://nepszava.hu/json/cikk.json?id=" + name, headers).text
    parsed = json.loads(req)
    title = ""
    content = ""

    for obj in parsed:
        if obj == "title":
            title = parsed[obj]
        if obj == "lead":
            content += parsed[obj]
        elif obj=="content": # list
            tags = parsed[obj]
            for tag in tags:
                content += ParseItem(tag)

    soup = BeautifulSoup(content, "html.parser")

    print(title)
    print (soup.get_text())

    return [title, soup.get_text()]

def LAKMUSZ(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='cp_content')
    RemoveAll(content, "figure")
    for item in content.find("img").find_all_next("br"):
        item.decompose()
    for item in content.find("img").find_all_next("span"):
        item.decompose()

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def INDEX(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    lead=soup.find("div", class_="lead").get_text();
    content=soup.find("div", class_='cikk-torzs')
    RemoveAll(content, "figure")
    RemoveAll(content, "div", 'miniapp')
    RemoveAll(content, "div", 'indavideo')
    RemoveAll(content, "div", 'meta-twitter')

    print(title)
    print(content.get_text())
    return [title, lead + "/n" + content.get_text()]

def QUBIT(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='post__content')
    RemoveAll(content, "div", 'post__authors')
    RemoveAll(content, "div", 'donation-line-fz3')
    RemoveAll(content, "figure")
    RemoveAll(content, "div", 'donation-box-gd5')
    paragrapsh=content.findAll("i")
    if 0 < len(paragrapsh) :
        paragrapsh[-1].decompose()

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def JELEN(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='content')
    RemoveAll(content, "div", 'cikkblock')

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def HVG(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    lead=soup.find("div", class_='article-lead entry-summary').get_text()
    content=soup.find("div", class_='article-content entry-content')
    RemoveAll(content, "figure")

    print(title)
    print(content.get_text())
    return [title, lead + "\n" + content.get_text()]

def VALASZ(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("article")
    RemoveAll(content, "div", 'hird-ferd-cont')
    RemoveAll(content, "div", 'hird-cont')
    RemoveAll(content, "footer")
    RemoveAll(content, "figure")
    RemoveAll(content, "h2")

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def VG(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    lead=soup.find("div", class_="article-desc").get_text()
    content=soup.find("app-article-text")
    RemoveAll(content, "figure")

    print(title)
    print(content.get_text())
    return [title, lead + "\n" + content.get_text()]

def HANG(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='entry-content')

    RemoveAll(content, "div", "banner-wrapper")
    RemoveAll(content, "div", "widget")
    RemoveAll(content, "div", "cikkblock")
    RemoveAll(content, "figure")

    print(title)
    print(content.get_text())
    return [title, content.get_text()]


def D36(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='entry-content')

    RemoveAll(content, "div", classes='felhivas')
    RemoveAll(content, "figure")

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def PORTFOLIO(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("article")
    content.find("ul", class_='tags').decompose()

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def G7(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='content')
    content.find("div", class_='donate__articleBox -donateArticleBox _ce_measure_widget').decompose()
    content.find("div", class_='fb-share-button').decompose()
    content.find("p", class_='buttons-container _ce_measure_widget').decompose()

    frames = content.findAllNext("iframe")
    for frame in frames:
        frame.decompose()


    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def TELEX(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    top_section=soup.find("p", class_='article__lead').get_text()
    content=soup.find("div", class_='article-html-content')
    figures = content.findAllNext("figure")
    for figure in figures:
        figure.decompose()

    print(top_section + '\n' + content.get_text())
    return [title, top_section + '\n' + content.get_text()]

def Huszon4hu(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser").find("div", {"class": "is_content"})
    content = soup.find("div", class_='o-post__body o-postCnt post-body')
    figures = content.findAllNext("figure")
    for figure in figures:
        figure.decompose()

    RemoveAll(content, "div", 'm-riporter')

    title=soup.find("h1").get_text();

    h3=soup.find("h3")
    if h3 is not None:
        h3.decompose()
    block=soup.find("blockquote", {"class": "embedly-card"})
    if block is not None:
        block.decompose()

    print(title)
    print(content.get_text())
    return [title, content.get_text()]

def NegyNegyNegy(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title = soup.find("h1")
    content = soup.find("div", class_='ls eu iP').findChildren("div", recursive=False)[0]
    figures = content.findAllNext("figure")
    for figure in figures:
        figure.decompose()
    # print(figures)
    content_text = content.get_text()
    content_text = re.sub(r'[\n\n]+', r'\n', content_text, re.MULTILINE)
    print(content_text)
    return [title.get_text(), content.get_text()]

def Atlatszo(url):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser").find("div", {"class": "inner-article_body"})
    title=soup.find("h1")
    content=soup.find("div", {"class": "the_content"})
    # soup.find("div", {"class": "article_head_box"}).decompose()
    #soup.find("div", {"class": "post_author_box"}).decompose()
    #soup.find("div", {"class": "post_intro_box"}).decompose()
    #soup.find("div", {"class": "post_outro_box"}).decompose()
    #soup.find("div", {"class": "the_tags"}).decompose()
    #soup.find("div", {"class": "html_banner"}).decompose()
    h3=soup.find("h3")
    if h3 is not None:
        h3.decompose()
    block=soup.find("blockquote", {"class": "embedly-card"})
    if block is not None:
        block.decompose()
    return [title.get_text(), content.get_text()]


def HandleArticle(url):

    if 'atlatszo.hu' in url:
        return Atlatszo(url)

    elif '24.hu' in url:
        return Huszon4hu(url)

    elif '444.hu' in url:
        return NegyNegyNegy(url)

    elif 'telex.hu' in url:
        return TELEX(url)

    elif 'g7.hu' in url:
        return G7(url)

    elif 'portfolio.hu' in url:
        return PORTFOLIO(url)

    elif 'direkt36.hu' in url:
        return D36(url)

    elif 'hang.hu' in url:
        return HANG(url)

    elif 'valaszonline' in url:
        return VALASZ(url)

    elif 'hvg.hu' in url:
        return HVG(url)

    elif 'vg.hu' in url:
        return VG(url)

    elif 'en.media' in url:
        return JELEN(url)

    elif 'bit.hu' in url:
        return QUBIT(url)

    elif 'index.hu' in url:
        return INDEX(url)

    elif 'lakmusz' in url:
        return LAKMUSZ(url)

    elif 'nepszava.hu' in url:
        return NEPSZAVA(url)

    else:
        print("Unknown site")

    return ['','']