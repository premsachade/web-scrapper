from app.notification.base import Notification


class ConsoleNotification(Notification):
    def __init__(self, recipients: list[str]) -> None:
        self.__recipients = recipients

    def send_message(self, message: str) -> None:
        for recipient in self.__recipients:
            print(f"{recipient} - {message}")
