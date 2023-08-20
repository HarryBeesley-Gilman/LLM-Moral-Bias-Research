def extract_number(text): #this code extracts numerical response from ChatGPT output


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
        if len(line) > 0 and "as a" not in line.lower() and "part" not in line.lower() and "sure" not in line.lower():
            # Check if the line contains a number between 1 and 32 followed by a period
            if any(f"{y}." in line for y in range(1, 33)) or "whether" in line.lower() or any(f"{x}" in line for x in range(0, 6)):
                valid_answers.append(line)
    return valid_answers

def split_and_filter_gpt(answer):
    lines = answer.splitlines()
    filtered_lines = [line for line in lines if line.strip() != '.' and len(line.strip()) > 0 and "part" not in line.lower() and "as a" not in line.lower() and "therefore" not in line.lower()]
    return filtered_lines