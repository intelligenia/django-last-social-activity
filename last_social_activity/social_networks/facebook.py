# -.- coding: utf-8 -.-

from __future__ import unicode_literals, absolute_import

from django.conf import settings

from dateutil import parser
import requests

try:
	from urllib.request import urlopen, HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError

from httplib import HTTPException

from last_social_activity.models import SocialNetworkItemCache


class FacebookReader(object):
	# To get an ACCESS TOKEN use
	# https://graph.facebook.com/oauth/access_token?client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&grant_type=client_credentials

	GET_POSTS_URL = 'https://graph.facebook.com/{0}/posts'

	def __init__(self):
		credentials = self._get_credentials()
		self.access_token = credentials["access_token"]
		self.profile = credentials["profile"]
		self.api = None

	def connect(self):
		self.api = None

	# Fetch the last num_posts posts
	def get_last_posts(self, num_posts=5):

		# If there is a hit, get from cache
		if SocialNetworkItemCache.hit("facebook", num_posts):
			return SocialNetworkItemCache.get("facebook", num_posts).response_dict

		parameters = {
			'access_token': self.access_token,
			'fields': 'type,created_time,link,permalink_url,message,message_tags,name,picture,full_picture,source',
			'limit': num_posts
		}

		try:
			response = requests.get(FacebookReader.GET_POSTS_URL.format(self.profile), params=parameters)
			posts = response.json().get('data')
		except (HttpError, HTTPException, ValueError, requests.exceptions.RequestException) as e:
			# If there is a hit, get from cache
			if SocialNetworkItemCache.hit("facebook", num_posts):
				return SocialNetworkItemCache.get("facebook", num_posts).response_dict
			return []

		for post in posts:
			post['created_at'] = parser.parse(post.get('created_time')).isoformat()

		SocialNetworkItemCache.create("facebook", num_posts, posts)
		return posts

	# Return the credentials of the Facebook account
	def _get_credentials(self):
		facebook_credentials = settings.LAST_SOCIAL_ACTIVITY_CREDENTIALS.get('facebook')

		if not facebook_credentials:
			raise AssertionError(u"Credentials not found for facebook")

		if type(facebook_credentials) is dict:
			return facebook_credentials

		raise AssertionError(u"No other credential source is implemented at the moment")
