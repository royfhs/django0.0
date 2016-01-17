#coding:utf-8
import sae
from m1 import wsgi

application = sae.create_wsgi_app(wsgi.application)
