
import glob
import os
import dask.bag as db
from crawl import html_to_txt, convert_pdf_to_txt
#from utils_and_paramaters import convert_to_text
from t_analysis import text_proc#, metrics
from natsort import natsorted, ns
import pprint
import pickle
import numpy as np
import os
def convert_to_text(fileName):
    b = os.path.getsize(fileName)
    urlDat = {}
    if b>250: # this is just to prevent reading in of incomplete data.
        try:
            file = open(fileName)
            if str('.html') in fileName:
                text = html_to_txt(file)
            else:
                text = convert_pdf_to_txt(file)
            #file.close()
            urlDat = {'link':fileName}
            urlDat = text_proc(text,urlDat)
            print(urlDat)
        except:
            pass
    return urlDat


TOURNAMENT = True

try:
    assert os.path.isfile('../BenchmarkCorpus/benchmarks_ranked.p')
    benchmarks = pickle.load(open('../BenchmarkCorpus/benchmarks_ranked.p','rb'))
    benchmarks = [ b[1] for b in benchmarks ]
    urlDats = []
    urlDats.extend(benchmarks)
    print('benchmarks loaded')
except:
    pass
if TOURNAMENT:
    # naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
    rick = natsorted(glob.glob(str(os.getcwd())+'/*rcgerkin*.html'))
    rick.extend(natsorted(glob.glob(str(os.getcwd())+'/*rcgerkin*.pdf')))
    sharon = natsorted(glob.glob(str(os.getcwd())+'/*scrook**.html'))
    sharon.extend(natsorted(glob.glob(str(os.getcwd())+'/*scrook*.pdf')))
    sarah = natsorted(glob.glob(str(os.getcwd())+'/*jarvis**.html'))
    sarah.extend(natsorted(glob.glob(str(os.getcwd())+'/*jarvis*.pdf')))


    grid0 = db.from_sequence(rick)
    grid1 = db.from_sequence(sharon)
    grid2 = db.from_sequence(sarah)

    rick = list(db.map(convert_to_text,grid0).compute())
    sharon = list(db.map(convert_to_text,grid1).compute())
    sarah = list(db.map(convert_to_text,grid2).compute())

    with open('tournment.p','wb') as handle:
        pickle.dump([sarah,rick,sharon,benchmarks],handle)

    urlDats.extend(sharon)
    urlDats.extend(rick)
    urlDats.extend(sarah)

    urlDats = list(filter(lambda url: len(list(url))>3, urlDats))
    urlDats = list(filter(lambda url: len(list(url.keys()))>3, urlDats))
    #urlDats = list(filter(lambda url: str('science') in url.keys(), urlDats))
    #urlDats = list(filter(lambda url: url['science'] == True, urlDats))
    urlDats = list(filter(lambda url: str('penalty') in url.keys(), urlDats))
    ranked = sorted(urlDats, key=lambda w: w['penalty'])   # sort by age
    sharon_mean = np.mean([r['penalty'] for r in ranked if 'scrook' in r['link']])
    rick_mean = np.mean([r['penalty'] for r in ranked if 'rcgerkin' in r['link']])
    sarah_mean = np.mean([r['penalty'] for r in ranked if 'jarvis' in r['link']])

    print(rick_mean,sharon_mean,sarah_mean)
    import pdb
    pdb.set_trace()


else:
    # naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
    lo_query_html = natsorted(glob.glob(str(os.getcwd())+'/*.html'))
    lo_query_pdf = natsorted(glob.glob(str(os.getcwd())+'/*.pdf'))


    grid0 = db.from_sequence(lo_query_html)
    grid1 = db.from_sequence(lo_query_pdf)
    urlDats = list(db.map(local_opt,grid0).compute())
    urlDats.extend(list(db.map(local_opt,grid1).compute()))
    urlDats = list(filter(lambda url: len(list(url))>3, urlDats))

    urlDats = list(filter(lambda url: len(list(url.keys()))>3, urlDats))
    urlDats = list(filter(lambda url: str('penalty') in url.keys(), urlDats))
    with open('unraveled_links.p','wb') as handle:
        pickle.dump(winners,handle)


    winners = sorted(urlDats0, key=lambda w: w['penalty'])   # sort by age

    text0 = print_best_text(winners[0]['link'])
    text1 = print_best_text(winners[1]['link'])


    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(winners[0])
    pp.pprint(text0)
    pp.pprint(winners[1])
    pp.pprint(text1)


    frames = False
    if frames ==True:
        unravel = process_dics(urlDats)
    else:
        unravel = urlDats
    #import pickle
    with open('winners.p','wb') as handle:
        pickle.dump(winners,handle)