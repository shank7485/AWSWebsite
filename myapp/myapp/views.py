from myapp import app
from flask import render_template, request, redirect
from wtforms import Form, TextField, TextAreaField, SubmitField
from flask_mail import Message, Mail
from flask_flatpages import FlatPages


class ContactForm(Form):
    name = TextField("Name")
    email = TextField("Email")
    subject = TextField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")


mail = Mail()

app.config["MAIL_SERVER"] = "mail.privateemail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@shashankkumar.me'
app.config["MAIL_PASSWORD"] = 'Bng2012#'

mail.init_app(app)

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR1 = 'posts1'
POST_DIR2 = 'posts2'
POST_DIR3 = 'posts3'
# add more Directories here.

flatpages = FlatPages(app)
app.config.from_object(__name__)



@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/academics')
def academics():
    return render_template('academics.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects_iot')
def projects_iot():
    return render_template('projects_iot.html')


@app.route('/projects_awscloud')
def projects_awscloud():
    return render_template('projects_awscloud.html')


@app.route('/projects_docker')
def projects_docker():
    return render_template('projects_docker.html')


@app.route('/projects_heroku')
def projects_heroku():
    return render_template('projects_heroku.html')


@app.route('/projects_sdn')
def projects_sdn():
    return render_template('projects_sdn.html')


@app.route('/projects_webpage')
def projects_webpage():
    return render_template('projects_webpage.html')


@app.route('/projects_database')
def projects_database():
    return render_template('projects_database.html')


@app.route('/projects_nfv')
def projects_nfv():
    return render_template('projects_nfv.html')


@app.route('/projects_queue')
def projects_queue():
    return render_template('projects_queue.html')


@app.route('/projects_view')
def projects_view():
    return render_template('projects_view.html')


# Add posts* here for more blogs.
@app.route('/posts1/')
def posts1():
    posts1 = [p for p in flatpages if p.path.startswith(POST_DIR1)]
    posts1.sort(key=lambda item: item['post_no'], reverse=True)
    return render_template('posts1.html', posts1=posts1)


@app.route("/posts1/<name>/")
def post1(name):
    path = '{}/{}'.format(POST_DIR1, name)
    post1 = flatpages.get_or_404(path)
    return render_template('post1.html', post1=post1)


@app.route("/posts2/")
def posts2():
    posts2 = [p for p in flatpages if p.path.startswith(POST_DIR2)]
    posts2.sort(key=lambda item: item['post_no'], reverse=True)
    return render_template('posts2.html', posts2=posts2)


@app.route("/posts2/<name>/")
def post2(name):
    path = '{}/{}'.format(POST_DIR2, name)
    post2 = flatpages.get_or_404(path)
    return render_template('post2.html', post2=post2)


@app.route("/posts3/")
def posts3():
    posts3 = [p for p in flatpages if p.path.startswith(POST_DIR3)]
    posts3.sort(key=lambda item: item['post_no'], reverse=True)
    return render_template('posts3.html', posts3=posts3)


@app.route("/posts3/<name>/")
def post3(name):
    path = '{}/{}'.format(POST_DIR3, name)
    post3 = flatpages.get_or_404(path)
    return render_template('post3.html', post3=post3)


@app.route('/hobby')
def hobby():
    return render_template('hobby.html')

@app.route('/blog_redirect/')
def blog_redirect():
    return redirect("http://shashankkumar.me/posts3/", code=302)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST':
        form.subject.data = 'Mail from AWS Website'
        msg = Message(form.subject.data, sender='contact@shashankkumar.me', recipients=['shank4804@gmail.com'])

        name = form.name.data
        email = form.email.data
        mess = form.message.data
        print(str(name) + str(email) + str(mess))

        msg.body = """
		From: %s
		Email: %s
		Message: %s
		""" % (name, email, mess)
        mail.send(msg)
        return render_template('contact.html', success=True)

    elif request.method == 'GET':
        return render_template('contact.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.secret_key = 'qaws!#()'
