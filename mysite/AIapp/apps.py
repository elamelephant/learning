from openai import OpenAI
from .vault import get_secret

client = OpenAI(api_key=get_secret("AIapp-key"))
########
# INIT
########

system_prompt = """You are an expert business consultant conducting a structured interview 
with an employee to uncover how their company should improve. 
Ask 5-10 dynamic, open-ended short questions ONE AT A TIME. 
Tailor each follow-up question based on their previous answers. 
Focus on: processes, culture, leadership, customer satisfaction, and bottlenecks.
When you have enough insight (after 5-10 questions), summarize the key improvement areas."""

employee_prompt = """You are an employee at a mid-sized logistics company with ~200 people. 
You have genuine frustrations: outdated software, poor cross-team communication, 
unclear KPIs, and a micromanaging middle management layer. 
Answer interview questions honestly and naturally, as a real employee would. Answer in one sentence"""

data = {"No_info":"No_info"}
summary = ""
NO_OF_CONVERSATION = 10

def simulate_conversation():
    interviewer_history = []
    employee_history = []
    
    # Interviewer opens
    interviewer_history.append({"role": "user", "content": "Start the interview."})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}] + interviewer_history
    )
    interviewer_msg = response.choices[0].message.content
    interviewer_history.append({"role": "assistant", "content": interviewer_msg})
    
    for turn in range(NO_OF_CONVERSATION):  # 10 Q&A pairs
        # Employee responds
        employee_history.append({"role": "user", "content": interviewer_msg})
        emp_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": employee_prompt}] + employee_history
        )
        employee_msg = emp_response.choices[0].message.content
        employee_history.append({"role": "assistant", "content": employee_msg})
        
        # Interviewer follows up
        interviewer_history.append({"role": "user", "content": employee_msg})
        int_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}] + interviewer_history
        )
        interviewer_msg = int_response.choices[0].message.content
        interviewer_history.append({"role": "assistant", "content": interviewer_msg})
    
    return interviewer_history

print(f"Simulating conversation ...")
convo = []
convo = simulate_conversation()
if convo != []:
    data.clear()
    for i in convo:
        if i["role"] == "user":
            user = i["content"]
        elif i["role"] == "assistant":
            data.update({user:i["content"]})
#print(data)

summary_prompt = "I want only summary in two line about most important things to do in my company based on the interview chats"

response = client.responses.create(
    model="gpt-4.1-mini",
    input=summary_prompt+" "+str(data)
)
#print("summary: ",response.output[0].content[0].text)
summary = response.output[0].content[0].text


