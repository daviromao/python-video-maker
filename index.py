import helperInput

def start():
    content = {}
    content['seachTerm'] = askAndReturnSearchTerm()
    content['prefix'] = askAndReturnPrefix()

    print(content)

def askAndReturnSearchTerm():
    term = input("Type a Wikipedia search term: ")

    return term

def askAndReturnPrefix():
    prefixes = ["Who is", "What is", 'Ther history of']
    selectedPrefixIndex = helperInput.keyInSelect(prefixes)
    selectedPrefixText = prefixes[selectedPrefixIndex]

    return selectedPrefixText





if __name__ == "__main__":
    start()