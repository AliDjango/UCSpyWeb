"""
                  *********************************************
                 *** AsH UCS-Py-Web , A Web interface to UCS ***
                  *********************************************
By Ali SH,GPL v3 License.you are asked to read the license and obey it terms in order to use this project.
"""
#TODO:Connect on request,this prevents error:mysql server has gone away
#TODO:Make Error handling on all pages as they are in index page.
""" Import neccessery things for running. this is the main file.
    Flask is a web framework for python,like Django"""
from flask import Flask , render_template ,abort ,url_for ,request,session,redirect
#base64 is used to encode user and clan IDs
from base64 import b64encode,b64decode
#api is used to get information
from api import *
import core




#setting up the Flask
app = Flask(__name__)
WTF_CSRF_ENABLED = True
app.secret_key = 'My own very very secret key that i know you wont guess it!'

perpage=20#results per page


#error handeling while indexing
def error1(page):
    if page < 1:
        return True


def error2(page,result):
    if not result and page != 1:
        return True

#Home Index
@app.route('/', defaults={'page':1})
@app.route('/users/page/<int:page>')
def index(page):
    try:
        if error1(page):
            return redirect(url_for('index'))
        con = core.connect_mdb()
        con.commit()
        cur = con.cursor()
        startat=(page*perpage)-perpage
        r=get_info_all(cur,perpage,startat)
        result=r[0]
        total=r[1]
        if error2(page,result):
            cur.close()
            con.close()
            return redirect(url_for('index'))
        return render_template('main.html',
                        title='Home',
                        info=result,
                        base64=b64encode,
                        active='home',
                        page=page,
                        total=(total//perpage)+2,
                        perpage=perpage,
                    )
    except Exception as e:
            return render_template('error.html',
                            title='Home',
                            error=str(e),
                        )

    cur.close()
    con.close()
#Ban Users
@app.route('/bans', defaults={'page':1})
@app.route('/bans/page/<int:page>')
def bans(page):
    try:
        if error1(page):
            return redirect(url_for('bans'))
        con = core.connect_mdb()
        con.commit()
        cur = con.cursor()
        startat=(page*perpage)-perpage
        con.commit()
        r=get_info_bans(cur,perpage,startat)
        info=r[0]#['player_info']
        #print(player_info)
        total=r[1]
        if error2(page,info):
            cur.close()
            con.close()
            return redirect(url_for('bans'))
        return render_template('main.html',
                               title='BanList',
                               info=info,
                               base64=b64encode,
                               page=page,
                               total=(total//perpage)+2,
                               perpage=perpage,
                               )
        cur.close()
        con.close()
    except Exception as e:
            return render_template('error.html',
                            title='Home',
                            error=str(e),
                        )

#Server Statistics
@app.route('/stats')
def stats():
    try:
        r=get_ucs_detailed_info()
        return render_template('stats.html',
                               title='Stats',
                               info=r,
                               )
    except Exception as e :
        return render_template('error.html',
                               title='Error',
                               error='Cannot Get Information:%s' % str(e),
                               )


#Game Administrators
@app.route('/admins', defaults={'page':1})
@app.route('/admins/page/<int:page>')
def admins(page):
    try:
        if error1(page):
            return redirect(url_for('admins'))
        con = core.connect_mdb()
        con.commit()
        cur = con.cursor()
        startat=(page*perpage)-perpage
        r=get_info_admins(cur,perpage,startat)
        info=r[0]#['player_info']
        total=r[1]
        if error2(page,info):
            cur.close()
            con.close()
            return redirect(url_for('admins'))
        return render_template('main.html',
                               title='Administrators',
                               info=info,
                               base64=b64encode,
                               page=page,
                               total=(total//perpage)+2,
                               perpage=perpage,
                               )
        cur.close()
        con.close()
    except Exception as e:
            return render_template('error.html',
                            title='Home',
                            error=str(e),
                        )

#Clans
@app.route('/clans', defaults={'page':1})#
@app.route('/clans/page/<int:page>')
def clans(page):
    try:
        if error1(page):
            return redirect(url_for('clans'))
        con = core.connect_mdb()
        con.commit()
        cur = con.cursor()
        startat=(page*perpage)-perpage
        r=get_info_clan_all(cur,perpage,startat)
        info=r[0]#['player_info']
        total=r[1]
        if error2(page,info):
            cur.close()
            con.close()
            return redirect(url_for('clans'))
        return render_template('clans.html',
                               title='Clans',
                               info=info,
                               base64=b64encode,
                               page=page,
                               total=(total//perpage)+2,
                               perpage=perpage,
                               )
        cur.close()
        con.close()
    except Exception as e:
            return render_template('error.html',
                            title='Home',
                            error=str(e),
                        )

#Player Profile
@app.route('/user/<userid>')
def show_user_profile(userid):
    try:
        if error1(page):
            return redirect(url_for('index'))
        con = core.connect_mdb()
        con.commit()
        cur = con.cursor()
        userid=b64decode(userid.encode('utf-8')).decode("utf-8")
        if does_exist_player(userid,cur) is True:
            general_info=get_player_info_general(userid,cur)
            unit_level=get_player_units_level(userid,cur)
            spell_level=get_spell_level(userid,cur)
            hero_level=get_hero_level(userid,cur)
            units=get_player_units(userid,cur)
            spells=get_player_spells(userid,cur)
            clan=get_clan_info(general_info['clan'],cur)
            buildings=get_buildings(userid,cur)
            obstacles=get_obstacles(userid,cur)
            resources=get_resources(userid,cur)
            decos=get_decos(userid,cur)
            traps=get_traps(userid,cur)
            if error2(page,result):
                cur.close()
                con.close()
                return redirect(url_for('index'))
            return render_template('player.html',
                                   title=general_info['name'],
                                   general_info=general_info,
                                   unit_level=unit_level,
                                   spell_level=spell_level,
                                   hero_level=hero_level,
                                   units=units,
                                   spells=spells,
                                   clan=clan,
                                   buildings=buildings,
                                   obstacles=obstacles,
                                   resources=resources,
                                   decos=decos,
                                   traps=traps,
                                   base64=b64encode,
                                   )
        else:
            return render_template('error.html',
                                   title='Error',
                                   error="Cannot Find this player!",
                                   )
        cur.close()
        con.close()
    except Exception as e:
            return render_template('error.html',
                            title='Home',
                            error=str(e),
                        )

#clan profile
@app.route('/clan/<clanid>')
def show_clan_profile(clanid):
    try:
        if error1(page):
            return redirect(url_for('index'))
        con = core.connect_mdb()
        con.commit()
        cur = con.cursor()
        clanid=b64decode(clanid.encode('utf-8')).decode("utf-8")
        if does_exist_clan(clanid,cur) is True:
            clan=get_clan_info(clanid,cur)
            return render_template('clan.html',
                                   title=clan['name'],
                                   clan=clan,
                                   base64=b64encode,
                                   )
        else:
            return render_template('error.html',
                                   title='Error',
                                   error="Cannot Find this Clan!",
                                   )
        cur.close()
        con.close()
    except Exception as e:
            return render_template('error.html',
                            title='Home',
                            error=str(e),
                        )

#Administrator Options
@app.route('/admin')
def admin_panel():
    return render_template('admin.html',title='Admin Panel')

#Signin
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if session.get('username'):
            return redirect(url_for('admin'))
    else:
            return render_template('signin.html')


#validate login
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    def check_password(user,pw):
        if user==config['login']['username'] and pw==config['login']['password']:#TODO:Make  A Database For users and settings.
            return True
        return False#beware that if True is returned,Then false will Not be returned.
    try:
        _username = request.form['inputusername']
        _password = request.form['inputPassword']
        if check_password(_username,_password)==True:
            session['username'] = _username
            return redirect(url_for('index'))
        else:
            return render_template('error.html',
                                   title='Unauthorized Access',
                                   error = 'Wrong Username or Password.',
                                   )
    except Exception as e:
            return render_template('error.html',
                                   title='Unauthorized Access',
                                   error = str(e),
                                   )


#signout
@app.route('/signout')
def signout():
  if 'username' not in session:
    return redirect(url_for('signin'))
  session.pop('username', None)
  return redirect(url_for('index'))

#run the app.
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port = 5001, threaded=True)
