from pymongo import MongoClient
import re
import random

client = MongoClient()
db = client['图书馆']
stu_table = db['student']
book_table = db['bookList']


def find_student(key):
    key = str(key)
    if len(key) > 7:
        student = stu_table.find_one({'id': key})
        return student
    else:
        student = stu_table.find_one({'name': key})
        return student


def __find_book_by_title(title):
    rs = book_table.find_one({'title': re.compile(title)})
    try:
        return rs.get('id')
    except AttributeError:
        return None
    # 启用相似率匹配算法
    # if rs:
    #     return rs.get('id'), 1
    # else:
    #     cursor = book_table.find()
    #     max = 0
    #     for document in cursor:
    #         b_title = document.get('title')
    #         ratio = SequenceMatcher(lambda x: x == ' ', title, b_title).ratio()
    #         if ratio > max:
    #             max = ratio
    #             best_book = document
    #     return best_book.get('id'), max


def __find_similarity(id):

    id = id.split('/')[0]
    cursor = book_table.find({'id': re.compile(id)})
    s_books = []
    for document in cursor:
        s_books.append(document)
    return s_books


def parse(name_or_id, num=8, max=10):
    """
    用来解析一个学生的最终书目推荐
    :param name_or_id: 可以填入学号或者姓名
    :param num: 该生推荐的书籍数量
    :param max: 从借阅记录中抽取的最大数量
    :return:
    """

    books = find_student(name_or_id).get('books')
    if len(books) > max:
        books = random.sample(books, max)
    print(books)
    ids = []
    for book in books:
        title = book.get('title').split('.', 1)[1].split('/', 1)[0]
        book_id = __find_book_by_title(title)
        if book_id:
            ids.append(book_id)
    rs = []
    for id in ids:
        this = __find_similarity(id)
        if this:
            rs.extend(this)
    if len(rs) > num:
        rs = random.sample(rs, num)
    return rs


if __name__ == '__main__':
    for book in parse('程利'):
        print(book)


#
#
#
#
# ids = []
# for title in titles:
#     print(title)
#     rs = book_table.find_one({'title': title})
#     ids.append(rs.get('id'))
#
#
# for id in ids:
#     find_similarity(id)




# 相似算法
# cursor = book_table.find()
# max = 0
# for document in cursor:
#     b_title = document.get('title')
#     ratio = SequenceMatcher(lambda x: x == ' ', 'F0-49/62', document.get('id')).ratio()
#     if ratio > max:
#         max = ratio
#         best_book=document
#         print(best_book)
# print(best_book)


