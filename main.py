import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("No api key found")
    
    parser = argparse.ArgumentParser(description="chatbor")
    parser.add_argument("user_prompt",type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model='gemini-2.5-flash',
                                               contents=messages,
                                               config=types.GenerateContentConfig(
                                                   tools=[available_functions], system_instruction=system_prompt
                                                   )
                                               )

    if response.usage_metadata == None:
        raise RuntimeError("Failed api request")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")

    function_call_results = []
    if response.function_calls == None:
        print(response.text)
    else:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if not function_call_result.parts:
                raise ValueError("The call_function returned a Content object with an empty 'parts' list!")

            if function_call_result.parts[0].function_response is None:
                raise ValueError("The call_function returned a Content object with a 'parts' list where the first part has a 'function_response' of None!")
            
            if function_call_result.parts[0].function_response.response is None:
                raise ValueError("The call_function returned a Content object with a 'parts' list where the first part has a 'function_response' with a 'response' of None!")

            function_call_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    

if __name__ == "__main__":
    main()
