#! python2.7
# -*- coding: utf-8 -*-
# recommendLastFm.py - get information from website named Lastfm using API

from lastfmlogin import API_KEY, API_SECRET, username, password
import pylast

password_hash = pylast.md5(password)

network = pylast.LastFMNetwork(api_key = API_KEY, \
            api_secret = API_SECRET, username = username, \
            password_hash = password_hash)
            
user = network.get_user("RJ")
tag = user.get_top_tags()
