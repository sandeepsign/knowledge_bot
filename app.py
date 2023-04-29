import random
import os
import openai
import gradio as gr

openai.api_key  =  os.getenv('OPENAI_API_KEY') # 'sk-xxx'

base_context = [ {'role':'system', 'content':"""
You are BeansBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]  # accumulate messages

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    print('making OpenAI call..')
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def state2context(chat_state):
    context = base_context.copy()
    if not chat_state:
        return context
    for prompt,response in chat_state:
        context.append({'role':'user', 'content':f"{prompt}"})
        context.append({'role':'assistant', 'content':f"{response}"})
    return context 

def context2state(context):
    chat_state = []
    i = 0
    while i <len(context):
        if context[i]['role']=='system':
            i+=1
            continue
        chat_state.append((context[i]['content'],context[i+1]['content']))
        i+=2
    return chat_state 

def chat(prompt, chat_state):
    prompt = prompt.lower()
    context = state2context(chat_state) # [(prompt,response)] => OpenAI Chat Context with Roles: [{'role':'system','content':""" kbody """},{'role':'user','content':'prompt'}]
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role':'assistant', 'content':f"{response}"})
    chat_response = context2state(context)
    return chat_response, chat_response

# def chat(message, history):
#     history = history or []
#     message = message.lower()
#     if message.startswith("how many"):
#         response = random.randint(1,10)
#     elif message.startswith("how"):
#         response = random.choice(["Great","Good","Ok","Bad"])
#     elif message.startswith("where"):
#         response = random.choice(["here","there","Somewhere"])
#     else:
#         response = "I don't know"
#     history.append((message,response))
#     return history, history

beansbot = gr.Chatbot().style(colormap=("green","pink"))

demo = gr.Interface(chat, 
                    ["text", "state"],
                    [beansbot, "state"],
                    allow_flagging="never")

demo.launch()
