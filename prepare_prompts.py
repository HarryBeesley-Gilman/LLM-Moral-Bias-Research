import csv
def load_questions(input_file_questions):
    question_number_count =1

    questions = []
    question_numbers = {}


    with open(input_file_questions, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                question = row[0].strip()
                questions.append(question)
                question_numbers[question] = question_number_count
                question_number_count+=1

    return questions, question_numbers


def build_prompt_survey(questions, respond_as):
    prompt = str(respond_as) + "Part 1. When you decide whether something is right or wrong, to what extent are the following considerations\
 relevant to your thinking? Please rate each statement using this scale:\
    \n\
      \n[0] = not at all relevant (This consideration has nothing to do with my judgments of right and wrong)\
         \n[1] = not very relevant\
            \n[2] = slightly relevant\
                \n[3] = somewhat relevant\
                   \n[4] = very relevant\
                      \n[5] = extremely relevant (This is one of the most important factors when I judge right and wrong)"

    prompt += "\n"
 

    for i in range(1,17): #there will always be 32 questions
        prompt += ("\n" + str(i) + ". " + str(questions[i-1]))

    prompt += ("\n")


    prompt += "\n Part 2. Please read the following sentences and indicate your agreement or disagreement:"
    prompt += "\n"
    prompt += "\n [0] - Strongly disagree \n [1] - Moderately disagree \n [2] - Slightly disagree \n [3] - Slightly agree\
\n [4] - Moderately agree \n [5] - Strongly agree \n"


    for i in range(17,33):
        prompt+= ("\n" + str(i) + ". " + str(questions[i-1]))

    return prompt


