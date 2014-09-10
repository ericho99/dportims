from app import app, cas
from app.models import *
from app.main import *
from flask import render_template, url_for
from flask import Flask, request, redirect
from flask_cas import CAS
import twilio.twiml
import pdb

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
        player_list.append(Player.query.get(att.player_id).email)
    return render_template('emaillist.html', game=game, player_list=player_list, user=user)

@app.route('/myims')
def myims():
    if cas.username is None:
        return redirect('/login')
    user = Player.query.filter(Player.netid==cas.username).first()
    if user is None:
        return redirect('/newuser')

    player_id = 1
    game_list = Attendance.query.filter(Attendance.player_id==player_id)
    mygames = []
    for g in game_list:
        mygames.append(Game.query.get(g.game_id))
    mygames = sorted(mygames, key=lambda game: game.date)
    return render_template('myims.html', mygames=mygames ,user=user)

@app.route('/newuser')
def newuser():
    if cas.username is None:
        return redirect('login')
    if Player.query.filter(Player.netid==cas.username).first() is not None:
        return redirect('/index')
    return render_template('newuser.html')

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
    player_id = 1
    player_att = Attendance.query.filter(Attendance.player_id==player_id)
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
    return render_template('upcoming.html', games=games, user=user)


@app.route('/rsvp/<int:gameid>', methods = ['POST'])
def rsvp(gameid):
    sport = Game.query.filter(Game.id==gameid).first().sport
    player_id = 1
    if Attendance.query.filter(Attendance.game_id==gameid).filter(Attendance.player_id==player_id).first() is None:
        a = Attendance(game_id=gameid,player_id=player_id)
        db.session.add(a)
        db.session.commit()
    return redirect(url_for('sports',sport=sport))

@app.route('/unrsvp/<int:gameid>', methods = ['POST'])
def unrsvp(gameid):
    sport = Game.query.filter(Game.id==gameid).first().sport
    player_id = 1
    a = Attendance.query.filter(Attendance.game_id==gameid).filter(Attendance.player_id==player_id).first()
    if a is not None:
        db.session.delete(a)
        db.session.commit()
    return redirect(url_for('sports',sport=sport))

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





