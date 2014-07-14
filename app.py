#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import *
import logging
import ldap
from logging import Formatter, FileHandler
from forms import *
from functools import wraps
import sqlite3

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
app.config['DATABASE'] = 'Task.db'



def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()



@app.errorhandler(404)
def page_not_found(e):
	return render_template('errors/404.html'),404


# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login',session=session) )
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
@login_required
def home():
    return render_template('pages/placeholder.home.html',session_status = {'session_status':"true"})


@app.route('/logout')
def logout():
    flash('You have been logged out successfully')
    session.pop('logged_in', None)
    session.pop('user_id',None)
    return redirect(url_for('login',session_status = {'session_status':"false"}))

@app.route('/about')
@login_required
def about():
    return render_template('pages/placeholder.about.html',session_status = {'session_status':"true"})


@app.route('/available')
@login_required
def available():
    g.db = connect_db()
    cur = g.db.execute('select demoname from demodetails')
    demo_details_names= [dict(demo_name=row[0]) for row in cur.fetchall()]
    g.db.close()
    return render_template('pages/placeholder.available.html', demo_details_names = demo_details_names ,session_status = {'session_status':"true"})


@app.route('/logs')
@login_required
def logs():
    g.db = connect_db()
    cur  = g.db.execute('select userid,demoname,booked_time,status from lab_history')
    lab_history_details = [dict(userid=row[0],demoname=row[1],booked_time =row[2],status=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('pages/placeholder.logs.html',lab_history_details = lab_history_details,session_status={'session_status':'true'})

@app.route('/reserved')
@login_required
def reserved():
    g.db = connect_db()
    cur = g.db.execute('select  demoid, demoname , description , device_details , status from demodetails where status=1')
    reserve_details= [dict(demo_id=row[0], demo_name=row[1], description=row[2], device_details=row[3],status=row[4]) for row in cur.fetchall()]
    g.db.close()
    return render_template('pages/placeholder.reserved.html', reserve_details = reserve_details,session_status = {'session_status':"true"} )

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@app.route('/authenticate',methods = ['GET','POST'])
def authenticate():
	username = request.form['name']
	password = request.form['password']
	user_dn = "uid="+username+","+app.config['LDAP_SEARCH_BASE']
	base_dn  = "ou=people,o=cisco.com"
	connect  = ldap.open(app.config['LDAP_HOST'])
	search_filter = "uid="+username
	try:
		connect.bind_s(user_dn,password)
		result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
		session['logged_in'] = True
		session['user_id'] = username
		return render_template('pages/placeholder.home.html', session_status = {'session_status':"true"})
	except ldap.LDAPError:
		connect.unbind_s()
		flash('Incorrect UserName/Password')
		return redirect(url_for('login'))


@app.route('/update_reserved_demo/',methods = ['GET','POST'])
def update_reserved_demo():
   	demoname = request.args.get('echoValue')
	g.db = connect_db()
	cur = g.db.execute('select demoname,description,device_details,status from demodetails where demoname= ?',[demoname])
	demo_specific_detail = [dict(demo_name=row[0],description=row[1],device_details=row[2],demo_status=row[3]) for row in cur.fetchall()]
	return Response(json.dumps(demo_specific_detail),  mimetype='application/json')


@app.route('/show_reserved_demo/',methods = ['GET','POST'])
def show_reserved_demo():
	current_status = False 
   	demoname = request.args.get('echoValue')
	g.db = connect_db()
	username = session['user_id']
	cur = g.db.execute('select demoname,description,device_details,status from demodetails where demoname= ?',[demoname])
	demo_specific_detail = [dict(demo_name=row[0],description=row[1],device_details=row[2],demo_status=row[3]) for row in cur.fetchall()]
	cur1 = g.db.execute('select demo_status from demo_user_table where userid=? AND demoname=?',[username,demoname])
	for i in cur1.fetchall():
		current_status = True
		if i[0]==1:
			demo_specific_detail.append({'reserved_by_user':'yes'})
	if current_status == False:
		demo_specific_detail.append({'reserved_by_user':'no'})
	return Response(json.dumps(demo_specific_detail),  mimetype='application/json')


@app.route('/reserve_the_demo/',methods = ['GET','POST'])
def reserve_the_demo():
	selectedvalue = request.args.get('selectedvalue')
	username = session['user_id']
	g.db = connect_db()
	g.db.execute('insert into demo_user_table (userid,demoname,demo_status) values (?,?,1)',[username,selectedvalue])
	g.db.execute('insert into lab_history(userid,demoname,booked_time,status) values (?,?,CURRENT_DATE,1)',[username,selectedvalue])
	g.db.execute('update demodetails set status=1 where demoname = ?',[selectedvalue])
	g.db.commit()
	g.db.close()	
	flash("successfully added")
	return render_template('pages/placeholder.home.html', session_status = {'session_status':"true"})

@app.route('/free_reserved_demo/',methods = ['GET','POST'])
def free_reserved_demo():
	selectedvalue = request.args.get('echoValue')
	username = session['user_id']
	print selectedvalue 
	print username  
	g.db = connect_db()
	g.db.execute('update demodetails set status=0 where demoname = ?',[selectedvalue])
	g.db.execute('delete from demo_user_table where userid=? and demoname=?',[username,selectedvalue])
	g.db.commit()
	g.db.close()
	flash('successfully deleted')
	return render_template('pages/placeholder.home.html', session_status = {'session_status':"true"})
		




# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html',session_status = {'session_status':"true"}), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html',session_status = {'session_status':"true"}), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
