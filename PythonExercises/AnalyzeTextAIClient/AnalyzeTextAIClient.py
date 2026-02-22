import json
from pathlib import Path
from dotenv import load_dotenv
import os

# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# pip install azure-ai-textanalytics==5.3.0
# pip install python-dotenv

def load_settings():
    # 1. Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # 2. Define the path to your json file relative to the script
    config_path = script_dir / "config.json"

    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find config.json at {config_path}")
        return {}

# Execution main method
def main():
    try:        
        print(f"App started.")
        
        # Load settings
        config = load_settings()
        print(f"Config loaded from: {Path(__file__).parent}")
        api_endpoint = config.get('api_endpoint')
        api_key = config.get('api_key')
        print(f"api_endpoint: {api_endpoint}")
        print(f"api_key: {api_key}")
        
        # Create client using endpoint and key
        credential = AzureKeyCredential(api_key)
        ai_client = TextAnalyticsClient(endpoint=api_endpoint, credential=credential)
        
        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguage = ai_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))
        
            # Get sentiment
            sentimentAnalysis = ai_client.analyze_sentiment(documents=[text])[0]
            print("\nSentiment: {}".format(sentimentAnalysis.sentiment))

            # Get key phrases
            phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))

            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))

            # Get linked entities
            entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nLinks")
                for linked_entity in entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))

        print(f"App finished.")
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()