#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

#from flask import Flask, render_template, request,g,session,flash
from flask import *
# from flask.ext.sqlalchemy import SQLAlchemy
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
            return redirect(url_for('login'))
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
@login_required
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
@login_required
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/available')
@login_required
def available():
    g.db = connect_db()
    cur = g.db.execute('select  demo_id, demo_name , description , device_details , status , duration from demodetails  where demo_name="admin"')
    demo_details= [dict(demo_id=row[0], demo_name=row[1], description=row[2], device_details=row[3],status=row[4],duration = row[5]) for row in cur.fetchall()]
    g.db.close()
    return render_template('pages/placeholder.available.html', demo_details = demo_details)

#    return render_template('pages/placeholder.available.html')

@app.route('/logs')
@login_required
def logs():
    return render_template('pages/placeholder.logs.html')

@app.route('/reserved')
@login_required
def reserved():
    return render_template('pages/placeholder.reserved.html')

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
		return render_template('pages/placeholder.about.html')
	except ldap.LDAPError:
		connect.unbind_s()
		print "authentication error"
		return render_template('pages/placeholder.failure.html')
# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

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
