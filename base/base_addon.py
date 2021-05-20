import json
import sys
import time
from abc import abstractmethod

import mitmproxy
from mitmproxy import http
from mitmproxy.net.http import Request
from mitmproxy.net.http import Response

from addon_config import AddOnConfig
from request_meta_data import RequestMetaData
from response_meta_data import ResponseMetaData

"""
    TODO: 
    - able to modify response body specific attribute
"""


class BaseAddOn:

    def __init__(self):
        self.config: AddOnConfig = self.create_add_on_config()

    def create_add_on_config(self) -> AddOnConfig:
        return AddOnConfig(
            name=self.__class__.__name__
        )

    @abstractmethod
    def request_matcher(self, req_meta_data: RequestMetaData, request: mitmproxy.http.HTTPRequest) -> bool:
        """
        implement your own matcher here. To get request body from gql request use request.get_text()
        """
        pass

    @property
    @abstractmethod
    def error_response_file(self) -> str:
        """
        Provide the error response json file path
        """
        pass

    @property
    @abstractmethod
    def modified_response_file(self) -> str:
        """
        Provide the success response json file path
        """
        pass

    def request_attribute_changer(self, request_meta_data: RequestMetaData, request: Request):
        request.text = json.dumps(request_meta_data.body)

    def response_attribute_changer(self, response_meta_data: ResponseMetaData, response: Response):
        response.text = json.dumps(response_meta_data.body)

    """Don't override this"""

    def request(self, flow: mitmproxy.http.HTTPFlow):
        if self.config.change_request_attribute and self.is_request_match(flow):
            self.change_request_attribute(flow)

    """Don't override this"""

    def change_request_attribute(self, flow: mitmproxy.http.HTTPFlow):
        self.logStr("Changing request attributes of: " + self.config.name)
        self.request_attribute_changer(RequestMetaData(flow), flow.request)

    """Don't override this"""

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if not self.is_request_match(flow):
            return
        if self.config.throttle_response:
            self.start_throttling_response()
        if self.config.simulate_error:
            self.simulate_error_response(flow)
        elif self.config.modify_response:
            self.change_response(flow)
        if self.config.change_response_attribute:
            self.change_response_attribute(flow)

    """Don't override this"""

    def change_response_attribute(self, flow: mitmproxy.http.HTTPFlow):
        self.logStr("Changing response attributes of: " + self.config.name)
        self.response_attribute_changer(ResponseMetaData(flow), flow.response)

    """Don't override this"""

    def simulate_error_response(self, flow):
        modified_response = open(self.error_response_file, "r").read()
        flow.response.text = modified_response
        self.logStr(self.config.name + ": simulate error")

    """Don't override this"""

    def change_response(self, flow):
        modified_response = open(self.modified_response_file, "r").read()
        flow.response.text = modified_response
        self.logStr(self.config.name + ": response modified")

    """Don't override this"""

    def start_throttling_response(self):
        print("\n\n\n\n\n")
        print(
            "Throttling response of " +
            self.config.name +
            " for " +
            str(self.config.throttle_time) +
            "s"
        )
        animation = "|/-\\"
        for i in range(self.config.throttle_time):
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
        print("Continuing " + self.config.name + " response...")
        print("\n\n\n\n\n")

    """Don't override this"""

    def is_request_match(self, flow: mitmproxy.http.HTTPFlow) -> bool:
        return self.request_matcher(RequestMetaData(flow), flow.request)

    def logStr(self, message):
        print("----------> " + message + " <----------")
