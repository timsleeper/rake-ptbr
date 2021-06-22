from fastapi import FastAPI
from pydantic import BaseModel
from rake import *
import json

class Message(BaseModel):
    num_terms: int
    message: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Oi, estou funcionando!"}

@app.post("/rake/")
async def run_rake(message: Message):

    payload = json.loads(message.json())
    num_terms = int(payload['num_terms'])

    sentenceList = split_sentences(payload['message'])
    stoppath = "stopwords_pt.txt"
    stopwordpattern = build_stop_word_regex(stoppath)

    phraseList = generate_candidate_keywords(sentenceList, stopwordpattern, load_stop_words(stoppath))

    wordscores = calculate_word_scores(phraseList)

    keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)

    sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)

    totalKeywords = len(sortedKeywords)

    rake = Rake("stopwords_pt.txt")
    keywords = rake.run(payload['message'])
    print(keywords)
    words =[]
    if len(keywords) >= num_terms:
        for i in range(num_terms):
            a, b = keywords[i]
            words.append(a)
    else:
        for i in range(len(keywords)):
            a, b = keywords[i]
            words.append(a)
    return {"keywords": words}
