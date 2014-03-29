from app import app
from app.models import *
from flask import render_template
from flask import Flask, request, redirect
import twilio.twiml,os
from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

IMSECS = {
    "+15038872891": "Eric",
    "+13037178692": "Maren",
    "+13048905251": "Connor",
    "+17082978240": "Julianne",
    "+16107375637": "Claire",
    "+16086954412": "Fabi",
}

@app.route('/')
@app.route('/index')
def index():
    return render_template('page.html')

@app.route('/textrequest', methods = ['GET','POST'])
def text_request():
    from_number = request.values.get('From', None)
    messages = client.messages.list()
    message = messages[0].body

    if message.strip().lower() == 'remove':
        u = User.query.filter(User.number==from_number).first()
        if u is not None:
            db.session.delete(u)
            db.session.commit()
        returnmessage = 'You have successfully been removed from the panlist'
    else:
        #if it's an IM sec
        if from_number in IMSECS:
            for user in Panlist.query.filter(Panlist.name=='textlist').first().users:
                client.messages.create(to=user.number, from_="+12038506957", body=IMSECS[from_number]+ ': ' + message)
            returnmessage = 'Thanks for sending that mass text ' + IMSECS[from_number]
        #if the number is not an IM sec number
        else:
            #if it's in there, just send a text to us with what they want to say
            if User.query.filter(User.number==from_number).first() is not None:
                for num in IMSECS:
                    client.messages.create(to=num, from_="+12038506957", body=message)
                returnmessage = 'The IM secs have received your message and thank you for your support.'
            #add them to the panlist
            else:
                p = Panlist.query.filter(Panlist.name=='textlist').first()
                u = User(number=from_number,panlist=p)
                db.session.add(u)
                db.session.commit()

                returnmessage = 'Thanks for joining the DAVENPORT TYNG CUP panlist! This is our year to win it all, and this panlist will be used primarily as an emergency if we do not have enough players for a particular sport. Text the word "remove" if you want to be removed from the list. GO DPORT!'

    resp = twilio.twiml.Response()
    resp.sms(returnmessage)
    return str(resp)

@app.route("/callrequest", methods=['GET', 'POST'])
def call_request():
    resp = twilio.twiml.Response()
    resp.say("DAVENPORT, DAVENPORT, WE ARE HERE. WE DON'T NEED NO FUCKING CHEER. DAVENPORT DAVENPORT WE ARE HERE. BEER BEER BEER BEER BEER BEER BEER")
    return str(resp)





