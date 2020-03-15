from . import helperInput
from . import state

def robot():

    content = {
        "maximumSentences": 7
    }

    content['searchTerm'] = askAndReturnSearchTerm()
    content['prefix'] = askAndReturnPrefix()
    
    state.save(content)
    
def askAndReturnSearchTerm():
    term = input("Type a Wikipedia search term: ")

    return term

def askAndReturnPrefix():
    prefixes = ["Who is", "What is", 'The history of']
    selectedPrefixIndex = helperInput.keyInSelect(prefixes)
    selectedPrefixText = prefixes[selectedPrefixIndex]

    return selectedPrefixText