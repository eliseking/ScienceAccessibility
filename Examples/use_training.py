
import glob
import math as math
import os
import pdb
import pickle
import pprint


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from bs4 import BeautifulSoup
from mpl_toolkits.mplot3d import Axes3D
from natsort import natsorted, ns
from pylab import rcParams
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import cmudict, stopwords, subjectivity
import re
from SComplexity.analysis import Analysis
from SComplexity.t_analysis import text_proc, perplexity, unigram_zipf

#from SComplexity.get_bmark_corpus import Analysis

from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import itertools
#from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.metrics import confusion_matrix
import pylab as pl


from sklearn import preprocessing
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
#from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
import sklearn

#from neuronunit.optimisation.optimisation_management import stochastic_gradient_descent
import seaborn as sns

#import seaborn as sns; sns.set()  # for plot styling

#here you construct the unigram language model

##
# This file can be used to show, that K-Means clustering
# a type of unsupervised classifier, can predict if something is a wikipedia article
# or not pretty well.
# It's my opinion that, the classifier could probably predict mainstream science or psuedo science too,
# given enough dimensions to seperate the clustered data points over.
##
FILES = natsorted(glob.glob(str(os.getcwd())+'/../SComplexity/ART_Corpus/*/*.xml'))
def proc_xml(FILES):
    urlDats = []
    for f in FILES:
        content = open(f,'r')
        soup = BeautifulSoup(content, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        #wt = copy.copy(text)
        #organize text
        lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
        text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
        buffer = str(text)
        urlDat = {}

        urlDat = text_proc(buffer,urlDat)
        urlDat['file_name'] = f
        print(urlDat)
        urlDats.append(urlDat)
    return urlDats

#import online_app_backend
#files = online_app_backend.download_course()
#import pdb; pdb.set_trace()
try:
    with open('traingDats.p','rb') as f:
        trainingDats = pickle.load(f)

except:

    trainingDats = proc_xml(FILES)
    with open('traingDats.p','wb') as f:
        pickle.dump(trainingDats,f)



FILES = natsorted(glob.glob(str(os.getcwd())+'/results_dir/*.p'))
A = Analysis(FILES, min_word_length = 200)
web_scrape = A.cas()


not_science = [ url for url in web_scrape if url['science'] == False ]
not_science = [ t for t in not_science if 'standard' in t.keys() ]
not_science = [ t for t in not_science if t['standard'] < 300.0 ]


bag_of_words = []
bag_of_words.extend(web_scrape)
bag_of_words.extend(trainingDats)
'''
X_scaler = StandardScaler()
X0_ = X_scaler.fit_transform(X0_)
X = X_scaler.transform(X0_)
Y = X_scaler.fit_transform(Y_)
Y = X_scaler.transform(Y)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3)
sgd = SGDRegressor(penalty='l2', max_iter=1000, learning_rate='constant' , eta0=0.001  )

mlp = MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(13, 13, 13), learning_rate='constant',
       learning_rate_init=0.001, max_iter=500, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

#sgd.fit(X_train, Y_train)
mlp.fit(X_train, Y_train)
hyperplane = mlp.coef_#+sgd.intercept_

'''

#print(not_science)
sci1 = pickle.load(open('author_results.p','rb'))
sb_results = pickle.load(open('sb_results.p','rb'))

#sci1 = [ t['standard'] for t in sci1 ]
#x.extend(sci1)
sci1 = [ v for v in sci1.values() ]
sci1 = [ t for t in sci1 if 'standard' in t.keys() ]

#sb = [v for v in sb_results.values()]
#sb = [ t for t in sb_results if 'standard' in t.keys() ]

trainingDats.extend(sci1)
#strainingDats.extend(sb)

terms = [ ws['tokens'] for ws in web_scrape ]
other_terms = [ ws['tokens'] for ws in trainingDats ]
terms.extend(other_terms)
try:
    big_model = pickle.load(open('big_model.p','rb'))
except:
    big_model = unigram(terms)
    pickle.dump(big_model,open('big_model.p','wb'))
for t in not_science:
    t['perplexity'] = perplexity(t['tokens'], big_model)
for t in trainingDats:
    t['perplexity'] = perplexity(t['tokens'], big_model)


perp_sci = [ t['perplexity'] for t in trainingDats ]
perp_ns = [ t['perplexity'] for t in not_science if 'standard' in t.keys() ]

plt.clf()
plt.title('perplexity')

import pdb; pdb.set_trace()
sns.distplot( perp_sci , color="skyblue", label="science")
sns.distplot( perp_ns, color="red", label="not science")
plt.legend(loc="upper left")
plt.savefig('perplexity.png')

standard_sci = [ t['standard'] for t in trainingDats ]
standard_ns = [ t['standard'] for t in not_science if 'standard' in t.keys() ]


subjectivity_sci = [ t['ss'] for t in trainingDats ]
subjectivity_ns = [ t['ss'] for t in not_science if 'standard' in t.keys() ]


polarity_sci = [ t['sp'] for t in trainingDats ]
polarity_ns = [ t['sp'] for t in not_science if 'standard' in t.keys() ]



info_sci = [ t['info_density'] for t in trainingDats ]
info_ns = [ t['info_density'] for t in not_science if 'standard' in t.keys() ]
#y = [ t['standard'] for t in not_science ]
plt.clf()
plt.title('info density')

sns.distplot( info_sci , color="skyblue", label="science")
sns.distplot( info_ns, color="red", label="not science")
plt.legend(loc="upper left")
plt.savefig('info_distribution_sci_vs_non_sci.png')

plt.clf()
plt.title('text-stat standard, reading grade level')

sns.distplot( standard_sci , color="skyblue", label="science")
sns.distplot( standard_ns, color="red", label="not science")
plt.legend(loc="upper left")
plt.savefig('complexity_distribution_sci_vs_non_sci.png')

plt.clf()
plt.title('sentiment subjectivity')

sns.distplot( subjectivity_sci , color="skyblue", label="science")
sns.distplot( standard_ns, color="red", label="not science")
plt.legend(loc="upper left")
plt.savefig('sentiment_distribution_sci_vs_non_sci.png')



plt.clf()
plt.title('sentiment polarity')

sns.distplot( polarity_sci , color="skyblue", label="science")
sns.distplot( polarity_ns, color="red", label="not science")
plt.legend(loc="upper left")
plt.savefig('negativity_distribution_sci_vs_non_sci.png')

file_names = sorted([(t['standard'],t['file_name']) for t in trainingDats ])
worset_file = file_names[-1]
best_file = file_names[0]

mean_sci = np.mean([t['standard'] for t in trainingDats ])
max_sci = np.max([t['standard'] for t in trainingDats ])
min_sci = np.min([t['standard'] for t in trainingDats ])


with open('bcm.p','rb') as f:
    bcm = pickle.load(f)
urlDat = {}
urlDat = text_proc(bcm,urlDat)
print(urlDat)
with open('benchmarks.p','rb') as f:
    benchmarks = pickle.load(f)

print(mean_sci,max_sci,min_sci)
pdb.set_trace()


#import pdb; pdb.set_trace()
'''
references = A.get_reference_web()

A = Analysis(FILES, min_word_length = 200)
try:
    references = A.get_reference_web()
except:
    pass
#import pdb
#pdb.set_trace()
urlDats = A.cas()

print(urlDats)

scraped_new = list(filter(lambda url: str('query') in url.keys(), urlDats))

#by_query[str('science')]['urlDats'] = list(filter(lambda url: url['query'] in science_keys, scraped))
for s in scraped_new:
    print(s['query'])
#import pdb;
#pdb.set_trace()

'''
reference = A.get_reference_web()
dfr = pd.DataFrame(reference)

labels = [ w['link'] for w in reference ]
by_query['reference'] = {}
#by_query['reference']['sp'] = [ w['sp'] for w in reference ]
by_query['reference']['standard'] = [ w['standard'] for w in reference ]
by_query['reference']['info_density'] = [ w['info_density'] for w in reference ]

low_standard = np.min(by_query['reference']['standard'])
high_standard = np.max(by_query['reference']['standard'])

low_info = np.min(by_query['reference']['info_density'])
high_info = np.max(by_query['reference']['info_density'])
print(low_info,high_info)
#import pdb; pdb.set_trace()

dfs = pd.DataFrame(scraped_new)
##
#
##


dfs = dfs[~dfs['link'].isin(['https://www.youtube.com/'])]
dfs = dfs[~dfs['link'].isin(['https://www.walmart.com'])]
dfs = dfs[~dfs['link'].isin(['https://foundation.wikimedia.org/wiki/Privacy_policy'])]

#wikipedia = wikipedia[wikipedia['link']==str('https://foundation.wikimedia.org/wiki/Privacy_policy')]
wikipedia = dfs[dfs['se']==str('wikipedia')]
#wikipedia = wikipedia[~wikipedia['link'].isin(['https://foundation.wikimedia.org/wiki/Privacy_policy'])]

np.random.seed(5)


# Use all information to create clusters,
# but only interested in expressing the clusters in first 3 Dimensions.
#for row in dfs.:
#    print(row['clue_words']) #= len(row['clue_words'])

dfs.replace([np.inf, -np.inf], np.nan)
dfs = dfs.dropna()

#X = dfs[['standard','sp','ss','info_density','gf','standard','uniqueness','info_density','penalty']]
X = dfs[['standard','sp','ss']]

X = X.as_matrix()
#import pdb; pdb.set_trace()

est = KMeans(n_clusters=3)

est.fit(X)

y_kmeans = est.predict(X)
centers = est.cluster_centers_
print(centers,'centers')

fignum = 1
fig = plt.figure(fignum, figsize=(4, 3))
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_kmeans, s=50)
ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], c='black', s=200, alpha=0.5);
ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('standard')
ax.set_ylabel('subjectivity')
ax.set_zlabel('sentiment polarity')
#ax.set_title(titles[fignum - 1])
#ax.dist = 12
fignum = fignum + 1
for x,i in enumerate(zip(y_kmeans,dfs['clue_words'])):
    try:
        print(i[0],i[1],dfs['link'][x],dfs['publication'][x],dfs['clue_links'][x],dfs['sp_norm'][x],dfs['ss_norm'][x],dfs['uniqueness'][x])
    except:
        print(i)

