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
    # "+13037178692": "Maren",
    # "+13048905251": "Connor",
    # "+17082978240": "Julianne",
    # "+16107375637": "Claire",
    # "+16086954412": "Fabi",
}

SEND_NUMBER = "+12035990002" #change to the appropriate number, depending on if it's in test mode or not

@app.route('/')
@app.route('/index')
def index():
    return render_template('page.html')

@app.route('/textrequest', methods = ['GET','POST'])
def text_request():
    from_number = request.values.get('From', None)
    message = request.values.get('Body', None).strip()

    p = Panlist.query.filter(Panlist.name=='textlist').first()
    user = User.query.filter(User.number==from_number).first()
    if user is not None and user.admin:
        command = message.split(' ', 1)[0].strip().lower()
        try:
            body = message.split(' ', 1)[1].strip()
        except:
            body = None
        if command == '@all':
            if body == None or body == '':
                returnmessage = 'Please enter a valid message.'
            else:
                for u in User.query.filter(User.panlist==p):
                    client.messages.create(to=u.number, from_=SEND_NUMBER, body=body)
                returnmessage = 'Mass text successfully sent'
        elif command == '@commands' or command == '@command':
            returnmessage = 'Here is a list of valid commands:' + '\n' + \
                            '@add - adds a user, in the form of "number;name"' + '\n' + \
                            '@all - sends a text to all users' + '\n' + \
                            '@block - blocks the specified user from the panlist' + '\n' + \
                            '@commands - brings up a list of commands' + '\n' + \
                            '@info - shows your username and number' + '\n' + \
                            '@leave - removes yourself from the panlist' + '\n' + \
                            '@makeadmin - makes the specified user an admin' + '\n' + \
                            '@name - changes name to the following phrase (max 25 chars)' + '\n' + \
                            '@remove - removes the specified user from the panlist' + '\n' + \
                            '@user - sends a text to the specified user after the command'
        elif command == '@info':
            returnmessage = 'Your username is ' + user.name + '. Your number is ' + from_number + '.'
        elif command == '@leave':
            db.session.delete(user)
            db.session.commit()
            returnmessage = 'You have successfully been removed from the panlist.'
        elif command == '@name':
            if User.query.filter(User.name==body).first() is None and len(message) < 26:
                user.name = body
                db.session.commit()
                returnmessage = 'Name change successful. Your new name is ' + body + '.'
            else:
                returnmessage = 'Name change failed. The name is taken or is longer than 25 characters.'
        elif command == '@user':
            returnmessage = 'got to user'
        else:
            returnmessage = 'Please enter a valid command. Text @commands for a list of valid commands.'
    else:
        if message == '':
            returnmessage = 'Please enter a valid message.'
        elif user is not None:
            if message[0] == '@':
                command = message.split(' ', 1)[0].strip().lower()
                try:
                    body = message.split(' ', 1)[1].strip()
                except:
                    body = None

                if command == '@add':
                    returnmessage = 'Successfully requested ' + body + ' to join the group.'
                elif command == '@commands' or command == '@command':
                    returnmessage = 'Here is a list of valid commands:' + '\n' + \
                                    '@add - adds a user to the list, in the form of "number;name"' + '\n' + \
                                    '@commands - brings up a list of commands' + '\n' + \
                                    '@info - shows your username and number' + '\n' + \
                                    '@leave - removes yourself from the panlist' + '\n' + \
                                    '@name - changes name to the following phrase (max 25 chars)'
                elif command == '@info':
                    returnmessage = 'Your username is ' + user.name + '. Your number is ' + from_number + '.'
                elif command == '@leave':
                    db.session.delete(user)
                    db.session.commit()
                    returnmessage = 'You have successfully been removed from the panlist.'
                elif command == '@name':
                    if User.query.filter(User.name==body).first() is None and len(message) < 26:
                        user.name = body
                        db.session.commit()
                        returnmessage = 'Name change successful. Your new name is ' + body + '.'
                    else:
                        returnmessage = 'Name change failed. The name is taken or is longer than 25 characters.'
                else:
                    returnmessage = 'Please enter a valid command. Text @commands for a list of valid commands.'
            else:
                for u in User.query.filter(User.panlist==p).filter(User.admin==True):
                    client.messages.create(to=u.number, from_=SEND_NUMBER, body=user.name + ': ' + message)
        else:
            if User.query.filter(User.name==message).first() is None and len(message) < 26:
                u = User(number=from_number,name=message,admin=0,panlist=p)
                db.session.add(u)
                db.session.commit()
                returnmessage = 'Thanks for joining the panlist, ' + message + '.'
            else:
                returnmessage = 'That name is taken or is invalid. Please enter a valid username of less than 25 characters.'


    resp = twilio.twiml.Response()
    resp.sms(returnmessage)
    return str(resp)

@app.route("/callrequest", methods=['GET', 'POST'])
def call_request():
    resp = twilio.twiml.Response()
    resp.say("DAVENPORT, DAVENPORT, WE ARE HERE. WE DON'T NEED NO FUCKING CHEER. DAVENPORT DAVENPORT WE ARE HERE. BEER BEER BEER BEER BEER BEER BEER")
    return str(resp)





