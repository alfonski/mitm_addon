import mitmproxy
from mitmproxy import http
from mitmproxy.net.http import Request, Response

from base.addon_config import AddOnConfig
from base.base_addon import BaseAddOn
from base.request_meta_data import RequestMetaData
from base.response_meta_data import ResponseMetaData

"""
Example url: 
https://ta.tokopedia.com/v1.3/display?item=1&user_id=19016250&inventory_id=5&page_token=&ep=banner&device=android&dimen_id=4
"""


class InboxTdn(BaseAddOn):
    responses = [
        "./inbox/response/inbox_tdn.json"
    ]

    def __init__(self):
        super().__init__()

    def create_add_on_config(self) -> AddOnConfig:
        return AddOnConfig(
            name="InboxTdn",
            # modify_response=True,
            # simulate_error=True,
            # throttle_response=True,
            # throttle_time=5,
            # change_request_attribute=True,
            # change_response_attribute=True
        )

    def request_matcher(
            self, req_meta_data: RequestMetaData, request: mitmproxy.http.HTTPRequest
    ) -> bool:
        return "ta.tokopedia.com/v1.3/display" in req_meta_data.url

    @property
    def modified_response_file(self) -> str: return self.responses[0]

    @property
    def error_response_file(self) -> str: return "./response/chat_attachment_error.json"

    def request_attribute_changer(self, request_meta_data: RequestMetaData, request: Request):
        super().request_attribute_changer(request_meta_data, request)

    def response_attribute_changer(self, response_meta_data: ResponseMetaData, response: Response):
        super().response_attribute_changer(response_meta_data, response)


addons = [
    InboxTdn()
]