fig.savefig('3dCluster.png')


X = dfs[['standard','sp']]
X = X.as_matrix()


est =  KMeans(n_clusters=2)
fignum = 1
titles = ['2 clusters in only 2D']
#for name, est in estimators:
fig = plt.figure(fignum, figsize=(4, 3))
#ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
est.fit(X)
#labels = est.labels_
plt.title('reading level versus sentiment subjectivity')
print(X[:, 1], X[:, 0])

plt.clf()
plt.scatter(X[:, 1], X[:, 0], edgecolor='k')
plt.savefig('reading_level_versus_sentiment_subjectivity.png')
#plt.scatter(, edgecolor='k')
#plt.savefig('reading_level_versus_sentiment_polarity.png')
X = dfs[['standard','ss','sp']]
X = X.as_matrix()
pdb.set_trace()

est =  KMeans(n_clusters=2)
fignum = 1
titles = ['2 clusters']
#for name, est in estimators:
fig = plt.figure(fignum, figsize=(4, 3))
#ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
est.fit(X)
y_kmeans = est.predict(X)
centers = est.cluster_centers_

plt.title('reading level versus sentiment subjectivity')
plt.scatter(X[:, 1], X[:, 0], edgecolor='k')
plt.savefig('reading_level_versus_sentiment_subjectivity.png')


