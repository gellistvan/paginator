import json
import re
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from media_utils import *



headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
}

def FindFirst(parent, object, classes = ''):
    if classes != '' :
        container=parent.findAllNext(object, class_=classes)
        if len(container) :
            return container[0]
    else :
        container=parent.findAllNext(object)
        if len(container) :
            return container[0]
    return None

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


def NEPSZAVA(url, count, imgpath, tempath):
    name=url.split("/")[-1]
    req = requests.get("https://nepszava.hu/json/cikk.json?id=" + name, headers).text
    parsed = json.loads(req)
    title = ""
    content = ""

    for obj in parsed:
        if obj == "title":
            title = parsed[obj]
        if obj == "lead":
            if isinstance(parsed[obj], str):
                content += parsed[obj]
        elif obj=="content": # list
            tags = parsed[obj]
            for tag in tags:
                content += ParseItem(tag)

    soup = BeautifulSoup(content, "html.parser")

    return [title, soup.get_text(), False]

def LAKMUSZ(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='cp_content')
    RemoveAll(content, "figure")
    if content.find("img") is not None:
        for item in content.find("img").find_all_next("br"):
            item.decompose()
        for item in content.find("img").find_all_next("span"):
            item.decompose()

    return [title, content.get_text(), False]

def INDEX(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    lead=soup.find("div", class_="lead").get_text();
    content=soup.find("div", class_='cikk-torzs')
    RemoveAll(content, "figure")
    RemoveAll(content, "div", 'miniapp')
    RemoveAll(content, "div", 'indavideo')
    RemoveAll(content, "div", 'meta-twitter')

    return [title, lead + "/n" + content.get_text(), False]

def QUBIT(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    imfound = False
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='post__content')
    image=FindFirst(content, "img")
    if image is not None:
        imurl=image['src'].strip()
        HandleImage(imurl, count, imgpath, tempath)
        imfound = True

    RemoveAll(content, "div", 'post__authors')
    RemoveAll(content, "div", 'donation-line-fz3')
    RemoveAll(content, "figure")
    RemoveAll(content, "div", 'donation-box-gd5')
    paragrapsh=content.findAll("i")
    if 0 < len(paragrapsh) :
        paragrapsh[-1].decompose()

    return [title, content.get_text(), imfound]

def JELEN(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='content')
    RemoveAll(content, "div", 'cikkblock')

    return [title, content.get_text(), False]

def HVG(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    lead=soup.find("div", class_='article-lead entry-summary').get_text()
    content=soup.find("div", class_='article-content entry-content')
    RemoveAll(content, "figure")

    return [title, lead + "\n" + content.get_text(), False]

def VALASZ(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("article")
    RemoveAll(content, "div", 'hird-ferd-cont')
    RemoveAll(content, "div", 'hird-cont')
    RemoveAll(content, "footer")
    RemoveAll(content, "figure")
    RemoveAll(content, "h2")

    return [title, content.get_text(), False]

def VG(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    lead=soup.find("div", class_="article-desc").get_text()
    content=soup.find("app-article-text")
    RemoveAll(content, "figure")

    return [title, lead + "\n" + content.get_text(), False]

def HANG(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='entry-content')

    RemoveAll(content, "div", "banner-wrapper")
    RemoveAll(content, "div", "widget")
    RemoveAll(content, "div", "cikkblock")
    RemoveAll(content, "figure")

    return [title, content.get_text(), False]


def D36(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='entry-content')

    RemoveAll(content, "div", classes='felhivas')
    RemoveAll(content, "figure")

    return [title, content.get_text(), False]

def PORTFOLIO(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("article")
    content.find("ul", class_='tags').decompose()

    return [title, content.get_text(), False]

def G7(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()
    content=soup.find("div", class_='content')
    content.find("div", class_='donate__articleBox -donateArticleBox _ce_measure_widget').decompose()
    content.find("div", class_='fb-share-button').decompose()
    content.find("p", class_='buttons-container _ce_measure_widget').decompose()
    RemoveAll(content, "p", "related-post")

    frames = content.findAllNext("iframe")
    for frame in frames:
        frame.decompose()


    return [title, content.get_text(), False]

def TELEX(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title=soup.find("h1").get_text()

    top_section = ''
    lead=soup.find("p", class_='article__lead')
    if lead is not None:
        top_section += lead.get_text()
    content = soup.find("div", class_='article-html-content')
    figures = content.findAllNext("figure")
    for figure in figures:
        figure.decompose()

    return [title, top_section + '\n' + content.get_text(), False]

def Huszon4hu(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser").find("div", {"class": "is_content"})
    content = soup.find("div", class_='o-post__body o-postCnt post-body')
    figures = content.findAllNext("figure")
    for figure in figures:
        figure.decompose()

    RemoveAll(content, "div", 'm-riporter')
    RemoveAll(content, "div", 'm-articRecommend')

    title=soup.find("h1").get_text();

    h3=soup.find("h3")
    if h3 is not None:
        h3.decompose()
    block=soup.find("blockquote", {"class": "embedly-card"})
    if block is not None:
        block.decompose()

    return [title, content.get_text(), False]

def NegyNegyNegy(url, count, imgpath, tempath):
    req = requests.get(url, headers).text
    soup = BeautifulSoup(req, "html.parser")
    title = soup.find("h1")
    content = soup.find("div", class_='lq et iP').findChildren("div", recursive=False)[0]
    # content = soup.find("div", class_='rich-text-feature')#.findChildren("div", recursive=False)[0]
    RemoveAll(content, "figure")

    return [title.get_text(), content.get_text(), False]

def Atlatszo(url, count, imgpath, tempath):
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
    return [title.get_text(), content.get_text(), False]


def HandleArticle(url, count, imgpath, tempath):

    if 'atlatszo.hu' in url:
        return Atlatszo(url, count, imgpath, tempath)

    elif '24.hu' in url:
        return Huszon4hu(url, count, imgpath, tempath)

    elif '444.hu' in url:
        return NegyNegyNegy(url, count, imgpath, tempath)

    elif 'telex.hu' in url:
        return TELEX(url, count, imgpath, tempath)

    elif 'g7.hu' in url:
        return G7(url, count, imgpath, tempath)

    elif 'portfolio.hu' in url:
        return PORTFOLIO(url, count, imgpath, tempath)

    elif 'direkt36.hu' in url:
        return D36(url, count, imgpath, tempath)

    elif 'hang.hu' in url:
        return HANG(url, count, imgpath, tempath)

    elif 'valaszonline' in url:
        return VALASZ(url, count, imgpath, tempath)

    elif 'hvg.hu' in url:
        return HVG(url, count, imgpath, tempath)

    elif 'vg.hu' in url:
        return VG(url, count, imgpath, tempath)

    elif 'en.media' in url:
        return JELEN(url, count, imgpath, tempath)

    elif 'bit.hu' in url:
        return QUBIT(url, count, imgpath, tempath)

    elif 'index.hu' in url:
        return INDEX(url, count, imgpath, tempath)

    elif 'lakmusz' in url:
        return LAKMUSZ(url, count, imgpath, tempath)

    elif 'nepszava.hu' in url:
        return NEPSZAVA(url, count, imgpath, tempath)

    else:
        print("Unknown site")

    return ['','']