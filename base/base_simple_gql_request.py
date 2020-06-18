from mitmproxy import ctx
import mitmproxy
import json
import time, sys
from abc import ABC, abstractmethod


class BaseRequest:

    def __init__(self):
        pass

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

    def request(self, flow):
        pass

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if self.simulate_error:
            self.simulate_error_response(flow)
        if self.modify_response and not self.simulate_error:
            self.change_response(flow)
        if self.throttling_response:
            self.start_throttling_response(flow)

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