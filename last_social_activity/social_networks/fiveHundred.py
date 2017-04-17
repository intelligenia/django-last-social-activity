# -.- coding: utf-8 -.-

from __future__ import unicode_literals

from django.conf import settings

# Import urlopen in Python2 and 3
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen

try:
	from urllib.request import urlopen, HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError

from httplib import HTTPException

import json

from last_social_activity.models import SocialNetworkItemCache


class FiveHundredReader(object):

	URL = 'https://api.500px.com/v1/photos?consumer_key={0}&feature=user&username={1}&rpp={2}&sort=created_at&include_store=store_download&include_states=voted&image_size=1,2,3,4,1080,1600'

	def __init__(self):
		credentials = self._get_credentials()
		self.access_token = credentials["access_token"]
		self.profile = credentials["profile"]
		self.api = None

	def connect(self):
		self.api = None

	def get_last_media(self, num_images=5):

		# If there is a hit, get from cache
		if SocialNetworkItemCache.hit("fivehundred", num_images):
			return SocialNetworkItemCache.get("fivehundred", num_images).response_dict

		# Otherwise fetch data from 500px servers
			url = FiveHundredReader.URL.format(self.access_token, self.profile, num_images)
		try:
			response = urlopen(url)
			data = json.load(response)
		except (HttpError, HTTPException, ValueError) as e:
			if SocialNetworkItemCache.hit("fivehundred", num_images):
				return SocialNetworkItemCache.get("fivehundred", num_images).response_dict
			return []

		media = data.get('photos', None)
		print media
		return media

	# Return the credentials of the 500px account
	def _get_credentials(self):
		fivehundred_credentials = settings.LAST_SOCIAL_ACTIVITY_CREDENTIALS.get("fivehundred")
		if not fivehundred_credentials:
			raise AssertionError(u"Credentials not found for 500px")

		if type(fivehundred_credentials) is dict:
			return fivehundred_credentials

		raise AssertionError(u"No other credential source is implemented at the moment")

