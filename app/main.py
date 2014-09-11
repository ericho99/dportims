from app import app
from app.models import *
from app.helpers import *
import os,re
from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

SEND_NUMBER = "+12035990002"

def main(from_number, message, pid, user):
    if user is not None and user.admin:
        command = message.split(' ', 1)[0].strip().lower()

        try:
            body = message.split(' ', 1)[1].strip()
        except:
            body = ''

        if command == '@add':
            return add(body, pid)
        elif command == '@admins':
            return admins(from_number, body, pid, user.name)
        elif command == '@all':
            return all_command(from_number, body, pid)
        elif command == '@block':
            return block(body, pid)
        elif command == '@commands' or command == '@command':
            return 'Here is a list of valid commands:' + '\n' + \
                   '@add - adds a user, in the form of "number:name"' + '\n' + \
                   '@admins - sends a text to all admins' + '\n' + \
                   '@all - sends a text to all users' + '\n' + \
                   '@block and @unblock - blocks/unblocks the specified user from the group' + '\n' + \
                   '@commands - brings up a list of commands' + '\n' + \
                   '@info - shows your username and number' + '\n' + \
                   '@leave - removes yourself from the group' + '\n' + \
                   '@makeadmin - makes the specified user an admin' + '\n' + \
                   '@name - changes name to the following phrase (max 25 chars)' + '\n' + \
                   '@remove - removes the specified user from the group' + '\n' + \
                   '@search - searches usernames for keywords (empty search gives all users)' + '\n' + \
                   '@user - sends a text to the specified user after the command (message separated by a colon)'
        elif command == '@deadmin':
            return deadmin(body, pid)
        elif command == '@info':
            return 'Your username is ' + user.name + '. Stop bothering me.'
        elif command == '@leave':
            return leave(user)
        elif command == '@makeadmin':
            return makeadmin(body, pid, user.name)
        elif command == '@name':
            return name_change(body, pid, user)
        elif command == '@remove':
            return remove(body, pid)
        elif command == '@search':
            return search(body, pid)
        elif command == '@unblock':
            return unblock(body, pid)
        elif command == '@user':
            return user_message(body, pid)
        else:
            return 'Please enter a valid command. Text @commands for a list of valid commands.'
    else:
        if message == '':
            return 'Please enter a valid message.'
        elif user is None:
            return store_user(message, pid, from_number)
        elif user.blocked == 1:
            return 'Sorry, you have been blocked from this application.'
        else:
            if message[0] == '@':
                command = message.split(' ', 1)[0].strip().lower()

                try:
                    body = message.split(' ', 1)[1].strip()
                except:
                    body = None

                if command == '@add':
                    return add(body, pid)
                elif command == '@commands' or command == '@command':
                    return 'Here is a list of valid commands:' + '\n' + \
                           '@add - adds a user to the list, in the form of "number:name"' + '\n' + \
                           '@commands - brings up a list of commands' + '\n' + \
                           '@info - shows your username and number' + '\n' + \
                           '@leave - removes yourself from the group' + '\n' + \
                           '@name - changes name to the following phrase (max 25 chars)'
                elif command == '@info':
                    return 'Your username is ' + user.name + ' and you are an IM superstar. Don\'t let anyone tell you otherwise.'
                elif command == '@leave':
                    return leave(user)
                elif command == '@name':
                    return name_change(body, pid, user)
                else:
                    return 'Please enter a valid command. Text @commands for a list of valid commands.'
            else:
                for u in User.query.filter(User.panlist_id==pid).filter(User.admin==1):
                    client.messages.create(to=u.number, from_=SEND_NUMBER, body=user.name + ': ' + message)
                return None
    return None

def add(body, pid):
    if body == None or body == '':
        return 'Invalid command.'

    username = body.split(':', 1)[0].strip()

    try:
        num = body.split(':', 1)[1].strip()
    except:
        num = None

    if num == None or num == '':
        return 'Please enter a valid user/number combo in the form of username:number.'
    elif is_user_by_num('+1' + num, pid):
        return 'This person is already part of the group.'

    try:
        client.messages.create(to=num, from_=SEND_NUMBER, body='Welcome to Davenport IM Updates! Please text back with your name to confirm your membership in the group.')
    except:
        return 'Please enter a valid user/number combo in the form of username:number.'
    return 'Successfully requested ' + username + ' to join the group.'

def admins(from_number, body, pid, username):
    if body == None or body == '':
        return 'Please enter a valid message.'

    for u in User.query.filter(User.panlist_id==pid).filter(User.admin==1).filter(User.number!=from_number):
        client.messages.create(to=u.number, from_=SEND_NUMBER, body='@adminonly ' + username + ': ' + body)
    return None

