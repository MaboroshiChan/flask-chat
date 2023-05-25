import openai
import logging as log
import os

key = os.environ['OPENAI_API_KEY']
openai.api_key = key

def prepare_data(message: list[dict[str, str]])->str:
    # TODO: Implement data preparation
    log.info("Preparing messages")
    result = ""
    for msg in message:
        result += msg["sender"] + ": " + msg["text"] + "\n"
    print(f"Result: \n{result}")
    return result

def askAI(message: str)->dict[str, str]:
    prompt = ""
    # open prompt.txt, read the contents, and append it to prompt
    with open("prompt.txt", "a") as f:
        f.write(prompt)
    
    log.info(f"Prompt: \n{prompt}")
    # append message to prompt
    prompt += message
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.75,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.5
    )
    log.info("Received response")
    answers = response.choices[0].text.strip().split(":")
    # get prefix of answer which ended with ：
    sender = answers[0]
    text = answers[1]
    log.info("Answer: \n" + text)
    return {
        "sender": sender,
        "text": text
    }