""" File Encryption and Decryption app built using kivy python Gui and kivy language,the logic is in this module, the presentation is in cryptee.kv file"""
import kivy
from kivy.uix.label import Label
from kivy.uix.textinput  import TextInput
from kivy.uix. button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.progressbar import ProgressBar
from kivy.properties import(StringProperty,NumericProperty,ObjectProperty)
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock
from functools import partial
import re
import Utils
import threading
from regmatch import searchListPat
from progdisplay import ProgDispatch
import time
import threading

lock=threading.Lock()

"""
class AppPop provides application feedback to the user a subclass of the FloatLayout
"""

class AppPop(FloatLayout):
	cancel=ObjectProperty()
	
	

class MsgLabel(Label):
	pass
	
class SuccessLabel(Label):
	pass



"""
class LoadEncFile,a class declaration for the presentation of the FieChooserIconView for the encryption mode,implemented in cryptee.kv as <LoadEncFile>:  
"""	
	
class LoadEncFile(FloatLayout):
	
	load=ObjectProperty()
	cancel=ObjectProperty()
	
"""
class LoadDecFile,a class declaration for the presentation of the FieChooserIconView for the encryption mode,implemented in cryptee.kv as <LoadDecFile>:  
"""	

class LoadDecFile(FloatLayout):
	
	load=ObjectProperty()
	cancel=ObjectProperty()

"""class SaveFile(FloatLayout):
	save=ObjectProperty()
	cancel=ObjectProperty()
"""
"""
Screen class declaration for the encryption mode implemented in cryptee.kv as Encryption a subclass 

"""
class Encryption(Screen):
	pass
			
"""
Screen class declaration for the decryption mode implemented in cryptee.kv as Decryption a subclass 

"""	
class Decryption(Screen):
	pass

"""
ApScreen, a class declaration for the ScreenManager, the root widget of the application

"""	
class ApScreen(ScreenManager):
	
	pathfile=StringProperty("")
	pwd=StringProperty(" ")
	path=StringProperty("")
	loadfile=ObjectProperty()
	savefile=ObjectProperty()
	mode=StringProperty("")
	result=StringProperty("")
	
	def dismiss_pop(self):
		 #dismiss all popup widget instance
		 self.pop.dismiss()
	
	def show_load(self,mode):
		#display Popup for FileChooserIconView, argument is mode either encrypt or decrypt
		if mode=="encrypt":
			content= LoadEncFile(load=self.load,cancel=self.dismiss_pop)
			self.pop=Popup(title="Open File",content=content,size_hint=(0.9,0.9))
			self.pop.open()
		elif mode=="decrypt":
			content= LoadDecFile(load=self.load,cancel=self.dismiss_pop)
			self.pop=Popup(title="Open File",content=content,size_hint=(0.9,0.9))
			self.pop.open()
			
		
		
	
	def load(self,path,filename,mode):
		#method that set the filepath of the file to encrypt or decrypt, argument are path directory of the file,filename name of the file amd mode
		path=path
		file=filename[0]
		filepath=os.path.join(path,file)
		if mode=="encrypt":
			self.ids.f_input1.text=filepath
		elif mode=="decrypt":
			self.ids.f_input2.text=filepath
		self.dismiss_pop()
	
	def validatepath(self,filepath):
		#method to validate filepath,argument filepath return boolean, True if path is valid and false otherwise
		if os.path.isfile(filepath):
			return True
		else:
			return False
	
	
			
	def validatepwd(self,psd):
		#method to validate password,argument password return boolean, True if password is valid and false otherwise
		pwd=psd
		pat=["[A-Z]+","[a-z]+","[0-9]+","[$€%_]+"]
		pwst=searchListPat(pat,pwd)
		if pwst and len(pwd)>=16 and len(pwd) <=20:
			return True
		else:
			return False
	
	
	def processAction(self,filepath,pwd,mode):
		# method to encrypt and decrypt file depending on the mode. Argument are filepath and password, return string succesful if no error
		filepath1=filepath
		pwd1=pwd
		mode1=mode	
		app1=AppPop()
		self.pop=Popup(title="Msg",content=app1,size_hint=(0.7,0.7))
		
		if not self.validatepath(filepath1):
			app1.ids.msg.text="Invalid File name"
			self.pop.open()		
		elif not self.validatepwd(pwd1):
			app1.ids.msg.text="Invalid Password"
			self.pop.open()	
		else:
			self.mode=mode1
			self.filepath=filepath1
			self.pwd=pwd1
			if self.mode=="encrypt":
				self.ids.e_msg.text="Please Wait....Encrypting.."
				
				Clock.schedule_once(partial(self.call_back,self.filepath,self.pwd,self.mode),4)
			
			elif self.mode=="decrypt":
				self.ids.d_msg.text="Please Wait...Decrypting.."
				
				Clock.schedule_once(partial(self.call_back,self.filepath,self.pwd,self.mode),4)
	

	def call_back(self,filepath,pwd,mode,*args):
		app1=AppPop()
		self.pop=Popup(title="Msg",content=app1,size_hint=(0.7,0.7))
		
		if self.mode=="encrypt":
				enc=Utils.encrypt(self.filepath,self.pwd)
				self.ids.e_msg.text=str(enc)
				app1.ids.msg.text=str(enc)
				self.pop.open()		
		elif self.mode=="decrypt":
			 enc=Utils.decrypt(self.filepath,self.pwd)	
			 self.ids.d_msg.text=str(enc)
			 app1.ids.msg.text=str(enc)
			 self.pop.open()
		
	
			 
	

"""
CrpteeApp, the entry point into the application, a subclass of kivy.app.App. It overide the parent build method with additional that contains the logic of the application. 
"""						
			
class CrypteeApp(App):
	def build(self):
		return ApScreen()
		
	
	
			 
					
		
			

Factory.register("MsgL",cls=MsgLabel)		
Factory.register("Load",cls=LoadEncFile)
Factory.register("Load",cls=LoadDecFile)
	

if __name__=="__main__":
		CrypteeApp().run()
		
		
		
	
	
	

		
		