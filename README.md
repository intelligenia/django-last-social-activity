# django-last-social-activity

A simple application for Django to fetch the last posts of your social network profiles in your site.

# Introduction

This package allows you to fetch your last status from your favorite social networks without having to
reimplment any functionality or integrating them on the browser side.

# Installation

When uploaded to pypi you would be able to install it easily:

```sh
pip install django-last-social-activity
```

or install it from this repository:

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
The first step is configure what social networks you want to include in your site.

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
		"url": "<main URL of the site>",
		"rss_url": "<RSS URL>",
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

# Authors
- Francisco Morales Gea (REMOVETHISfrancisco.REMOVETHISmorales@intelligenia.com )
- Diego J. Romero López (diegoREMOVETHIS@intelligenia.com)

Remove REMOVETHIS before emailing to one of the authors.

