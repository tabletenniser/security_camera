# -*- coding: utf-8 -*-
"""
This file is the main entry of the front end website. It launches a simple search engine at http://localhost:8080
and upong form submission, it displays the frequency of each word in the latest query as well as culmulative
frequency of all keywords since the website is launched.
"""
from bottle import route, run, get, request, static_file, redirect, error, view
import bottle
import operator
import json
import httplib2
from beaker.middleware import SessionMiddleware
from oauth2client import client
from googleapiclient.discovery import build
import picamera
import time
import os
# DEPLOYMENT(TODO): Change this to the following line when deploying to AWS
# from gevent import monkey; monkey.patch_all()

################################################################################
#                       GLOBAL SETTINGS / CONSTANTS
################################################################################
camera = picamera.PiCamera()
camera.vflip = True

session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

################################################################################
#                      WEBPAGES FROM BOTTLE FRAMEWORK
################################################################################
@route('/img/<filename>')
def image(filename):
    return static_file(filename, root='img/')

@route('/css/<filename>')
def image(filename):
    return static_file(filename, root='css/')

@route('/js/<filename>')
def image(filename):
    return static_file(filename, root='js/')

@route('/take_picture')
def display():
    camera.capture('/home/tabletenniser/security_camera/img/test.jpg')
    return "img/test.jpg"

@route('/take_video')
def display():
    os.system("rm -rf /home/tabletenniser/security_camera/img/v.h264")
    camera.start_recording("/home/tabletenniser/security_camera/img/v.h264")
    time.sleep(60)
    camera.stop_recording()
    print "Finished recording!"
    os.system("rm -rf /home/tabletenniser/security_camera/img/v.mp4")
    os.system("MP4Box -add /home/tabletenniser/security_camera/img/v.h264 /home/tabletenniser/security_camera/img/v.mp4")
    return "img/v.mp4"

@route('/picture')
@route('/')
@view('picture')
def display():
    beaker_session = bottle.request.environ.get('beaker.session')
    if 'email' not in beaker_session:
        return bottle.redirect("/sign_in")
    elif beaker_session['email'] != 'tabletenniser@gmail.com' and beaker_session['email'] != 'zhaoyucheng0212@gmail.com':
        return bottle.redirect("/invalid_cred")

    result_dict = {}
    return result_dict

@get('/redirect')
def redirect_page():
    beaker_session = bottle.request.environ.get('beaker.session')
    code = request.query.get('code', '')
    print "Code: ", code
    with open('client_secrets.json') as client_secret_file:
        client_secret = json.load(client_secret_file)
        flow = client.OAuth2WebServerFlow(
            client_id = client_secret['web']['client_id'],
            client_secret = client_secret['web']['client_secret'],
            scope = 'https://www.googleapis.com/auth/userinfo.email',
            redirect_uri = 'http://24.19.49.108.xip.io:8080/redirect')
        credentials = flow.step2_exchange(code)

        token = credentials.id_token['sub']
        http = credentials.authorize(httplib2.Http())

        user_service = build('oauth2', 'v2', http = http)
        user_document = user_service.userinfo().get().execute()
        beaker_session['email'] = user_document['email']
        beaker_session.save()
    return bottle.redirect('/')

@route('/sign_in')
def display():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/userinfo.email',
        redirect_uri='http://24.19.49.108.xip.io:8080/redirect')
    auth_uri = flow.step1_get_authorize_url()
    print 'Redirecting to ', auth_uri
    return bottle.redirect(auth_uri)

@view('invalid_cred')
def display():
    return "Sorry, you do not have access to the web content!"

@error(404)
@error(500)
@view('error')
def error_page(error):
    return {}

################################################################################
#                            MAIN FUNCTION
################################################################################
# Start the website on http://0.0.0.0:8080
if __name__ == "__main__":
    # DEPLOYMENT(TODO): Change this to the following line when deploying to AWS
    # run(app=app, host='0.0.0.0', port=8080, server='gevent', debug=True)
    run(app=app, host='0.0.0.0', port=8080, debug=True)
    # run(app=app, host='localhost', port=8080, debug=True)
