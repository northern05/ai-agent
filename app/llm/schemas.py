class LlmResponse:
    def __init__(self, text: str, decision: str) -> None:
        self.text = text
        self.decision = decision