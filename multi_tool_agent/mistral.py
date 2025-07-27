import litellm 
# litellm._turn_on_debug() # turn on debug to see the request
from litellm import completion

# response = completion(
#     # model="ollama/mistral-7b-instruct",
#     model="ollama/llama2",
#     prompt="Hello, world!",
#     api_base="http://10.0.0.245:11434",
#     stream=True
# )
# response = completion(
#     model="ollama/llama2", 
#     messages=[{ "content": "respond in 20 words. who are you?","role": "user"}], 
#     api_base="http://10.0.0.245:11434"
# )

response = completion(
    model="ollama/mistral", 
    messages=[{ "content": "respond in 20 words. who are you?","role": "user"}], 
    api_base="http://10.0.0.245:11434"
)

print(response)
