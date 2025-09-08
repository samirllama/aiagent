import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

def get_args():
    """Parses command line arguments"""
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
    return parser

def main():
    """
    Main function to generate content using the Gemini API.
    """
    parser = get_args()
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # Check if the exit code is 2 (the argparse default for command-line errors).
        if e.code == 2:
            print("Error: The 'prompt' argument is required.", file=sys.stderr)
            sys.exit(1) # Exit with code 1 instead.
        else:
            # Handle other SystemExit cases, like --help, by exiting with the original code.
            sys.exit(e.code)

    user_prompt = args.prompt



    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except KeyError:
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    # Create client instance
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    print("Please wait...")

    generate_content(client, messages)


def generate_content(client, messages):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages
        )
        # Ensure response contains text before attempting to print.
        if response.text:
            print("\n--- Generated Content ---")
            print(response.text)
        else:
            print("Error: The model did not return any text. Please try again.", file=sys.stderr)
            sys.exit(1)

    except genai.APIError as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
