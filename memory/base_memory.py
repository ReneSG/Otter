import logging


logger = logging.getLogger(__name__)


class BaseMemory:
    def __init__(self, scope_name: str, type_name: str, limits: (int, int)):
        """The BaseMemory is the class in charge of keeping the memory spaces during compilation.
        
        Arguments:
            - scope_name [str]: The name of the scope of this instance.
            - type_name [str]: The type of variables being kept in memory.
            - limits [(int, int)]: The limits of this memory. One of TypeRanges.
        """
        self.__scope_name = scope_name
        self.__type_name = type_name
        self.__inf_limit, self.__max_limit = limits
        self.__variable_counter = 0

    @property
    def variable_counter(self):
        return self.__variable_counter

    def next_available(self) -> int:
        """Retrieves the single next available space in memory.

        Returns:
            - [int] The next available memory address.

        Raises:
            Exception: If the amount of variable surpasses the available memory limits.
        """
        next_available_space = self._get_next_available_space(1)

        logger.debug(
            f"Added variable to {self.__scope_name} {self.__type_name} memory in space {next_available_space}.")
        return next_available_space

    def next_memory_chunk(self, chunk_size: int) -> int:
        """Separates a chunk of memory for arrays in memory.

        Arguments:
            - chunk_size [int]: The amount of memory spaces which should be saved.

        Returns:
            - [int] The single next available memory space from the reserved chunk.

        Raises:
            Exception: If the amount of variable surpasses the available memory limits.
        """
        next_available_space = self._get_next_available_space(chunk_size)

        logger.debug(
            f"Added chunk of size {chunk_size + 1} to {self.__scope_name} {self.__type_name} memory from {next_available_space - 1} to {self.__inf_limit + self.__variable_counter}.")
        return next_available_space

    def _get_next_available_space(self, chunk_size: int) -> int:
        """Separates the memory space for the amount of chunk_size.

        Arguments:
            - chunk_size [int]: The amount of memory spaces which should be saved.

        Returns:
            - [int] The single next available memory space from the reserved chunk.

        Raises:
            Exception: If the amount of variable surpasses the available memory limits.
        """
        next_available_space = self.__inf_limit + self.__variable_counter
        self.__variable_counter += chunk_size

        # Stop compilation if program has too many variables.
        if self.__inf_limit + self.__variable_counter > self.__max_limit:
            raise Exception(
                f"Too many variables for {self.__scope_name} {self.__type_name} memory.")

        return next_available_space
