import time
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
from math import floor


def heuristic1(lol, year, abstract, int_list, authors_last_name):
    study_start_date = lol["protocolSection"]["statusModule"]["startDateStruct"]["date"]

    if time.strptime(study_start_date.split("-")[0], f"%Y") > time.strptime(
        f"{year}", f"%Y"
    ):
        return True

    name_str = lol["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"][
        "name"
    ]

    try:
        name_str += " "
        name_str += lol["protocolSection"]["sponsorCollaboratorsModule"][
            "responsibleParty"
        ]["investigatorFullName"]
    except Exception as e:
        pass

    try:
        name_str += " "
        name_str += lol["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"][
            "name"
        ]
    except Exception as e:
        pass

    names = get_names(name_str)

    # if id == "NCT04454229":
    #    breakpoint()
    flag = True
    for name in names:
        if name in authors_last_name or name in abstract.lower():
            flag = False

    flag2 = True

    if lol["protocolSection"]["designModule"]["enrollmentInfo"]["count"] in int_list:
        flag2 = False

    if flag and flag2:
        return True

    return False


def heuristic2(lol, year, abstract, int_list, authors_last_name, id=None):
    authors_list = []
    for x in lol["protocolSection"]["referencesModule"]["references"]:
        cit = x["citation"]
        cit = cit.split(".")[0]
        for r in cit.split(","):
            authors_list.append(r.strip().split(" ")[0].lower())

    # if id == "NCT03855137":
    #    breakpoint()

    if len(set(authors_list) & set(authors_last_name)) < min(
        5, max(1, floor(len(authors_last_name) / 3))
    ):
        return True
    return False
