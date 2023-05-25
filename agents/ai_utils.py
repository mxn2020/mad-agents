import time
import openai

retry_limit = 50


def api_call(chat_messages):
    # Make the API request and store the response in the api_response variable
    api_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_messages,
        max_tokens=3000,
        temperature=1.2,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

def handle_api_error(retry, error_text, wait_time):
    if retry == retry_limit - 1:
        raise openai.error.RateLimitError(error_text + "Exceeded retry limit, unable to get response due to rate limit.")

    print(error_text + "Retrying...")
    time.sleep(wait_time)

def ai_response(prompt):
    error_text = None
    retry_count = 0
    wait_time = 15

    while retry_count < retry_limit:
        try:
            response = api_call(prompt)  # Replace with your OpenAI API call
            return response  # Return the response if the API call is successful

        except TimeoutError:
            error_text = "Timeout error occurred. "
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

        except openai.error.APIError as e:
            error_text = "OpenAI API returned an API Error. "
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

        except openai.error.RateLimitError as e:
            error_text = "Rate limit exceeded. "
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

        except openai.error.APIConnectionError as e:
            error_text = "Issue connecting to OpenAI services. "
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

        except openai.error.InvalidRequestError as e:
            error_text = "Invalid request. "
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

        except openai.error.AuthenticationError as e:
            error_text = "Authentication error. "
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

        except openai.error.ServiceUnavailableError as e:
            error_text = "OpenAI service unavailable. "
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

        except Exception as e:
            error_text = "Unkown Error occurred. " + str(e)
            handle_api_error(retry_count, error_text, wait_time)
            retry_count += 1
            wait_time += 5

    raise Exception("Error: Unable to get response after multiple retries.")
