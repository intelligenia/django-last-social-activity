# -.- coding: utf-8 -.-

from __future__ import unicode_literals, absolute_import

import json
from last_social_activity.models import SocialNetworkItemCache
from django.conf import settings

# Import urlopen in Python2 and 3
try:
	from urllib.request import urlopen, HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError

from httplib import HTTPException


# A simple Pinterest reader
class PinterestReader:

	USER_INFO_URL = "https://api.pinterest.com/v1/users/{0}/?access_token={1}&fields=first_name%2Cid%2Clast_name%2Curl%2Cimage%2Caccount_type%2Cbio%2Ccounts%2Ccreated_at"
	MY_INFO_URL = 'https://api.pinterest.com/v1/me/?access_token={0}&fields=username,first_name,last_name,counts,image'
	LAST_PINS_URL = 'https://api.pinterest.com/v1/me/pins/?access_token={0}&fields=id,creator,note,image,url,media,metadata&limit={1}'

	def __init__(self):
		credentials = self._get_credentials()
		self.access_token = credentials["access_token"]
		self.profile = credentials["profile"]
		self.api = None
		self.user = None

	# Dummy method kept for compatibility reasons
	def connect(self):
		pass

	# Get last pins of the user
	def get_last_pins(self, num_pins=5):
		last_activity = self.get_last_activity(num_pins)
		return last_activity["last_pins"]

	# Get last activity of the user
	def get_last_activity(self, num_pins=5):

		if SocialNetworkItemCache.hit("pinterest", num_pins):
			return SocialNetworkItemCache.get("pinterest", num_pins).response_dict

		try:
			response = urlopen(PinterestReader.LAST_PINS_URL.format(self.access_token, num_pins))
			response_data = json.load(response)
		except (HttpError, HTTPException, ValueError) as e:
			if SocialNetworkItemCache.hit("pinterest", num_pins):
				return SocialNetworkItemCache.get("pinterest", num_pins).response_dict
			return {"user": None, "last_pins": []}

		last_pins = response_data.get('data', [])
		for pin in last_pins:
			creator_id = pin["creator"]["id"]
			pin["creator"] = self._get_user_data(creator_id)

		pinterest_data = {"user": self._get_my_data(), "last_pins": last_pins}
		SocialNetworkItemCache.create("pinterest", num_pins, pinterest_data)
		return pinterest_data

	# Fetch this user data
	def _get_my_data(self):
		response = urlopen(PinterestReader.MY_INFO_URL.format(self.access_token))
		data = json.load(response)
		return data.get('data', [])

	# Fetch a user's data
	def _get_user_data(self, userid):
		get_user_data_url = PinterestReader.USER_INFO_URL.format(userid, self.access_token)
		response = urlopen(get_user_data_url)
		response_data = json.loads(response.read())
		user_info = response_data.get('data', [])
		return user_info

	# Return the credentials of the Pinterest account
	def _get_credentials(self):
		pinterest_credentials = settings.LAST_SOCIAL_ACTIVITY_CREDENTIALS.get("pinterest")
		if not pinterest_credentials:
			raise AssertionError(u"Credentials not found for pinterest")

		if type(pinterest_credentials) is dict:
			return pinterest_credentials

		raise AssertionError(u"No other credential source is implemented at the moment")
