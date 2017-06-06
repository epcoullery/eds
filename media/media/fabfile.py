# -*- coding: utf-8 -*-
import os
import sys

from fabric.api import cd, env, get, local, prefix, prompt, run
from fabric.utils import abort

env.user = 'alzo'

env.hosts = ['clio.webzos.net']
APP_DIR = '/var/www/histone'

def toto():
    with cd ('/home/alzo/'):
        run('./.maj.sh')
	



