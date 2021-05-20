import json

import mitmproxy
from mitmproxy import http


class ResponseMetaData:
    def __init__(
            self,
            flow: mitmproxy.http.HTTPFlow
    ) -> None:
        self.headers = flow.response.headers
        self.body = {}
        self.body_data = {}
        try:
            self.body = json.loads(flow.response.get_text())
            self.body_data = self.body[0]["data"]
        except:
            pass
