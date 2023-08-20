from bardapi.core import Bard
from dotenv import load_dotenv
load_dotenv("api_keys.env")
import os 
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
bard_api_key = os.getenv("BARD_API_KEY")

def call_bard(query, api_key):
	BARD_API_KEY = api_key
	bard = Bard(BARD_API_KEY)
	answer = bard.get_answer(query)
	return (answer['content'])

def call_ChatGPT(question, temperature, max_retries):
    for i in range(max_retries):
        try:
            print("trying")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ],
                temperature = temperature
            )
            
            answer = response['choices'][0]['message']['content'].strip()
            
            # Check if the answer contains '1.' and '2.'
            if '1.' in answer.lower() and '2.' in answer.lower():
                return answer

        except openai.error.RateLimitError as e:
            print("Rate limit error, retrying... ({}/{})".format(i+1, max_retries))
            if i < max_retries - 1:
                sleep(20)  # Wait for 20 seconds before trying again
            else:
                raise




