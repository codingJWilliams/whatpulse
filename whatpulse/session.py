from . import config
from .responses import Response
import requests
from lxml import etree
from lxml.builder import E

class Session(object):
	def __init__(self):
		self.s = requests.Session()
		self.s.headers.update({'User-Agent': 'WhatPulse Client ' + config.client_version})

	def requests(self, reqs):
		requests = E.requests()
		for req in reqs:
			requests.append(req.tree)

		tree = (
			E.client(
				requests
			)
		)

		xml = etree.tostring(tree, encoding='UTF-8', xml_declaration=True) # declaration uses ' instead of "

		r = self.s.post('https://client.whatpulse.org/v1.1/', verify='whatpulse.pem', data={'client_version': config.client_version, 'xml': xml})
		print(r.text)
		tree = etree.fromstring(r.text)
		ress = tree.xpath('/server/responses/response')

		ret = []
		for res in ress:
			ret.append(Response.parse(res))

		return ret

	def request(self, req):
		return self.requests([req])[0]

__all__ = ["Session"]
