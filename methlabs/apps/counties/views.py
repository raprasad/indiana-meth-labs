
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext


def view_author_list(request):
    return HttpResponse('authors')