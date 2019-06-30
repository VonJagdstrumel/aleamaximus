#!/usr/bin/env python3

import getopt
import json
import sys

import tweepy

opts, _ = getopt.getopt(sys.argv[1:], "t:c:a:s:f:")
opts = dict(opts)
consumer_token = opts['-t']
consumer_secret = opts['-c']
access_token = opts.get('-a')
access_secret = opts.get('-s')
reply_to = opts.get('-r')
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

if access_token and access_secret:
    auth.set_access_token(access_token, access_secret)
    tweet = sys.stdin.readline()
    api = tweepy.API(auth)

    if reply_to:
        tweet = '@' + api.get_status(reply_to).author.screen_name + ' ' + tweet
        api.update_status(tweet, reply_to)
    else:
        api.update_status(tweet)

else:
    print(auth.get_authorization_url())
    verifier = input('Verifier:')
    auth.request_token = { 'oauth_token': auth.request_token['oauth_token'], 'oauth_token_secret': verifier }
    print(auth.get_access_token(verifier))
