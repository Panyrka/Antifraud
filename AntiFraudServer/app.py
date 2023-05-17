from flask import Flask, request, Response
from flask_db import db
from flask import render_template, redirect, request
from models import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose

import AntiFraudLogic
import logging
import database
import config
import PlatFormLists
import AntiFraudLogic
import datetime as dt
import Profile
import round_time

def get_user_config():
    return config.UserConfig

def get_app_config():
    return config.ApplicationConfig

def db_connect(user_config):
    db = database.DatabaseHandler(user_config)
    db.create_connection()
    return db

def getAFLogic(conn, app_config):
    pl = PlatFormLists.ListsHandler(conn, app_config)
    pl.update_list_of_lists_and_content_from_db()
    channelList = ['Web', 'App', 'Ter']
    profiles_handler = Profile.ProfilesHandler(conn)
    profiles_handler.update()
    afLogic = AntiFraudLogic.AFLogic()
    afLogic.initializeContext(pl, channelList, profiles_handler)
    return afLogic

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        arg1 = 'Hello'
        return self.render('templates/admin/graph.html', arg1=arg1)
        
def main():
    user_config = get_user_config()
    app_config = get_app_config()
    conn = db_connect(user_config)
    afLogic = getAFLogic(conn, app_config)
    
    app = Flask(__name__)
    app.secret_key = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/AntiFraud'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    db.init_app(app)
    app.app_context().push()
    db.create_all()
    all_lists = {}
    

    admin = Admin(app, name = "Antifraud", template_mode='bootstrap3')
    admin.add_view(ModelView(Transaction, db.session, name="Транзакции"))
    admin.add_view(ModelView(active_rule, db.session, name="Правила"))
    admin.add_view(ModelView(PlatformList, db.session, name="Списки"))
    admin.add_view(ModelView(rule_result, db.session, name="Результаты сработки правил"))
    admin.add_view(ModelView(profiles, db.session, name="Профили"))
    admin.add_view(ModelView(alert, db.session, name="Оповещения"))
    



    
    @app.route('/transactions',methods = ["POST"])
    def parse_request():
        try:
            data = request.json
            print(type(data))
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
        flask_profiles = profiles.query.all()
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
            r = active_rule(name, description, code, dt.datetime.now())
            db.session.add(r)
            db.session.commit()
            return redirect('/rules')            
        return render_template('add_rule.html')
    
    @app.route('/rules', methods=['GET', 'POST'])
    def index9():
        if request.method == "POST":
            this_id = request.form['id']
            active_rule.query.filter_by(id=this_id).delete()
            db.session.commit()
        res = active_rule.query.all()
        return render_template('rules.html', rules=res)
    
    @app.route('/home')
    def index_home():
        conn.cur.execute("""SELECT date_trunc('minute', normalized_datetime) AS minute, COUNT(*) AS count, r.rule_result
FROM rule_Result r
WHERE normalized_datetime >= NOW() - INTERVAL '60 minutes'
GROUP BY minute, r.rule_result
ORDER BY minute ASC;
            """)
        res = conn.cur.fetchall()
        conn.conn.commit()
        labels = []
        data1 = []
        data2 = []
        myCounter = 0
        for i in range(60):
            tm = round_time.round_to_min( dt.datetime.now() - dt.timedelta(minutes=(60-i)))
            if myCounter < len(res) and tm == res[myCounter][0]:   
                labels.append(myCounter)
                if (res[myCounter][2] == True):
                    data1.append(res[myCounter][1])
                else:
                    data2.append(res[myCounter][1])
                myCounter += 1 
                if (res[myCounter][2] == True):
                    data1.append(res[myCounter][1])
                else:
                    data2.append(res[myCounter][1])
                myCounter += 1 
            else:
                data1.append(0)
                data2.append(0)
                labels.append(i)
        res = alert.query.all()
        lenn = len(res)
        return render_template('graph.html', labels = labels, data1 = data1, data2 = data2, rules_triggered = myCounter, alerts = res, alerts_count = lenn)
    
    app.run(debug=True,port=2000)

if __name__ == '__main__':
    main()