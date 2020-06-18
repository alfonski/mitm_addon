import mitmproxy

from base.base_simple_gql_request import BaseRequest


class ChatOrderProgress(BaseRequest):

    def __init__(self):
        super().__init__()

    @property
    def error_response_file(self) -> str:
        return "./response/chat_attachment_error.json"

    @property
    def modified_response_file(self) -> str:
        return "./response/order_progress_state_new_order.json"

    @property
    def query_matcher(self) -> str:
        return "query chatOrderProgress"

    @property
    def simulate_error(self) -> bool:
        return False

    @property
    def modify_response(self) -> bool:
        return True

addons = [
    ChatOrderProgress()
]