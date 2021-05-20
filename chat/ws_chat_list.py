import asyncio
import json
import sys

from mitmproxy.http import HTTPFlow, HTTPRequest
from mitmproxy.net.http import Request, Response
from mitmproxy.websocket import WebSocketFlow

from base.addon_config import AddOnConfig
from base.base_addon import BaseAddOn
from base.request_meta_data import RequestMetaData
from base.response_meta_data import ResponseMetaData


class WSChatList(BaseAddOn):
    EVENT_TOPCHAT_TYPING = 203
    EVENT_TOPCHAT_END_TYPING = 204
    EVENT_TOPCHAT_REPLY_MESSAGE = 103

    scenarios_file = "./chat/responsews/scenarios/try_sugi_all_scene.json"

    def __init__(self):
        super().__init__()
        self.ws_flow_id = ""
        self.is_ws_endpoint_match = False
        self.inject_message = True

    def create_add_on_config(self) -> AddOnConfig:
        return AddOnConfig(
            name="Chat list websocket"
        )

    def request_matcher(
            self, req_meta_data: RequestMetaData, request: HTTPRequest
    ) -> bool:
        return True

    def websocket_handshake(self, flow: HTTPFlow):
        self.is_ws_endpoint_match = self.is_request_match(flow)
        if self.is_ws_endpoint_match:
            self.logStr("Websocket handshake on " + self.config.name)

    def websocket_start(self, flow: WebSocketFlow):
        self.update_config(flow)
        if self.is_chat_list_ws(flow):
            self.logStr("Websocket start on " + self.config.name)
            if self.inject_message:
                self.inject_chat_list_message(flow)

    def websocket_message(self, flow: WebSocketFlow):
        self.log_websocket_message_response(flow)

    def websocket_error(self, flow: WebSocketFlow):
        if self.is_chat_list_ws(flow):
            self.logStr("Websocket error on " + self.config.name + ". Reason: " + flow.error.msg)

    def websocket_end(self, flow: WebSocketFlow):
        if self.is_chat_list_ws(flow):
            self.logStr("Websocket end on " + self.config.name + ". Reason: " + str(flow.close_code))

    """
    |
    |
    |
        Private function below
    |
    |
    |
    """

    def log_websocket_message_response(self, flow):
        last_content = flow.messages[-1].content
        is_response = not flow.messages[-1].from_client
        last_content_obj = json.loads(last_content)
        if self.is_chat_list_ws(flow) and last_content_obj["code"] == self.EVENT_TOPCHAT_REPLY_MESSAGE:
            self.logStr("Websocket new message for " + self.config.name)
            print(is_response)
            print(json.dumps(last_content_obj, indent=2))

    def update_config(self, flow: WebSocketFlow):
        if self.is_ws_endpoint_match:
            self.ws_flow_id = flow.id
            self.is_ws_endpoint_match = False

    def is_chat_list_ws(self, flow: WebSocketFlow) -> bool:
        return self.ws_flow_id == flow.id

    def inject_chat_list_message(self, flow):
        asyncio.get_event_loop().create_task(self.inject(flow))

    async def inject(self, flow: WebSocketFlow):
        scenarios = [json.loads(open(self.scenarios_file, "r").read())][0]
        interval = 1
        i = 0
        self.logStr("Prepare for " + str(len(scenarios)) + " message/s injection on " + self.config.name)
        await asyncio.gather(self.loading(5, "Delaying injection for 5s"))
        while not flow.ended and not flow.error and i < len(scenarios):
            self.logStr("Injecting message on " + self.config.name + " in " + str(interval) + "s")
            await asyncio.gather(self.loading(interval, "Injecting message in"))
            self.logStr("Injecting message on " + self.config.name)
            flow.inject_message(flow.client_conn, str(scenarios[i]))
            i += 1
        self.logStr("Finish Injecting " + str(len(scenarios)) + " message/s on " + self.config.name)

    async def loading(self, interval: int, message: str):
        animation = "|/-\\"
        for i in range(interval):
            await asyncio.sleep(1)
            sys.stdout.write(
                "\r" +
                animation[i % len(animation)] + " " + message + ": " + str(i + 1)
            )
            sys.stdout.flush()
        print("")

    """
    |
    |
    |
        Ignore function below
    |
    |
    |
    """

    @property
    def modified_response_file(self) -> str:
        return ""

    @property
    def error_response_file(self) -> str:
        return "./chat/response/chat_bundle_sticker_error.json"

    def request_attribute_changer(self, request_meta_data: RequestMetaData, request: Request):
        super().request_attribute_changer(request_meta_data, request)

    def response_attribute_changer(self, response_meta_data: ResponseMetaData, response: Response):
        super().response_attribute_changer(response_meta_data, response)


addons = [
    WSChatList()
]
