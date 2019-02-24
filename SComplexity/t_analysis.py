    # Scientific readability project
# authors ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu
# Patrick McGurrin
# patrick.mcgurrin@gmail.com


import base64
import copy
import math
import os
import pickle
import re
import sys
import time
import collections

import matplotlib  # Its not that this file is responsible for doing plotting, but it calls many modules that are, such that it needs to pre-empt
matplotlib.use('Agg')

import numpy as np
import pandas as pd
from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import cmudict, stopwords, subjectivity
from nltk.probability import FreqDist
from nltk.sentiment import SentimentAnalyzer
from nltk.tag.perceptron import PerceptronTagger
import nltk
# english_check
from SComplexity.utils import (black_string, clue_links, clue_words,
                               comp_ratio, publication_check)
from tabulate import tabulate
from textblob import TextBlob
from textstat.textstat import textstat

# setting of an appropriate backend not an X11 one.



#text analysis imports

def isPassive(sentence):
    # https://github.com/flycrane01/nltk-passive-voice-detector-for-English/blob/master/Passive-voice.py
    beforms = ['am', 'is', 'are', 'been', 'was', 'were', 'be', 'being']               # all forms of "be"
    aux = ['do', 'did', 'does', 'have', 'has', 'had']                                  # NLTK tags "do" and "have" as verbs, which can be misleading in the following section.
    words = nltk.word_tokenize(sentence)
    tokens = nltk.pos_tag(words)
    tags = [i[1] for i in tokens]
    if tags.count('VBN') == 0:                                                            # no PP, no passive voice.
        return False
    elif tags.count('VBN') == 1 and 'been' in words:                                    # one PP "been", still no passive voice.
        return False
    else:
        pos = [i for i in range(len(tags)) if tags[i] == 'VBN' and words[i] != 'been']  # gather all the PPs that are not "been".
        for end in pos:
            chunk = tags[:end]
            start = 0
            for i in range(len(chunk), 0, -1):
                last = chunk.pop()
                if last == 'NN' or last == 'PRP':
                    start = i                                                             # get the chunk between PP and the previous NN or PRP (which in most cases are subjects)
                    break
            sentchunk = words[start:end]
            tagschunk = tags[start:end]
            verbspos = [i for i in range(len(tagschunk)) if tagschunk[i].startswith('V')] # get all the verbs in between
            if verbspos != []:                                                            # if there are no verbs in between, it's not passive
                for i in verbspos:
                    if sentchunk[i].lower() not in beforms and sentchunk[i].lower() not in aux:  # check if they are all forms of "be" or auxiliaries such as "do" or "have".
                        break
                else:
                    return True
    return False

tagger = PerceptronTagger(load=False)

def unigram(tokens):
    model = collections.defaultdict(lambda: 0.01)
    tokens = [ term for t in tokens for term in t ]
    for f in tokens:
        try:
            model[f] += 1
        except KeyError:
            model[f] = 1
            continue
    for word in model:
        model[word] = model[word]/float(sum(model.values()))
    return model

def perplexity(testset, model):
    # https://stackoverflow.com/questions/33266956/nltk-package-to-estimate-the-unigram-perplexity
    perplexity = 1
    N = 0
    for word in testset:
        N += 1
        perplexity = perplexity + (1.0/model[word])
        print(perplexity)
        #import pdb; pdb.set_trace()
    #try:
    #    perplexity = pow(perplexity, 1.0/float(N))
    #except:
    #    perplexity = 0.0
    return perplexity



DEBUG = False
#from numba import jit

