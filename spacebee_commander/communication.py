import abc


class Communication(abc.ABC):

    @abc.abstractmethod
    def send(self, message: bytes): ...

    @abc.abstractmethod
    def receive(self) -> bytes: ...
