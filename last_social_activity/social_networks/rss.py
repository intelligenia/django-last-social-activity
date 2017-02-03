# -.- coding: utf-8 -.-

from __future__ import unicode_literals, absolute_import

# Import urlopen in Python2 and 3
try:
	from urllib.request import urlopen, HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError

from httplib import HTTPException

import dateutil
from bs4 import BeautifulSoup
from django.conf import settings
from dateutil import parser
from last_social_activity.models import SocialNetworkItemCache


class RssReader(object):

	def __init__(self, id):
		rss_settings = self._get_rss_settings(id)
		self.rss_url = rss_settings["rss_url"]
		self.url = rss_settings["url"]

	# Fetch the last num_items items
	def get_last_items(self, num_items=5):

		# If there is a hit, get from cache
		if SocialNetworkItemCache.hit("rss", num_items=num_items, rss_url=self.rss_url):
			return SocialNetworkItemCache.get("rss", num_items=num_items , rss_url=self.rss_url).response_dict

		# If this URL does not exist or the chache has expired, get a new version of the RSS and update it
		url = self.rss_url

		try:
			data = urlopen(url)
			soup = BeautifulSoup(data, 'xml')
		except (HttpError, HTTPException, ValueError) as e:
			if SocialNetworkItemCache.hit("rss", num_items=num_items, rss_url=self.rss_url):
				return SocialNetworkItemCache.get("rss", num_items=num_items, rss_url=self.rss_url).response_dict
			return {'info': None, 'rss_items': [], 'url': self.url}

		#info
		title = soup.find('title')
		description = soup.find('description')
		categories_xml = soup.find_all('category')
		categories = []
		for category in categories_xml:
			categories.append(category.string)

		info = {
			'title': title.string,
			'description': description.string,
			'categories': categories
		}

		# Use BeautifulSoup to process the items
		items = soup.find_all('item', limit=num_items)
		rss_items = []
		for item in items:
			item_content = {}
			for content in item.contents:
				if content.name:
					field_name = content.name.lower()
					field_content = content.string
					# If the field is a pubdate, convert it to date
					if field_name == 'pubdate':
						field_content = dateutil.parser.parse(field_content).isoformat()
					item_content[field_name] = field_content

			rss_items.append(item_content)

		rss_last_items = {'info': info, 'rss_items': rss_items, 'url': self.url}
		SocialNetworkItemCache.create("rss", num_items, response=rss_last_items, rss_url=self.rss_url)

		return rss_last_items

	# Return the settings
	def _get_rss_settings(self, id):
		rss_settings = settings.LAST_SOCIAL_ACTIVITY_CREDENTIALS.get('rss')

		if not rss_settings:
			raise AssertionError(u"Settings not found for RSS sources")

		particular_rss_settings = rss_settings.get(id)

		if type(particular_rss_settings) is dict:
			return particular_rss_settings

		raise AssertionError(u"No RSS settings for source {0} has been found".format(id))
