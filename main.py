# May 21st, 2023
# Code for ChatGPT


import csv
import itertools
import openai
import pyperclip
from time import sleep 
import os 
from bardapi.core import Bard
import pandas as pd 
from survey_methods import *
from text_processing import *
from prepare_prompts import *

load_dotenv("api_keys.env")

openai.api_key = os.getenv("OPENAI_API_KEY")
bard_api_key = os.getenv("BARD_API_KEY")
standard_questions = 'foundations_questions.csv'
variated_questions = 'variated_foundations_questions.csv'








def get_answers(ai, input_file, output_file, respond_as, temperature_list, trials):
    print("running get answers")
    questions, question_numbers = load_questions(input_file)
    answers = []

    prompt = build_prompt_survey(questions, respond_as)

    data = {'trial_number' :[],
        'question': [],
        'question_number' : [],
        'raw_response': [],
        'numerical_response': [],
        'ai' : [],
        'temperature': []}


    df = pd.DataFrame(data)

    for temperature in temperature_list:

        for i in range(trials):

            answer_list_raw = [] 
            answer_list_numerical = []

        #   Define the query
            if ai == 'chatgpt':
                answer = call_ChatGPT(prompt, temperature, 10)
                filtered_answers = split_and_filter_gpt(answer)

            elif ai == 'bard':
                prompt = prompt + 'Answer with temperature ' + str(temperature)
                answer = call_bard(prompt, bard_api_key)
                filtered_answers = split_and_filter_bard(answer)

            else:
                print('no AI specified')

            print("printing filtered_answers")
            print(filtered_answers)


            bad_answer_count = 0 

            while len(filtered_answers) != 32:
                print("trying again since length was wrong")

                if ai == 'chatgpt':
                    answer = call_ChatGPT(prompt, temperature, 10)
                    filtered_answers = split_and_filter_gpt(answer)

                elif ai == 'bard':
                    prompt = prompt + 'Answer with temperature ' + str(temperature)
                    answer = call_bard(prompt, bard_api_key)
                    filtered_answers = split_and_filter_bard(answer)

                else:
                    print('no AI specified')

      
                if bad_answer_count == 5:
                    print("we have too many bad answers and are giving up")
                    return

                bad_answer_count += 1



            for all in filtered_answers:
                answer_list_raw.append(all)
                answer_list_numerical.append(extract_number(all))



            for idx, answer_raw in enumerate(answer_list_raw):
  
                response = [i, questions[idx], idx+1, answer_raw, answer_list_numerical[idx], ai, temperature]
                df = pd.concat([df, pd.DataFrame([response], columns=df.columns)], ignore_index=True)



            print("writing to csv")
            df.to_csv(output_file, index=False)


    print("done!!")


    #return answers





