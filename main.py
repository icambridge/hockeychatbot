#!/usr/bin/env python3
import twitter
import twitter_client
import eliteprospect
import parser
import engine
import logging
import tasks
import os
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.model import Metadata, Interpreter

builder = ComponentBuilder(use_cache=False)

try:
    model_dir = os.environ["MODEL_DIR"]
    twitter_consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    twitter_consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    twitter_access_token_key = os.environ["TWITTER_ACCESS_TOKEN_KEY"]
    twitter_access_token_secret  = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    eliteprospect_key = os.environ["EP_API_KEY"]
except KeyError:
    print "Please set all the env variables"
    sys.exit(1)

# where `model_directory points to the folder the mo
interpreter = Interpreter.load(model_dir)

api = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token_key,
                  access_token_secret=twitter_access_token_secret)


logging.basicConfig(level=logging.INFO)
intents = {}
intents["whoIs"] = eliteprospect.WhoIsTask(eliteprospect_key)
intents["teamRoster"] = eliteprospect.TeamRosterTask(eliteprospect_key)
intents["affirm"] = tasks.YesTask()
intents["greeting"] = tasks.HelloTask()

client = twitter_client.TwitterClient(api)
parser = parser.Parser(interpreter)

engine = engine.MainEngine(client, parser, intents)
engine.run()