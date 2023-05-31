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
        if msg["sender"] == "prompt":
            # TODO: generate a prompt for the following message
            result += "[{prompt}]\n".format(prompt=msg["text"])
        result += msg["sender"] + ": " + msg["text"] + "\n"
    print(f"Result: \n{result}")
    return result

def askAI(message: str)->dict[str, str]:
    prompt = ""
    # open prompt.txt, read the contents, and append it to prompt
    with open("./source/prompt.txt", "r") as f:
        prompt += f.read()
    
    log.info(f"Read prompt: \n{prompt}")
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
    answers = response.choices[0].text.strip()
    # get prefix of answer which ended with ：

    log.info("Answer: \n" + answers)
    return {
        "sender": 'bob',
        "text": answers
    }