def all_command(from_number, body, pid):
    if body == None or body == '':
        return 'Please enter a valid message.'

    for u in User.query.filter(User.panlist_id==pid).filter(User.number!=from_number):
        client.messages.create(to=u.number, from_=SEND_NUMBER, body=body)
    return 'Mass text successfully sent.'

def block(body, pid):
    user = get_user_by_string(body, pid)
    if user is not None and not user.admin:
        if user.blocked == 1:
            return user.name + ' is already blocked.'
        else:
            user.blocked = 1
            db.session.commit()
            return 'You have successfully blocked ' + user.name + '.'
    return 'Please specify a valid user to block.'

def check_user(number):
    try:
        client.messages.create(to=number, from_=SEND_NUMBER, body='Welcome to Davenport IM Updates!')
    except:
        return 'Please enter a valid user/number combo in the form of username:number.'

def deadmin(body, pid):
    user = get_user_by_string(body, pid)
    if user is not None:
        if user.admin == 0:
            return user.name + ' is not an admin.'
        else:
            user.admin = 0
            db.session.commit()
            return 'You have successfully made ' + user.name + ' a regular user.'
    return 'Please specify a valid user to de-admin.'

def leave(user):
    db.session.delete(user)
    db.session.commit()
    return 'You have successfully left the group.'

def makeadmin(body, pid, username):
    user = get_user_by_string(body, pid)
    if user is not None:
        if user.admin == 1:
            return user.name + ' is already an admin.'
        else:
            user.admin = 1
            db.session.commit()
            client.messages.create(to=user.number, from_=SEND_NUMBER, body=username + ' has made you an admin of this group.')
            return 'You have successfully made ' + user.name + ' an admin.'
    return 'Please specify a valid user to make an admin.'

def name_change(body, pid, user):
    if not is_user_by_string(body, pid) and len(body) < 26 and body != '':
        user.name = body
        db.session.commit()
        return 'Name change successful. Your new name is ' + body + '.'
    return 'Name change failed. The name is taken or is longer than 25 characters.'

def name_check(name, pid):
    if not is_user_by_string(name, pid) and len(name) < 26 and name != '':
        return True
    return False

def number_check(num, name):
    try:
        client.messages.create(to='+1'+num, from_=SEND_NUMBER, body='Welcome to Davenport IM Updates, ' + name + '. Text @commands for a list of valid commands, or @leave to leave the group. Messages you send to this number will be sent directly to the Intramural Secretaries.')
        return True
    except:
        return False

def remove(body, pid):
    user = get_user_by_string(body, pid)
    if user is not None and not user.admin:
        db.session.delete(user)
        db.session.commit()
        return 'You have successfully removed ' + user.name + ' from the group.'
    return 'Please specify a valid user to remove.'

def search(body, pid):
    returnmessage = ''
    pattern = re.compile(body,re.IGNORECASE)
    for u in User.query.filter(User.panlist_id==pid):
        if pattern.search(u.name) is not None:
            returnmessage = returnmessage + u.name + '\n'
    if returnmessage == '':
        return 'No users found.'
    return returnmessage

def store_user(message, pid, from_number):
    if not is_user_by_string(message, pid) and len(message) < 26:
        u = User(number=from_number, name=message, admin=0, panlist_id=pid, blocked=0)
        db.session.add(u)
        db.session.commit()
        return 'Welcome to Davenport IM Updates, ' + message + '. Text @commands for a list of valid commands, or @leave to leave the group. Messages you send to this number will be sent directly to the Intramural Secretaries.'
    return 'That name is taken or is invalid. Please enter a valid username of less than 25 characters.'

def unblock(body, pid):
    user = get_user_by_string(body, pid)
    if user is not None:
        if user.blocked == 0:
            return user.name + ' is not blocked.'
        else:
            user.blocked = 0
            db.session.commit()
            client.messages.create(to=user.number, from_=SEND_NUMBER, body='You have been unblocked from this group!')
            return 'You have successfully unblocked ' + user.name + '.'
    return 'Please specify a valid user to unblock.'

def user_message(body, pid):
    if body == None or body == '':
        return 'Please enter a valid user.'
    else:
        username = body.split(':', 1)[0].strip()
        try:
            text = body.split(':', 1)[1].strip()
        except:
            text = None

        if text == None or text == '':
            return 'Please enter a valid user/message combo in the form of username:message (case sensitive).'
        
        user = get_user_by_string(username, pid)
        if user is not None:
            client.messages.create(to=user.number, from_=SEND_NUMBER, body=text)
            return 'Message successfully sent to ' + user.name + '.'
        return 'Please enter a valid user/message combo in the form of username:message (case sensitive).'





