import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from argparse import ArgumentParser
from config import system_prompt, MAX_ITERS 
from available_functions import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key is not found")  
client = genai.Client(api_key=api_key)

parser = ArgumentParser(description="AI Agent")
parser.add_argument("user_prompt", type=str, help = "User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


for _ in range(MAX_ITERS):
    try:
        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents = messages,
        config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))


        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if not response.function_calls and response.text:
            print("Final response:")
            print(response.text)
            break
        if response.usage_metadata is None:
            raise RuntimeError("Likely failed API request")



        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception(f'Empty .parts list')
                if not function_call_result.parts[0].function_response:
                    raise Exception('Not a FunctionResponse object')
                if not function_call_result.parts[0].function_response.response:
                    raise Exception('Function result is None')
                function_results.append(function_call_result.parts[0])

        if function_results:
            messages.append(types.Content(role='user', parts = function_results))




        if args.verbose:
            print(f"User prompt:{args.user_prompt}")
            print(f"""Prompt tokens:{response.usage_metadata.prompt_token_count} 
        Response tokens: {response.usage_metadata.candidates_token_count}""")    
            #print(response.text)
            print(f"-> {function_call_result.parts[0].function_response.response}")







        


    except Exception as e:
        print(f'Exception: {e}')

        