'''
model = RandomForestClassifier()
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
accuracy_score(y_test.values, y_predict)
'''

#scraped = scraped_new
scraped_new  = [ w for w in scraped_new if str('sp') in w.keys() ]

sps = [ w['sp'] for w in scraped_new ]

fogss = [ w['gf'] for w in scraped_new ]
infos = [ w['info_density'] for w in scraped_new ]
ranks = [ w['page_rank'] for w in scraped_new ]
print(scraped_new)

by_query = {}
by_engine = {}

# These lines can be written more concisely using PD-frames.
# example:
# by_engine[str('wiki')] = list(dfs[dfs['se']==str('wikipedia')].as_matrix())
##

by_engine[str('yahoo')] = list(filter(lambda url: str('yahoo') in url['se'], urlDats))
by_engine[str('scholar')] = list(filter(lambda url: str('scholar') in url['se'], urlDats))
by_engine[str('bing')] = list(filter(lambda url: str('bing') in url['se'], urlDats))
by_engine[str('google')] = list(filter(lambda url: str('google') in url['se'], urlDats))
by_engine[str('duckduckgo')] = list(filter(lambda url: str('duckduckgo') in url['se'], urlDats))
by_engine[str('wiki')] = list(filter(lambda url: str('wiki') in url['se'], urlDats))

plt.clf()

