import openai
import logging as log
import os

key = os.environ['OPENAI_API_KEY']
openai.api_key = key
path = "./source/prompt.txt"

class PreProcessor:
    def __init__(self, prompt_path: str):
        self.prompt_path = prompt_path
        self.prompt = ""
        self.messages: list[dict[str, str]] = []
        # open prompt.txt, read the contents, and append it to prompt
        with open(path, "r") as f:
            prompt += f.read()
        log.info(f"Read prompt: \n{prompt}")
    
    def append_prompt(prompt: str ,message: str)->str:
        prompt += message
        return prompt
    
    def prepare_data(self)->str:
        # TODO: Implement data preparation
        log.info("Preparing messages")
        self.final_prompt = self.prompt

        for msg in self.messages:
            if msg["sender"] == "prompt":
                # TODO: generate a prompt for the following message
                final_prompt += "[{prompt}]\n".format(prompt=msg["text"])
            final_prompt += msg["sender"] + ": " + msg["text"] + "\n"

        self.final_prompt += "Chris: "
        print(f"Final Prompt: \n{final_prompt}")
        return self.final_prompt
    
    def askAI(self, stream: bool)->dict[str, str]:
        try:
            if not self.final_prompt or self.final_prompt == "":
                raise Exception("Prompt is empty")
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=self.final_prompt,
                temperature=0.75,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.5,
                stream=stream
            )
            log.info("Received response")

            if stream:
                for chunk in response:
                    resp: str = chunk.choices[0].text.strip()
                    yield {
                        "sender": 'Chris',
                        "text": resp
                    }
            else:
                answers = response.choices[0].text.strip()
                log.info("Answer: \n" + answers)
                return {
                    "sender": 'Chris',
                    "text": answers
                }
            
        except Exception as e:
            log.error("Error: " + str(e))
            return {
                "sender": 'System',
                "text": "Error: " + str(e)
            }

        
 

def askAIStream(message: str):
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

def ping():
    return askAI("你喜欢我吗?")

def ping_stream():
    return askAIStream("Tell me about the history of the United States of America")