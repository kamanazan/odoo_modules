#!/usr/bin/python

import xmlrpclib

HOST='localhost'
PORT='8069'
db='training'
user='admin'
password='admin'

url = 'http://%s:%s/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')

uid = common_proxy.login(db,user,password)
print "uid:",uid

session_ids = object_proxy.execute(db,uid,password,'openacademy.session','search',[])
print "session_ids:",session_ids

session_data = object_proxy.execute(db,uid,password,'openacademy.session','read',session_ids,[])#optionally use fields name to filter result
print 'session_data:',session_data

new_session_id = object_proxy.execute(db,uid,password,'openacademy.session','create',{'name':'SESSION CREATE RPC','seats':5})
print 'new_session_id:',new_session_id
