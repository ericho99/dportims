from app import app, cas
from app.models import *
from app.main import *
from flask import render_template, url_for, flash
from flask import Flask, request, redirect
from flask_cas import CAS
from forms import UserForm, EditUserForm
import twilio.twiml
import pdb,os

SECRET_PASS = os.environ['SECRET_KEY_DPORT']

@app.route('/')
@app.route('/index')
def index():
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')
    return render_template('page.html',user=user)

@app.route('/contact')
def contact():
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')
    return render_template('contact.html',user=user)

@app.route('/editprofile', methods = ['GET', 'POST'])
def editprofile():
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    form = EditUserForm()
    if form.validate_on_submit():
        if not name_check(form.name.data,1):
            return render_template('editprofile.html',user=user,form=form,validname=0)
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        return redirect('/index')
    form.name.data = user.name
    form.email.data = user.email
    return render_template('editprofile.html',user=user,form=form,validname=1)

@app.route('/emaillist/<int:gameid>')
def email_list(gameid):
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    game = Game.query.filter(Game.id==gameid).first()
    att_list = Attendance.query.filter(Attendance.game_id==gameid)
    player_list = []
    for att in att_list:
        player_list.append(Player.query.get(att.player_id).email.lower())
    return render_template('emaillist.html', game=game, player_list=player_list, user=user)

@app.route('/myims')
def myims():
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    game_list = Attendance.query.filter(Attendance.player_id==user.id)
    mygames = []
    for g in game_list:
        mygames.append(Game.query.get(g.game_id))
    mygames = sorted(mygames, key=lambda game: game.date)
    return render_template('myims.html', mygames=mygames ,user=user)

@app.route('/newuser', methods = ['GET', 'POST'])
def newuser():
    if cas.username is None:
        return redirect('login')
    if Player.query.filter(Player.netid==cas.username).first() is not None:
        return redirect('/index')

    form = UserForm()
    if form.validate_on_submit():
        if form.password.data != SECRET_PASS:
            return render_template('newuser.html',form=form,validnumber=1,validname=1,validpass=0)

        if not name_check(form.name.data,1):
            return render_template('newuser.html',form=form,validnumber=1,validname=0,validpass=1)
        
        try:
            num = int(form.number.data)
        except:
            return render_template('newuser.html',form=form,validnumber=0,validname=1,validpass=1)
        if num != 0:
            if num >= 10000000000:
                return render_template('newuser.html',form=form,validnumber=0,validname=1,validpass=1)
            if not number_check(form.number.data,form.name.data):
                return render_template('newuser.html',form=form,validnumber=0,validname=1,validpass=1)
        p = Player(netid=cas.username,name=form.name.data,email=form.email.data)
        db.session.add(p)
        if num != 0:
            u = User(number='+1'+form.number.data,name=form.name.data,admin=0,blocked=0,panlist_id=1)
            db.session.add(u)
        db.session.commit()
        return redirect('/index')
    return render_template('newuser.html',form=form,validnumber=1,validname=1,validpass=1)

@app.route('/playerlist/<int:gameid>')
def player_list(gameid):
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    game = Game.query.filter(Game.id==gameid).first()
    att_list = Attendance.query.filter(Attendance.game_id==gameid)
    player_list = []
    for att in att_list:
        player_list.append(Player.query.get(att.player_id).name.lower())
    return render_template('playerlist.html', game=game, player_list=player_list, user=user)

@app.route('/sports')
@app.route('/sports/<int:sport>')
def sports(sport):
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    games = Game.query.filter(Game.sport==sport)
    games = sorted(games, key=lambda game: game.date)
    player_att = Attendance.query.filter(Attendance.player_id==user.id)
    game_list = []
    for att in player_att:
        game_list.append(att.game_id)
    return render_template('sport.html', sport=sport, games=games, game_list=game_list, user=user)

@app.route('/upcoming')
def upcoming():
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    games = Game.query.filter(Game.win == 2)
    games = sorted(games, key=lambda game: game.date)
    player_att = Attendance.query.filter(Attendance.player_id==user.id)
    game_list = []
    for att in player_att:
        game_list.append(att.game_id)
    return render_template('upcoming.html', games=games, game_list=game_list, user=user)


@app.route('/rsvp/<int:gameid>', methods = ['POST'])
def rsvp(gameid):
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    sport = Game.query.filter(Game.id==gameid).first().sport
    if Attendance.query.filter(Attendance.game_id==gameid).filter(Attendance.player_id==user.id).first() is None:
        a = Attendance(game_id=gameid,player_id=user.id)
        db.session.add(a)
        db.session.commit()
    return redirect(redirect_url())

@app.route('/unrsvp/<int:gameid>', methods = ['POST'])
def unrsvp(gameid):
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    sport = Game.query.filter(Game.id==gameid).first().sport
    a = Attendance.query.filter(Attendance.game_id==gameid).filter(Attendance.player_id==user.id).first()
    if a is not None:
        db.session.delete(a)
        db.session.commit()
    return redirect(redirect_url())

@app.route('/textrequest', methods = ['GET','POST'])
def text_request():
    from_number = request.values.get('From', None)
    message = request.values.get('Body', None).strip()

    p = Panlist.query.filter(Panlist.name=='textlist').first()
    user = User.query.filter(User.number==from_number).filter(User.panlist_id==p.id).first()

    returnmessage = main(from_number, message, p.id, user)

    resp = twilio.twiml.Response()
    if returnmessage is not None:
        resp.sms(returnmessage)
    return str(resp)

# @app.route("/callrequest", methods=['GET', 'POST'])
# def call_request():
#     resp = twilio.twiml.Response()
#     resp.say("DAVENPORT, DAVENPORT, WE ARE HERE. WE DON'T NEED NO FUCKING CHEER. DAVENPORT DAVENPORT WE ARE HERE. BEER BEER BEER BEER BEER BEER BEER")
#     return str(resp)





