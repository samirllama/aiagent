import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    # Collect positional args as user prompt
    # args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Loop with a maximum of 20 iterations
    for i in range(20):
        try:
            response_text = generate_content(client, messages, verbose)
            if response_text:
                # Final model output received
                print(response_text)
                break
        except Exception as e:
            print(f"Error on iteration {i+1}: {e}", file=sys.stderr)
            break
    else:
        # If loop finishes without breaking
        print("Reached maximum iterations without final response.")


def generate_content(client, messages, verbose):
    """
    Generate content from Gemini, handle candidates and function calls,
    and update messages with the model's responses and function outputs.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            # print(f"Candidate: {candidate}")
            if hasattr(candidate, "content") and candidate.content:
                messages.append(candidate.content)

    # Print token usage if verbose
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # If no function calls, return immediately with text
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise ValueError("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise ValueError("no function responses generated, exiting.")

    for fr in function_responses:
        messages.append(types.Content(role="user", parts=[fr]))

    # Return None to indicate conversation should continue
    return None


if __name__ == "__main__":
    main()
