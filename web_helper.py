from retrying import retry
import requests


@retry(retry_on_exception=lambda x: isinstance(x, ConnectionError), stop_max_attempt_number=3, wait_random_min=500,
       wait_random_max=2000)
def get_html(url, save_html=False, filename=None):
    """
    just request with retry mechanism

    :param url:
    :param save_html: default False
    :param filename: default "output/*.html", extracted from url
    :return: tuple[bytes] = request.content
    """
    req = requests.get(url)
    if {req.status_code}.intersection({200, 201}):
        html = req.content,
        if save_html:
            endpoint = req.url.split(sep='/')[-1]
            auto_filename = "output/" + (endpoint if endpoint != "" else req.url.split(sep='.')[-2]) + ".html"
            filename = auto_filename if filename is None else filename
            save_as(html[0].decode('utf-8', errors='ignore'), filename)
            # req.content/text return one element tuple (tuple[byte]), so to remove b notation used above decode
        return html
    else:
        print("Warning:\nSite Address:", url, "\nStatus Code:", req.status_code, end='\n\n')
        raise ConnectionError


def save_as(data: str, filename: str) -> None:
    """
    saves str into file, overrides previous data

    :param data: string/text data
    :param filename: filename with extension
    :return: None
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)


