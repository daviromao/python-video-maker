import Algorithmia
import json
import re
import pysbd

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def robot(content):
    fetchContentFromWikipedia(content)
    sanitizeContent(content)
    breakContentIntoSentences(content)
    limitMaximumSentences(content)
    fetchKeywordsOfAllSentences(content)

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

def limitMaximumSentences(content):
    maximumSentences = content["maximumSentences"]
    content["sentences"] = content["sentences"][0:maximumSentences]

def getAlgorithmiaApiKey():
    with open("credentials/algorithmia.json") as f:
        data = json.load(f)
    
    return data['apikey']

def getWatsonData():
    with open("credentials/watson-nlu.json") as f:
        data = json.load(f)

    return data

def acessAndReturnNLU():
    data = getWatsonData()

    authenticator = IAMAuthenticator(data["apikey"])

    nlu = NaturalLanguageUnderstandingV1(version='2018-03-16',
                                         authenticator=authenticator)

    nlu.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

    return nlu

def fetchWatsonAndReturnKeywords(sentence):
    global nlu

    response = nlu.analyze(
        text=sentence,
        features=Features(keywords=KeywordsOptions())
    ).get_result()

    keywords = list(map(lambda keywordData: keywordData["text"], response["keywords"]))

    return keywords

def fetchKeywordsOfAllSentences(content):
    for sentence in content["sentences"]:
        sentence["keywords"] = fetchWatsonAndReturnKeywords(sentence["text"])

nlu = acessAndReturnNLU()