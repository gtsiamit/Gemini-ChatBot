import time
import json
import gradio as gr
from utils import load_json
from chatbot_backend import ChatBot
from typing import Generator, Callable


def create_chatbot_instance(config: json) -> ChatBot:
    """
    Create a ChatBot instance using the provided configuration.

    Args:
        config (json): A JSON object containing the API key and model name.

    Returns:
        ChatBot: An instance of the ChatBot class initialized
    """

    chatbot_instance = ChatBot(
        api_key=config["GOOGLE_AI_STUDIO_API_KEY"], model_name=config["MODEL_NAME"]
    )

    return chatbot_instance


def handle_chat_wrapper(cb: ChatBot) -> Callable:
    """
    Create a wrapper function for the chat interface.

    Args:
        cb (ChatBot): An instance of the ChatBot class.

    Returns:
        Callable: A function that takes a message and history, and returns a generator yielding the response.
    """

    def chat_wrapper(message: str, history: list) -> Generator[str, None, None]:
        """
        Handles the chat interaction with the ChatBot instance.

        Args:
            message (str): The input message from the user.
            history (list): The chat history, which is not used in this implementation.

        Yields:
            Generator[str, None, None]: A generator that yields the response from the ChatBot instance.
        """

        # Get response from the ChatBot instance
        response = cb.get_response(input_message=message)

        # Initialize output string and yield each part of the
        # response with a delay to simulate typing effect
        output = ""
        for k in response:
            time.sleep(0.03)
            output += k

            yield output

    return chat_wrapper


def launch_ui(chat_wrapper_function: Callable) -> None:
    """
    Launch the Gradio UI for the chatbot.

    Args:
        chat_wrapper_function (Callable): A function that handles the chat interaction with the ChatBot instance.
    """

    gr.ChatInterface(
        fn=chat_wrapper_function,
        type="messages",
        textbox=gr.Textbox(
            placeholder="Ask me anything...", submit_btn=True, stop_btn=True
        ),
        title="AI Assistant for General Use",
        description="AI Assistant",
        theme="origin",
    ).launch()


def main():
    """
    Main function to initialize the chatbot and launch the UI.
    """

    # Load the configuration from the JSON file
    config = load_json("config.json")

    # Create a ChatBot instance using the configuration
    chatbot_instance = create_chatbot_instance(config)
    # Create a wrapper function for the chat interface
    chat_wrapper = handle_chat_wrapper(chatbot_instance)

    # Launch the Gradio UI with the chat wrapper function
    launch_ui(chat_wrapper_function=chat_wrapper)


if __name__ == "__main__":
    main()
