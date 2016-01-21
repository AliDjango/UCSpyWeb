""" Api File For App.py
    this file does all background things like getting information from database and process them and make them readable
    in this way,we can easily use them in main app and HTML rendering.  """

""" Imports Libs used in this file
    Json used for proccessing game objects,userinformation"""
import json
""" urllib used for connecting to UCS Pro API and catching Information.
    Used from for easier access to function,if you want to make your own function,Take care of this.    """
from urllib.request import urlopen
""" Config Parser can be used or : ` from backbeat import configparser`
    Used for getting Config Variables like Database or ...  """
import configparser
#   Core File is used for checking if server is UP or not
import core


#Getting Admin Login Information
config = configparser.ConfigParser()
config.read('config.ini')
#Catching UCS Server Information From Config file
debug=config['ucs debugging']
debug_port=debug['port']
debug_key=debug['key']
debug_url=debug['url']
server=config['server']

#troop Names/Need some Editing.TODO:Correct names that are different in game,like ProtoType or Gargoyle or ...
troop = [
        'Barbarian','Archer','Goblin','Giant','Wall Breaker','Balloon',
        'Wizard','Healer','Dragon','PEKKA','Minion','Hog Rider','Valkyride','Golem',
        'Golem Secondary','witch','AirDefenceSeeker','Lava Hound',
        'TrapSkeletonGround','GargoyleTrap','TrapSkeletonAir',
        'Prototype_1','Prototype_2','Prototype_3',
        ]


#spell Names/Need some Editing.TODO:Correct names that are different in game,like HasteWave,BoostDefences or ...
spell = [
        'LighningStorm', 'HealingWave', 'HasteWave',
        'JumpSpell', 'xmas', 'FreezeSpell',
        'xmas2013', 'Slow', 'BoostDefences',
        'Poison', 'Earthquake', 'SpeedUp',
        ]


#Building Names/Need some Editing.TODO:Correct names that are different in game,like Communications mast or ...
building = [
        'Army Camp','Town Hall','Elixir Collector','Elixir Storage',
        'Gold Mine','Gold Storage','Barrack','Laboratory','Cannon',
        'Archer Tower','Wall','Wizard Tower','Air Defense','Mortar',
        'Clan Castle','Builder Nut','Communications mast',
        'Goblin Town Hull','Goblin hut','Tesla Tower',
        'Spell Factory','XBow','Barbarian King','Dark Elixir Collector',
        'Dark Elixir Storage','Archer Queen','Dark Elixir Barrack',
        'Inferno Tower','Air Sweeper','Dark Spell Factory'
           ]


""" Decoration Names/Need some Editing.
    TODO:Correct names that are different in game,like GBR Flag(i guess it is Great Britain or ...  """
deco = [
        'Barbarian Statue','Torch','Goblin Pole','White Flag','Skull Flag',
        'Flower box 1','Flower box 2','Windmeter','Down Arrow Flag',
        'Up Arrow Flag','Skull Altar','USA Flag','Canada Flag','Italia Flag',
        'Germany Flag','Finland Flag','Spain Flag','France Flag','GBR Flag',
        'Brazil Flag','China Flag','Norway Flag','Thailand Flag','Thailand Flag',
        'India Flag','Australia Flag','South Korea Flag','Japan Flag',
        'Turkey Flag','Indonesia Flag','Netherlands Flag','Philippines Flag',
        'Singapore Flag','PEKKA Statue','Russia Flag','Russia Flag','Greece Flag'
      ]

