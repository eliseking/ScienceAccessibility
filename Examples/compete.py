

try:
    assert os.path.isfile('results.p')
    winners = pickle.load(open('results.p','rb'))
except:
    peter = str('https://academic.oup.com/beheco/article-abstract/29/1/264/4677340')
    xkcd_self_sufficient = str('http://splasho.com/upgoer5/library.php')
    high_standard = str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D')
    rgerkin = str('https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=sra')
    scrook = str('https://scholar.google.com/citations?user=xnsDhO4AAAAJ&hl=en&oe=ASCII&oi=sra')

    from bs4 import BeautifulSoup
    from crawl import collect_pubs
    import os.path
    import pickle


    from crawl import FetchResource
    from t_analysis_csv import text_proc


    try:
        assert os.path.isfile('authors.p')
        authors = pickle.load(open('authors.p','rb'))
    except:
        rgerkin = collect_pubs(rgerkin)
        scrook = collect_pubs(scrook)
        authors = {}
        authors['rgerkin'] = rgerkin
        authors['scrook'] = scrook
        with open('authors.p','wb') as f:
            pickle.dump(authors,f)




    fr = FetchResource(high_standard)
    hs = fr.run()
    urlDat = {'link':high_standard}
    hss = text_proc(hs,urlDat)

    fr = FetchResource(xkcd_self_sufficient)
    bench_mark = fr.run()
    urlDat = {'link':xkcd_self_sufficient}
    bench = text_proc(bench_mark,urlDat)

    fr = FetchResource(peter)
    pmarting = fr.run()
    urlDat = {'link':peter}
    pm = text_proc(pmarting,urlDat)

    try:
        assert os.path.isfile('author_results.p')
        author_results = pickle.load(open('author_results.p','rb'))
    except:
        author_results = {'rgerkin':{}, 'scrook':{}}
        for author,links in authors.items():
            for r in links:
                fr = FetchResource(r)
                corpus = fr.run()
                if corpus is not None:
                    urlDat = {'link':r}
                    urlDat = text_proc(corpus,urlDat)

                    if str(r) not in author_results.keys():
                        author_results[author][str(r)] = urlDat
                    else:
                        author_results[author][str(r)] = urlDat
            print(author_results)
        with open('author_results.p','wb') as f:
            pickle.dump(author_results,f)

    rg = list(author_results['rgerkin'].values())
    sc = list(author_results['scrook'].values())
    import numpy as np

    def metrics(rg):
        if type(rg) is type([]):
            pub_count = len(rg)
            fog = np.mean([ r['gf'] for r in rg ])
            unique = np.mean([ r['uniqueness'] for r in rg ])
            density = np.mean([ r['info_density'] for r in rg ])
            wcount = np.mean([ r['wcount'] for r in rg ])
            scaled_density = density/wcount
            obj = np.mean([ r['sp'] for r in rg ])
        else:
            pub_count = 1
            fog = rg['gf']
            unique = rg['gf']
            density = rg['info_density']
            wcount = rg['wcount']
            obj = rg['sp']
            scaled_density = density/wcount # higher better
            # good writing should be readable, objective, concise.
        penalty = fog + abs(obj) - scaled_density + unique
        return (fog, obj, scaled_density, unique, penalty)


    rick = metrics(rg)[4]
    scrook = metrics(sc)[4]
    bench = metrics(bench)[4]
    pm = metrics(pm)[4]
    hss = metrics(hss)[4]
    winners = [('rgerkin',rick),('scrook',scrook),('upgoer5_corpus',bench),('the readability of science decr over time', hss), ('peter',pm)]
    with open('results.p','wb') as f:
        pickle.dump(winners,f)

winners = sorted([(w[1],w[0]) for w in winners])
print(winners)