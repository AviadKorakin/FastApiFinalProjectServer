from abc import ABC, abstractmethod


class EmailService(ABC):

    @abstractmethod
    def send_verification_email(self, recipient_email: str, verification_url: str):
        pass