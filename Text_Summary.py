import spacy
from spacy.lang.en.stop_words import  STOP_WORDS
from string import punctuation
from heapq import nlargest
# import en_core_web_sm

text = """
Peaky Blinders is a British crime drama television series created by Steven Knight. Set in Birmingham, England, it follows the exploits of the Peaky Blinders crime gang in the direct aftermath of the First World War. 
The fictional gang is loosely based on a real urban youth gang of the same name who were active in the city from the 1880s to the 1910s.

It features an ensemble cast led by Cillian Murphy, starring as Tommy Shelby, Helen McCrory as Elizabeth "Polly" Gray, Paul Anderson as Arthur Shelby and Joe Cole as John Shelby, the gang's senior members. 
Tom Hardy, Sam Neill, Annabelle Wallis, Iddo Goldberg, Charlotte Riley, Paddy Considine, Adrien Brody, Aidan Gillen, Anya Taylor-Joy, Sam Claflin, James Frecheville and Stephen Graham have recurring roles. 
It premiered on 12 September 2013, telecast on BBC Two until the fourth series (with repeats on BBC Four), then moved to BBC One for the fifth and sixth series.

The fifth series premiered on BBC One on 25 August 2019 and finished on 22 September 2019. Netflix, under a deal with Weinstein Company and Endemol, acquired the rights to release the show in the United States and aro0und the world. 
In January 2021, it was announced that series six would be the last, followed by a spinoff film. Series six was broadcast from 27 February 2022 to 3 April 2022.

"""

# stopwords = list(STOP_WORDS)
# # print(stopwords)
#
# nlp = spacy.load('en_core_web_sm')
# doc = nlp(text)
# print(doc)

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc]

    word_freq = {}

    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                    # sent is beign stored in sent_scores and the corresponding frequency is beign saved
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)

    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)


    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))




