from abc import ABC, abstractmethod


class DomainModel(ABC):
    def __init__(self):
        self.__validation_errors = []

    def add_validation_error(self, error: str):
        if error:
            self.__validation_errors.append(error)

    def get_validation_errors(self):
        return self.__validation_errors

    def clear_validation_errors(self):
        self.__validation_errors = []

    @abstractmethod
    def e_valida(self) -> bool:
        pass
