from google import genai
import time


class ChatBot:
    # A chatbot class that uses Google Gemini API to interact with a chat model.

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-lite"):
        """
        Initializes the ChatBot with the provided API key and model name.

        Args:
            api_key (str): The API key for Google Gemini API.
            model_name (str): The name of the model to use. Default is "gemini-2.0-flash-lite".
        """

        # Set the model name and API key
        self.model = model_name
        self.api_key = api_key

        # Set up the client and chat session
        self.client = self._setup_client()
        self.chat = self._init_chat()

    def _setup_client(self) -> genai.Client:
        """
        Initializes the Google Gemini client with the provided API key.

        Returns:
            genai.Client: A client instance for interacting with the Google Gemini API.
        """

        return genai.Client(api_key=self.api_key)

    def _init_chat(self) -> genai.chats.Chat:
        """
        Initializes a chat session with the Google Gemini model.

        Returns:
            genai.chats.Chat: A chat session instance for interacting with the model.
        """

        config = genai.types.GenerateContentConfig(
            systemInstruction="You are a useful assistant. Answer the questions. Be brief in your responses."
        )

        chat = self.client.chats.create(model=self.model, config=config)

        return chat

    def get_chat_history(self) -> list:
        """
        Retrieves the chat history from the current chat session.

        Returns:
            list: A list of messages in the chat history.
        """

        return self.chat.get_history()

    def _call_model(self, input_message: str) -> str:
        """
        Sends a message to the model and retrieves the response.

        Args:
            input_message (str): The message to send to the model.

        Returns:
            str: The response text from the model.
        """

        response = self.chat.send_message(input_message)

        return response.text

    def get_response(self, input_message: str, retries: int = 4) -> str:
        """
        Sends a message to the model and retrieves the response, with retries in case of server overload.

        Args:
            input_message (str): The message to send to the model.
            retries (int, optional): The number of retries in case of server overload. Defaults to 4.

        Raises:
            RuntimeError: If the model is overloaded and the request fails after the specified number of retries.

        Returns:
            str: The response text from the model.
        """

        for attempt in range(retries):

            try:
                # Attempt to call the model
                response = self._call_model(input_message=input_message)
                return response

            except genai.errors.ServerError as e:
                # If the model is overloaded, wait and retry
                time.sleep(2 * (attempt + 1))

        # If all retries fail, raise an error
        raise RuntimeError(f"Failed after {retries} retries due to model overload.")
