class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id: int) -> None:
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):
    entity_name: str = "User"


class EventNotFoundError(NotFoundError):
    entity_name: str = "Event"

class DuplicatedError(Exception):
    ...

class InvalidUsernameOrPasswordError(Exception):
    ...