#obstacles/Need Lots of Editing.TODO:Correct names that are different in game.
obstacle = [
            'Pine Tree', 'Large Stone', 'Small Stone 1', 'Small Stone 2',
            'Square Bush', 'Square Tree', 'Tree Trunk 1', 'Tree Trunk 2', 'Mushrooms',
            'TombStone', 'Fallen Tree', 'Small Stone 3', 'Small Stone 4', 'Square Tree 2',
            'Stone Pillar 1', 'Large Stone', 'Sharp Stone 1', 'Sharp Stone 2', 'Sharp Stone 3',
            'Sharp Stone 4', 'Sharp Stone 5', 'Xmas tree', 'Hero TombStone', 'DarkTombStone',
            'Passable Stone 1', 'Passable Stone 2', 'Campfire', 'Campfire', 'Xmas tree2013',
            'Xmas TombStone', 'Bonus Gembox', 'Halloween2014', 'Xmas tree2014', 'Xmas TombStone2014',
            'Npc Plant 1', 'Npc Plant 2', 'Halloween2015'
           ]

#Country Names/Need some Editing.TODO:Check Names
country = [
         'Europe', 'North America', 'South America', 'Asia', 'Australia', 'Africa',
         'International', 'Afghanistan', 'Åland Islands', 'Albania ', 'Algeria', 'American Samoa',
         'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
         'Armenia', 'Aruba', 'Ascension Island', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
         'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda',
         'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil',
         'British Indian Ocean Territory', 'British Virgin Islands', 'Brunei', 'Bulgaria',
         'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Canary Islands',
         'Cape Verde', 'Caribbean Netherlands', 'Cayman Islands', 'Central African Republic',
         'Ceuta and Melilla', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands',
         'Colombia', 'Comoros', 'Congo (DRC)', 'Congo (Republic)', 'Cook Islands', 'Costa Rica',
         'Côte d’Ivoire', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark',
         'Diego Garcia', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt',
         'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands',
         'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia',
         'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana',
         'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala',
         'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard & McDonald Islands',
         'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq',
         'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan',
         'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
         'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
         'Macau', 'Macedonia (FYROM)', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali',
         'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
         'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique',
         'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
         'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea',
         'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama',
         'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland',
         'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Rwanda', 'Saint Barthélemy',
         'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Pierre and Miquelon',
         'Samoa', 'San Marino', 'São Tomé and Pr�\xadncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
         'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa',
         'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'St. Vincent & Grenadines', 'Sudan', 'Suriname',
         'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
         'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tristan da Cunha', 'Tunisia',
         'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'U.S. Outlying Islands', 'U.S. Virgin Islands',
         'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan',
         'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wallis and Futuna', 'Western Sahara', 'Yemen',
         'Zambia', 'Zimbabwe', '', '', '', '', ''
         ]

#Hero Names/COC version 8 or higher is not supported.
hero = ['Barbarian King','Archer Queen']


#Account Status.0=normal and 00=banned.
status = {0:'Normal',99:'Banned'}

#resources/need some editing.Correct names that are different in game.
resource = [
        'Diamonds', 'Gold', 'Elixir', 'Dark Elixir', 'War Gold', 'War Elixir', 'War Dark Elixir'
         ]

#traps
trap = [
        'Mine', 'Ejector', 'Super bomb', 'Halloween bomb', 'Slow bomb',
        'Air Trap', 'Mega Air Trap', 'Santa Trap', 'Halloween skells'
        ]


#administrator Status/Need some Editing.TODO:Correct names that are Different with UCS defaults
admin_status={
            0:'Normal',
            1:'admin',
            2:'Super admin',
            3:'UnAssigned',
            4:'Moderator',
            5:'Owner'
            }

#Clan role/Need Editing.TODO:Improve and Correct Ranks.
clan_role={ 0:'Normal Member',
            1:'Normal Member',
            2:'Leader'
            }
#database Connection type.MySQL OR sqlite
database={
    'ucsdbEntities':'MySQL',
    'sqliteEntities':'Sqlite',
}


#Player Vs. Goblins Difficulty
pve={
    'true':'Hard',
    'false':'Easy',
}

#Online Status.Please Reffer to Core.py for Better Understanding.
online={
    True:'Online',
    False:'Offline',
}

#Maintenance Status.
maintenance={
    'true':'Yes',
    'false':'No',
}


