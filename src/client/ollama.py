from abc import ABC, abstractmethod
from ollama import Client
client = Client(host='http://ollama-server:11434')

class ResponseGenerator(ABC):
    @abstractmethod
    def generate(self):
        pass

class Ollama(ResponseGenerator):
    def __init__(self, context: str = "", model: str = "llama3.1"):
        self.model = model
        self.context = context

    def generate(self, query):
        res = client.chat(model=self.model, messages=[
            {
                "role": "system",
                "content": self.context,
            },
            {
                'role': 'user',
                'content': query,
            },
        ])
        return res['message']['content']