# word limit smaller than 1000 gets product/merchandise sites.
def text_proc(corpus, urlDat = {}, WORD_LIM = 100):

    #remove unreadable characters
    if type(corpus) is str and str('privacy policy') not in corpus:
        corpus = corpus.replace("-", " ") #remove characters that nltk can't read
        textNum = re.findall(r'\d', corpus) #locate numbers that nltk cannot see to analyze
        tokens = word_tokenize(corpus)

        stop_words = stopwords.words('english')
        #We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.

        tokens = [ word for word in tokens if not word in stop_words]
        tokens = [ w.lower() for w in tokens ] #make everything lower case

        # the kind of change that might break everything
        urlDat['wcount'] = textstat.lexicon_count(str(tokens))
        word_lim = bool(urlDat['wcount']  > WORD_LIM)

        ## Remove the search term from the tokens somehow.
        urlDat['tokens'] = tokens

        if 'big_model' in urlDat.keys():
            urlDat['perplexity'] = perplexity(corpus, urlDat['big_model'])
        else:
            urlDat['perplexity'] = None
        # Word limits can be used to filter out product merchandise websites, which otherwise dominate scraped results.
        # Search engine business model is revenue orientated, so most links will be for merchandise.

        urlDat['publication'] = publication_check(str(tokens))[1]
        urlDat['clue_words'] = clue_words(str(tokens))[1]
        if str('link') in urlDat.keys():
            urlDat['clue_links'] = clue_links(urlDat['link'])[1]

            temp = len(urlDat['clue_words'])+len(urlDat['publication'])+len(urlDat['clue_links'])
            if temp  > 10 and str('wiki') not in urlDat['link']:
                urlDat['science'] = True
            else:
                urlDat['science'] = False
            if str('wiki') in urlDat['link']:
                urlDat['wiki'] = True
            else:
                urlDat['wiki'] = False
        # The post modern essay generator is so obfuscated, that ENGLISH classification fails, and this criteria needs to be relaxed.
        not_empty = bool(len(tokens) != 0)

        if not_empty and word_lim: #  and server_error:

            tokens = [ w.lower() for w in tokens if w.isalpha() ]
            #fdist = FreqDist(tokens) #frequency distribution of words only
            # The larger the ratio of unqiue words to repeated words the more colourful the language.
            lexicon = textstat.lexicon_count(corpus, True)
            urlDat['uniqueness'] = len(set(tokens))/float(len(tokens))
            # It's harder to have a good unique ratio in a long document, as 'and', 'the' and 'a', will dominate.
            # big deltas mean redudancy/sparse information/information/density


            urlDat['info_density'] =  comp_ratio(corpus)

            #Sentiment and Subjectivity analysis
            testimonial = TextBlob(corpus)
            urlDat['sp'] = testimonial.sentiment.polarity
            urlDat['ss'] = testimonial.sentiment.subjectivity
            urlDat['sp_norm'] = np.abs(testimonial.sentiment.polarity)
            urlDat['ss_norm'] = np.abs(testimonial.sentiment.subjectivity)
            urlDat['gf'] = textstat.gunning_fog(corpus)

            # explanation of metrics
            # https://github.com/shivam5992/textstat

            urlDat['standard'] = textstat.text_standard(corpus, float_output=True)
            #urlDat['standard_'] = copy.copy(urlDat['standard'] )
            # special sauce
            # Good writing should be readable, objective, concise.
            # The writing should be articulate/expressive enough not to have to repeat phrases,
            # thereby seeming redundant. Articulate expressive writing then employs
            # many unique words, and does not yield high compression savings.
            # Good writing should not be obfucstated either. The reading level is a check for obfucstation.
            # The resulting metric is a balance of concision, low obfucstation, expression.

            wc = float(1.0/urlDat['wcount'])
            # compressed/uncompressed. Smaller is better.
            # as it means writing was low entropy, redundant, and easily compressible.
            urlDat['scaled'] = wc * urlDat['standard']
            urlDat['conciseness'] = urlDat['wcount']*(urlDat['uniqueness']) + \
            urlDat['wcount']*(urlDat['info_density'])
            if urlDat['perplexity'] is not None:
                penalty = (urlDat['standard'] + urlDat['conciseness']+\
                urlDat['scaled'] + urlDat['perplexity'])/4.0
            else:
                penalty = (urlDat['standard'] + urlDat['conciseness']+urlDat['scaled'] )/3.0

            #computes perplexity of the unigram model on a testset

            #urlDat['standard'] = textstat.text_standard(corpus, float_output=True)

            urlDat['penalty'] = penalty

        return urlDat


def process_dics(urlDats):
    dfs = []
    for urlDat in urlDats:
        # pandas Data frames are best data container for maths/stats, but steep learning curve.
        # Other exclusion criteria. Exclude reading levels above grade 100,
        # as this is most likely a problem with the metric algorithm, and or rubbish data in.
        # TODO: speed everything up, by performing exclusion criteri above not here.
        if len(dfs) == 0:
            dfs = pd.DataFrame(pd.Series(urlDat)).T
        dfs = pd.concat([ dfs, pd.DataFrame(pd.Series(urlDat)).T ])
    return dfs
