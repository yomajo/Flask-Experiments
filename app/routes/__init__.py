from flask import Blueprint, render_template


site = Blueprint('site', __name__)


@site.route('/')
def index():
    return render_template('index.html')

@site.route('/bulma')
def bulma():
    return render_template('bulma.html')
