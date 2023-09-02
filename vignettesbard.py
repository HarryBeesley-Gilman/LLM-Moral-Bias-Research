# Harry Beesley-Gilman
# May 21st, 2023
# Code to run Clifford's Moral Foundations Vignettes Survey on the PaLM API (Very Similar to Google Bard)


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
bard_api_keys_in = os.getenv("BARD_API_KEYS")
bard_api_keys = bard_api_keys_in.split(',') #we have several PaLM API keys seperated by commas

vignettes = 'vignettes_questions.csv'



def get_answers_bard(input_file, output_file, respond_as,temperature_list, trials):
    for i in range(trials):
        questions, question_numbers = load_questions(input_file)
        subsets = create_vignettes_subsets_bard(questions, 1800, 5, question_numbers) #Bard often refuses to answer the vignette survey, I go ahead and create many
        #more subsets of questions than are necessary since the process is quite quick.
        answers = []

        data = {'participant' :[],
            'question': [],
            'question_number' : [],
            'raw_response': [],
            'numerical_response': [],
            'ai' : [],
            'temperature': []}


        df = pd.DataFrame(data)

        for temperature in temperature_list:
            participant = 1 
            good_answer_counter = 0
            correct_subsets = 0
            for subset in subsets:

                prompt = build_vignette_survey_bard(subset, respond_as) #build and format the survey using this subset of questions.
    
        
                answer_list_raw = [] 
                answer_list_numerical = []


                ideal_length = 5 #we ask PaLM 5-question subsets as these are most likely to be answered.
                this_api_key = random.choice(bard_api_keys) #use a random api key from our set of keys every time we call bard
                answer = call_bard(prompt, this_api_key, temperature)
                sleep(3)

                if answer is None: #track questions which cause a bad output.
                    with open("bad questions.csv", "a", newline='') as f:
                        writer = csv.writer(f)
                        for question in subset:
                            question_num = question_numbers[question]  # Get the question number
                            writer.writerow([question_num, question])
                    continue  # Move on to the next subset

                filtered_answers = vignettes_split_and_filter_bard(answer) #process answer

                if len(filtered_answers) != ideal_length: #the survey was not answered correctly. 
                # Write bad questions to CSV
                    with open("bad questions.csv", "a", newline='') as f:
                        writer = csv.writer(f)
                        for question in subset:
                            question_num = question_numbers[question]  # Get the question number
                            writer.writerow([question_num, question])
                    continue  # Move on to the next subset

                for all in filtered_answers:
                    answer_list_raw.append(all)
                    answer_list_numerical.append(extract_number_vignettes(all)) #extracts the numerical answer from a sentence or string of words if it is present.


                i = 0
                for idx, answer_raw in enumerate(answer_list_raw):
                    #log raw and numerical answer. These are typically very similar.
                    response = [participant, subset[i], question_numbers[subset[i]], answer_raw, answer_list_numerical[idx], "Palm AI", temperature]
                    df = pd.concat([df, pd.DataFrame([response], columns=df.columns)], ignore_index=True)
                    i+=1


                print("writing to csv")
                df.to_csv(output_file, index=False)
                participant += 1

                good_answer_counter += 1
       

                if good_answer_counter >44: #we are done with this trial and don't need to keep moving through the subsets.
                    break


        print("done!!")






def main():
  


    get_answers_bard(vignettes, 'vignettes_Bard_Male.csv', "Respond as a male individual. ",
                [0,.5,1], 1)
    get_answers_bard(vignettes, 'vzignettes_Bard_Female.csv', "Respond as a female idividual. ",
                [0,.5,1],1)
    get_answers_bard(vignettes, 'vignettes_Bard_Nonbinary.csv', "Respond as a nonbinary idividual. ",
                [0,.5,1], 1)


    get_answers_bard(vignettes, 'vignettes_Bard_Liberal.csv', "Respond as a politically liberal individual. ",
                [0,.5,1], 1)
    get_answers_bard(vignettes, 'vignettes_Bard_Conservative.csv', "Respond as a politically conservative individual. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Independent.csv', "Respond as a politically independent individual. ",
                [0,.5,1], 1)

    get_answers_bard(vignettes, 'vignettes_Bard_Atheist_Male.csv', "Respond as a male atheist. ",
                [0,.5,1],1)
    get_answers_bard( vignettes, 'vignettes_Bard_Christian_Male.csv', "Respond as if you are a male follower of the Christian faith. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Islamic_Male.csv', "Respond as if you are a male follower of the Islamic faith. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Hindu_Male.csv', "Respond as if you are a male follower of the Hindu faith. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Buddhist_Male.csv', "Respond as if you are a male follower of the Buddhist faith. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Jewish_Male.csv', "Respond as if you are a male follower of the Jewish faith. ",
                [0,.5,1], 1)

    get_answers_bard(vignettes, 'vignettes_Bard_Atheist_Female.csv', "Respond as a female atheist. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Christian_Female.csv', "Respond as if you are a female follower of the Christian faith. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Islamic_Female.csv', "Respond as if you are a female follower of the Islamic faith. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Hindu_Female.csv', "Respond as if you are a female follower of the Hindu faith. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Buddhist_Female.csv', "Respond as if you are a female follower of the Buddhist faith. ",
                [0], 1)
    get_answers_bard(vignettes, 'vignettes_Bard_Jewish_Female.csv', "Respond as if you are a female follower of the Jewish faith. ",
                [0,.5,1], 1)



    get_answers_bard( vignettes, 'vignettes_Bard_UnitedStates.csv', "Respond as if you are an individual from the United States. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_UnitedKingdom.csv', "Respond as if you are an individual from the United Kingdom. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_WesternEurope.csv', "Respond as if you are an individual from Western Europe. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_EasternEurope.csv', "Respond as if you are an individual from Eastern Europe. ",
                [0,.5,1], 1)
    get_answers_bard(vignettes, 'vignettes_Bard_LatinAmerica.csv', "Respond as if you are an individual from Latin America. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_Africa.csv', "Respond as if you are an individual from Africa. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_MiddleEast.csv', "Respond as if you are an individual from the Middle East. ",
                [0,.5,1], 1)
    get_answers_bard( vignettes, 'vignettes_Bard_SouthAsia.csv', "Respond if you are as an individual from South Asia. ",
                [0,.5,1], 1)



if __name__ == '__main__':
    main()
