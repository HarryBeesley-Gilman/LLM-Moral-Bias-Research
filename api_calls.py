# Harry Beesley-Gilman
# May 21st, 2023
# Call OpenAI and PaLM API's

from bardapi.core import Bard
from dotenv import load_dotenv
import os 
import openai
from bardapi import BardCookies
from Bard import Chatbot
import google.generativeai as palm
import random




def call_bard(query, api_key, temperature_in):



    palm.configure(api_key=api_key)


    temp = temperature_in


    print("answering query:")
    print(query)

    completion = palm.generate_text(
        model= "models/text-bison-001",
        prompt= query,
        temperature=temp,
        # The maximum length of the response (in tokens)
        max_output_tokens=1000,
    )


    print(completion.result)
  

    return completion.result


def call_ChatGPT(question, temperature, max_retries):
    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ],
                temperature = temperature
            )
            
            answer = response['choices'][0]['message']['content'].strip()

            return answer

            

        except openai.error.RateLimitError as e:
            print("Rate limit error, retrying... ({}/{})".format(i+1, max_retries))
            if i < max_retries - 1:
                sleep(20)  # Wait for 20 seconds before trying again
            else:
                raise
    print("exhausted errors")
    return None