#   check if user exist
def does_exist_player(id,cur):
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result=cur.fetchone()
    if result is None:#No match Founds so no user exists like that
        return False#False is returned
    else:#there is a result.so user Exists
        return True#True is returned


#   check if clan exists.Very similar to does_exist_player function
def does_exist_clan(id,cur):
    query="SELECT * FROM `clan` WHERE `ClanId`=%s"%id
    cur.execute(query)
    result=cur.fetchone()
    if result is None:#No match Founds so no clan exists like that
        return False#False is returned
    else:#there is a result.so clan Exists
        return True#True is returned


#   Gets player general informations
def get_player_info_general(n,cur):
    global player_info#globals the variable,this maybe used instead of returning in future.
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%n
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    if result['alliance_id']!=0:#0=No Clan
        clan=result['alliance_id']
    else:#Player has No CLan
        clan=None
    player_info={
        'name':result['avatar_name'],
        'id':result2[0],
        'status':status[result2[1]],
        'privileges':admin_status[result2[2]],
        'last_update':result2[3],
        'townhall':result['townhall_level']+1,
        'level':result['avatar_level'],
        'experience':result['experience'],
        'score':result['score'],
        'gems':result['current_gems'],
        'gold':result['resources'][0]['value'],
        'elixir':result['resources'][1]['value'],
        'darkelixir':result['resources'][2]['value'],
        'clan':clan,
        }
    return player_info


#   Gets player unit levels.Spell levels are seperated.
def get_player_units_level(id,cur):
    global unit_level
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    unit_level={}
    for i in result['unit_upgrade_levels']:
            unit_level[troop[i['global_id']-4000000]]=i['value']+1#global_ids for units start from 4000000
    return unit_level


#   Gets player spell levels.unit levels are seperated.
def get_spell_level(id,cur):
    global spell_level
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    spell_level={}
    for i in result['spell_upgrade_levels']:
            spell_level[spell[i['global_id']-26000000]]=i['value']+1#global_ids for spell start from 26000000
    return spell_level


#   Gets player Hero(s) Level.
def get_hero_level(id,cur):
    global hero_level
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    hero_level={}
    for i in result['hero_upgrade_levels']:
            hero_level[hero[i['global_id']-28000000]]=i['value']+1#global_ids for units start from 28000000
    return hero_level


#   Gets player units,not their levels.
def get_player_units(id,cur):
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    units={}
    for i in result['units']:
            units[troop[i['global_id']-4000000]]=i['value']#global_ids for units start from 4000000
    return units


#   Gets player spells,not their levels.
def get_player_spells(id,cur):
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    spells={}
    for i in result['spells']:
            spells[spell[i['global_id']-26000000]]=i['value']#global_ids for spell start from 26000000
    return spells


#   Gets player buildings.we return just the number of them.
#   TODO:Make a seperate building page or anything...
#   TODO:Make a seperate Function for quantity...
def get_buildings(id,cur):
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result2[5]
    result=json.loads(result)
    building_t=[0]*len(building)
    buildings={}
    for i in result['buildings']:
        ind=i['data']-1000000#global_ids for buildings start from 1000000
        building_t[ind]+=1
    for i in range(len(building)):
        if building_t[i]!=0:
            buildings[building[i]]=building_t[i]
    return buildings


#   Gets player obstacles.we return just the number of them.
#   TODO:Make a seperate obstacle page or anything...
#   TODO:Make a seperate Function for quantity...
def get_obstacles(id,cur):
    try:
        global obstacles
        query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
        cur.execute(query)
        result2=result=cur.fetchone()
        result=result[5]
        result=json.loads(result)
        obstacles_t=[0]*len(obstacle)
        obstacles={}
        for i in result['obstacles']:
            ind=i['data']-8000000#global_ids for obstacles start from 8000000
            obstacles_t[ind]+=1
        for i in range(len(building)):
            if obstacles_t[i]!=0:
                obstacles[obstacle[i]]=obstacles_t[i]
        return obstacles
    except:
        return []


