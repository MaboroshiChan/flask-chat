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

def read_prompt(path)->str:
    prompt = ""
    # open prompt.txt, read the contents, and append it to prompt
    with open(path, "r") as f:
        prompt += f.read()
    
    log.info(f"Read prompt: \n{prompt}")
    return prompt

def append_prompt(prompt: str ,message: str)->str:
    prompt += message
    return prompt


def askAI(message: str)->dict[str, str]:
    prompt = read_prompt("./source/prompt.txt")
    prompt = append_prompt(prompt, message)
    try:
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

    except Exception as e:
        log.error("Error: " + str(e))
        return {
            "sender": 'system',
            "text": "Error: " + str(e)
        }

    log.info("Answer: \n" + answers)
    return {
        "sender": 'bob',
        "text": answers
    }

"""
    This function is used to stream the response from GPT-3
    It is not used in the current version of the app
"""
def askAIStream(message: str):
    prompt = read_prompt("./source/prompt.txt")
    prompt = append_prompt(prompt, message)

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.75,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.5,
            stream=True
        )
        log.info("Received response")
    
        for chunk in response:
            resp: str = chunk.choices[0].text.strip()
            yield {
                "sender": 'bob',
                "text": resp
            }

    except Exception as e:
        log.error("Error: " + str(e))
        yield {
            "sender": 'system',
            "text": "Error: " + str(e)
        }

    