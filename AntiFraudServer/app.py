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
        
class UserAdminView(ModelView):
    def get_edit_form(self):
        form = super(UserAdminView, self).get_edit_form()
        print(form.transaction_id)
        form.a = '<input id="q" maxlength="64" name="c" required type="text" value="2">'
        print(type(form))
        return form

    def edit_form(self, obj=None):
        form = super(UserAdminView, self).edit_form(obj)
        print(form.transaction_id)
        form.a = '<input id="s" maxlength="64" name="d" required type="text" value="3">'
        print(type(form))
        return form

from flask_admin.form import rules

class RuleView(ModelView):
    form_edit_rules = ('transaction_id', 'client_id', 'normalized_datetime', 'triggered_rules', 'status', rules.HTML('''
                                                      <br>
                                                      <br>
                                                      <div style="display: flex; justify-content: center;">
  <input class="btn btn-primary" type="submit" onclick="sendGetRequest()" value ="Отправить в систему источник" >
<a class="btn btn-primary" onclick="openTransaction()">Открыть транзакцию</a>
</div>

                                                      <style>
                                                      .center {
   
}
                                                      </style>
                                                      <script>
  function sendGetRequest() {
      var transactionIdInput = document.getElementById('transaction_id');
var transactionIdValue = transactionIdInput.value;

var spanElement = document.getElementById('select2-chosen-1');
var statusid = spanElement.innerText; // или spanElement.textContent
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://92.255.107.213:2000/api/send_response/'+transactionIdValue+'/'+statusid, true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        alert(xhr.response);
      } else {
        alert('Ошибка выполнения GET-запроса');
      }
    };
    xhr.send();
  }
  function openTransaction(event) {
            var transactionIdInput = document.getElementById('transaction_id');
var transactionIdValue = transactionIdInput.value;
  window.open('http://92.255.107.213:2000/admin/transaction/edit/?id=' +transactionIdValue + '&url=%2Fadmin%2Ftransaction%2F', '_blank');

}
</script>
                                                      '''))




