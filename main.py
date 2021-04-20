from hashlib import md5
from flask import Flask, redirect, render_template, session, request
import wikipediaapi

from db import DB
from users_model import UsersModel
from history_model import HistoryModel
from favorites_model import FavoritesModel
from login_form import LoginForm
from registration_form import RegistrationForm
from find_form import FindForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wikipedia'
db = DB()
UsersModel(db.get_connection()).init_table()
HistoryModel(db.get_connection()).init_table()
FavoritesModel(db.get_connection()).init_table()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def main_page():
    hm = HistoryModel(db.get_connection())
    form = FindForm()
    if form.information.data:
        info = form.information.data
        return redirect('/find/{}'.format(info))
    if 'username' not in session:
        return render_template('index.html', text='Index', info=[], form=form, username='')
    texts = []
    try:
        found = hm.get_users(session['username'])
        for i in range(min(10, len(found))):
            texts.append(found[i])
    except Exception:
        pass
    return render_template('index.html', text='Index', info=texts, form=form, username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<error>', methods=['GET', 'POST'])
def login(error=None):
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, str(md5(bytes(password,
                                                            encoding='utf-8')).hexdigest()))  # encoding
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        else:
            return redirect('/login/notexist')
        return redirect("/")
    return render_template('login.html', title='Login', form=form,
                           error=error)


@app.route('/registration', methods=["GET", "POST"])
@app.route('/registration/<er>', methods=["GET", "POST"])
def registration(er=None):
    form = RegistrationForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        users.insert(form.username.data, str(md5(bytes(form.password.data,
                                                       encoding='utf-8')).hexdigest()))
        return redirect('/login')
    return render_template('registration.html', form=form, error=er)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/delete/<int:id>/<string:where>', methods=['GET'])
def delete_info(id, where):
    if 'username' not in session:
        return redirect('/login')
    if where == 'favorites':
        fm = FavoritesModel(db.get_connection())
        fm.delete(id)
    else:
        hm = HistoryModel(db.get_connection())
        hm.delete(id)
    return redirect("/{}".format(where))


@app.route('/find/<string:word>', methods=["GET", "POST"])
def delete(word):
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(word)
    if not page.exists():
        return render_template('info.html', error='notfound', info='', word=word, url='')
    summary = page.summary
    url = page.fullurl
    hm = HistoryModel(db.get_connection())
    if 'username' in session:
        if not hm.exists(word)[0]:
            hm.insert(session['username'], word, summary)
    return render_template('info.html', info=summary, word=word, url=url, error='no')


@app.route('/favorites', methods=["GET", "POST"])
def favorites():
    if 'username' not in session:
        return redirect('/login')
    fm = FavoritesModel(db.get_connection())
    info = fm.get_users(session['username'])
    return render_template('favorites.html', favorites=info)


@app.route('/add/<string:word>/<string:info>', methods=["GET", "POST"])
def add(word, info):
    if 'username' not in session:
        return redirect('/login')
    fm = FavoritesModel(db.get_connection())
    if not fm.exists(word)[0]:
        fm.insert(session['username'], word, info)
    return redirect('/favorites')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.2', debug=True)
