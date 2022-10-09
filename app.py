from flask import Flask, render_template
from flask_navigation import Navigation

app = Flask(__name__)
nav = Navigation(app)

# initializes navigations, add each url here
nav.Bar('top', [
    nav.Item('home', 'index'),
    nav.Item('aboutUs', 'about_us'),
    nav.Item('account', 'account'),
    nav.Item('FAQ', 'faq'),
    nav.Item('generateSchedule', 'generate_schedule'),
    nav.Item('Settings', 'settings'),
    nav.Item('uploadCSV', 'upload_csv'),
])


@app.route('/')  # this block is for the default page
def home():
    return render_template('index.html')


@app.route('/aboutUs') # make each of these for each html
def about_us():
    return render_template('aboutUs.html')


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/generate_schedule')
def generate_schedule():
    return render_template('generateSchedule.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/uploadCSV')
def upload_csv():
    return render_template('uploadCSV.html')


if __name__ == '__main__':
    app.run()
