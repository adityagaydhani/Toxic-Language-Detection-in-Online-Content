import config
import csv
import pickle
import time
import tweepy
import numpy as np
import pandas as pd
from models.predict_model import predictResult
from settings import *
from tkinter import *
from tkinter import messagebox

def back(new_window):
	new_window.destroy()

def post(text):
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_key, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	api.update_status(text)
	messagebox.showinfo("Result","clean tweet posted")

def Enterlogin(top):
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_key, access_token_secret)
	#api = tweepy.API(auth, wait_on_rate_limit=True)
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	messagebox.showinfo("Autentication","Successful")
	top.destroy()
	root =Tk()
	app=App(root)


class pollwindow:

	def __init__(self,new_window):
		new_window.title('Tweet polling window')
		self.button1 =Button(new_window, text="Fetch from "+str(username)+" timeline",font=("Helvetica",10), command=lambda:self.get_tweets())
		self.button1.grid(row=0, column=1,padx=5,pady=5)
		self.button1 =Button(new_window, text="Stop ",font=("Helvetica",10), command=lambda:back(new_window))
		self.button1.grid(row=0, column=2,padx=5,pady=5)
		self.text1=Text(new_window,height=5,font=("Helvetica",15))
		self.text1.grid(row=1, column=1,padx=10,pady=10)
		#text1.grid(row=, column=1,padx=10,pady=10)
		new_window.mainloop()


	def get_tweets(self):

		auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
		auth.set_access_token(access_key, access_token_secret)
		#api = tweepy.API(auth, wait_on_rate_limit=True)
		api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
		tmp=[]
		read_tweets = api.user_timeline(user=username,count=10)
		tmp.extend(read_tweets)
		newest=tmp[0].id
		outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in tmp]
		with open('%s_tweets.csv' % username, mode='w', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(["id","created_at","text"])
			writer.writerows(outtweets)
		df = pd.read_csv('%s_tweets.csv' % username, index_col=False)
		texts = df['text'].values
		for txt in texts:
			txt=txt[1:]
			length=len(txt)
			#print (length)
			predicted_class =str(predictResult([txt], obj))
			if predicted_class=="[0]":
				self.text1.insert(INSERT,txt+"\t\t...(hate)\n")
			elif predicted_class=="[1]":
				self.text1.insert(INSERT,txt+"\t\t...(offensive)\n")
			elif predicted_class=="[2]":
				self.text1.insert(INSERT,txt+"\t\t...(clean)\n")

		#polling for tweets
		flag=0
		val=0
		while True:	#len(read_tweets) > 0:
			if val>0:
				if messagebox.askyesno('Verify', 'Contine?'):
					val+=1
				else:
					break
			print ("getting tweets before tweet id :" +str(newest))
			print (str(len(tmp))+"... tweets downloaded so far")
			read_tweets = api.user_timeline(user= username,count=1,since_id=newest)
			for status in api.user_timeline():
				print ("newest tweet ID : "+str(status.id))
				print ("previous latest tweet ID :"+str(newest))
				if status.id == newest:
					flag=1
					break
				else:
					flag=0
					break
			if flag==1:
				flag=0
				val+=1
				time.sleep(5)
				continue
	
				#save most recent tweets
			tmp.extend(read_tweets)
		
				#update the id of the oldest tweet less one
			newest = tmp[0].id
			print (str(len(tmp))+"... tweets downloaded so far")
			with open('%s_tweets.csv' % username, mode='w', encoding='utf-8') as f:
				writer = csv.writer(f)
				writer.writerow(["id","created_at","text"])
				writer.writerows(outtweets)
			df = pd.read_csv('%s_tweets.csv' % username, index_col=False)
			texts = df['text'].values
			txt=texts[0]
			txt=txt[1:]
			length=len(txt)
			print (length)
			predicted_class = str(predictResult([txt], obj))
			if predicted_class=="[0]":
				self.text1.insert(INSERT,txt+"\t\t...(hate)\n")
			elif predicted_class=="[1]":
				self.text1.insert(INSERT,txt+"\t\t...(offensive)\n")
			elif predicted_class=="[2]":
				self.text1.insert(INSERT,txt+"\t\t...(clean)\n")
		
		

class cleanwindow:

	def __init__(self,new_window,text):
		new_window.title('cleanWindow')
		new_window.minsize(width=300,height=100)
		new_window.title('Message')
		Label(new_window, text="Result: clean speech message detected "+text,font=("Helvetica",10)).pack()
		B1=Button(new_window, text="Close", command=lambda:back(new_window))
		B1.pack()
		B2=Button(new_window, text="Post", command=lambda:post(text))
		B2.pack()
		new_window.mainloop()



class App:
	def fetch(self):
		new_window = Tk()
		app2=pollwindow(new_window)


	def enter(self):
		#print (self.text.get("1.0",END))
		self.text1.delete(1.0,END)
		length=len(self.text.get("1.0",END))
		numberow=1
		predicted_class = str(predictResult([self.text.get("1.0",END)], obj))
		if predicted_class=="[0]":
			self.text1.insert(INSERT,self.text.get("1.0",END))
			self.text1.tag_add("newtag"+str(numberow),str(numberow)+".0",str(numberow)+"."+str(length))
			self.text1.tag_config("newtag"+str(numberow),background="red")
			numberow=numberow+1
			messagebox.showwarning("Result","hate speech detected")
		if predicted_class=="[1]":
			self.text1.insert(INSERT,self.text.get("1.0",END))
			self.text1.tag_add("newtag"+str(numberow),str(numberow)+".0",str(numberow)+"."+str(length))
			self.text1.tag_config("newtag"+str(numberow),background="yellow")
			numberow=numberow+1
			messagebox.showwarning("Result","Offensive speech detected")
		if predicted_class=="[2]":
			self.text1.insert(INSERT,self.text.get("1.0",END))
			self.text1.tag_add("newtag"+str(numberow),str(numberow)+".0",str(numberow)+"."+str(length))
			self.text1.tag_config("newtag"+str(numberow),background="green")
			numberow=numberow+1
			new_window = Tk()
			app1=cleanwindow(new_window,self.text.get("1.0",END))			

	def __init__(self,root):
		root.title('Hate Speech Window')
		root.minsize(width=600,height=400)
		#root.resizeable(widht=False,height=False)
		self.text=Text(root,height=5,font=("Helvetica",15))
		Label(root, text="Chat Box:",font=("Helvetica",15)).grid(row=0,column=1,padx=10,pady=1)
		self.text.grid(row=1, column=1,padx=10,pady=10)
		self.button1 =Button(root, text="Check",fg="black",font=("Helvetica",15),relief="groove",command=self.enter)
		self.button1.grid(row=1, column=2,padx=20,pady=10)
		self.button2 =Button(root, text="Fetch",fg="black",font=("Helvetica",15),relief="groove",command=self.fetch)
		self.button2.grid(row=2, column=2,padx=20,pady=10)
		Label(root, text="Output:",font=("Helvetica",15)).grid(row=3,column=1,padx=10,pady=1)
		self.button3 =Button(root, text="Quit",fg="black",font=("Helvetica",15),relief="groove",command=lambda:back(root))
		self.button3.grid(row=4, column=2,padx=20,pady=10)
		self.text1=Text(root,height=5,font=("Helvetica",15))
		self.text1.grid(row=4, column=1,padx=10,pady=10)
		root.mainloop()

class Login:

	def __init__(self,top):
		top.title('Login')
		#top.minsize(width=600,height=500)
		#root.resizeable(widht=False,height=False)
		Label(top, text="Username: ",font=("Helvetica",15)).grid(row=0,column=1,padx=5,pady=5)
		self.E1 = Text(top,height=1,font=("Helvetica",15))
		self.E1.grid(row=0,column=2,padx=5,pady=5)
		self.E1.insert(END, "Test_tweets")
		global username
		username=self.E1.get("1.0",'end-1c')
		print ("You are using keys:\n"+username)
		con_key = config.consumer_key
		con_secret = config.consumer_secret
		acc_token = config.access_token
		acc_token_secret = config.access_token_secret

		Label(top, text="Consumer key: ",font=("Helvetica",15)).grid(row=1,column=1,padx=5,pady=5)
		self.E2 = Text(top,height=1,font=("Helvetica",15))
		self.E2.grid(row=1,column=2,padx=5,pady=5)
		self.E2.insert(END, con_key)
		global consumer_token
		consumer_token=self.E2.get("1.0",'end-1c')
		print (consumer_token)

		Label(top, text="Consumer secret key ",font=("Helvetica",15)).grid(row=2,column=1,padx=5,pady=5)
		self.E3 =Text(top,height=1,font=("Helvetica",15))
		self.E3.grid(row=2,column=2,padx=5,pady=5)
		self.E3.insert(END, con_secret)
		global consumer_secret
		consumer_secret=self.E3.get("1.0",'end-1c')
		print (consumer_secret)

		Label(top, text="Access token key: ",font=("Helvetica",15)).grid(row=3,column=1,padx=5,pady=5)
		self.E4 = Text(top,height=1,font=("Helvetica",15))
		self.E4.grid(row=3,column=2,padx=5,pady=5)
		self.E4.insert(END, acc_token)
		global access_key
		access_key=self.E4.get("1.0",'end-1c')
		print (access_key)

		Label(top, text="Access token secret key ",font=("Helvetica",15)).grid(row=4,column=1,padx=5,pady=5)
		self.E5 = Text(top,height=1,font=("Helvetica",15))
		self.E5.grid(row=4,column=2,padx=5,pady=5)
		self.E5.insert(END, acc_token_secret)
		global access_token_secret
		access_token_secret=self.E5.get("1.0",'end-1c')
		print (access_token_secret)

		self.button1 =Button(top, text="Authenticate",fg="black",font=("Helvetica",10),relief="groove",command=lambda:Enterlogin(top))
		self.button1.grid(row=5, column=2,padx=5,pady=5)
		top.mainloop()


with open(FINAL_VECT, 'rb') as final_count_vect:
	count_vect = pickle.load(final_count_vect)
with open(FINAL_TFIDF, 'rb') as final_tf_transformer:
	tf_transformer = pickle.load(final_tf_transformer)
with open(FINAL_MODEL, 'rb') as final_model:
	lr_clf = pickle.load(final_model)
obj = [count_vect, tf_transformer, lr_clf]
top =Tk()
app=Login(top)
