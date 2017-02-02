# -.- coding: utf-8 -.-
from __future__ import unicode_literals

from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
import json


# Create your models here.
class SocialNetworkItemCache(models.Model):
	TYPES = (
		("twitter", "Twitter"),
		("facebook", "Facebook"),
		("instagram", "Instagram"),
		("pinterest", "Pinterest"),
		("rss", "RSS")
	)
	num_items = models.PositiveIntegerField(verbose_name=u"Number of stored items")
	response = models.TextField(verbose_name=u"Raw response of the API call")
	creation_datetime = models.DateTimeField(verbose_name=u"When this cache was created")
	type = models.CharField(choices=TYPES, verbose_name=u"Type", max_length=16)
	rss_url = models.URLField(verbose_name=u"RSS URL", null=True, blank=True, default=None)

	# Check if there is a cache entry and is not expired
	@staticmethod
	def hit(social_network_type, num_items, rss_url=None):
		return SocialNetworkItemCache.exists(social_network_type, num_items, rss_url) and\
				not SocialNetworkItemCache.is_expired(social_network_type, num_items, rss_url)

	# Check if there is a cache entry for this social network and number of items
	@staticmethod
	def exists(social_network_type, num_items, rss_url=None):
		cache_filter = {
			"type": social_network_type,
			"num_items": num_items,
		}

		if social_network_type == "rss":
			cache_filter["rss_url"] = rss_url

		return SocialNetworkItemCache.objects.filter(**cache_filter).exists()

	# Check if the cache entry for a social network is expired
	@staticmethod
	def is_expired(social_network_type, num_items, rss_url=None):
		cache_max_life = SocialNetworkItemCache._cache_max_life()

		cache_filter = {
			"type": social_network_type,
			"num_items": num_items,
			"creation_datetime__lte": cache_max_life
		}

		if social_network_type == "rss":
			cache_filter["rss_url"] = rss_url

		return SocialNetworkItemCache.objects.filter(**cache_filter).exists()

	# Get the active cache entry
	@staticmethod
	def get(social_network_type, num_items, rss_url=None):

		get_cache_filter = {
			"type": social_network_type,
			"num_items": num_items,
		}

		if social_network_type == "rss":
			get_cache_filter["rss_url"] = rss_url

		return SocialNetworkItemCache.objects.get(**get_cache_filter)


	# Create a new cache entry
	@staticmethod
	def create(social_network_type, num_items, response, rss_url=None):
		# Expire the old cache
		SocialNetworkItemCache.expire(social_network_type, num_items, rss_url)

		# Serialize response if needed
		if type(response) is dict or type(response) is list or type(response) is object:
			response = json.dumps(response)

		# Creation of cache
		cache = SocialNetworkItemCache(
			type=social_network_type,
			num_items=num_items,
			response=response,
			creation_datetime=timezone.now()
		)
		if social_network_type == "rss" and rss_url:
			cache.rss_url = rss_url
		cache.save()

		# Always return the new cache entry
		return cache

	# Delete the old cache entries for this social network and for this number of items
	@staticmethod
	def expire(social_network_type, num_items, rss_url=None):
		cache_max_life = SocialNetworkItemCache._cache_max_life()
		cache_filter = {
			"type": social_network_type,
			"num_items": num_items
		}
		if social_network_type == "rss" and rss_url:
			cache_filter["rss_url"] = rss_url

		SocialNetworkItemCache.objects.filter(**cache_filter).delete()

	# Deserialize the response
	@property
	def response_dict(self):
		return json.loads(self.response)

	# Compute the max duration of the cache elements
	@staticmethod
	def _cache_max_life():
		now = timezone.now()
		if hasattr(settings, "LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_HOURS") and settings.LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_HOURS:
			return now - timedelta(hours=settings.LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_HOURS)

		if hasattr(settings, "LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_MINUTES") and settings.LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_MINUTES:
			return now - timedelta(minutes=settings.LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_MINUTES)

		if hasattr(settings, "LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_SECONDS") and settings.LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_SECONDS:
			return now - timedelta(seconds=settings.LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_SECONDS)

		raise AssertionError(u"LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_HOURS or LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_MINUTES or LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_SECONDS must exist")