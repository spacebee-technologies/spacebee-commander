import abc


class Communication(abc.ABC):

    @abc.abstractmethod
    def send(self, message): ...

    @abc.abstractmethod
    def receive(self): ...
