from groq import Groq

api_file_path="../Phantom_X/API.env"

def read_api_file(file_path):
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def generate_ai_response(question: str, model_ch: int, prompt: str):

    client = Groq(api_key=read_api_file(file_path=api_file_path)["api_key"])
    models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

    completion = client.chat.completions.create(
        model=models[model_ch],
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        stream=True,
    )

    full_response = ""   

    for chunk in completion:
        token = chunk.choices[0].delta.content or ""
        # print(token, end="")      
        full_response += token    
    return full_response         