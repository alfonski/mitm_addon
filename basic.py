from mitmproxy import ctx
import mitmproxy
import json


class BasicAddOn:

    def __init__(self):
        pass

    def request(self, flow):
        ctx.log.info("testing this request: %s" % flow.request.host)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        ctx.log.info("testing this response: %s" % flow.response.status_code)


addons = [
    BasicAddOn()
]

