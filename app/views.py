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





