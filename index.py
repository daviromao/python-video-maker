import helperInput
from robots import text

def start():
    content = {}
    content['searchTerm'] = askAndReturnSearchTerm()
    content['prefix'] = askAndReturnPrefix()

    text.robot(content)
    
def askAndReturnSearchTerm():
    term = input("Type a Wikipedia search term: ")

    return term

def askAndReturnPrefix():
    prefixes = ["Who is", "What is", 'The history of']
    selectedPrefixIndex = helperInput.keyInSelect(prefixes)
    selectedPrefixText = prefixes[selectedPrefixIndex]

    return selectedPrefixText



if __name__ == "__main__":
    start()