from google import genai

class GeminiConnector:
    def __init__(self, api_keys: list[str]):
        self.clients = [genai.Client(api_key=key) for key in api_keys]
        self.current_client_index = 0
    def generate_content(self, model:str, prompt:str, max_retries:int=3):
        for attempt in range(max_retries):
            client = self.clients[self.current_client_index]
            try:
                response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )
                return response.text
            except Exception as e:
                print(f"Error with client {self.current_client_index}: {e}")
                self.current_client_index = (self.current_client_index + 1) % len(self.clients)
        
        print("All clients failed after retries.")
        return None
