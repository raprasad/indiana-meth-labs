from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext


def view_hello(request):
    return HttpResponse('hello')


def view_hello2(request):
    d = {}
    d['greeting'] = 'hello'
    d['pets'] = ['dog', 'cat', 'bird']
        
    return render_to_response('hello/view_hello2.html'\
                            , d\
                            , context_instance=RequestContext(request))

def view_lab_list(request):
    
    d = {}
    return render_to_response('view_lab_list.html'\
                              , d\
                              , context_instance=RequestContext(request))