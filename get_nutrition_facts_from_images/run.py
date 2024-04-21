from openai import OpenAI  # openai>=1.2.0
import requests
import json
import cv2

docai_api_key = "hack-with-upstage-docai-0420"
solar_api_key = "hack-with-upstage-solar-0420"
data = {}

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

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        print('space')
        # SPACE pressed
        img_name = "nutrition_label_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        context = analyze_layout(img_name)

        protein_question = "How much protein is there?"
        for _ in range(3):
            protein_answer = ask_solar(context, protein_question)
            grounded = check_groundedness(context, protein_question, protein_answer)
            if grounded:
                data['protein'] = protein_answer
                break

        servings_per_container_question = "How many servings per container are there?"
        for _ in range(3):
            servings_per_container_answer = ask_solar(context, servings_per_container_question)
            grounded = check_groundedness(context, servings_per_container_question, servings_per_container_answer)
            if grounded:
                data['servings per container'] = servings_per_container_answer
                break

        calories_question = "How many calories per serving are there?"
        for _ in range(3):
            calories_answer = ask_solar(context, calories_question)
            grounded = check_groundedness(context, calories_question, calories_answer)
            if grounded:
                data['calories'] = calories_answer
                break

        prices_question = "What is the price?"
        for _ in range(3):
            prices_answer = ask_solar(context, prices_question)
            grounded = check_groundedness(context, prices_question, prices_answer)
            if grounded:
                data['price'] = prices_answer
                break

        name_question = "What is the name?"
        for _ in range(3):
            name_answer = ask_solar(context, name_question)
            grounded = check_groundedness(context, name_question, name_answer)
            if grounded:
                data['name'] = name_answer
                break

        json_data = json.dumps(data, indent=4)
        f = open("output.json", "a")
        f.write(json_data)
        f.close()
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
