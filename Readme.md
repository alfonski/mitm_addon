MITM Addons for Tokopedia usage only

# Installation

install mitmproxy first. Then make the wrapper allow execution by typing:

```sh
chmod +x ./mitmwebw
```

# How to run

To run all scripts on the folder:

```sh
./mitmwebw
```

To run just several selected scripts, note that you can have multiple `-s {script_file_path.py}` arguments:

```sh
mitmweb --ignore-hosts '^(?![0-9\.]+:)(?!([^\.:]+\.)*tokopedia\.(com|net):)' -s main.py -s {script_file_path.py}
```

# Shortcuts

Known shortcut/s:

- `z`: Clear network list.

# Creating new Addon

This is new Addon template:

```python
import mitmproxy
from mitmproxy import http
from mitmproxy.net.http import Request, Response

from base.addon_config import AddOnConfig
from base.base_addon import BaseAddOn
from base.request_meta_data import RequestMetaData
from base.response_meta_data import ResponseMetaData

"""Give class name whatever you want"""
class NotificationDetail(BaseAddOn):

    """Provide the json relative file path"""
    responses = [
        "./response/inbox/notification_detail_v3_empty.json",
        "./notifcenter/response/notifcenter_detail_v3_try_sugi.json"
    ]

    def __init__(self):
        super().__init__()

    """Adjust the config based on your need, just comment/uncomment the config argument below"""
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

    """Provide your own logic here how to match the request"""
    def request_matcher(
            self, req_meta_data: RequestMetaData, request: mitmproxy.http.HTTPRequest
    ) -> bool:
        return "query notifcenter_detail_v3" in req_meta_data.body_query

    """The success json file relative path if request match logic is True"""
    @property
    def modified_response_file(self) -> str: return self.responses[1]

    """The error json file relative path if request match logic is True"""
    @property
    def error_response_file(self) -> str: return "./response/chat_attachment_error.json"

    """Change the request attributes (headers, req body, etc) here if request match logic is True"""
    def request_attribute_changer(self, request_meta_data: RequestMetaData, request: Request):
        # request_meta_data.body_params["new_param"] = "new_param"
        super().request_attribute_changer(request_meta_data, request)

    """Change the response attributes (headers, response body, etc) here if request match logic is True"""
    def response_attribute_changer(self, response_meta_data: ResponseMetaData, response: Response):
        # response_meta_data.body_data["notifcenter_detail_v3"]["empty_state_content"] = "new content"
        super().response_attribute_changer(response_meta_data, response)


addons = [
    NotificationDetail()
]
```

# Learn more

see the [mitmproxy docs](https://docs.mitmproxy.org/stable/) to learn more about mitmproxy.
