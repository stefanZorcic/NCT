from math import floor, ceil
from nltk.corpus import stopwords

#
import datetime
import requests as req
import json
from json.decoder import JSONDecodeError

from sklearn.feature_extraction.text import TfidfVectorizer

import time
import datetime
from core.pmid_utils import get_year, get_abstract, get_title, get_authors_last_name
import requests
from requests.sessions import Session
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, local


def info(link):
    return req.get(link)


def multiThreadDownload(url_list):
    thread_local = local()

    content = []

    def get_session() -> Session:
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    def download_link(url: str):
        session = get_session()
        with session.get(url) as response:
            content.append(response)

    def download_all(urls: list) -> None:
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(download_link, url_list)

    download_all(url_list)

    return content


def get_responses(title, year):
    urls = []

    for word in options(title):
        urls.append(
            f"https://clinicaltrials.gov/api/v2/studies?query.titles={word}&pageSize=10&query.term=AREA[LastUpdatePostDate]RANGE[{year-5}-01-01,MAX]"
        )

    return multiThreadDownload(urls)


def get_integers(arr: str = None):
    """
    Takes a string (arr) as input and returns all the integers in the string in an array
    Trys to find the number of participants in the study given the abstract
    """

    ans = []
    for x in arr.split():
        try:
            ans.append(int(x))
        except ValueError:
            continue
    return ans
    ans = []
    arr = arr.split()
    n = len(arr)

    for i in range(1, n):
        if arr[i][:-1].isalpha():
            try:
                ans.append(int(arr[i - 1]))
            except ValueError:
                continue

    return ans


def check_val(val: int, arr, tolerance):
    """
    Takes a value and returns if the value exists in an array of integers within some percent tolerance
    """
    return True
    for x in arr:
        if x >= floor(val * (1 - tolerance)) and x <= ceil(val * (1 + tolerance)):
            return True
    return False


def position(nct, arr):

    counter = 1
    for a, b in arr:
        if b == nct:
            return counter
        counter += 1
    return None


global s


def setup():
    import nltk

    nltk.download("stopwords")


def options(title: str):
    title.replace(",", " ")
    title.replace(":", " ")
    title.replace(";", " ")
    s = set(stopwords.words("english"))
    p = [x for x in filter(lambda w: not w in s, title.split())]
    arr = p
    n = len(arr)
    ans = []
    for i in range(n):
        for j in range(i + 1, n):
            ans.append(arr[i] + " " + arr[j])
    return ans


def get_names(name):
    name.replace(",", " ")
    s = set(stopwords.words("english"))
    name = [x for x in filter(lambda w: not w in s, name.split())]
    # name.split()
    ans = []
    illegal = ["MD"]
    for x in name:
        if len(x) != 0:
            if x not in illegal:
                ans.append(x.lower())
    return ans
