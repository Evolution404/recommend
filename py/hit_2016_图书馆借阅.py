import xlrd
import requests
from requests import ReadTimeout, RequestException
from pyquery import PyQuery as pq
from pymongo import MongoClient
import time


def get_id_name(this_line):
    workbook = xlrd.open_workbook('2016级学分结算表.xls')
    worksheet = workbook.sheet_by_index(0)  # 取第一张表
    # 取文件的行数
    line_num = worksheet.nrows
    if this_line < 2 or this_line > 2637:
        print('输入行数不符合正确范围[{}-{}]'.format(2, line_num))
        return None
    # 读取某行某列的值
    name = worksheet.cell_value(this_line - 1, 4)
    id = worksheet.cell_value(this_line - 1, 3)
    return name, id


proxies = {}

header = {
    'Cookie': 'JSESSIONID=1A1CDBA3954D0A9EF1A9B03FCD4154F7'
}

data = {
    'username': '',
    'passwd': '',
    'name': '',
    'verifyCode': '',
    'weixinCode': 'fdsafdssadfs',
    'type': '1',
    'submitType': 'reg'
}


def update_proxies():
    response = requests.get('http://115.159.209.36:5555/get')
    proxies['http'] = 'http://'+response.text

def refresh_data(line_num):
    name, id = get_id_name(line_num)
    data['username'] = id
    data['passwd'] = id
    data['name'] = name


def log_in():
    response = requests.post('http://libwx.hitwh.edu.cn/m/weixin/weixin_reg.php', headers=header, data=data ,proxies=proxies)
    # http://libwx.hitwh.edu.cn/m/weixin/check_name.php
    if '验证姓名' in response.text:
        response = requests.post('http://libwx.hitwh.edu.cn/m/weixin/check_name.php', headers=header, data=data, proxies=proxies)
    return response.text


def get_all_page_num():
    response = requests.get(
        'http://libwx.hitwh.edu.cn/m/weixin/wlend_hist.action?code=11111&state=123&page={}'.format(1),
        headers=header, timeout=5, proxies=proxies)
    doc = pq(response.text)
    try:
        return int(doc('.center').text().split('/')[1])
    except:
        return 1


def parse_books(page_num):
    books_list = []
    response = requests.get('http://libwx.hitwh.edu.cn/m/weixin/wlend_hist.action?code=11111&state=123&page={}'.format(page_num), headers=header, timeout=5 ,proxies=proxies)
    # print(response.text)
    doc = pq(response.text)
    books_num = len(doc('.weui_media_bd'))
    for i in range(books_num):

        title = doc('.weui_media_bd').eq(i)('h4').text()
        lend_time = doc('.weui_media_bd').eq(i)('p').text().split('：')[1]
        back_time = doc('.weui_media_bd').eq(i)('li').eq(0).text().split('：')[1]
        position = doc('.weui_media_bd').eq(i)('li').eq(1).text().split('：')[1]
        book = {}
        book['title'] = title
        book['lend_time'] = lend_time
        book['back_time'] = back_time
        book['position'] = position
        books_list.append(book)
    return books_list


def get_one_person(line_num):
    person = {}
    books = []
    refresh_data(line_num)
    text = log_in()
    print(text)
    if '错误' in text:
        print('学号'+data['username']+'姓名'+data['name']+'密码错误')
        with open('log.txt', 'a') as file:
            file.write('学号'+data['username']+'姓名'+data['name']+'密码错误\n')
        return None
    elif '验证姓名' in text:
        print('学号' + data['username'] + '姓名' + data['name'] + '需要验证姓名')
        with open('log.txt', 'a') as file:
            file.write('学号' + data['username'] + '姓名' + data['name'] + '需要验证姓名\n')
        return None
    time.sleep(0.3)
    pages = get_all_page_num()
    time.sleep(0.2)
    for i in range(pages):
        books.extend(parse_books(i+1))
        time.sleep(0.3)
    person['id'] = data['username']
    person['name'] = data['name']
    person['books'] = books
    return person


client = MongoClient()
db = client['图书馆']
table = db['data']

for i in range(416, 2638):
    try:
        person = get_one_person(i)
        print(person)
        if (not table.find_one({'id': person['id']})):
            cursor = table.insert_one(person)
            print('插入成功')
        else:
            print('重复')

    except RequestException:
        update_proxies()
        print('更新代理为'+proxies['http'])
        person = get_one_person(i)
    except:
        print('跳出')
        with open('log.txt', 'a') as file:
            file.write('学号'+data['username']+'姓名'+data['name']+'获取失败\n')
        continue



