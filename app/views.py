from app import app
from app.models import *
from app.main import *
from flask import render_template
from flask import Flask, request, redirect
import twilio.twiml

@app.route('/')
@app.route('/index')
def index():
    return render_template('page.html')

@app.route('/sports')
@app.route('/sports/<int:sport>')
def sports(sport=1):
    games = Game.query.filter(Game.sport==sport)
    player_id = 1
    return render_template('sport.html', sport=sport, games=games, player_id=player_id)

@app.route('/playerlist/<int:gameid>')
def player_list(gameid):
    game = Game.query.filter(Game.id==gameid).first()
    player_list = Attendance.query.filter(Attendance.game_id==gameid)
    email_list = []
    for att in player_list:
        email_list.append(Player.query.get(att.player_id).email)
    return render_template('playerlist.html', game=game, player_list=email_list)

@app.route('/rsvp/<int:gameid>', methods = ['POST'])
def rsvp(gameid):
    player_id = 1
    if Attendance.query.filter(Attendance.game_id==gameid).filter(Attendance.player_id==player_id) is None:
        a = Attendance(game_id=gameid,player_id=player_id)
        db.session.add(a)
        db.session.commit()
    return

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





