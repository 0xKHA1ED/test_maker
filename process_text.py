def clean_spaces(text):
    while text[0] == ' ':
        text = text[1:]
    
    while text[-1] == ' ':
        text = text[:-1]
    
    return text

def process_text(text):
    delimiters = [')', '-', '_']
    choice_letters = ['a', 'b', 'c', 'd']
    
    lines = text.replace('\r', '').split('\n')
    
    question = clean_spaces(lines[0])
    answers = lines[1]

    delimiter = ''
    for char in delimiters:
        if char in answers:
            delimiter = char
            break
    
    choices = []
    for i in range(len(choice_letters)):
        if i != len(choice_letters) - 1:
            current_choice = answers[answers.index(choice_letters[i] + delimiter)+2:answers.index(choice_letters[i+1] + delimiter)]
            choices.append(clean_spaces(current_choice))
        else:
            current_choice = answers[answers.index(choice_letters[i] + delimiter)+2:]
            choices.append(clean_spaces(current_choice))
    
    print([question, choices])
    return question, choices

