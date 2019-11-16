import logging


logger = logging.getLogger(__name__)

class BaseMemory:
    def __init__(self, scope_name: str, type_name: str, limits: (int, int)):
        self.__scope_name = scope_name
        self.__type_name = type_name
        self.__inf_limit, self.__max_limit = limits
        self.__variable_counter = 0

    def next_available(self) -> int:
        next_available_space = self.__inf_limit + self.__variable_counter

        # Stop compilation if program has too many variables.
        if next_available_space > self.__max_limit:
            logger.error(
                f"BaseMemory: Too many variables for {self.__scope_name} {self.__type_name} memory.")
            exit(1)

        self.__variable_counter += 1
        logger.debug(
            f"BaseMemory: Added variable to {self.__scope_name} {self.__type_name} memory in space {next_available_space}.")
        return next_available_space
