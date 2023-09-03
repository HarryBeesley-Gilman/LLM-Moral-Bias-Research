import re

def extract_number(text): #this code extracts numerical response from AI output


    if 'not at all relevant' in text or 'Strongly disagree' in text:
        return 0

    if 'not very relevant' in text or 'Moderately disagree' in text:
        return 1

    elif 'slightly relevant' in text or 'Slightly disagree' in text:
        return 2

    elif 'somewhat relevant' in text or 'Slightly agree' in text:
        return 3

    elif 'very relevant' in text or 'Moderately agree' in text:
        return 4

    elif 'extremely relevant' in text or 'Strongly agree' in text:
        return 5

    # Remove non-digit characters from the text

    value = None 
    for char in text: #returns the last number in the answer. Empiracly, this seemed to always be correct, as answer is almost always in the format (question number). (answer).
        if char.isdigit():
            value = char
    
    # Return the extracted number if it exists, otherwise return None
    if value:
        return value
    else:
        return None

def extract_number_vignettes(text): #vignettes survey language is slightly different.
    if 'not at all' in text:
        return 1

    elif 'not too' in text:
        return 2

    elif 'somewhat wrong' in text:
        return 3

    elif 'very wrong' in text:
        return 4

    elif 'extremely wrong' in text:
        return 5

    # Remove non-digit characters from the text

    value = None 
    for char in text:
        if char.isdigit():
            value = char
    
    # Return the extracted number if it exists, otherwise return None
    if value:
        return value
    else:
        return None

def split_and_filter_bard(answer):
 
    valid_answers = []


    for line in answer.splitlines():
        line = line.strip()

        # Ignore undesired lines used to describe how the answer is coming from an AI
        if not any(substring in line.lower() for substring in ["as a", "part", "sure"]):

            # Check if the line contains a number followed by a period or the word 'whether'. We have 32 questions in the mfq survey so look for an answer to one of those questions.
            if any(f"{y}." in line for y in range(1, 33)) or "whether" in line.lower():
                valid_answers.append(line)

            # Check if the line starts with a number (your answer)
            elif line and line[0].isdigit(): #if the answer is just a number.
                valid_answers.append(line)

    return valid_answers



def split_and_filter_gpt(answer):
    lines = answer.splitlines() 
    filtered_lines = [line for line in lines if line.strip() != '.' and len(line.strip()) > 0 and "part" not in line.lower() and "as a" not in line.lower() and "therefore" not in line.lower() and "please note" not in line.lower()]
    return filtered_lines

def accepted_line(line):
    accepted_phrases = [ 
            "not at all wrong", "not too", "somewhat", 
            "very wrong", "extremely", "you see"
    ]
        
    if ("1 to 5") in line.lower(): #this someitmes comes at the start of answers
        return False
    if ("part 1." in line.lower() or "part 2." in line.lower()): #these lines are not part of our survey answer.
        return False
        # Check for the presence of any accepted phrases
    if any(phrase in line for phrase in accepted_phrases):
        return True

        
        # Check if we have any numbered answers 1-15 (this is used for vignetttes questions.)
    if any(re.search(f'(?<!\d){n}(?!\d)', line) for n in range(1, 16)):
        return True
        
    return False

def vignettes_split_and_filter_bard(answer):

    valid_answers = []
    for line in answer.splitlines():
    # Check if the length of valid_answers has reached 5
        if len(valid_answers) > 5:
            break
        line = line.strip()
        if len(line) > 0 and "as a" not in line.lower() and "part" not in line.lower() and "sure" not in line.lower():
        # These are good answers.
            if "whether" in line.lower() or any(f"{x}" in line for x in range(0, 6)):
                valid_answers.append(line)
    return valid_answers

def vignettes_split_and_filter_gpt(answer):
    lines = answer.splitlines() 
    filtered_lines = [
        line for line in lines if line.strip() != '.' and len(line.strip()) > 0 and "as an AI language" not in line.lower() and accepted_line(line)]
    return filtered_lines


