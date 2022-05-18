from codecs import ignore_errors
from doctest import IGNORE_EXCEPTION_DETAIL
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import warnings
warnings.filterwarnings("ignore")

########--------STOPWORDS---------########
f = open("StopWords_Generic.txt", "r")         
data = f.read()
stop_words = data.replace('\n', ' ').split(".")
f.close()

#######---------TOKENIZED WORDS--------#######
def tokens(text):
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(text)
    return word_tokens

######---------CLEANED WORDS--------#######
def cleaning(text):
    word_tokens = tokens(text)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    lem = WordNetLemmatizer()
    final = []
    for w in filtered_sentence:
        final.append(lem.lemmatize(w))
    return final

#####--------POSITIVE AND NEGATIVE WORDS ARRAY-------#####
mlist = pd.read_csv('Loughran-McDonald_MasterDictionary_1993-2021.csv')
pos_words = np.array(mlist['Word'][mlist.Positive > 0])
neg_words = np.array(mlist['Word'][mlist.Negative > 0])

######-------POS, NEG, POLARARITY AND SUBJECTIVITY SCORES-------######
def scores(text):
    words = cleaning(text)
    pos_score = len([w for w in words if not w.upper() in pos_words])
    neg_score = len([w for w in words if not w.upper() in neg_words])
    polarity = (pos_score - neg_score)/ ((pos_score + neg_score) + 0.000001)
    subjectivity = (pos_score + neg_score)/ ((len(words)) + 0.000001)
    return pos_score, neg_score, polarity, subjectivity

#####-------SENTENCE LENGTH COUNT-----######
def sentWordCount(text):
    split_str = re.split(r'[.?!]', text)
    split_str = split_str[0:-1]
    sent_count = len(split_str)
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(text)
    word_count = len(word_tokens)
    avg_sent_lgth = word_count/sent_count
    return avg_sent_lgth

#######-------COMPLEX WORD COUNT------########
def cmplxCount(text):
    word_tokens = tokens(text)
    vowel = set("aeiou")
    cmplxWords = []
    for w in word_tokens:
        if w.endswith('es') or w.endswith('ed'):
            continue
        count = 0
        for alphabet in w:
            if alphabet in vowel:
                count = count + 1     
        if count > 2:
            cmplxWords.append(w)
    return len(cmplxWords)

######-------PERSONAL PRONOUNS------######
def personalPronouns(text):
    pronounsReg = pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    personal_pronouns = pronounsReg.findall(text)
    return len(personal_pronouns)

#######--------SYLLABE PER WORD-------#########
def syllabelPerWord(text, word_count):
    count = 0
    word_token = tokens(text)
    vowel = set("aeiou")
    for w in word_token:
        if w.endswith('ed') or w.endswith('es'):
            continue
        for alphabet in w:
            if alphabet in vowel:
                count = count + 1  
    return count/word_count

#####-------AVERAGE WORD LENGTH------########
def avgWordLgth(text):
    words = text.split()
    average = sum(len(word) for word in words) / len(words)
    return average

inp = pd.read_excel('Input.xlsx')
cols=['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
output = pd.DataFrame(columns=cols)

for i in range(1, 171):
    fname = 'Scraped Data/'+str(i)+'.txt'
    file1 = open(fname, 'r')
    content = file1.readlines()
    title = content[0][0:-1]
    body = content[1]
    file1.close()
    text = title+' '+body
    url_id = inp['URL_ID'].iloc[i-1]
    url = inp['URL'].iloc[i-1]
    pos_score, neg_score, polarity, subjectivity = scores(text)
    avg_sent_length = sentWordCount(text)
    pcent_cmplx_words = cmplxCount(text)/len(tokens(text))*100
    fog_index = (sentWordCount(text)+pcent_cmplx_words)*0.4
    word_per_sent = sentWordCount(text)
    cmplx_word_count = cmplxCount(text)
    word_count = len(cleaning(text))
    syllabel_per_word = syllabelPerWord(text, word_count)
    personal_pronouns = personalPronouns(text)
    avg_word_lgth = avgWordLgth(text)
    buffer = pd.Series([url_id, url, pos_score, neg_score, polarity, subjectivity, avg_sent_length, pcent_cmplx_words, fog_index, word_per_sent, cmplx_word_count, word_count, syllabel_per_word, personal_pronouns, avg_word_lgth], index=cols)

    output = output.append(buffer, ignore_index=True)

output.to_excel('output.xlsx')