"""Parent class for all nlp models.
"""

class NLPModel:
    """The parent class of all implementation of nlp models used for news event extraction.
    """

    def __init__(self) -> None:
        """Parent class empty init function as placeholder.
        """
        pass

    def find_events(self, text: str) -> list:
        """Parent class empty find_events function as placeholder.

        Args:
            text: The input text to be extracted from.
        """
        raise NotImplementedError("Subclasses must implement the find_events method.")
