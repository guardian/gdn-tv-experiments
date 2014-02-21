import webapp2
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from collections import namedtuple

from google.appengine.api import urlfetch

import headers
import content_api

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class USRecapPromoHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('components/recaps-promo.v2.html')
		
		template_values = {}

		headers.cors(self.response)

		self.response.out.write(template.render(template_values))

class USRecapRhsHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('components/recaps-promo-rhs.html')
		
		template_values = {}

		headers.cors(self.response)

		self.response.out.write(template.render(template_values))

Show = namedtuple('Show', ['name', 'url', 'recaps'])

class USRecapRhsV2Handler(webapp2.RequestHandler):
	def get(self):


		headers.cors(self.response)

		template = jinja_environment.get_template('components/recaps-promo-rhs.v2.html')
		
		template_values = {'shows' : []}

		basic_query = {
			'show-fields' : 'headline,byline,trailText,thumbnail',
		}

		for tag, name in [ ('tv-and-radio/series/lena-dunham-s-girls-episode-by-episode', 'Girls'),
			('tv-and-radio/series/house-of-cards-episode-recaps', 'House of Cards'),
			('tv-and-radio/series/looking-episode-by-episode', 'Looking'),
			('tv-and-radio/series/game-of-thrones-episode-by-episode', 'Game of Thrones'),]:
			query = {'tag' : tag}
			query.update(basic_query)

			response = content_api.search(query)

			if response:
				data = json.loads(response)
				recaps = [r for r in data.get('response', {}).get('results', [])][:2]
				if recaps:
					show_url = "http://www.theguardian.com/%s" % tag
					template_values['shows'].append(Show(name, show_url, recaps))

		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
	('/components/us/tv/recaps-promo', USRecapPromoHandler),
	('/components/us/tv/recaps-promo-rhs', USRecapRhsHandler),
	('/components/us/tv/recaps-promo-rhs/v2', USRecapRhsV2Handler),],
                              debug=True)