import requests
import html
from pyquery import PyQuery as pq
from pymongo import MongoClient

client = MongoClient()
db = client['图书馆']
table = db['bookList']

# response = requests.get('http://222.194.14.124:8080/browse/cls_browsing_book.php?s_doctype=all&cls=A&page=10')
# content = html.unescape(response.text)
# doc = pq(content)


def save_one_page(html):
    doc = pq(html)

    for i in range(doc('h3').length):
        title = doc('h3 a').eq(i).text()
        list = doc('h3').eq(i).text().split(title)
        book = {
            'title': title,
            'id': list[1],
            'creator': doc('.list_books p').eq(i).text()
        }
        if (not table.find_one({'id': book['id']})):
            cursor = table.insert_one(book)
            print(book.get('id') + '-----插入成功')
        else:
            print(book)
            print(book.get('id') + '-----重复')


def get_page_num(html):
    doc = pq(html)
    page_num = int(doc('b font:nth-child(2)').text())
    return page_num


def get_content(char, pagenum):
    url = 'http://222.194.14.124:8080/browse/cls_browsing_book.php?s_doctype=all&cls={}&page={}'.format(char, pagenum)
    response = requests.get(url, timeout=5)
    content = html.unescape(response.text)
    return content


start_char = 'F'
start_page = 2276
flag = True

char = start_char
content = get_content(char, 1)
page_num = get_page_num(content)
if flag:
    x = start_page-1
else:
    x = 0
for j in range(x, page_num):
    try:
        content = get_content(char, j + 1)
        save_one_page(content)
        print(char + '---' + str(j + 1) + '页')
    except:
        print(char + '---' + str(j + 1) + '页超时')
flag = False