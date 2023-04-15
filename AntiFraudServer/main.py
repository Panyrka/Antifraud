from flask import Flask, request, Response
from flask_db import db
from flask_sqlalchemy import SQLAlchemy
from Transaction import Transaction
from flask import render_template, redirect, request
from platform_lists import PlatformList
from flask_profile import flask_profile
from rule_result import rule_result
from sqlalchemy import select
from list import dummy_list
from rules import rule
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, BaseView, AdminIndexView
from flask_admin.actions import action
from flask_admin.menu import MenuLink
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink

import AntiFraudLogic
import logging
import database
import config
import PlatFormLists
import AntiFraudLogic
import AFRules
import datetime as dt

def get_user_config():
    return config.UserConfig

def get_app_config():
    return config.ApplicationConfig

def db_connect(user_config):
    db = database.DatabaseHandler(user_config)
    db.create_connection()
    return db

def getAFLogic():
    user_config = get_user_config()
    app_config = get_app_config()
    conn = db_connect(user_config)
    pl = PlatFormLists.ListsHandler(conn, app_config)
    pl.update_list_of_lists_and_content_from_db()
    rules = AFRules.rules
    channelList = ['Web', 'App', 'Ter']
    afLogic = AntiFraudLogic.AFLogic()
    afLogic.initializeContext(pl, rules, channelList)
    return afLogic

def main():
    afLogic = getAFLogic()
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/AntiFraud'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False



    db.init_app(app)
    app.app_context().push()
    db.create_all()
    all_lists = {}
    
    admin = Admin(app, name = "Antifraud", template_mode='bootstrap3')
    admin.add_view(ModelView(Transaction, db.session, name="Тарнзакции"))
    admin.add_view(ModelView(rule, db.session, name="Правила"))
    admin.add_view(ModelView(PlatformList, db.session, name="Листы"))
    admin.add_view(ModelView(rule_result, db.session, name="результаты"))
    admin.add_view(ModelView(flask_profile, db.session, name="профили"))
        
    @app.route('/transactions',methods = ["POST"])
    def parse_request():
        try:
            data = request.json
            print(type(data))
            #transaction = Dict2Obj(data)
            response = afLogic.transactionHandler(data, db)
            return response
        except Exception as e:
            logging.error(e)
            return Response(response = "Bad message!", status = 503)
    
    @app.route('/transactions_view')
    def index():
        transactions = Transaction.query.all()
        return render_template('transactions.html', transactions=transactions)
    
    @app.route('/platform_lists')
    def index2():
        platform_lists = PlatformList.query.all()
        for pl in platform_lists:
            if (pl.name not in all_lists):
                all_lists[pl.name] = type(pl.name, (dummy_list, db.Model), {'__tablename__': pl.name})
        return render_template('platform_lists.html', platform_lists=platform_lists)

    @app.route('/platform_lists/<string:name>')
    def index5(name):
        if (name in all_lists):
            cc = all_lists[name]
            lists = cc.query.all()
            return render_template('list.html', lists=lists)
        return redirect('/platform_lists')
        #with db.engine.connect() as connection:
        #    result = connection.execute(db.text("select * from " + str(name)))
        #    return render_template('list.html', lists=result)
    
    @app.route('/main')
    def index3():
        return render_template('main.html')
    
    @app.route('/profiles')
    def index4():
        flask_profiles = flask_profile.query.all()
        return render_template('profiles.html', flask_profiles=flask_profiles)
    
    @app.route('/results')
    def index7():
        res = rule_result.query.all()
        return render_template('rule_result.html', rule_result=res)
    
    @app.route('/add_rule', methods=['POST', 'GET'])
    def index8():
        if request.method == "POST":
            name = request.form['name']
            code = request.form['code']
            description = request.form['description']
            r = rule(name, description, code, dt.datetime.now())
            db.session.add(r)
            db.session.commit()
            return redirect('/rules')            
        return render_template('add_rule.html')
    
    @app.route('/rules', methods=['GET', 'POST'])
    def index9():
        if request.method == "POST":
            this_id = request.form['id']
            rule.query.filter_by(id=this_id).delete()
            db.session.commit()
        res = rule.query.all()
        return render_template('rules.html', rules=res)

    app.run(debug=True,port=2000)

if __name__ == '__main__':
    main()