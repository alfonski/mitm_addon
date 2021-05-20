class AddOnConfig:
    def __init__(
            self,
            name: str = "some request",
            modify_response: bool = False,
            simulate_error: bool = False,
            throttle_response: bool = False,
            throttle_time: bool = 5,
            change_request_attribute: bool = False,
            change_response_attribute: bool = False
    ) -> None:
        self.name = name
        self.modify_response = modify_response
        self.simulate_error = simulate_error
        self.throttle_response = throttle_response
        self.throttle_time = throttle_time
        self.change_request_attribute = change_request_attribute
        self.change_response_attribute = change_response_attribute
