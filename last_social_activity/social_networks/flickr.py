# -.- coding: utf-8 -.-

from __future__ import unicode_literals

import hashlib

from django.conf import settings

# Import urlopen in Python2 and 3
try:
	from urllib.request import urlopen, HTTPError
except ImportError:
	from urllib2 import urlopen, HTTPError
import json


class FlickrReader(object):

	URL = 'https://api.flickr.com/services/rest/'


	def __init__(self):
		credentials = self._get_credentials()
		self.access_token = credentials["access_token"]
		self.user_id = credentials["user_id"]
		self.album_id = credentials["album_id"]
		self.api = None

	def connect(self):
		self.api = None

	def get_last_media(self, num_images=5):
		photos = self.get_album_photos(num_images)

		for photo in photos:
			photo['size'] = self.get_size_photo(photo['id'])
			photo['info'] = self.get_info_photo(photo['id'])

		return photos

	# Return the credentials of the Flickr account
	def _get_credentials(self):
		flickr_credentials = settings.LAST_SOCIAL_ACTIVITY_CREDENTIALS.get("flickr")
		if not flickr_credentials:
			raise AssertionError(u"Credentials not found for 500px")

		if type(flickr_credentials) is dict:
			return flickr_credentials

		raise AssertionError(u"No other credential source is implemented at the moment")

	#return photos in album
	def get_album_photos(self, num_images):
		url = FlickrReader.URL
		url = url + "?method=flickr.photosets.getPhotos"
		url = url + "&api_key=" + self.access_token
		url = url + "&photoset_id=" + self.album_id
		url = url + "&user_id=" + self.user_id
		url = url + "&format=json&nojsoncallback=1"

		response = urlopen(url)
		data = json.load(response)
		stat = data.get('stat', None)
		if stat != 'ok':
			return []

		photoset = data.get('photoset', None)
		photos = photoset.get('photo', None)
		photos = photos[:num_images]

		return photos

	# return sizes in photo
	def get_size_photo(self, id):
		url = FlickrReader.URL
		url = url + "?method=flickr.photos.getSizes"
		url = url + "&api_key=" + self.access_token
		url = url + "&photo_id=" + id
		url = url + "&format=json&nojsoncallback=1"

		response = urlopen(url)
		data = json.load(response)
		stat = data.get('stat', None)
		if stat != 'ok':
			return []

		sizes = data.get('sizes', None)
		size = sizes.get('size', None)
		photos_sizes = {}
		for photo_size in size:
			photos_sizes.update({photo_size['label']: photo_size})

		return photos_sizes

	# return sizes in photo
	def get_info_photo(self, id):
		url = FlickrReader.URL
		url = url + "?method=flickr.photos.getInfo"
		url = url + "&api_key=" + self.access_token
		url = url + "&photo_id=" + id
		url = url + "&format=json&nojsoncallback=1"

		response = urlopen(url)
		data = json.load(response)
		stat = data.get('stat', None)
		if stat != 'ok':
			return []

		info = data.get('photo', None)
		info['title']['content'] = info['title']['_content']
		info['description']['content'] = info['description']['_content']
		for url in info['urls']['url']:
			url['content'] = url['_content']

		return info

