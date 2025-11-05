from utils.gemini import model

history = [
    {
        "role" : "user",
        "parts" : [
            {
                "text" : "You are a House Assistant. You are made for the task of keeping a family healthy in respect of their food choices"
                         "while trying to maintain their happiness at the same time by considering their likes and dislikes."
                         "The health of the family should be given more priority."
                         "I have already created a proper system with the help of which a family member can ask food recommendation"
                         "based on himself or based on any other family member."
                         "WHAT YOU WILL GET AS INPUT ? : You will be provided some data retrieved from the database where food details are stored"
                         "and a user prompt."
                         "WHAT YOU WILL RETURN AS OUTPUT ? : You must return a proper, brainstormed response after analysing all the inputs and their linkages."
                         "Your output must not involve any metadata since you are directly interacting with the user. Provide the output in markdown format."
            }
        ]
    }
]

chat = model.start_chat(history=history)

def ai_analysis(user_request, data):
    global history

    prompt = f'''Data from database : {data},
                User query : {user_request}'''
    
    response = chat.send_message(prompt,stream=True)
    response.resolve() # Ensure the response is fully generated

    history.append({"role" : "user","parts":[{"text":prompt}]})
    history.append({"role" : "model","parts":[{"text":response.text}]})

    return response.text