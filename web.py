from search import parse, find_student
from flask import Flask, render_template, request, session, redirect, url_for,g
from exts import db
import config
from models import User, Question, Answer
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    if session.get('phone'):
        context = {
            'questions': Question.query.order_by('-creat_time').all()
        }
        return render_template('index.html', **context)
    else:
        return render_template('login.html')


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        if session.get('phone'):
            return redirect(url_for('index'))
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone).first()
        if not user:
            return '确认有没有注册呦^_^'
        elif user.password != password:
            return '怕不是没记清密码呀o(╯□╰)o'
        elif user.password == password:
            session['phone'] = phone
            session.permanent = True
            return '登陆成功'
        return '未知请求'


@app.route('/regist', methods=['get', 'post'])
def regist():
    if request.method == 'GET':
        if session.get('phone'):
            return redirect(url_for('index'))
        return render_template('regist.html')
    else:
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        this_user = User.query.filter(User.phone == phone).first()
        if this_user:
            return '该手机号码已被注册，请更换手机号码'
        else:
            user = User(phone=phone, username=username, password=password)
            session['phone'] = phone
            session.permanent = True
            db.session.add(user)
            db.session.commit()
            return '注册成功'


@app.route('/delete')
def delete():
    session.clear()
    return redirect(url_for('index'))


@app.route('/question', methods=['get', 'post'])
def question():
    if request.method == 'GET':
        if session.get('phone'):
            return render_template('question.html')
        return render_template('login.html')
    else:
        title = request.form.get('title')
        context = request.form.get('context')
        author_id = User.query.filter(User.phone == session.get('phone')).first().id
        db.session.add(Question(title=title, author_id=author_id, context=context))
        db.session.commit()
        return '提交成功'


@app.route('/detail/<question_id>')
def detail(question_id):
    if session.get('phone'):
        question = Question.query.filter(Question.id == question_id).first()
        return render_template('detail.html', question=question)
    return redirect('/')


@app.route('/answer', methods=['post'])
def answer():
    context = request.form.get('context')
    question_id = request.form.get('question_id')
    author_id = User.query.filter(User.phone == session.get('phone')).first().id
    if not (context and question_id and author_id):
        return '缺少必须的数据'
    db.session.add(Answer(author_id=author_id, context=context, question_id=question_id))
    db.session.commit()
    return '提交成功'


@app.route('/search')
def search():
    if session.get('phone'):
        key = request.args.get('key')
        questions = Question.query.filter(or_(Question.title.contains(key), Question.context.contains(key))).order_by('-creat_time')
        return render_template('index.html', questions=questions)
    return redirect('/')


@app.route('/user/<userid>')
def user(userid):
    if session.get('phone'):
        return render_template('user.html')


@app.before_request
def my_before_request():
    phone = session.get('phone')
    if phone:
        user = User.query.filter(User.phone == phone).first()
        if user:
            g.user = user


@app.context_processor
def my_context():
    if session.get('phone'):
        user = User.query.filter(User.phone == session.get('phone')).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
