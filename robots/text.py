import Algorithmia
import json
import re
import pysbd

def robot(content):
    fetchContentFromWikipedia(content)
    sanitizeContent(content)
    breakContentIntoSentences(content)

def fetchContentFromWikipedia(content):
    algorithmiaApiKey = getAlgorithmiaApiKey()
    algorithmiaAuthenticated = Algorithmia.client(algorithmiaApiKey)
    wikipediaAlgorithm = algorithmiaAuthenticated.algo("web/WikipediaParser/0.1.2")
    wikipediaResponde = wikipediaAlgorithm.pipe(content["searchTerm"])
    wikipediaContent = wikipediaResponde.result

    content["sourceContentOriginal"] = wikipediaContent["content"]

def sanitizeContent(content):
    def removeBlankLinesAndMarkdown(text):
        allText = text.split("\n")
        whitoutBlankLinesAndMarkdown = list(filter(lambda line: len(line)>0 and not(line.startswith("=")), allText))
        
        return ' '.join(whitoutBlankLinesAndMarkdown)

    def removeDatesInParenteses(text):
        text = re.sub(r'\([^()]*\)', '', text)
        text = re.sub(r'  ', '', text)

        return text

    whitoutBlankLinesAndMarkdown = removeBlankLinesAndMarkdown(content["sourceContentOriginal"])
    whitouDatesInParenteses = removeDatesInParenteses(whitoutBlankLinesAndMarkdown)

    content["sourceContentSanitized"] = whitouDatesInParenteses

def breakContentIntoSentences(content):
    seg = pysbd.Segmenter(language="en", clean=False)
    sentences = seg.segment(content["sourceContentSanitized"])
    
    content["sentences"] = []

    for sentence in sentences:
        content["sentences"].append(
            {
                "text": sentence,
                "keywords": [],
                "images": []
            }
        )
    
    print(content["sentences"])

def getAlgorithmiaApiKey():
    with open("credentials/algorithmia.json") as f:
        data = json.load(f)
    
    return data['apikey']

