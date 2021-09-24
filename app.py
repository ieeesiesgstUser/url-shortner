from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(10))

    def __init__(self, long, short):
        self.long = long
        self.short = short



@app.route('/admin/pt/2021', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('url_page.html', vals=Urls.query.all()) 
    if request.method == "POST":
        url_received = request.form["nm"]
        custom_short_url = request.form["surl"]
        small_url = Urls.query.filter_by(short=custom_short_url).first()
        if small_url:
            return redirect(url_for("home"))
        else:
            new_url = Urls(url_received, custom_short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=custom_short_url))
    else:
        return render_template('url_page.html')

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return render_template('404.html')

def new_func():
    url_for("not_found")

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)

@app.route('/all_urls')
def display_all():
    return render_template('all_urls.html', vals=Urls.query.all())

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == '__main__':
    app.run(port=5000)
