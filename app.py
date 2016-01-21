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


con = core.connect_mdb()
cur = con.cursor()


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
        startat=(page*perpage)-perpage
        con.commit()
        r=get_info_all(cur,perpage,startat)
        result=r[0]
        total=r[1]
        if error2(page,result):
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
            import sys,traceback
            result=traceback.extract_tb(sys.exc_info()[2])[-1:][0]
            out='There was an error while processing your request.\nerror:%s\n\n' % str(e)
            out+='file: %s\n' % result[0]
            out+='line: %s\n' % result[1]
            out+='Function: %s\n' % result[2]
            out+='Code: %s\n' % result[3]
            return render_template('error.html',
                            title='Home',
                            error=out,
                        )


#Ban Users
@app.route('/bans', defaults={'page':1})
@app.route('/bans/page/<int:page>')
def bans(page):
    startat=(page*perpage)-perpage
    con.commit()
    r=get_info_bans(cur,perpage,startat)
    info=r[0]#['player_info']
    #print(player_info)
    total=r[1]
    return render_template('main.html',
                           title='BanList',
                           info=info,
                           base64=b64encode,
                           page=page,
                           total=(total//perpage)+2,
                           perpage=perpage,
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
    startat=(page*perpage)-perpage
    con.commit()
    r=get_info_admins(cur,perpage,startat)
    info=r[0]#['player_info']
    total=r[1]
    return render_template('main.html',
                           title='Administrators',
                           info=info,
                           base64=b64encode,
                           page=page,
                           total=(total//perpage)+2,
                           perpage=perpage,
                           )


#Clans
@app.route('/clans', defaults={'page':1})
@app.route('/clans/page/<int:page>')
def clans(page):
    startat=(page*perpage)-perpage
    con.commit()
    r=get_info_clan_all(cur,perpage,startat)
    info=r[0]#['player_info']
    total=r[1]
    return render_template('clans.html',
                           title='Clans',
                           info=info,
                           base64=b64encode,
                           page=page,
                           total=(total//perpage)+2,
                           perpage=perpage,
                           )


#Player Profile
@app.route('/user/<userid>')
def show_user_profile(userid):
    con.commit()
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


#clan profile
@app.route('/clan/<clanid>')
def show_clan_profile(clanid):
    con.commit()
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


#Administrator Options
@app.route('/admin')
def admin_panel():
    con.commit()
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
        if user==config['login']['username'] and pw==config['login']['password']:
            return True
        return False
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
    app.run(host='127.0.0.1',port = 5001)
