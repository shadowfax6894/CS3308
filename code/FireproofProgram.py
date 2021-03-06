import Tkinter as tk
import tkMessageBox
from Tkinter import *
from LoginFunctions import *
import MySQLdb as mdb
from config import *
from Service import *

TITLE_FONT = ("Helvetica", 16, "bold")
TITLE_X = 20
TITLE_Y = 100
BACK_X = 150
BACK_Y = 350
SECONDARY_X = 300
SECONDARY_Y = 350

class Fireproof(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		""" Initializes the main Tkinter frame container.
		Also places the Fireproof graphic onto every frame.

        :param tk.TK: Toplevel widget of Tkinter which represents the main window of the Fireproof appliation
		"""
		tk.Tk.__init__(self, *args, **kwargs)

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		self.current_account = None

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		fireproof_image = PhotoImage(file="../images/fireproof.png")
		fireproof_banner = Label(image=fireproof_image)
		fireproof_banner.image = fireproof_image
		fireproof_banner.place(bordermode=OUTSIDE,x=150,y=15)		

		self.frames = {}
		for F in (LoginPage, CreateAccountPage, ServicesPage, SettingsPage, ServiceInfoPage, AddNewServicePage, EditPage):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.LoginPage = LoginPage
		self.CreateAccountPage = CreateAccountPage
		self.ServicesPage = ServicesPage
		self.SettingsPage = SettingsPage
		self.ServiceInfoPage = ServiceInfoPage
		self.AddNewServicePage = AddNewServicePage
		self.EditPage = EditPage

		self.show_frame(LoginPage)

	def show_frame(self, c):
		""" This function changes frame (c) so it is visible to the user.

        :param c: Name of frame
		"""
		frame = self.frames[c]
		#tk.Tk.update(self)
		frame.tkraise()

	def getFrame(self, c):
		return self.frames[c]


class LoginPage(tk.Frame):
	def __init__(self, parent, controller):
		""" This initializes the login frame for the app. The login frame
		allows the user to sign in to an existing account, or create a new
		account.

        :param tk.Frame: Tkinter frame widget
		"""
		tk.Frame.__init__(self, parent) 

		username_form_label = Label(self,text="Username")
		username_form_label.place(bordermode=OUTSIDE,x=60,y=140)

		password_form_label = Label(self,text="Password")
		password_form_label.place(bordermode=OUTSIDE,x=60,y=190)
		
		self.username_input_form = Entry(self,bd=5)
		self.username_input_form.place(bordermode=OUTSIDE,x=180,y=140)

		self.password_input_form = Entry(self,bd=5,show="*")
		self.password_input_form.place(bordermode=OUTSIDE,x=180,y=190)
		
		login_button = Button(self, text ="Login", command= lambda: LoginFunctions.checkIfUser(self.username_input_form.get(),self.password_input_form.get(),self,controller))
		login_button.place(bordermode=OUTSIDE,x=SECONDARY_X,y=SECONDARY_Y)		
		
		new_user_label = tk.Label(self, text="New User?")
		new_user_label.place(bordermode=OUTSIDE,x=155,y=310)
		
		create_account_label = tk.Label(self, text="Click here to create an account")
		create_account_label.place(bordermode=OUTSIDE,x=90,y=330)
		
		sign_up_button = Button(self, text ="Sign Up", command=lambda: controller.show_frame(CreateAccountPage))
		sign_up_button.place(bordermode=OUTSIDE,x=BACK_X,y=BACK_Y)
				

class CreateAccountPage(tk.Frame):
	def __init__(self, parent, controller):
		""" This initializes the create account frame for the app. The create
		account frame allows the person to enter information that will be used
		to create a new account in the database.

        :param tk.Frame: Tkinter frame widget
		"""
		tk.Frame.__init__(self, parent)
		
		information_form_label_1 = Label(self, text="Passwords must contain an uppercase letter,")
		information_form_label_1.place(bordermode=OUTSIDE, x=TITLE_X, y=TITLE_Y)
		
		information_form_label_2 = Label(self, text="a lowercase letter, a number and a symbol.")
		information_form_label_2.place(bordermode=OUTSIDE, x=20, y=120)
		
		username_form_label = Label(self,text="Username")
		username_form_label.place(bordermode=OUTSIDE,x=60,y=160) #140

		password_form_label = Label(self,text="Password")
		password_form_label.place(bordermode=OUTSIDE,x=60,y=210)
		
		confirm_password_form_label = Label(self,text="Confirm Password")
		confirm_password_form_label.place(bordermode=OUTSIDE,x=60,y=260)

		self.username_input_form = Entry(self,bd=5)
		self.username_input_form.place(bordermode=OUTSIDE,x=180,y=160)

		self.password_input_form = Entry(self,bd=5,show="*")
		self.password_input_form.place(bordermode=OUTSIDE,x=180,y=210)
		
		self.confirm_password_input_form = Entry(self,bd=5,show="*")
		self.confirm_password_input_form.place(bordermode=OUTSIDE,x=180,y=260)
		
		create_account_button = Button(self, text ="Create Account", command=lambda: LoginFunctions.createAccount(self.username_input_form.get(),\
			self.password_input_form.get(),self.confirm_password_input_form.get(),self,controller))
		create_account_button.place(bordermode=OUTSIDE,x=SECONDARY_X,y=SECONDARY_Y)
		
		go_back_button = Button(self, text ="Back", command=lambda: controller.show_frame(LoginPage))
		go_back_button.place(bordermode=OUTSIDE,x=BACK_X,y=BACK_Y)
		
		#tips = Label(self,text="Passwords should be at least 8 characters")
		#tips.place(bordermode=OUTSIDE,x=60,y=140)								
		
class ServicesPage(tk.Frame):
	def __init__(self, parent, controller):
		""" This initializes the services page frame for the app. This frame
		displays a list of the user's stored services, and provides buttons
		that allow the user to transition to other frames.

        :param tk.Frame: Tkinter frame widget
		"""
		tk.Frame.__init__(self, parent)

		logout_button = Button(self, text="Logout", command=lambda: controller.show_frame(LoginPage))
		logout_button.place(bordermode=OUTSIDE,x=5,y=5)
		
		text_label = "Welcome! Here are your stored services:"
		ListboxLabel = Label(self, text = text_label, font=TITLE_FONT)
		ListboxLabel.place(x=TITLE_X, y=TITLE_Y)
		
		scrollbar = Scrollbar(self, orient=VERTICAL)
		scrollbar.pack(side=RIGHT, fill=Y)
		
		self.CurrentServices = Listbox(self)
		self.CurrentServices.pack()
		
		self.CurrentServices.config(borderwidth=4, height=14, width=38)
		scrollbar.config(command=self.CurrentServices.yview)
		
		self.CurrentServices.place(bordermode=OUTSIDE,x=20,y=145)
		scrollbar.place(x=335,y=145, height=230)
		
		change_password_button = Button(self, text="Settings", command=lambda: controller.show_frame(SettingsPage))
		change_password_button.place(bordermode=OUTSIDE,x=417,y=5)
		
		view_button = Button(self, text="      View Info     ", command=lambda: Service.viewService(self.CurrentServices.curselection()[0],self,controller))
		view_button.place(bordermode=OUTSIDE,x=355,y=260)
		
		add_new_service_button = Button(self, text="Add new service", command=lambda: controller.show_frame(AddNewServicePage))
		add_new_service_button.place(bordermode=OUTSIDE,x=355,y=290)
        
		edit_service_button = Button(self, text="   Edit service    ", command=lambda: Service.populateEditService(self.CurrentServices.curselection()[0],self,controller))
		edit_service_button.place(bordermode=OUTSIDE,x=355,y=320)

		delete_service_button = Button(self, text="  Delete service  ", command=lambda: Service.confirmRemoveService(self,controller))
		delete_service_button.place(bordermode=OUTSIDE, x=355,y=350)
	
	def addToCurrentServicesListBox(self,string):
		self.CurrentServices.insert(END, string)

	def removeFromCurrentServicesListBox(self,index):
		self.CurrentServices.delete(index)

class SettingsPage(tk.Frame):
	def __init__(self, parent, controller):
		""" This initializes the settings page frame for the app. This frame
		provides the user with some buttons for adjusting the settings of
		the app.

        :param tk.Frame: Tkinter frame widget
		"""
		tk.Frame.__init__(self, parent)

		text_label = "Change Fireproof Account Settings:"
		PageLabel = Label(self, text = text_label, font=TITLE_FONT)
		PageLabel.place(x=TITLE_X, y=TITLE_Y)

		change_password_button = Button(self, text="Change Account Username ", command=lambda: controller.show_frame(AddNewServicePage))
		change_password_button.place(bordermode=OUTSIDE,x=150,y=220)
		
		change_password_button = Button(self, text="Change Account Password", command=lambda: controller.show_frame(AddNewServicePage))
		change_password_button.place(bordermode=OUTSIDE,x=150,y=250)
		
		back_button = Button(self, text="Back", command=lambda: controller.show_frame(ServicesPage))
		back_button.place(bordermode=OUTSIDE,x=BACK_X,y=BACK_Y)
		
class ServiceInfoPage(tk.Frame):	#ViewServicePage
	def __init__(self, parent, controller):
		""" This initializes the individual service page frames for the services
		that are stored on this account. This frame displays the stored username,
		password and name of the service. It also displays a button that allows
		the user to edit the information associated with this service.

        :param tk.Frame: Tkinter frame widget
		"""
		tk.Frame.__init__(self, parent)
		
		text_label = "Service Information:"
		PageLabel = Label(self, text = text_label, font=TITLE_FONT)
		PageLabel.place(x=TITLE_X, y=TITLE_Y)
		
		service_form_label = Label(self,text="Service Name:")
		service_form_label.place(bordermode=OUTSIDE,x=60,y=140)
		
		curr_username_form_label = Label(self,text="Current Username:")
		curr_username_form_label.place(bordermode=OUTSIDE,x=60,y=165)
		
		curr_password_form_label = Label(self,text="Current Password:")
		curr_password_form_label.place(bordermode=OUTSIDE,x=60,y=190)
        
		edit_service_button = Button(self, text="     Edit service     ", command=lambda: Service.populateEditServiceFromServiceInfo(self,controller))
		edit_service_button.place(bordermode=OUTSIDE,x=SECONDARY_X,y=SECONDARY_Y)
		
		back_button = Button(self, text="Back", command=lambda: Service.hideFields(self,controller))
		back_button.place(bordermode=OUTSIDE,x=BACK_X,y=BACK_Y)

class EditPage(tk.Frame):
	def __init__(self, parent, controller):
		""" This initializes the edit page frame for the app. This frame
		displays the service name along with the current stored username
		and password, and allows the user to save a new username and 
		password for this service.

        :param tk.Frame: Tkinter frame widget
		"""
		tk.Frame.__init__(self, parent)

		text_label = "Edit this service:"
		PageLabel = Label(self, text = text_label, font=TITLE_FONT)
		PageLabel.place(x=TITLE_X, y=TITLE_Y)

		service_form_label = Label(self,text="Service Name:")
		service_form_label.place(bordermode=OUTSIDE,x=60,y =140)
		
		curr_username_form_label = Label(self,text="Current Username:")
		curr_username_form_label.place(bordermode=OUTSIDE,x=60,y=165)
		
		curr_password_form_label = Label(self,text="Current Password:")
		curr_password_form_label.place(bordermode=OUTSIDE,x=60,y=190)
		
		username_form_label = Label(self,text="New Username")
		username_form_label.place(bordermode=OUTSIDE,x=60,y=235)
		username_input_form = Entry(self,bd=5)
		username_input_form.place(bordermode=OUTSIDE,x=210,y=230)
		
		password_form_label = Label(self,text="New Password")
		password_form_label.place(bordermode=OUTSIDE,x=60,y=270)
		password_input_form = Entry(self,bd=5,show="*")
		password_input_form.place(bordermode=OUTSIDE,x=210,y=265)
		
		confirm_password_label = Label(self,text="Confirm New Password")
		confirm_password_label.place(bordermode=OUTSIDE,x=60,y=305)
		confirm_password_input_form = Entry(self,bd=5,show="*")
		confirm_password_input_form.place(bordermode=OUTSIDE,x=210,y=300)
		
		back_button = Button(self, text="Cancel", command=lambda: Service.hideFields(self,controller))
		back_button.place(bordermode=OUTSIDE,x=BACK_X,y=BACK_Y)

		save_button = Button(self, text="Save", command=lambda: Service.saveNewServiceInfo(self,controller,username_input_form.get(),password_input_form.get(),confirm_password_input_form.get()))

		save_button.place(bordermode=OUTSIDE,x=SECONDARY_X,y=SECONDARY_Y)

class AddNewServicePage(tk.Frame):
	def __init__(self, parent, controller):
		""" This initializes the add new service page frame for the app.
		This page allows the user to enter in the service name, along with
		the username and password for that service, to be stored in a 
		database.

        :param tk.Frame: Tkinter frame widget
		"""
		tk.Frame.__init__(self, parent)
		
		text_label = "Add information for a new service:"
		PageLabel = Label(self, text = text_label, font=TITLE_FONT)
		PageLabel.place(x=TITLE_X, y=TITLE_Y)
		
		service_form_label = Label(self, text = "Service Name")
		service_form_label.place(bordermode=OUTSIDE, x=50, y=140)
		
		self.service_input_form = Entry(self, bd=5)
		self.service_input_form.place(bordermode=OUTSIDE, x=200, y=140)
		
		username_form_label = Label(self, text = "Username")
		username_form_label.place(bordermode=OUTSIDE, x=50, y=180)
		
		password_form_label = Label(self, text = "Password")
		password_form_label.place(bordermode=OUTSIDE, x=50, y=220)
		
		self.username_input_form = Entry(self, bd=5)
		self.username_input_form.place(bordermode=OUTSIDE, x=200, y=180)
		
		self.password_input_form = Entry(self, bd=5, show="*")
		self.password_input_form.place(bordermode=OUTSIDE, x=200, y=220)
		
		existingForm = Label(self, text = "Add to existing service:")
		existingForm.place(bordermode=OUTSIDE, x=50, y=265)
				
		scrollbar = Scrollbar(self, orient=VERTICAL)
		scrollbar.pack(side=RIGHT, fill=Y)
		
		self.add_to_existing = Listbox(self, yscrollcommand=scrollbar.set)
		self.add_to_existing.pack(side=LEFT, fill=BOTH)
		
		self.add_to_existing.config(yscrollcommand=scrollbar.set, borderwidth=4, height=2, width=21)
		scrollbar.config(command=self.add_to_existing.yview)
		
		self.add_to_existing.place(bordermode=OUTSIDE,x=200,y=260)
		scrollbar.place(x=380,y=260, height=40)
				
		add_service_button = Button(self, text ="Add Service", command=lambda: Service.addServiceChecker(self.username_input_form.get(),\
			self.password_input_form.get(),self.service_input_form.get(),self,controller))
		add_service_button.place(bordermode=OUTSIDE,x=SECONDARY_X,y=SECONDARY_Y)
		
		#more_options_button = Button(self, text ="More Options", command=lambda: controller.show_frame(ServicesPage))
		#more_options_button.place(bordermode=OUTSIDE,x=200,y=350)
		
		back_button = Button(self, text ="Back", command=lambda: controller.show_frame(ServicesPage))
		back_button.place(bordermode=OUTSIDE,x=BACK_X,y=BACK_Y)

	def addToExistingServicesListBox(self,string):
		self.add_to_existing.insert(END, string)

	def removeFromExistingServicesListBox(self,index):
		self.add_to_existing.delete(index)

if __name__ == "__main__":

	con = mdb.connect(MYSQL_LOC,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DBNAME);

	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS FireproofAccountLogin")
		cur.execute("DROP TABLE IF EXISTS FireproofServices")
		cur.execute("DROP TABLE IF EXISTS FireproofServicesAccounts")
		cur.execute("CREATE TABLE FireproofAccountLogin (id INT(6) PRIMARY KEY,UserName VARCHAR(30) NOT NULL,\
			PasswordName VARCHAR(30) NOT NULL)")
			
	Service.createServiceTable()
	ServiceAccount.createServiceAccountsTable()
    
	app = Fireproof()
	window_width = 500
	window_height = 400
	screen_width = app.winfo_screenwidth()
	screen_height = app.winfo_screenheight()
	position_x = (screen_width/2) - (window_width/2)
	position_y = (screen_height/2) - (window_height/2)
	app.wm_geometry('%dx%d+%d+%d' % (window_width, window_height, position_x, position_y))
	app.mainloop()
