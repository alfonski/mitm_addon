import sys
import time
import warnings
from abc import abstractmethod

import mitmproxy
from mitmproxy import http

"""Deprecated"""
class BaseRequest:

    def __init__(self):
        warnings.warn("This base class is deprecated, please use the new base addon class: BaseAddon")

    @property
    @abstractmethod
    def error_response_file(self) -> str:
        pass

    @property
    @abstractmethod
    def modified_response_file(self) -> str:
        pass

    @property
    @abstractmethod
    def query_matcher(self) -> str:
        pass

    @property
    def throttle_time(self) -> int:
        return 5

    @property
    def simulate_error(self) -> bool:
        return False

    @property
    def throttling_response(self) -> bool:
        return False

    @property
    def modify_response(self) -> bool:
        return False

    """
    Response immediately without hitting server
    """

    @property
    def modify_response_immediately(self) -> bool:
        return False

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if self.modify_response_immediately and not self.simulate_error:
            self.change_response_immediately(flow)

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if self.simulate_error:
            self.simulate_error_response(flow)
        if self.modify_response and not self.simulate_error:
            self.change_response(flow)
        if self.throttling_response:
            self.start_throttling_response(flow)

    def change_response_immediately(self, flow: mitmproxy.http.HTTPFlow):
        if self.is_request_match(flow):
            modified_response = open(self.error_response_file, "r").read()
            flow.response = http.HTTPResponse.make(
                200,  # (optional) status code
                modified_response,  # (optional) content
                {
                    "access-control-allow-origin": "https://www.tokopedia.com",
                    "access-control-allow-credentials": "true",
                    "content-type": "application/json",
                    "access-control-allow-headers": "Content-type, Fingerprint-Data, Fingerprint-Hash, x-user-id, Webview-App-Version, Redirect, Access-Control-Allow-Origin, Content-MD5, Tkpd-UserId, X-Tkpd-UserId, Tkpd-SessionId, X-Device, X-Source, X-Method, X-Date, Authorization, Accounts-Authorization, flight-thirdparty, x-origin, Cshld-SessionID, X-Mitra-Device, x-tkpd-akamai, x-tkpd-lite-service, x-ga-id, Akamai-Bot, x-tkpd-app-name, x-tkpd-clc, x-return-hmac-md5"
                }
            )

    def simulate_error_response(self, flow):
        if self.is_request_match(flow):
            modified_response = open(self.error_response_file, "r").read()
            flow.response.text = modified_response
            print(self.query_matcher + ": simulate error")

    def change_response(self, flow):
        if self.is_request_match(flow):
            modified_response = open(self.modified_response_file, "r").read()
            flow.response.text = modified_response
            print(self.query_matcher + ": response modified")

    def start_throttling_response(self, flow: mitmproxy.http.HTTPFlow):
        if self.is_request_match(flow):
            print(
                "Throttling response of " +
                self.query_matcher +
                " for " +
                str(self.throttle_time) +
                "s"
            )
            animation = "|/-\\"
            for i in range(self.throttle_time):
                time.sleep(1)
                sys.stdout.write(
                    "\r" +
                    animation[i % len(animation)] +
                    " " +
                    "elapsed time: " +
                    str(i + 1)
                )
                sys.stdout.flush()
            print("")
            print("Continuing " + self.query_matcher + " response...")

    def is_request_match(self, flow: mitmproxy.http.HTTPFlow):
        query = flow.request.get_text()
        return self.query_matcher in query