def main():
  
    get_answers('chatgpt', standard_questions, 'standard_GPT.csv', "",
                [0,.25,.5,.75,1], 10)
    get_answers('chatgpt', variated_questions, 'variated_GPT.csv', "",
                [0,.25,.5,.75,1], 10)

    get_answers('chatgpt', standard_questions, 'GPT_Male.csv', "Respond as a male individual",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Female.csv', "Respond as a female idividual",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Nonbinary.csv', "Respond as a nonbinary idividual",
                [0,.5,1], 10)

    get_answers('chatgpt', standard_questions, 'GPT_Liberal.csv', "Respond as a liberal individual",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Conservative.csv', "Respond as a conservative idividual",
                [0,.5,1], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Independent.csv', "Respond as a politically independent idividual",
                [0,.5,1], 10)

    get_answers('chatgpt', standard_questions, 'GPT_Christian_Male.csv', "Respond as a male follower of the Christian faith",
                [0,.5,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Islamic_Male.csv', "Respond as a male follower of the Islamic faith",
                [0,.5,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Hindu_Male.csv', "Respond as a male follower of the Hindu faith",
                [0,.5,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Buddhist_Male.csv', "Respond as a male follower of the Buddhist faith",
                [0,.5,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Jewish_Male.csv', "Respond as a male follower of the Jewish faith",
                [0,.5,1], 5)

    get_answers('chatgpt', standard_questions, 'GPT_Christian_Female.csv', "Respond as a male follower of the Christian faith",
                [0,.5,.75,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Islamic_Female.csv', "Respond as a male follower of the Islamic faith",
                [0,.5,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Hindu_Female.csv', "Respond as a male follower of the Hindu faith",
                [0,.5,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Buddhist_Female.csv', "Respond as a male follower of the Buddhist faith",
                [0,.5,1], 5)
    get_answers('chatgpt', standard_questions, 'GPT_Jewish_Female.csv', "Respond as a male follower of the Jewish faith",
                [0,.5,1], 5)



    get_answers('chatgpt', standard_questions, 'GPT_UnitedStates.csv', "Respond as an individual from the United States",
                [0.7], 10)
    get_answers('chatgpt', standard_questions, 'GPT_UnitedKingdom.csv', "Respond as an individual from the United Kingdom",
                [0.7], 10)
    get_answers('chatgpt', standard_questions, 'GPT_WesternEurope.csv', "Respond as an individual from Western Europe",
                [0.7], 10)
    get_answers('chatgpt', standard_questions, 'GPT_EasternEurope.csv', "Respond as an individual from Eastern Europe",
                [0.7], 10)
    get_answers('chatgpt', standard_questions, 'GPT_LatinAmerica.csv', "Respond as an individual from Latin America",
                [0.7], 10)
    get_answers('chatgpt', standard_questions, 'GPT_Africa.csv', "Respond as an individual from Africa",
                [0.7], 10)
    get_answers('chatgpt', standard_questions, 'GPT_MiddleEast.csv', "Respond as an individual from the Middle East",
                [0.7], 10)
    get_answers('chatgpt', standard_questions, 'GPT_SouthAsia.csv', "Respond as an individual from South Asia",
                [0.7], 10)

    get_answers('bard', standard_questions, 'standard_bard.csv', "",
                [0,.25,.5,.75,1], 10)
    get_answers('bard', variated_questions, 'variated_bard.csv', "",
                [0,.25,.5,.75,1], 10)

    get_answers('bard', standard_questions, 'bard_Male.csv', "Respond as a male individual",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Female.csv', "Respond as a female idividual",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Nonbinary.csv', "Respond as a nonbinary idividual",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'bard_Liberal.csv', "Respond as a liberal individual",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Conservative.csv', "Respond as a conservative idividual",
                [0,.5,1], 10)
    get_answers('bard', standard_questions, 'bard_Independent.csv', "Respond as a politically independent idividual",
                [0,.5,1], 10)

    get_answers('bard', standard_questions, 'bard_Christian_Male.csv', "Respond as a male follower of the Christian faith",
                [0,.5,1], 5)
    get_answers('bard', standard_questions, 'bard_Islamic_Male.csv', "Respond as a male follower of the Islamic faith",
                [0,.5,1], 5)
    get_answers('bard', standard_questions, 'bard_Hindu_Male.csv', "Respond as a male follower of the Hindu faith",
                [0,.5,1], 5)
    get_answers('bard', standard_questions, 'bard_Buddhist_Male.csv', "Respond as a male follower of the Buddhist faith",
                [0,.5,1], 5)
    get_answers('bard', standard_questions, 'bard_Jewish_Male.csv', "Respond as a male follower of the Jewish faith",
                [0,.5,1], 5)

    get_answers('bard', standard_questions, 'bard_Christian_Female.csv', "Respond as a male follower of the Christian faith",
                [0,.5,.75,1], 5)
    get_answers('bard', standard_questions, 'bard_Islamic_Female.csv', "Respond as a male follower of the Islamic faith",
                [0,.5,1], 5)
    get_answers('bard', standard_questions, 'bard_Hindu_Female.csv', "Respond as a male follower of the Hindu faith",
                [0,.5,1], 5)
    get_answers('bard', standard_questions, 'bard_Buddhist_Female.csv', "Respond as a male follower of the Buddhist faith",
                [0,.5,1], 5)
    get_answers('bard', standard_questions, 'bard_Jewish_Female.csv', "Respond as a male follower of the Jewish faith",
                [0,.5,1], 5)



    get_answers('bard', standard_questions, 'bard_UnitedStates.csv', "Respond as an individual from the United States",
                [0.7], 10)
    get_answers('bard', standard_questions, 'bard_UnitedKingdom.csv', "Respond as an individual from the United Kingdom",
                [0.7], 10)
    get_answers('bard', standard_questions, 'bard_WesternEurope.csv', "Respond as an individual from Western Europe",
                [0.7], 10)
    get_answers('bard', standard_questions, 'bard_EasternEurope.csv', "Respond as an individual from Eastern Europe",
                [0.7], 10)
    get_answers('bard', standard_questions, 'bard_LatinAmerica.csv', "Respond as an individual from Latin America",
                [0.7], 10)
    get_answers('bard', standard_questions, 'bard_Africa.csv', "Respond as an individual from Africa",
                [0.7], 10)
    get_answers('bard', standard_questions, 'bard_MiddleEast.csv', "Respond as an individual from the Middle East",
                [0.7], 10)
    get_answers('bard', standard_questions, 'bard_SouthAsia.csv', "Respond as an individual from South Asia",
                [0.7], 10)


if __name__ == '__main__':
    main()
