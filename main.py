import requests as req
import json
from json.decoder import JSONDecodeError

from sklearn.feature_extraction.text import TfidfVectorizer

import time
import datetime

from core.utils import (
    get_integers,
    check_val,
    options,
    setup,
    info,
    get_responses,
    get_names,
)
from core.pmid_utils import get_year, get_abstract, get_title, get_authors_last_name
from core.heuristics import heuristic1, heuristic2
import sys

sys.setrecursionlimit(1500)

global times


def func(wip=None):
    d = {}

    print(f"Processing PMID: {wip}")

    link = f"https://pubmed.ncbi.nlm.nih.gov/{wip}/"
    content = info(link)

    year = get_year(content)
    abstract = get_abstract(content)
    title = get_title(content)
    authors_last_name = get_authors_last_name(content)
    q = len(authors_last_name)
    l = q * q
    score = {}

    for x in authors_last_name:
        score[x] = l
        l -= q

    corpus = [abstract]

    qp = []

    responses = get_responses(title, year)

    int_list = get_integers(abstract)

    for x in responses:
        try:
            loaded = json.loads(x.content)["studies"]
            if len(loaded) > 10000:
                continue
        except JSONDecodeError:
            continue

        for lol in loaded:
            try:
                id = lol["protocolSection"]["identificationModule"]["nctId"]

                if heuristic2(lol, year, abstract, int_list, authors_last_name, id):
                    continue

                if id in qp:
                    continue
                qp.append(id)

                corpus.append(
                    lol["protocolSection"]["descriptionModule"]["briefSummary"]
                )

            except KeyError:
                continue

    amount = len(corpus)

    print(f"Candidates: {amount}")

    # NLP
    vect = TfidfVectorizer(min_df=1, stop_words="english")
    tfidf = vect.fit_transform(corpus)
    pairwise_similarity = tfidf * tfidf.T

    r = pairwise_similarity.toarray()

    counter = 0
    ans = []

    # Weighting
    for i in range(len(r[0][1:])):
        ans.append(
            [
                r[0][i + 1],
                qp[counter],
            ]
        )
        counter += 1

    ans.sort(reverse=True)

    # Probability vector
    return ans
