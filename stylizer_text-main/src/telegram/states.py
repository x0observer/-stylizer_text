

from typing import Optional


class Event:
    def __init__(self, update_id: Optional[int], chat_id: Optional[int]):
        pass


class Body:
    def __init__(self, ):
        pass


class States:
    active_state: Optional[tuple] = None
    last_event: Optional[Event] = None
    body: Optional[Body] = None
    is_sended: Optional[bool] = None


class StatesManager:
    pass
