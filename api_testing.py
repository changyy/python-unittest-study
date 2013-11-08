#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse, getpass
import json, unittest, urllib, urllib2, pycurl, StringIO

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

uri = 'https://api.github.com'
user = 'changyy'
password = ''

class APIQueryTestBase(unittest.TestCase):
	def setUp(self):
		self.uri = uri
		self.user = user
		self.password = password 

	def query(self, api, get=None, post=None, json_output=True, debug=False):
		target = self.uri + api
		if get <>None:
			target = target + '?' + urllib.urlencode(get)
		if debug:
			print "Origin:", self.uri + api
			print "Full:", target
			print "GET:", get
			print "POST:", post

		c = pycurl.Curl()
		c.setopt( pycurl.URL , target )
		c.setopt( pycurl.FOLLOWLOCATION , True )
		c.setopt( pycurl.SSL_VERIFYPEER , False )
		#c.setopt( pycurl.SSL_VERIFYHOST , 0 )
		c.setopt( pycurl.SSLVERSION, pycurl.SSLVERSION_SSLv3)
		#c.setopt( pycurl.COOKIEFILE , '/tmp/pycurl' )
		#c.setopt( pycurl.COOKIEJAR , '/tmp/pycurl' )
		
		if post:
			c.setopt(pycurl.POST, True)
			c.setopt(pycurl.POSTFIELDS, urllib.urlencode(post) )

		b = StringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		c.perform()
		r = b.getvalue()
		b.close()
		b = StringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		if json_output:
			return json.loads(r)
		else:
			return r

	def doLogin(self):
		ret = self.query(api='/login.php')
		self.assertTrue( 'status' in ret )
		self.assertFalse( 'token' in ret )
		ret = self.query(api='/login.php', get={'user':self.user, 'password':self.password})
		self.assertTrue( 'status' in ret )
		self.assertTrue( ret['status'] )
		self.assertTrue( 'token' in ret )

		self.token = ret['token']

	def doLogout(self):
		ret = self.query(api='/logout.php', get={'user':self.user, 'token':self.token})
		self.assertTrue( 'status' in ret )
		self.assertTrue( ret['status'] )
		self.token = None
'''
class LoginAPITestCase(APIQueryTestBase):
	def runTest(self):
		self.doLogin()
class LogoutAPITestCase(APIQueryTestBase):
	def runTest(self):
		self.doLogin()
		token = self.token
		self.doLogout()
		ret = self.query(api='/login.php', get={'user':self.user, 'token':token} )
		self.assertTrue( 'status' in ret )
		self.assertFalse( 'token' in ret )
'''

class GithubUserAPITestCase(APIQueryTestBase):
	def check_format(self, ret):
		self.assertTrue( 'login' in ret )
		self.assertTrue( 'id' in ret )
		self.assertTrue( 'url' in ret )
		self.assertTrue( 'blog' in ret )

	def runTest(self):
		ret = self.query(api='/users/'+user)
		self.check_format(ret)

class GithubUserRepoAPITestCase(APIQueryTestBase):
	def check_format(self, ret):
		self.assertTrue( type(ret) == list )

	def runTest(self):
		ret = self.query(api='/users/'+user+'/repos', get={'page':1})
		self.check_format(ret)
		ret = self.query(api='/users/'+user+'/repos', get=[('page',1)] )
		self.check_format(ret)

if __name__ == '__main__':
	"""
	parser = argparse.ArgumentParser(description='api auto testing')
	parser.add_argument(
		'--host', dest='host', 
		default=''
		help='host'
	)
	parser.add_argument(
		'--user', dest='account', 
		default='frank',
		help='account'
	)
	parser.add_argument(
		'--pass', dest='password', 
		help='password'
	)
	results = parser.parse_args()
	uri = results.host
	user = results.account
	password = results.password
	if password == None:
		password = getpass.getpass()
	"""
	unittest.main()
