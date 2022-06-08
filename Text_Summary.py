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

# making a summarizer function and taking a variable named rawdocs
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS) # saving the stopwords in a list
    # loading the en_core_web_sm module
    nlp = spacy.load('en_core_web_sm')
    # saving it in doc variable
    doc = nlp(rawdocs)
    """
    for token in doc = getting every word, punctuation from every doc and then saving it as token into token.text
    and then saving it in a list.
    """
    tokens = [token.text for token in doc]

    """
    making a dictionary know as word_freq, it would save corresponding frequency of every word
    """
    word_freq = {}

    for word in doc:
        # only taking those words which are not presented in stopwords and punctuations 
        # means eliminating stopwords and punctuations words and taking the rest of the words
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            # converting word in to text and checking is it in word_freq dictionary or not
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # getting the maximum word frequency of a word
    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        # getting normalize freq of every word..while deviding the word_freq by max-freq
        # normalize_freq is the unit freq
        word_freq[word] = word_freq[word] / max_freq

    # picking every sentence and saving is as tokens in sent_tokens list
    sent_tokens = [sent for sent in doc.sents]

    # dictionary for scores of each  sentence tokens
    sent_scores = {}
    # picking every sentence in sent_token list
    for sent in sent_tokens:
        # then getting every word from every sentence
        for word in sent:
            # checking in word_freq dictionary that the word is present or not
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                    # sent is beign stored in sent_scores and the corresponding frequency(word_freq)of sentence is beign saved
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3) # taking 30 percent(0.3) of sent_tokens and then converting into integer and saving 
    # it to select_len
    
    # geeting highest frequency of sentence and then it would store into summary
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    # print(summary)

    # converting the listed summary into word.text and joining space with every word 
    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)


    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))




