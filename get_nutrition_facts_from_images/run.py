from openai import OpenAI  # openai>=1.2.0
import requests

docai_api_key = "hack-with-upstage-docai-0420"
solar_api_key = "hack-with-upstage-solar-0420"

client = OpenAI(
    api_key=solar_api_key,
    base_url="https://api.upstage.ai/v1/solar"
)

def analyze_layout(filename):
    url = "https://api.upstage.ai/v1/document-ai/layout-analyzer"
    headers = {"Authorization": f"Bearer {docai_api_key}"}
    files = {"document": open(filename, "rb")}
    response = requests.post(url, headers=headers, files=files)
    return response.json()["html"]

def ask_solar(context, question):
    response = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=[
          {
            "role": "user",
            "content": "Answer the following question:" + question
                + "by using the following context:" + context
          }
        ]
    )
    return response.choices[0].message.content

def check_groundedness(context, question, answer):
    response = client.chat.completions.create(
        model="solar-1-mini-answer-verification",
        messages=[
            {"role": "user", "content": context},
            {"role": "assistant", "content": question + answer}
        ]
    )
    return response.choices[0].message.content == "grounded"

context = analyze_layout("image_001.jpeg")

protein_question = "How much protein is there?"
for _ in range(3):
    protein_answer = ask_solar(context, protein_question)
    grounded = check_groundedness(context, protein_question, protein_answer)
    if grounded:
        print(protein_answer)
        break

servings_per_container_question = "How many servings per container are there?"
for _ in range(3):
    servings_per_container_answer = ask_solar(context, servings_per_container_question)
    grounded = check_groundedness(context, servings_per_container_question, servings_per_container_answer)
    if grounded:
        print(servings_per_container_answer)
        break
        
calories_question = "How many calories per serving are there?"
for _ in range(3):
    calories_answer = ask_solar(context, calories_question)
    grounded = check_groundedness(context, calories_question, calories_answer)
    if grounded:
        print(calories_answer)
        break
