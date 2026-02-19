from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# pip install azure-identity
# pip install azure.ai.projects 
# pip install openai

# Used az-login command to sign in before running the code.


print("App started.")

try:

    # Get project client
    project_endpoint = "https://exercise-foundry-resource.services.ai.azure.com/api/projects/exercise-foundry-project"
    deployment_name = "gpt-4o"
    project_client = AIProjectClient(            
            credential=DefaultAzureCredential(),
            endpoint=project_endpoint,
        )
    
    # Get a chat client
    chat_client = project_client.get_openai_client(api_version="2024-10-21")

        # Get a chat completion based on a user-provided prompt
    user_prompt = "How many people were killed in world war 2?" # input("Enter a question:")
    
    response = chat_client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_prompt}
        ]
    )
    print(response.choices[0].message.content)

    ## List all connections in the project
    connections = project_client.connections
    print("List all connections:")
    for connection in connections.list():
        print(f"{connection.name} ({connection.type})")

except Exception as ex:
    print(ex)

print("App finished.")
