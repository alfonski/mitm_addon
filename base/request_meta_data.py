import json

import mitmproxy
from mitmproxy import http


class RequestMetaData:
    def __init__(
            self,
            flow: mitmproxy.http.HTTPFlow
    ) -> None:
        self.headers = flow.request.headers
        self.host = flow.request.pretty_host
        self.url = flow.request.pretty_url
        self.params = flow.request.query
        self.body = {}
        self.body_params = {}
        self.body_query = ""
        try:
            self.body = json.loads(flow.request.get_text())
            self.body_params = self.body["variables"]
            self.body_query = self.body["query"]
        except:
            pass
