import mitmproxy
from mitmproxy import http
from mitmproxy.net.http import Request, Response

from base.addon_config import AddOnConfig
from base.base_addon import BaseAddOn
from base.request_meta_data import RequestMetaData
from base.response_meta_data import ResponseMetaData


class NotificationDetail(BaseAddOn):
    responses = [
        "./notifcenter/response/notification_detail_v3_empty.json",
        "./notifcenter/response/notifcenter_detail_v3_try_sugi.json",
        "./notifcenter/response/notification_detail_v3.json"
    ]

    def __init__(self):
        super().__init__()

    def create_add_on_config(self) -> AddOnConfig:
        return AddOnConfig(
            name="NotificationDetail query notifcenter_detail_v3",
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
        return "query notifcenter_detail_v3" in req_meta_data.body_query

    @property
    def modified_response_file(self) -> str: return self.responses[1]

    @property
    def error_response_file(self) -> str: return "./global/responses/general_error.json"

    def request_attribute_changer(self, request_meta_data: RequestMetaData, request: Request):
        # request_meta_data.body_params["new_param"] = "new_param"
        super().request_attribute_changer(request_meta_data, request)

    def response_attribute_changer(self, response_meta_data: ResponseMetaData, response: Response):
        # response_meta_data.body_data["notifcenter_detail_v3"]["empty_state_content"] = "new content"
        super().response_attribute_changer(response_meta_data, response)


addons = [
    NotificationDetail()
]
