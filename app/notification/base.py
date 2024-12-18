from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    async def send_message(self, message):
        pass
