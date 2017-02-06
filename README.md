# django-last-social-activity

A simple application for [Django](https://www.djangoproject.com/) to fetch the last posts of your social network profiles in your site.

# Introduction

This package allows you to fetch your last status from your favorite social networks without having to
reimplement any functionality or integrating them on the browser side.

The development repository is [https://github.com/intelligenia/django-last-social-activity](https://github.com/intelligenia/django-last-social-activity).

The main aim of this software is having [Django template tags](https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/) ready to load your last posts in templates:

```html
{# Load django-last-social-activity template tags #}
{% load last_social_activity %}

<div class="my-social-networks">
  {# Get the last 10 items of your RSS 'myblog' as defined in settings.py #}
  {% last_rss_items 'myblog' 10 %}

  {# Get the last 3 posts of your Facebook wall #}
  {% last_facebook_posts 3 %}

  {# Get the last 8 tweets #}
  {% last_tweeets 8 %}

  {# Get the last 12 images of Instagram #}
  {% last_instagram_media 12 %}

  {# Get the last 15 pins of Pinterest #}
  {% last_pinterest_pins 15 %}
</div>

```

The idea is personalize the default templates in your **templates** folder as you need.

# Installation

[This package is in pypi](https://pypi.python.org/pypi/django-last-social-activity) so you can install it easily using pip command:

```sh
pip install django-last-social-activity
```

or install it from [this GitHub repository](https://github.com/intelligenia/django-last-social-activity) if you want last features of the master branch:

```sh
# Master will allways be stable
pip install https://github.com//intelligenia/django-last-social-activity/archive/master.zip

```

# Dependencies

This package depends on some other Python packages:

- beautifulsoup4
- python-dateutil
- python-twitter
- requests

They are included in the requirements of this package so you won't have to install them by hand.

# Configuration

## Django settings.py
The first step is include the application **last_social_activity** to your INSTALLED_APPS tuple:

```python
INSTALLED_APPS = (
  #...
  "last_social_activity"
  #...
)

```

The second step is configuring what social networks you want to include in your site.

Put this dictionary in your **settings.py** file filling the.

```python
LAST_SOCIAL_ACTIVITY_CREDENTIALS = {
	"twitter": {
		"profile_url": "<your twitter profile>",
		"username": "<your twitter username>",
		"consumer_key": "<consumer key>",
		"consumer_secret": "<consumer secret>",
		"access_token_key": "<access token key>",
		"access_token_secret": "<access token secret>"
	},
	"instagram": {
		"profile": "<instagram username>",
		"access_token" :"<instagram access token>"
	},
	"pinterest": {
		"profile": "<pinterest username>",
		"access_token" :"<pinterest access token>"
	},
	"facebook": {
		"profile": "<facebook username>",
		"access_token" :"<facebook access token>"
	},
	"rss": {
		"<RSS source id>"{
			"url": "<main URL of the site>",
			"rss_url": "<RSS URL>",
		}
	}
}
```

If you don't want to fetch some social network (or don't have an account), you can
leave empty the dictionary for that social network.

Thus, you have to include the cache configuration:

```python
# Cache stores information for 1 hour
LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_HOURS = 1
LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_MINUTES = None
LAST_SOCIAL_ACTIVITY_CACHE_DURATION_IN_SECONDS = None
```

By default, it caches the last posts/items in your profile in each social network for 1 hour
if you want to change that, set None the fields you don't want and set a number for the field
you want.

Note the amount of duration is not additive so you only can define max lifetime for full hours, minutes and seconds.


## Migrations
Don't forget to execute migrations to create cache table for this application.

```sh
python manage.py migrate
```

# Use

## Template tags

Load this template tag in your templates:

```html
{% load last_social_activity %}
```

For example:

```html

{# Get the last 10 items of your RSS 'mysite' channel as defined in settings.py #}
{% last_rss_items 'mysite' 10 %}

{# Get the last 3 posts of your Facebook wall #}
{% last_facebook_posts 3 %}

{# Get the last 8 tweets #}
{% last_tweeets 8 %}

{# Get the last 12 images of Instagram #}
{% last_instagram_media 12 %}

{# Get the last 15 pins of Pinterest #}
{% last_pinterest_pins 15 %}

```

## Customization

Customize each one of the templates creating a directory **last_social_activity** with one child with the name
**social_networks**. That directory will contain a template for each social network (and your RSS channel if is configured):

- facebook.html
- instagram.html
- pinterest.html
- rss.html
- twitter.html


### Facebook

You have a list of post objects called **posts** with the following attributes:

- id: id of this post
- name: title of the post.
- created_time: creation datetime of the post.
- type: type of the post.
- message: content of the post.
- link: link to this facebook post.
- permalink_url: link to this facebook post.

Take a look to the [default template](last_social_activity/templates/last_social_activity/social_networks/facebook.html) for an example.

### Instagram

Data available comes from the member **data** of the following URL: [https://api.instagram.com/v1/users/self/media/recent/?access_token=XXXX](https://www.instagram.com/developer/endpoints/users/#get_users_media_recent_self)

Look to the [default template](last_social_activity/templates/last_social_activity/social_networks/instagram.html).

### Pinterest

Available fields are the ones returned by [https://api.pinterest.com/v1/me/pins/?access_token=XXXX](https://developers.pinterest.com/docs/api/pins/).

Look to the [default template](last_social_activity/templates/last_social_activity/social_networks/pinterest.html).

### RSS

All RSS data is available as context in the template in the **rss_items** list.

You can access to all the attributes of each of your RSS items: name, description, pubdate, etc.

Look to the [default template](last_social_activity/templates/last_social_activity/social_networks/rss.html).

### Twitter

Available context is a dict with the following structure:

```python
{
	"tweets": [
		{
			"id": "<id of this tweet>",
			"text": "<content of the tweet>",
			"created_at": "<creation datetime of this tweet>"
		},
		# ...
	],
	"profile_url": "<twitter_profile_url>",
	"username": "<twitter_username>"
}


```

Look to the [default template](last_social_activity/templates/last_social_activity/social_networks/twitter.html).

# Authors
- Francisco Morales Gea (REMOVETHISfrancisco.REMOVETHISmorales@intelligenia.com) (development)
- Diego J. Romero López (diegoREMOVETHIS@intelligenia.com) (corresponding author, software architecture, caching and fault-tolerance)

Remove REMOVETHIS before emailing to one of the authors.

