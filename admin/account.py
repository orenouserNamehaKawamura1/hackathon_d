#アカウント機能
from flask import Blueprint, render_template, redirect, url_for, request, session
import os,string,random
import db

account_bp = Blueprint('account',__name__,url_prefix='/account')

@account_bp.route('/list')
def list():
    lists = db.ac_list()
    
    return render_template('report/list.html',lists=lists)
