# Harry Beesley-Gilman
# May 21st, 2023
# Code for ChatGPT and Palm AI MFQ Experiment

import google.generativeai as palm
import csv
import openai
from time import sleep 
import os 
from bardapi.core import Bard
import pandas as pd 
from random import *
from survey_methods import *
from text_processing import *
from prepare_prompts import *
import numpy as np

load_dotenv("api_keys.env") #load in API keys so as not to display them in actual code
openai.api_key = os.getenv("OPENAI_API_KEY")
bard_api_keys_in = os.getenv("BARD_API_KEYS")
bard_api_keys = bard_api_keys_in.split(',') #we have several PaLM API keys seperated by commas

standard_questions = 'foundations_questions.csv' #load in questions files.
variated_questions = 'variated_foundations_questions.csv'



def get_answers(ai, input_file, output_file, respond_as, temperature_list, trials):
    questions, question_numbers = load_questions(input_file) #load questions method stored in another file
    answers = []
    if ai == 'chatgpt':
        prompt = build_prompt_survey(questions, respond_as) #constructs the prompt from the list of questions
    else:
        prompt = bard_build_prompt_survey(questions, respond_as) #this prompt asks the exact same question and uses the same words
        #but formats the line spacing slightly differently so PaLM is more likely to answer.



    data = {'trial_number' :[],
        'question': [],
        'question_number' : [],
        'raw_response': [],
        'numerical_response': [],
        'ai' : [],
        'temperature': []}


    df = pd.DataFrame(data)

    for temperature in temperature_list: #collect data at several temperature values


        working_prompt = prompt
        for i in range(trials):

            answer_list_raw = [] 
            answer_list_numerical = []

        #   Define the query
            if ai == 'chatgpt':
                answer = call_ChatGPT(prompt, temperature, 10)
                sleep(1+.5*5.5*np.random.rand()) #sleep so as not to lodge too many requests too frequently
                filtered_answers = split_and_filter_gpt(answer)

            elif ai == 'bard':
                this_api_key = random.choice(bard_api_keys) #use a random api key from our set of keys every time we call bard
                answer = call_bard(working_prompt, this_api_key, temperature) #passes in several API keys to rotate through. Helps when PaLM starts deciding not to answer the survey
                sleep(1+.5*5.5*np.random.rand()) #again sleep 
                filtered_answers = split_and_filter_bard(answer) #splits answer statement into its 32 lines and filters out unnessecary text at the beginning or end.

            else:
                print('no AI specified')

            print("printing filtered_answers") #displays answers to each to each query.
            print(filtered_answers)


            bad_answer_count = 0 

            while len(filtered_answers) != 32: #allows retry if survey isn't answered normally. This almost never happened with the MFQ
                print("trying again since length was wrong")

                if ai == 'chatgpt':
                    sleep(1+.5*5.5*np.random.rand())
                    answer = call_ChatGPT(prompt, temperature, 10)
                    filtered_answers = split_and_filter_gpt(answer)

                elif ai == 'bard': #
                    sleep(1+.5*5.5*np.random.rand()) #prevent rate limitting errors.
                    this_api_key = random.choice(bard_api_keys)
                    answer = call_bard(working_prompt, this_api_key, temperature)
                    filtered_answers = split_and_filter_bard(answer)  #split the answer, which is a single block of text with many lines, into 32 individul answers.

                else:
                    print('no AI specified')

      
                if bad_answer_count == 5: 
                    print("we have too many bad answers and are giving up")
                    return

                bad_answer_count += 1


            for all in filtered_answers: #The next 10 lines process our answer and extracts a 1-5 numerical score for placement on the datasheet.
                answer_list_raw.append(all)
                answer_list_numerical.append(extract_number(all))


            for idx, answer_raw in enumerate(answer_list_raw): #goes through answers and fills out results sheet.
                response = [i, questions[idx], idx+1, answer_raw, answer_list_numerical[idx], ai, temperature]
                df = pd.concat([df, pd.DataFrame([response], columns=df.columns)], ignore_index=True)



            print("writing to csv")
            df.to_csv(output_file, index=False)


    print("done!!")




