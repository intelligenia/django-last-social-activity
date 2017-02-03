# -.- coding: utf-8 -.-

from __future__ import unicode_literals, absolute_import

import twitter
import dateutil
from django.conf import settings

try:
	from urllib.request import urlopen, HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError

from httplib import HTTPException

# A wrapper of the official Twitter API
from last_social_activity.models import SocialNetworkItemCache


class TwitterReader(object):

	def __init__(self):
		credentials = self._get_credentials()
		self.profile_url = credentials["profile_url"]
		self.username = credentials["username"]
		self.consumer_key = credentials["consumer_key"]
		self.consumer_secret = credentials["consumer_secret"]
		self.access_token_key = credentials["access_token_key"]
		self.access_token_secret = credentials["access_token_secret"]
		self.api = None

	def connect(self):
		self.api = twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)

	def get_last_tweets(self, num_tweets=5):

		# If there is a hit, get from cache
		if SocialNetworkItemCache.hit("twitter", num_tweets):
			return SocialNetworkItemCache.get("twitter", num_tweets).response_dict

		# Otherwise, get from Twitter
		try:
			tweets = self.api.GetUserTimeline(screen_name=self.username)[:num_tweets]
		except (HttpError, HTTPException, ValueError, requests.exceptions.RequestException) as e:
			if SocialNetworkItemCache.hit("twitter", num_tweets):
				return SocialNetworkItemCache.get("twitter", num_tweets).response_dict
			return []

		tweet_list = []
		for tweet in tweets:
			tweet.created_at = dateutil.parser.parse(tweet.created_at)
			tweet_as_dict = {
				"id": tweet.id,
				"text": tweet.text,
				"created_at": tweet.created_at.isoformat()
			}
			tweet_list.append(tweet_as_dict)

		SocialNetworkItemCache.create("twitter", num_tweets, tweet_list)
		return tweet_list

	# Return the credentials of the Twitter account
	def _get_credentials(self):
		twitter_credentials = settings.LAST_SOCIAL_ACTIVITY_CREDENTIALS.get("twitter")
		if not twitter_credentials:
			raise AssertionError(u"Credentials not found for twitter")

		if type(twitter_credentials) is dict:
			return twitter_credentials

		raise AssertionError(u"No other credential source is implemented at the moment")

