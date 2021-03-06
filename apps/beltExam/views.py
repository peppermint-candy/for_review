from django.shortcuts import render, redirect, HttpResponse
from django.db.models import F
import bcrypt
import re
from django.contrib import messages
from .models import User, Poke
from django.core.urlresolvers import reverse


def index(request):
	return render(request, "index.html")
# Create your views here.
def register(request):
	if request.method == 'POST':
		user_tuple2 = User.userManager.register(request.POST['first_name'], request.POST['alias'], request.POST['email'], request.POST['pw'], request.POST['c_pw'])
		if user_tuple2[0]:
			print User.userManager.all()
			Poke.objects.create(userpoked = user_tuple2[1].id, poked = 0)
			request.session['id'] = user_tuple2[1].id
			request.session['name'] = user_tuple2[1].first_name
			return redirect('/pokes')
		else:
			for i in user_tuple2[1]:
				messages.info( request, user_tuple2[1][i], extra_tags = 'rg')
		 	return redirect('/')

def login(request):
	if request.method == 'POST':
		user_tuple = User.userManager.login(request.POST['elogin'] , request.POST['Lpw'])
		if user_tuple[0]:
			request.session['id'] = user_tuple[1].id
			request.session['name'] = user_tuple[1].first_name

			return redirect('/pokes')
		else:	
			for i in user_tuple[1]:
				messages.info( request, user_tuple[1][i], extra_tags = 'lg')
			return redirect('/')

def pokes(request):
	context = {
		"users" : User.userManager.exclude( id = request.session['id']),
		"pokes" : Poke.objects.all(),
		"ppp"	: Poke.objects.filter(userpoked = request.session['id'])
	}
	return render(request, "index2.html",context)

def logoff(request):
	request.session.clear()
	return redirect('/')

def clickpoke(request, id):
	if request.method == "POST":
		try: 
			p1 = User.userManager.get( p1 = request.session['id'])
			p2 = User.userManager.get( p2 = id)
			print "1" * 50
			if p1 and p2:
				print "2" * 50
				Poke.objects.get( userpoke = p1[0], userpoked=p2[0])[0].update( poked = F('poked') + 1 )
				print "5" * 60
				p1.save()
				p2.save()
				print " Poke update"
				return redirect('/pokes')
		except:
			print "3" * 50
			Poke.objects.create( userpoke = request.session['id'], userpoked = User.userManager.get( id = id))
			print "Create new poke"
			return redirect('/pokes')
	else:
		return HttpResponse('error')

def check(request):
	user = User.userManager.get(id = request.session['id'])
	print user
	return redirect('/pokes')