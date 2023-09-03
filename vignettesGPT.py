# Harry Beesley-Gilman
# May 21st, 2023
# Code to run Clifford's Moral Foundations Vignettes Survey on ChatGPT


import csv
import itertools
import openai
import pyperclip
from time import sleep 
import os 
from bardapi.core import Bard
import pandas as pd 
from survey_methods import *
from answer_processing import *
from prepare_prompts import *
import numpy as np

load_dotenv("api_keys.env") #load in API keys so as not to display them in actual code
openai.api_key = os.getenv("OPENAI_API_KEY")
bard_api_keys_in = os.getenv("BARD_API_KEYS")
bard_api_keys = bard_api_keys_in.split(',') #we have several PaLM API keys seperated by commas

vignettes = 'vignettes_questions.csv'


def get_answers_gpt(input_file, output_file, respond_as,temperature_list, trials):
    for i in range(trials): #running one trial will result in 15 surveys answered at a given temp
        questions, question_numbers = load_questions(input_file)
        subsets = create_vignette_subsets(questions, 15, 15) #ask random 15-question subsets 15 times.
        answers = []


        data = {'participant' :[], #participant used in a loose sense here; really represents which iteration we're on at a given temperature level.
            'question': [],
            'question_number' : [],
            'raw_response': [],
            'numerical_response': [],
            'ai' : [],
            'temperature': []}


        df = pd.DataFrame(data)

        for temperature in temperature_list:
            participant = 1 
            correct_subsets = 0
            for subset in subsets: #these subsets are 15-question groups of questions, selected randomly.
                question_list = []
                for all in subset:
                    question_list.append(all)
                prompt = build_vignette_survey_gpt(subset, respond_as) #put the survey together, maintaining formatting from original study.
            
                answer_list_raw = [] 
                answer_list_numerical = []

            #   Define the query
                answer = call_ChatGPT(prompt, temperature, 10)
                sleep(1+.5*5.5*np.random.rand()) #sleep so as not to overwhelm the API
                answer_split = answer.splitlines() #split the answer into lines.

                filtered_answers = vignettes_split_and_filter_gpt(answer)

                bad_answer_count = 0 
                ideal_length = 15 #we have 15 questions and should get 15 answers.
    
                while len(filtered_answers) != ideal_length: #sometimes, ChatGPT will not answer the survey. This simply retries a few times if we don't get a full answer.

                    answer = call_ChatGPT(prompt, temperature, 10) 
                    answer_split = answer.splitlines()

                    filtered_answers = vignettes_split_and_filter_gpt(answer)
          
                    if bad_answer_count == 5:
                        print("we have too many bad answers and are giving up")
                        return

                    bad_answer_count += 1



                for all in filtered_answers:
                    answer_list_raw.append(all)
                    answer_list_numerical.append(extract_number_vignettes(all))


                i = 0
                for idx, answer_raw in enumerate(answer_list_raw): #fill out our pandas dataframe for writing to the answer file. Stores a universal question number value for each question.
      
                    response = [participant, question_list[i], question_numbers[question_list[i]], answer_raw, answer_list_numerical[idx], "chatGPT", temperature]
                    df = pd.concat([df, pd.DataFrame([response], columns=df.columns)], ignore_index=True)
                    i+=1


                print("writing to csv")
                df.to_csv(output_file, index=False)
                participant += 1


        print("done!!")









def main():
  
    # get_answers_gpt(vignettes, 'vignettes_GPT.csv', "",
    #             [0,.5,1], 1)


    # get_answers_gpt(vignettes, 'vignettes_gpt_male.csv', "Respond as a male individual. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Female.csv', "Respond as a female idividual. ",
    #             [0,.5,1],1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Nonbinary.csv', "Respond as a nonbinary idividual. ",
    #             [0,.5,1], 1)

    # get_answers_gpt(vignettes, 'vignettes_GPT_Liberal.csv', "Respond as a politically liberal individual. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Conservative.csv', "Respond as a politically _gptconservative idividual. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Independent.csv', "Respond as a politically independent idividual. ",
    #             [0,.5,1], 1)

    # get_answers_gpt(vignettes, 'vignettes_GPT_Atheist_Male.csv', "Respond as a male atheist. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Christian_Male.csv', "Respond as a male follower of the Christian faith. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Islamic_Male.csv', "Respond as a male follower of the Islamic faith. ",
    #            [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Hindu_Male.csv', "Respond as a male follower of the Hindu faith. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Buddhist_Male.csv', "Respond as a male follower of the Buddhist faith. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Jewish_Male.csv', "Respond as a male follower of the Jewish faith. ",
    #             [0,.5,1], 1)

    get_answers_gpt(vignettes, 'vignettes_GPT_Atheist_Female.csv', "Respond as a female atheist. ",
               [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Christian_Female.csv', "Respond as a female follower of the Christian faith. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Islamic_Female.csv', "Respond as a female follower of the Islamic faith. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Hindu_Female.csv', "Respond as a female follower of the Hindu faith. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Buddhist_Female.csv', "Respond as a female follower of the Buddhist faith. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Jewish_Female.csv', "Respond as a female follower of the Jewish faith. ",
    #             [0,.5,1], 1)

    # get_answers_gpt(vignettes, 'vignettes_GPT_UnitedStates.csv', "Respond as an individual from the United States. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_UnitedKingdom.csv', "Respond as an individual from the United Kingdom. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_WesternEurope.csv', "Respond as an individual from Western Europe. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_EasternEurope.csv', "Respond as an individual from Eastern Europe. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_LatinAmerica.csv', "Respond as an individual from Latin America. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_Africa.csv', "Respond as an individual from Africa. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_MiddleEast.csv', "Respond as an individual from the Middle East. ",
    #             [0,.5,1], 1)
    # get_answers_gpt(vignettes, 'vignettes_GPT_SouthAsia.csv', "Respond as an individual from South Asia. ",
    #             [0,.5,1], 1)




if __name__ == '__main__':
    main()
