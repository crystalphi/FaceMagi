from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..models import User


@main.route('/hello', methods=['GET', 'POST'])
def index():
  return 'hello world 2!'
