import webapp2
import jinja2
import os
import json
import logging
from urllib import quote, urlencode

from google.appengine.api import urlfetch

import headers

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class USRecapPromoHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('components/recaps-promo.v2.html')
		
		template_values = {}

		headers.cors(self.response)

		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/components/us/tv/recaps-promo', USRecapPromoHandler)],
                              debug=True)