#   Gets player resources.
def get_resources(id,cur):
    global resources
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[4]
    result=json.loads(result)
    resources={}
    for i in result['resources']:
        resources[resource[i['global_id']-3000000]]=i['value']#global_ids for resources start from 3000000
    return resources


#   Gets player Decorations
def get_decos(id,cur):
    global decos
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[5]
    result=json.loads(result)
    decos={}
    deco_t=[0]*len(deco)
    for i in result['decos']:
        ind=i['data']-18000000#global_ids for decos start from 18000000
        deco_t[ind]+=1
    for i in range(len(deco)):
        if deco_t[i]!=0:
            decos[deco[i]]=deco_t[i]
    return decos


#   Gets player Traps
def get_traps(id,cur):
    global traps
    query="SELECT * FROM `player` WHERE `PlayerId`=%s"%id
    cur.execute(query)
    result2=result=cur.fetchone()
    result=result[5]
    result=json.loads(result)
    traps={}
    trap_t=[0]*len(trap)
    for i in result['traps']:
        ind=i['data']-12000000#global_ids for traps start from 12000000
        trap_t[ind]+=1
    for i in range(len(trap)):
        if trap_t[i]!=0:
            traps[trap[i]]=trap_t[i]
    return traps


#   Gets a clan Info
def get_clan_info(id,cur):
    if id!=None:
        query="SELECT * FROM `clan` WHERE `ClanId`=%s"%id
        cur.execute(query)
        clan2=clan=cur.fetchone()
        clan=clan[2]
        clan=json.loads(clan)
        members={}
        messages=[0]*len(clan['chatMessages'])
        for member in clan['members']:
            #get_player_info_general(member,cur)
            inf=get_player_info_general(member['avatar_id'],cur)
            members[inf['name']]={
                'role':clan_role[member['role']],
                'id':inf['id'],
            }

        for i in range(len(clan['chatMessages'])):
            message=clan['chatMessages'][i]
            messages[i]={
                'sender_name':message['sender_name'],
                'sender_role':clan_role[message['sender_role']],
                'sender_id':message['sender_id'],
                'message':message['message'],
                'pos':i,
            }
        if clan['alliance_origin']-32000000<0:#Clan origin id starts from 32000000
            clan['alliance_origin']+=32000000
        clan_info={
            'name': clan['alliance_name'],
            'id':clan['alliance_id'],
            'score':clan['score'],
            'needed_score':clan['required_score'],
            'experience':clan['alliance_experience'],
            'level':clan['alliance_level'],
            'description':clan['description'],
            'members':members,
            'members_len':len(clan['members']),
            'messages':messages,
            'messages_len':len(clan['chatMessages']),
            'location':country[clan['alliance_origin']-32000000],
        }
        return clan_info


#   Gets General information for all players.Used in Index Page.
def get_info_all(cur,perpage,startat):
    global out
    query="SELECT * FROM `player`"
    cur.execute(query)
    total=cur.rowcount
    result=cur.fetchall()
    query="SELECT * FROM `player` ORDER BY `AccountPrivileges` DESC LIMIT %s,%s" %(startat,perpage)
    cur.execute(query)
    result=cur.fetchall()
    len=cur.rowcount
    out=['']*len
    g=0
    for i in result:
        out[g]=get_player_info_general(result[g][0],cur)
        out[g]['pos']=g
        g+=1
    return [out,total]


#   Gets information for all banned players.Used in Bans Page.
def get_info_bans(cur,perpage,startat):
    query="SELECT * FROM `player` WHERE `AccountStatus` > 0"
    cur.execute(query)
    total=cur.rowcount
    result=cur.fetchall()
    query="SELECT * FROM `player` WHERE `AccountStatus` > 0 LIMIT %s,%s" %(startat,perpage)
    cur.execute(query)
    result=cur.fetchall()
    len=cur.rowcount
    out=['']*len
    g=0
    for i in result:
        get_player_info_general(result[g][0],cur)
        out[g]=player_info
        out[g]['pos']=g+1
        g+=1
    return [out,total]