def main():
  
    get_answers('chatgpt', standard_questions, 'standard_GPT.csv', "",
                [0,.5,1], 20)
    get_answers('chatgpt', variated_questions, 'variated_GPT.csv', "",
                [0,.5,1], 20)

    get_answers('chatgpt', standard_questions, 'GPT_Male.csv', "Respond as a male individual",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Female.csv', "Respond as a female idividual",
                [1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Nonbinary.csv', "Respond as a nonbinary idividual",
                [0,.5,1], 10)

    get_answers('chatgpt', standard_questions, 'GPT_Liberal.csv', "Respond as a politically liberal individual",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Conservative.csv', "Respond as a politically conservative idividual",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Independent.csv', "Respond as a politically independent idividual",
                [0,.5,1], 10)

    get_answers('chatgpt', standard_questions, 'GPT_Atheist_Male.csv', "Respond as a male atheist",
                 [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Christian_Male.csv', "Respond as a male follower of the Christian faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Islamic_Male.csv', "Respond as a male follower of the Islamic faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Hindu_Male.csv', "Respond as a male follower of the Hindu faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Buddhist_Male.csv', "Respond as a male follower of the Buddhist faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Jewish_Male.csv', "Respond as a male follower of the Jewish faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Islamic_Male.csv', "Respond as a male follower of the Islamic faith",
                 [0,.5,1], 10)


    get_answers('chatgpt', standard_questions, 'GPT_Atheist_Female.csv', "Respond as a female atheist",
                 [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Christian_Female.csv', "Respond as a female follower of the Christian faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Islamic_Female.csv', "Respond as a female follower of the Islamic faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Hindu_Female.csv', "Respond as a female follower of the Hindu faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Buddhist_Female.csv', "Respond as a female follower of the Buddhist faith",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Jewish_Female.csv', "Respond as a female follower of the Jewish faith",
                [0,.5,1], 10)



    get_answers('chatgpt', standard_questions, 'GPT_UnitedStates.csv', "Respond as an individual from the United States",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_UnitedKingdom.csv', "Respond as an individual from the United Kingdom",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_WesternEurope.csv', "Respond as an individual from Western Europe",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_EasternEurope.csv', "Respond as an individual from Eastern Europe",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_LatinAmerica.csv', "Respond as an individual from Latin America",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Africa2.csv', "Respond as an individual from Africa",
                [1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_MiddleEast.csv', "Respond as an individual from the Middle East",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_SouthAsia.csv', "Respond as an individual from South Asia",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'standard_bard.csv', "",
                [0,.5,1], 20)
    get_answers('bard', variated_questions, 'variated_bard.csv', "",
                [0,.5,1], 20)

    get_answers('bard', standard_questions, 'bard_Male.csv', "Respond as a male individual",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Female.csv', "Respond as a female idividual",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Nonbinary.csv', "Respond as a nonbinary idividual",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'bard_Liberal.csv', "Respond to as a politically liberal individual",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'bard_Conservative.csv', "Respond as a politically conservative idividual",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Independent.csv', "Respond as a politically independent idividual",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'bard_Atheist_Male.csv', "Respond as a male atheist",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Atheist_Female.csv', "Respond as a female atheist",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'bard_Christian_Male.csv', "Respond as a male follower of the Christian faith",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Islamic_Male.csv', "Respond as a male follower of the Islamic faith",
                [0],10)
    get_answers('bard', standard_questions, 'bard_Hindu_Male.csv', "Respond as a male follower of the Hindu faith",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Buddhist_Male.csv', "Respond as a male follower of the Buddhist faith",
                [0], 10)
    get_answers('bard', standard_questions, 'bard_Jewish_Male.csv', "Respond as a male follower of the Jewish faith",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'bard_Christian_Female.csv', "Respond as a female follower of the Christian faith",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Islamic_Female.csv', "Respond as a female follower of the Islamic faith",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Hindu_Female.csv', "Respond as a female follower of the Hindu faith",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Buddhist.csv', "Respond as a female follower of the Buddhist faith",
                [0], 10)
    get_answers('bard', standard_questions, 'bard_Jewish_Female.csv', "Respond as a female follower of the Jewish faith",
                [0,.5,1], 10)



    get_answers('bard', standard_questions, 'bard_UnitedStates.csv', "Respond as an individual from the United States",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_UnitedKingdom.csv', "Respond as an individual from the United Kingdom",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_WesternEurope.csv', "Respond as an individual from Western Europe",
                [0,.5,1],10)
    get_answers('bard', standard_questions, 'bard_EasternEurope.csv', "Respond as an individual from Eastern Europe",
                [0,.5,1],10)
    get_answers('bard', standard_questions, 'bard_LatinAmerica.csv', "Respond as an individual from Latin America",
                [0,.5,1],10)
    get_answers('bard', standard_questions, 'bard_Africa.csv', "Respond as an individual from Africa",
                [0,.5,1],10)
    get_answers('bard', standard_questions, 'bard_MiddleEast.csv', "Respond as an individual from the Middle East",
                [0,.5,1],10)
    get_answers('bard', standard_questions, 'bard_SouthAsia.csv', "Respond as an individual from South Asia",
                [0,.5,1],10)

if __name__ == '__main__':
    main()
