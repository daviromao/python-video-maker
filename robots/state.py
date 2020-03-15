import json

def save(content):
    with open('./content/content.json', 'w') as f:
        json.dump(content, f, indent=4)

def load():
    with open('./content/content.json', 'r') as f:
        content = json.load(f)
    
    return content
