import json
# from tkinter import *
import sys
import time

import mitmproxy.http
import mitmproxy.websocket


class ChatRoomWs:

    def __init__(self):
        self.log_json = False

    # Websocket lifecycle
    def websocket_handshake(self, flow: mitmproxy.http.HTTPFlow):
        # print(flow.request)
        """
            Called when a client wants to establish a WebSocket connection. The
            WebSocket-specific headers can be manipulated to alter the
            handshake. The flow object is guaranteed to have a non-None request
            attribute.
        """

    def websocket_start(self, flow: mitmproxy.websocket.WebSocketFlow):
        # print("websocket start")
        # window = Tk()
        # a = Label(window, text="Hello World")
        # a.pack()
        #
        # window.mainloop()
        """
            A websocket connection has commenced.
        """

    def websocket_message(self, flow: mitmproxy.websocket.WebSocketFlow):
        messages = flow.messages[-1]
        last_content = flow.messages[-1].content
        last_content_obj = json.loads(last_content)
        is_response = not flow.messages[-1].from_client
        self.handle_sticker(last_content, last_content_obj, is_response, flow)
        if self.log_json:
            print(is_response)
            print(json.dumps(last_content_obj, indent=2))

        if not messages.from_client and not "attachment" in last_content:
            pass
        # print(json.dumps(last_content_obj, indent=2))
        # self.start_throttling_response()
        # print("------------------->" + "from server")
        """
            Called when a WebSocket message is received from the client or
            server. The most recent message will be flow.messages[-1]. The
            message is user-modifiable. Currently there are two types of
            messages, corresponding to the BINARY and TEXT frame types.
        """

    def start_throttling_response(self):
        print("\n\n\n\n\n")
        print(
            "Throttling response of " +
            "Ws response" +
            " for " +
            "3" +
            "s"
        )
        animation = "|/-\\"
        for i in range(3):
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
        print("Continuing " + "ws" + " response...")
        print("\n\n\n\n\n")

    def websocket_error(self, flow: mitmproxy.websocket.WebSocketFlow):
        # print(flow.request)
        """
            A websocket connection has had an error.
        """

    def websocket_end(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            A websocket connection has ended.
        """

    def handle_sticker(
            self,
            content,
            content_obj,
            is_response,
            flow: mitmproxy.websocket.WebSocketFlow):
        if is_response:
            enable = False
            matcher = "sticker_profile"
            if matcher in content and enable:
                # time.sleep(10)
                modified_response = open("response/chat_sticker_reply_ws.json", "r").read()
                flow.messages[-1].content = modified_response


addons = [
    ChatRoomWs()
]
