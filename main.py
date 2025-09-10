import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


def main():
    load_dotenv()

    try:
        args = get_args()
    except SystemExit as e:
        # Check if the exit code is 2 (the argparse default for command-line errors).
        if e.code == 2:
            print("Error: The 'prompt' argument is required.", file=sys.stderr)
            sys.exit(1) # Exit with code 1 instead.
        else:
            sys.exit(e.code)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = args.prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    print("Please wait...")
    generate_content(client, messages, args.verbose)


def get_args():
    parser = argparse.ArgumentParser(
        description="Generate content using GEMINI",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="The prompt for AI. \n"
        "Example: 'Why are episodes 7-9 so much worse than 1-6?'"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Display verbose output, including the user prompt and token count."
    )
    return parser.parse_args()


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        # No function was called, so it should be a text response
        print(response.text)

if __name__ == "__main__":
    main()
