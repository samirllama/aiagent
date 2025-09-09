import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types



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
    generate_content(client, user_prompt, args.verbose)


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


def generate_content(client, messages, verbose=False):
    try:
        if verbose:
            print(f"User prompt:{messages}")

        print("Generating response, please wait...")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages
        )

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.text:
            print("Error: The model did not return any text. Please try again.", file=sys.stderr)
            sys.exit(1)

        print("\n--- Response ---")
        print(response.text)

    except genai.APIError as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
