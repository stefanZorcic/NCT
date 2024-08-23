def get_year(content):
    return int(
        content.content.decode("utf-8")
        .split('<div class="article-source">')[1]
        .split('<span class="cit">')[1]
        .split(" ")[0]
    )


def get_abstract(content):
    abstract = ""

    for a in (
        content.content.decode("utf-8")
        .split("abstract-content selected")[1]
        .split("</div")[0]
        .split("</strong>")[1:]
    ):
        abstract += a.split("<")[0].strip()
        abstract += " "

    return abstract


def get_title(content):
    stupid = (
        content.content.decode("utf-8")
        .split('<h1 class="heading-title">')[1]
        .split("header")[0]
    )

    stupid1 = stupid.split("</h1>")[0]
    title = stupid1.strip()
    return title


def get_authors_last_name(content):
    authors_last_name = []

    stupid = (
        content.content.decode("utf-8")
        .split('<h1 class="heading-title">')[1]
        .split("header")[0]
    )

    for stupider in stupid.split('<span class="authors-list-item ">')[1:]:
        authors_last_name.append(
            stupider.split("</a>")[0].split(">")[-1].split(" ")[-1].lower()
        )

    return authors_last_name