def main():
    user_config = get_user_config()
    app_config = get_app_config()
    conn = db_connect(user_config)
    afLogic = getAFLogic(conn, app_config)
    
    # Создайте класс представления для главной страницы
    class HomeAdminView(AdminIndexView):
        endpoint = 'home'
        url = '/'
        name = 'Dashboard'
        
        @expose('/')
        def index(self):
            current_time = dt.datetime.now()
            start_time = current_time - dt.timedelta(minutes=60)
            triggered_rules = rule_result.query.filter(rule_result.normalized_datetime >= start_time).count()
            created_alerts = alert.query.filter(alert.normalized_datetime >= start_time).count()
            alerts = alert.query.filter(alert.normalized_datetime >= start_time)
            
            labels = []
            rules = []
            alerts_arr = []
            
            conn.cur.execute("""
            SELECT date_trunc('minute', normalized_datetime) AS minute, COUNT(*) AS count
            FROM rule_Result r
            WHERE normalized_datetime >= NOW() - INTERVAL '60 minutes'
            GROUP BY minute, r.rule_result
            ORDER BY minute ASC;""")
            rules_arr = conn.cur.fetchall()
            conn.conn.commit()
            
            conn.cur.execute("""
            SELECT date_trunc('minute', normalized_datetime) AS minute, COUNT(*) AS count
            FROM alerts r
            WHERE normalized_datetime >= NOW() - INTERVAL '60 minutes'
            GROUP BY minute
            ORDER BY minute ASC;""")
            alerts_sql = conn.cur.fetchall()
            conn.conn.commit()
            
            rules_array_counter = 0
            alerts_array_counter = 0
            for i in range(60):
                current_time = round_time.round_to_min(dt.datetime.now() - dt.timedelta(minutes=(60-i)))
                labels.append(i)
                if rules_array_counter < len(rules_arr) and rules_arr[rules_array_counter][0] == current_time:
                    rules.append(rules_arr[rules_array_counter][1])
                    rules_array_counter += 1
                else:
                    rules.append(0)
                    
                if alerts_array_counter < len(alerts_sql) and alerts_sql[alerts_array_counter][0] == current_time:
                    alerts_arr.append(alerts_sql[alerts_array_counter][1])
                    alerts_array_counter += 1
                else:
                    alerts_arr.append(0)
            
            import random
            rules = []
            for _ in range(60):
                value = random.randint(10, 40)  # Генерация случайного числа от 1 до 40
                rules.append(value)
                        # Создание второго массива
            alerts_arr = []
            for _ in range(60):
                value = random.randint(1, 10)  # Генерация случайного числа от 1 до последнего значения в первом массиве
                alerts_arr.append(value)
                                        
            triggered_rules = sum(rules)
            created_alerts = sum(alerts_arr)

            return self.render('admin/graph.html', labels=labels, data1=rules, data2=alerts_arr, rules_triggered=triggered_rules, alerts=alerts, alerts_count=created_alerts)
            #conn.cur.execute("""SELECT date_trunc('minute', normalized_datetime) AS minute, COUNT(*) AS count, r.rule_result
            #                    FROM rule_Result r
            #                    WHERE normalized_datetime >= NOW() - INTERVAL '60 minutes'
            #                    GROUP BY minute, r.rule_result
            #                    ORDER BY minute ASC;
            #                    """)
            #res = conn.cur.fetchall()
            #conn.conn.commit()
            #labels = []
            #data1 = []
            #data2 = []
            #myCounter = 0
            #for i in range(60):
            #    tm = round_time.round_to_min(dt.datetime.now() - dt.timedelta(minutes=(60-i)))
            #    if myCounter < len(res) and tm == res[myCounter][0]:   
            #        labels.append(myCounter)
            #        if res[myCounter][2] == True:
            #            data1.append(res[myCounter][1])
            #        else:
            #            data2.append(res[myCounter][1])
            #        myCounter += 1 
            #        if myCounter >= len(res):
            #            break
            #        if res[myCounter][2] == True:
            #            data1.append(res[myCounter][1])
            #        else:
            #            data2.append(res[myCounter][1])
            #        myCounter += 1 
            #    else:
            #        data1.append(0)
            #        data2.append(0)
            #        labels.append(i)
            #res = alert.query.all()
            #lenn = len(res)
            #return self.render('admin/graph.html', labels=labels, data1=data1, data2=data2, rules_triggered=myCounter, alerts=res, #alerts_count=lenn)

    
    app = Flask(__name__)
    app.secret_key = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@127.0.0.1:5432/antifraud'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    db.init_app(app)
    app.app_context().push()
    db.create_all()
    all_lists = {}

    admin = Admin(app, name = "Antifraud", template_mode='bootstrap3', index_view=HomeAdminView(name='Рабочее пространство'))
    admin.add_view(ModelView(Transaction, db.session, name="Транзакции"))
    admin.add_view(ModelView(active_rule, db.session, name="Правила"))
    admin.add_view(ModelView(PlatformList, db.session, name="Списки"))
    admin.add_view(ModelView(rule_result, db.session, name="Результаты сработки правил"))
    admin.add_view(ModelView(profiles, db.session, name="Профили"))
    #admin.add_view(ModelView(alert, db.session, name="Оповещения"))
    #admin.add_view(UserAdminView(alert, db.session, name="AA"))
    admin.add_view(RuleView(alert, db.session, name="Оповещения"))
    
    from flask_admin.menu import MenuLink
    #admin.add_link(MenuLink(name='Login', url='/login'))
    admin.add_link(MenuLink(name='Выход', url='/home'))

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
    
    @app.route('/home1')
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
        return render_template('admin/graph.html', labels = labels, data1 = data1, data2 = data2, rules_triggered = myCounter, alerts = res, alerts_count = lenn)
    
    @app.route('/api/send_response/<string:id>/<string:response>', methods=['GET'])
    def process_api_request(id, response):
        result = f"В систему источник по транзакции # {id} отправлен статус {response}."
        return result
    
    #app.run(debug=True,port=2000, host='0.0.0.0')

    @app.route('/login', methods=['GET'])
    def process_api_request1():
        return render_template('login.html')

    @app.route('/singup', methods=['GET'])
    def process_api_request2():
        return render_template('register.html')


    @app.route('/home', methods=['GET'])
    def process_api_request3():
        return render_template('home.html')

    app.run(debug=True,port=2000, host='0.0.0.0')
    #app.run(debug=True,port=2000)

if __name__ == '__main__':
    main()