#   Gets information for all admins.Used in admins Page.
def get_info_admins(cur,perpage,startat):
    query='SELECT * FROM `player` WHERE `AccountPrivileges`> 0'
    cur.execute(query)
    total=cur.rowcount
    result=cur.fetchall()
    query="SELECT * FROM `player` WHERE `AccountPrivileges`> 0 ORDER BY `AccountPrivileges` DESC LIMIT %s,%s" %(startat,perpage)
    cur.execute(query)
    result=cur.fetchall()
    len=cur.rowcount
    out=['']*len
    g=0
    for i in result:
        out[g]=get_player_info_general(result[g][0],cur)
        out[g]['pos']=g+1
        g+=1
    return [out,total]


#   Gets information for all Clans.Used in Clans index page.
def get_info_clan_all(cur,perpage,startat):
    query="SELECT * FROM `clan`"
    cur.execute(query)
    total=cur.rowcount
    result=cur.fetchall()
    query="SELECT * FROM `clan` LIMIT %s,%s" %(startat,perpage)
    cur.execute(query)
    result=cur.rowcount
    result2=cur.fetchall()
    out=['']*result
    for i in range(result):
        out[i]=get_clan_info(result2[i][0],cur)
        out[i]['pos']=i+1
    return [out,total]


#   Creates a connection to UCS Pro Debug page and catches information.
def get_ucs_info():
    url='http://'+debug_url+':'+debug_port+'/'+debug_key
    result=urlopen(url).read()
    result=result.decode('utf-8')
    result=json.loads(result)
    return result['UCS']


#   Formates the catches information from function above.
def get_ucs_detailed_info():
    out={}
    try:
        r=get_ucs_info()
        out['clientversion']=r['ClientVersion']
        out['Codename']=r['Codename']
        out['databasetype']=database[r['DatabaseType']]
        out['pve']=pve[r['ExpertPVE'].lower()]
        out['inmemoryclans']=r['InMemoryClans']
        out['inmemoryplayers']=r['InMemoryPlayers']
        out['logginglevel']=r['LoggingLevel']
        out['maintenance']=maintenance[r['Maintenance'].lower()]
        out['maintenancetimeleft']=r['MaintenanceTimeLeft']
        out['onlineplayers']=r['OnlinePlayers']
        out['serverport']=r['ServerPort']
        out['serverversion']=r['ServerVersion']
        out['startingdarkelixir']=r['StartingDarkElixir']
        out['startingelixir']=r['StartingElixir']
        out['startinggold']=r['StartingGold']
        out['startinggems']=r['StartingGems']
        out['startinglevel']=r['StartingLevel']
        out['startingexperience']=r['StartingExperience']
        out['startingshieldtime']=r['StartingShieldTime']
        out['startingtrophies']=r['StartingTrophies']
        out['totalclans']=r['TotalClans']
        out['totalplayers']=r['TotalPlayer']
        out['totalconnectedclients']=r['TotalConnectedClients']
        out['serveronline']=online[core.isup(config['server']['host'],config['server']['port'])]
    except:#this way we return -.TODO:Use better algorithm and method for returning offline server status
        out['clientversion']='-'
        out['Codename']='-'
        out['databasetype']='-'
        out['pve']='-'
        out['inmemoryclans']='-'
        out['inmemoryplayers']='-'
        out['logginglevel']='-'
        out['maintenance']='No'
        out['maintenancetimeleft']='-'
        out['onlineplayers']='-'
        out['serverport']=server['port']
        out['serverversion']='-'
        out['startingdarkelixir']='-'
        out['startingelixir']='-'
        out['startinggold']='-'
        out['startinggems']='-'
        out['startinglevel']='0'
        out['startingexperience']='0'
        out['startingshieldtime']='-'
        out['startingtrophies']='-'
        out['totalclans']='-'
        out['totalplayers']='-'
        out['totalconnectedclients']='-'
        out['serveronline']=online[core.isup(config['server']['host'],config['server']['port'])]
    return out
