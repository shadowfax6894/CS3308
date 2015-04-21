#!/usr/bin/python
#heart of our database

import MySQLdb as mdb
import sys
from config import *
import os
from AESCipher import *
from FireproofProgram import *

class MasterAccount:

	count = 0

	def __init__(self,username,password,service_name_list=[]):
		self.id_num = MasterAccount.count
		MasterAccount.count += 1
		self.username = username
		self.password = password
		key_hash_obj = AESCipher.hashPassword(self.password) #sha256 more secure than md5
		self.iv = os.urandom(16)
		self.key = key_hash_obj.digest()
		self.username_enc = AESCipher.encryptCredentials(self.key,self.iv,self.username)
		self.password_enc = AESCipher.encryptCredentials(self.key,self.iv,self.password)
		self.service_name_list = service_name_list

	def __str__(self):
		return self.__class__.__name__ + "(" + self.username + ", " + self.password + ")"
				
	def insertMasterAccount(self):

		con = mdb.connect(MYSQL_LOC,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DBNAME);

		with con:
			cur = con.cursor()
			#important info on preventing SQL injection
			#http://bobby-tables.com/python.html
			
			insert_account_command = "INSERT INTO FireproofAccountLogin (id,UserName,PasswordName) VALUES (%s,%s,%s)"
			cur.execute(insert_account_command,(self.id_num,self.username_enc,self.password_enc))
	
	@staticmethod		
	def retrieveMasterAccountId(username_enc,password_enc):
		con = mdb.connect(MYSQL_LOC,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DBNAME);

		with con:
			cur = con.cursor()
			retrieve_account_id_command = "SELECT Id FROM FireproofAccountLogin WHERE (UserName,PasswordName) = (%s,%s)"
			cur.execute(retrieve_account_id_command, (username_enc,password_enc))
			id_number = cur.fetchone()

		return id_number


	@staticmethod
	def changeMasterPassword(account,new_password,confirm_password):
		#updating key to use new password
		old_password = account.password
		old_key = account.key
		key_hash_obj = AESCipher.hashPassword(new_password)
		new_key = key_hash_obj.digest()
		account.key = new_key		

		con = mdb.connect(MYSQL_LOC,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DBNAME);

		with con:
			cur = con.cursor()
			#must decrypt and reencrypt the master username and password in the database
			new_username_enc = AESCipher.encryptCredentials(account.key,account.iv,account.username)
			new_password_enc = AESCipher.encryptCredentials(account.key,account.iv,account.password)
			old_username_enc = account.username_enc
			old_password_enc = account.password_enc
			account.username_enc = new_username_enc
			account.password_enc = new_password_enc			
			#insert_username_command = "UPDATE FireproofAccountLogin SET UserName = new_username_enc WHERE (UserName) = (%s)"
			#insert_password_command = "UPDATE FireproofAccountLogin SET PasswordName = new_password_enc WHERE (PasswordName) = (%s)"
			#cur.execute(insert_username_command, (old_username_enc))
			#cur.execute(insert_password_command, (old_password_enc))
			
			#add the new enc username and password to the database

			#need to reencrypt the service names and service account username/passwords
			for service in account.service_name_list:
				service_id_num = service.id_num
				old_service_name_enc = service.service_name_enc
				encrypted_service = AESCipher.encryptCredentials(account.key,account.iv,service.service_name)
				#insert_service_command = "UPDATE FireprooServices SET Servicename = encrypted_service WHERE (Servicename) = (%s)"
				#cur.execute(insert_service_command, (old_service_name))

				for service_account in servicename.service_accounts:
					old_sa_username_enc = service_account.username_enc
					old_sa_password_enc = service_account.password_enc
					encrypted_service_account_username = AESCipher.encryptCredentials(account.key,account.iv,service_account.username)
					encrypted_service_account_password = AESCipher.encryptCredentials(account.key,account.iv,service_account.password)

					#insert_sa_username_command = 
					#insert_sa_password_command = 

#	@staticmethod
#	def changeMasterUsername(account,new_username): 
