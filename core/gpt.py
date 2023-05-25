import openai
import logging as log
import os

key = os.environ['OPENAI_API_KEY']
openai.api_key = key

def prepare_data(message: dict[str, str])->str:
    # TODO: Implement data preparation
    log.info("Preparing messages")
    result = ""
    for key, value in message.items():
        log.info(f"Key: {key}, Value: {value}")
        result += f"{key}: {value}\n\n"
    return result

def askAI(message)->str:
    prompt = f"{message}\n"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.75,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.5,
        stop=["\n"]
    )
    log.info("Received response")
    answer = response.choices[0].text.strip()
    log.info("Answer: \n" + answer)
    return answer