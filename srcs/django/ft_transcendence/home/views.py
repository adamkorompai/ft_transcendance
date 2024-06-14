from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Score
from django.http import HttpResponse
from render_block import render_block_to_string
import json
import logging

# get acces to environment variables
log = logging.getLogger(__name__)
logging.basicConfig(filename="logs.txt", encoding='utf-8', level=logging.DEBUG)

@login_required(login_url='/accounts/login/?redirected=true')
def welcome(request):
	context = {
		"show_alert": True,
		"all_users": User.objects.all(),
	}
	log.info("In welcome views")
	log.info(request.META)
	if 'HTTP_SPA_CHECK' in request.META:
		html = render_block_to_string('welcome.html', 'body', context)
		return HttpResponse(json.dumps({"html": html, "title": "Home"}), content_type="application/json")
	return render(request, 'welcome.html', context)