fig, ax = plt.subplots()
plt.title('rank versus standard reading level'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('standard')
#print(by_engine['wiki']['ranks'],by_engine['wiki']['standard'])
by_engine['wiki'] = [i for i in by_engine['wiki'] if 'standard' in i.keys()]
#import pdb
#pdb.set_trace()
plt.scatter([i['page_rank'] for i in by_engine['wiki']],[i['standard'] for i in by_engine['wiki']])
#plt.plot([i for i in range(0,int(low_standard))],[low_standard for i in range(0,int(low_standard))])
#plt.plot([i for i in range(0,int(high_standard))],[high_standard for i in range(0,int(high_standard))])

#print(by_engine[key]['standard'], by_engine[key]['ranks'])
plt.savefig('standard_vs_rank'+str('wiki')+'.png')


plt.clf()
plt.title('rank versus standard reading level'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('standard')
df1 = pd.DataFrame({'reading_level':[i['standard'] for i in by_engine['wiki']],'rank':[i['page_rank'] for i in by_engine['wiki']]})
ax = sns.regplot(x="rank", y="reading_level", data=df1, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('Trend rank versus standard reading level'+str(' wikipedia'))
plt.close()

plt.clf()
fig, ax = plt.subplots()
plt.title('compression ratio versus rank'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('compression ratio')
#plt.scatter(by_engine['wiki']['ranks'],by_engine['wiki']['standard'])
plt.scatter([i['page_rank'] for i in by_engine['wiki']],[i['info_density'] for i in by_engine['wiki']])

#plt.plot([i for i in range(0,int(low_info))],[low_standard for i in range(0,int(low_info))])
#plt.plot([i for i in range(0,int(high_info))],[high_standard for i in range(0,int(high_info))])

#print(by_engine[key]['info_density'], by_engine[key]['ranks'])
plt.savefig('compression_ratio'+str('wiki')+'.png')


plt.clf()
plt.title('rank versus compression ratio'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('standard')
df1 = pd.DataFrame({'compressiion_ratio':[ i['info_density'] for i in by_engine['wiki']],'rank':[ i['page_rank'] for i in by_engine['wiki']]})
ax = sns.regplot(x="rank", y="compressiion_ratio", data=df1, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('Trend rank versus compression ratio'+str(' wikipedia'))
plt.close()


plt.clf()
fig, axes = plt.subplots()
axes.set_title('reference versus reading level')
plt.xlabel('reference source')
plt.ylabel('reading level')
'''
#plt.scatter(sps,fogss,label="scrapped data points")
axis = [i for i in range(0,len(labels))]
plt.scatter(axis,by_query['reference']['standard'])#,label=labels)
for (label, x) in zip(labels,axis):
    plt.annotate(
        label,
        xy=(x, x), xytext=(40, 40),
        textcoords='offset points', ha='left', va='top',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
        #arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.legend(loc="upper left")
fig.tight_layout()

plt.savefig('reference_versus_reading_level.png')

plt.clf()
fig, axes = plt.subplots()
axes.set_title('reference versus compression ratio')
plt.xlabel('reference source')
plt.ylabel('compression ratio')

plt.scatter([i for i in range(0,len(labels))],by_query['reference']['info_density'],label=labels)
for (label, x) in zip(labels,axis):
    plt.annotate(
        label,
        xy=(x, x), xytext=(40, 40),
        textcoords='offset points', ha='left', va='top',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
        #arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.savefig('reference_versus_compression_ratio.png')
'''


query_keys = list(set([ s['query'] for s in urlDats ]))
engine_keys = by_engine.keys()

science_keys = [ 'evolution', 'photosysnthesis' ,'Transgenic', 'GMO', 'climate change', 'cancer', 'Vaccines', 'Genetically Modified Organism']
culture_keys = ['reality TV', 'prancercise philosophy',  'play dough delicious deserts', 'unicorn versus brumby', 'football soccer']

by_query[str('science')] = {}
by_query[str('science')]['urlDats'] = list(filter(lambda url: url['query'] in science_keys, scraped_new))

by_query[str('culture')] = {}
by_query[str('culture')]['urlDats'] = list(filter(lambda url: url['query'] in culture_keys, scraped_new))


fogss_culture = [ w['gf'] for w in by_query[str('culture')]['urlDats'] ]
ranks_culture = [ w['page_rank'] for w in by_query[str('culture')]['urlDats'] ]



fogss_science = [ w['gf'] for w in by_query[str('science')]['urlDats'] ]
ranks_science = [ w['page_rank'] for w in by_query[str('science')]['urlDats'] ]


plt.clf()
fig, ax = plt.subplots()



plt.clf()
plt.title('culture rank versus complexity')
plt.xlabel('rank')
plt.ylabel('standard')
df0 = pd.DataFrame({'complexity':fogss_culture,'rank':ranks_culture})
ax = sns.regplot(x="rank", y="complexity", data=df0, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('culture_rank_vs_complexity.png')
plt.close()


plt.clf()
plt.title('science rank versus complexity')
plt.xlabel('rank')
plt.ylabel('standard')
df1 = pd.DataFrame({'complexity':fogss_science,'rank':ranks_science})
ax = sns.regplot(x="rank", y="complexity", data=df1, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('science_rank_vs_complexity.png')
plt.close()


ses = [ url['se'] for url in scraped_new ]

# import pdb; pdb.set_trace()

#exit

for key in query_keys:
    by_query[key] = {}
    by_query[key]['urlDats'] = list(filter(lambda url: str(key) == url['query'], scraped_new))
    by_query[key]['ranks'] = [ w['page_rank'] for w in by_query[key]['urlDats'] ]
    by_query[key]['standards'] = [ w['standard'] for w in by_query[key]['urlDats'] ]
    by_query[key]['penalty'] = [ w['penalty'] for w in by_query[key]['urlDats'] ]
    by_query[key]['sp'] = [ w['sp'] for w in by_query[key]['urlDats'] ]
    by_query[key]['s_mean'] = np.mean([ w['standard'] for w in by_query[key]['urlDats'] ])
    by_query[key]['s_std'] = np.std([ w['standard'] for w in by_query[key]['urlDats'] ])

    by_query[key]['info_density'] = [ w['info_density'] for w in by_query[key]['urlDats'] ]
    plt.clf()
    fig, ax = plt.subplots()

    plt.title('sent versus complexity'+ str(key))
    plt.xlabel('sentiment')
    plt.ylabel('standard')
    df = pd.DataFrame({'complexity': by_query[key]['standards'],'sentiment': by_query[key]['sp']})
    ##
    # Uncomment to compare to reference data points.
    ##

    # ref = pd.DataFrame({'complexity': [ w['standard'] for w in reference ],'sentiment': [ w['sp'] for w in reference ]})
    # ax = sns.regplot(x="complexity",y="sentiment", data=ref, ax=ax)

    ax = sns.regplot(x="complexity",y="sentiment", data=df, ax=ax)

    legend = ax.legend(loc='upper center', shadow=True)
    plt.legend(loc="upper left")

    plt.savefig('sentiment_vs_complexity_{0}.png'.format(key))
    plt.close()


    plt.clf()
    plt.title('rank versus complexity '+ str(key))
    plt.xlabel('rank')
    plt.ylabel('standard')
    df = pd.DataFrame({'complexity':by_query[key]['standards'],'rank':by_query[key]['ranks']})
    ax = sns.regplot(x="complexity",y="rank", data=df)
    plt.legend(loc="upper left")
    plt.savefig('rank_vs_complexity{0}.png'.format(key))
    plt.close()



for key in engine_keys:
    by_engine[key] = {}

    by_engine[key]['urlDats'] = list(filter(lambda url: str(key) == url['se'], scraped_new))
    by_engine[key]['ranks'] = [ w['page_rank'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['standard'] = [ w['standard'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['penalty'] = [ w['penalty'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['sp'] = [ w['sp'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['s_mean'] = np.mean([ w['standard'] for w in by_engine[key]['urlDats'] ])
    by_engine[key]['s_std'] = np.std([ w['standard'] for w in by_engine[key]['urlDats'] ])

    by_engine[key]['info_density'] = [ w['info_density'] for w in by_engine[key]['urlDats'] ]
    plt.clf()

    fig, ax = plt.subplots()
    plt.title('rank versus standard reading level: '+str(key))
    plt.xlabel('rank')
    plt.ylabel('standard')
    plt.scatter(by_engine[key]['ranks'],by_engine[key]['standard'])
    #print(by_engine[key]['standard'], by_engine[key]['ranks'])
    plt.savefig('standard_vs_rank'+str(key)+'.png')

    plt.clf()
    fig, ax = plt.subplots()
    plt.title('compression ratio versus rank: '+str(key))
    plt.xlabel('rank')
    plt.ylabel('compression ratio')
    plt.scatter(by_engine[key]['ranks'],by_engine[key]['standard'])
    #print(by_engine[key]['info_density'], by_engine[key]['ranks'])
    plt.savefig('compression_ratio'+str(key)+'.png')

    #df = pd.DataFrame({'complexity': by_engine[key]['standards'],'ranks':by_engine[key]['ranks']})
    ##
    # Uncomment to compare to reference data points.

    #ax = sns.regplot(x="complexity",y="ranks", data=df, ax=ax)
    #df = pd.DataFrame({'scaled_info_density': by_engine[key]['scaled_info_density'],'ranks':by_engine[key]['ranks']})
    ##
    # Uncomment to compare to reference data points.
    ##

    # ref = pd.DataFrame({'complexity': [ w['standard'] for w in reference ],'sentiment': [ w['sp'] for w in reference ]})
    # ax = sns.regplot(x="complexity",y="sentiment", data=ref, ax=ax)
    #ax = sns.regplot(x="scaled_info_density",y="ranks", data=df, ax=ax)
    #legend = ax.legend(loc='upper center', shadow=True)
    #plt.legend(loc="upper left")

    #plt.savefig('sentiment_vs_complexity_{0}.png'.format(key))
    #plt.close()

    '''
    plt.clf()
    plt.title('rank versus complexity')
    plt.xlabel('rank')
    plt.ylabel('standard')
    df = pd.DataFrame({'complexity':by_engine[key]['standards'],'rank':by_engine[key]['ranks']})
    ax = sns.regplot(x="complexity",y="rank", data=df)
    plt.legend(loc="upper left")
    plt.savefig('rank_vs_complexity{0}.png'.format(key))
    plt.close()
    '''

#print(labels)
'''
plt.clf()
fig, axes = plt.subplots()
axes.set_title('gunning fog complexity versus sentiment polarity')
#plt.xlabel('sentiment')
plt.scatter(spk,fogk,label="reference data")


plt.plot()
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('sentiment_vs_complexity.png'))
plt.close()

plt.clf()
axes.set_title('info versus fog')
plt.xlabel('info density')
plt.ylabel('gunning fog')
plt.scatter(infos,fogss,label="scrapped data points")
plt.scatter(infok,fogk,label="reference data points")
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('info_density_vs_complexity.png'))
plt.close()


plt.clf()
axes.set_title('gunning fog complexity versus page rank in climate')
plt.xlabel('page rank')
plt.ylabel('gunning fog')
plt.scatter(climate_ranks,climate_fogs,label="scrapped data points")
#plt.scatter(spk,fogk,label="reference points")
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('gf_vs_page_rank_climate.png'))
plt.close()

Word Complexity Project:

General hypothesis: The language that scientists and many science educators use online is more complex than language used by non-scientists and science deniers.

Problem: This leads to the most readable and findable information being potentially less accurate (especially regarding controversial issues),
while the most accurate information is likely more difficult to find in searches and will have less impact.

1. Text complexity vs. site ranking within and between searches
Are simpler texts ranking higher in Google?
How do scientific texts fare within this ranking?
a. For various scientific searches vs. various non-scientific searches
i. Sci searches may be: Genetics, evolution, cancer, vaccine, GMO, climate change, photosynthesis
ii. Non-sci searches may be: Soccer, culture, reality television, ???
b. Also perhaps targeted comparisons of ideal educational websites vs average?

2. Text complexity vs. text sentiment
Are more neutral/factual websites more complex?
a. Rank pro, anti, and neutral websites for text complexity
i. Vaccines
ii. GMOs
iii. Climate change

3. Case studies: Complexity of texts using scientific vs. non-scientific terms
Are scientists using overly complex (but more precise) language online?
a. GMO vs. transgenics
b. Global warming vs. climate change vs. anthropogenic climate change
c. (though non-scientific, perhaps) Intelligent design vs. evolution
d. Also perhaps targeted comparisons of scientist-led blogs vs. public-led blogs covering specific scientific subjects? *can’t be batch processed

Additional questions:
-In Russell’s general search graphs, two clusters of websites seemed to fall out in the graphs. How do we figure out what is causing this?

Issues to consider:
-Are the first few, super successful sites outliers? Should we run these with and without the first page of results to see the differences?

-If AAB sources come up in any of these, should they be automatically excluded?
'''


#ax = sns.regplot(x=x, y=y, color="g")
#sns.lmplot("x", "y", data=df, hue='dataset', fit_reg=False)
