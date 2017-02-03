# -.- coding: utf-8 -.-

from __future__ import unicode_literals, absolute_import

import dateutil
from django import template
from django.template import loader
from django.conf import settings

from last_social_activity.social_networks.facebook import FacebookReader
from last_social_activity.social_networks.instagram import InstagramReader
from last_social_activity.social_networks.pinterest import PinterestReader
from last_social_activity.social_networks.rss import RssReader
from last_social_activity.social_networks.twitter import TwitterReader

register = template.Library()


# Show last tweets
# Use {% last_tweets X %} where X is the number of tweets to show
@register.simple_tag
def last_tweeets(num_tweets=5, template_path="last_social_activity/social_networks/twitter.html"):
	try:
		twitter_reader = TwitterReader()
	except AssertionError as e:
		return ""
	twitter_reader.connect()
	tweets = twitter_reader.get_last_tweets(num_tweets)
	for tweet in tweets:
		tweet["created_at"] = dateutil.parser.parse(tweet["created_at"])

	# Render template with the last tweets
	tag_template = loader.get_template(template_path)
	replacements = {"tweets": tweets, "profile_url": twitter_reader.profile_url, "username": twitter_reader.username}
	return tag_template.render(replacements)


# Show last tweets
# Use {% last_instagram_media X %} where X is the number of images to show
@register.simple_tag
def last_instagram_media(num_items=5, template_path="last_social_activity/social_networks/instagram.html"):
	try:
		instagram_reader = InstagramReader()
	except AssertionError:
		return ""
	instagram_reader.connect()
	instagram_media_items = instagram_reader.get_last_media(num_items)
	# Render template the last instagram media
	tag_template = loader.get_template(template_path)
	replacements = {"instagram_media_items": instagram_media_items, "instagram_username": instagram_reader.profile}
	return tag_template.render(replacements)


# Show last tweets
# Use {% last_pinterest_pins X %} where X is the number of images to show
@register.simple_tag
def last_pinterest_pins(num_pins=5, template_path="last_social_activity/social_networks/pinterest.html"):
	try:
		pinterest_reader = PinterestReader()
	except AssertionError:
		return ""
	pinterest_reader.connect()
	pinterest_last_activity = pinterest_reader.get_last_activity(num_pins)
	pinterest_pins = pinterest_last_activity["last_pins"]
	pinterest_user = pinterest_last_activity["user"]
	# Render the last pins
	tag_template = loader.get_template(template_path)
	replacements = {"pins": pinterest_pins, "pinterest_user": pinterest_user}
	return tag_template.render(replacements)


# Show last facebook posts
# Use {% last_facebook_posts X %} where X is the number of posts to show
@register.simple_tag
def last_facebook_posts(num_posts=5, template_path="last_social_activity/social_networks/facebook.html"):
	try:
		facebook_reader = FacebookReader()
	except AssertionError:
		return ""
	facebook_reader.connect()
	facebook_posts = facebook_reader.get_last_posts(num_posts)
	for facebook_post in facebook_posts:
		facebook_post["created_at"] = dateutil.parser.parse(facebook_post["created_at"])
	# Render the last posts
	tag_template = loader.get_template(template_path)
	replacements = {"posts": facebook_posts, "profile": facebook_reader.profile}
	return tag_template.render(replacements)


# Show last rss posts
# Use {% last_rss_posts SOURCE X %} where
# SOURCE is the id of the RSS URL (especified in settings.py) and
# X is the number of posts to show
@register.simple_tag
def last_rss_items(rss_id, num_posts=5, template_path="last_social_activity/social_networks/rss.html"):
	try:
		rss_reader = RssReader(id=rss_id)
	except AssertionError as e:
		print e
		return ""

	rss_last_items = rss_reader.get_last_items(num_posts)
	for rss_item in rss_last_items["rss_items"]:
		rss_item["pubdate"] = dateutil.parser.parse(rss_item["pubdate"])

	# Render the last posts
	tag_template = loader.get_template(template_path)
	replacements = {"rss_items": rss_last_items['rss_items'], "profile_info": rss_last_items['info'], "url": rss_last_items['url']}
	return tag_template.render(replacements)
