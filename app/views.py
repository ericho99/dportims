from app import app
from flask import render_template
from flask import Flask, request, redirect
import twilio.twiml,os
from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

IMSECS = {
	"+15038939333": "Eric",
	"+15038872891": "Eric",
}

#TO DO LIST
#2. Front end - be able to join the panlist online
#1. Heroku

@app.route('/')
@app.route('/index')
def index():
    return render_template('page.html')

@app.route('/textrequest', methods = ['GET','POST'])
def text_request():
    from_number = request.values.get('From', None)
    messages = client.messages.list()
    message = messages[0].body

    if from_number in IMSECS:
        f = open('app/datafile.txt', 'r')
        num = f.readline()
        while num != '':
            client.messages.create(to=num, from_="+12038506957", body=message)
            num = f.readline()
        returnmessage = 'Thanks for sending that mass text ' + IMSECS[from_number]
        f.close()
    #if the number is not an IM sec number
    else:
    	#check if it's already in the panlist
    	f = open('app/datafile.txt', 'r')
    	inlist = False
    	num = f.readline()
    	while num != '':
    	    if from_number.strip() == num.strip():
    	        inlist = True
    	    num = f.readline()
    	f.close()

    	#if it's in there, just send a text to us with what they want to say
        if inlist:
            client.messages.create(to="+15038872891", from_="+12038506957", body=message)
            #change the 'to' category to the new groupme number
            returnmessage = 'Thanks for your input!'
        #add them to the panlist
        else:
            f = open('app/datafile.txt', 'a')
            f.write(from_number + '\n')
            returnmessage = 'Thanks for joining the DAVENPORT TYNG CUP panlist! \
            Remember that you are anonymous if you respond to this number, so be \
            sure to leave your name so we know who you are! GO DPORT!'
            f.close()

    resp = twilio.twiml.Response()
    resp.sms(returnmessage)
    return str(resp)







