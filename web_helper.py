from retrying import retry
import requests
from requests import Session


@retry(retry_on_exception=lambda x: isinstance(x, ConnectionError), stop_max_attempt_number=3,
       wait_random_min=500, wait_random_max=2000)
def get_html(url: str, save_html: bool = False, filename: str = None,
             session: Session = None, ) -> (tuple[bytes], Session):
    """
    just request/request.session with retry mechanism

    :param url:
    :param session: default None, pass existing request session for faster web loading
    :param save_html: default False
    :param filename: default "output/*.html", extracted from url

    """
    session = requests.Session() if session is None else session
    req = session.get(url)
    if req.status_code == 200:
        html = req.content,
        if save_html:
            if filename is None:
                filename = filename_from_url(req.url)
            save_as(html[0].decode('utf-8', errors='ignore'), filename)
            # req.content/text return one element tuple (tuple[byte]), so to remove b notation used above decode
        return html, session
    else:
        print("Warning:\nSite Address:", url, "\nStatus Code:", req.status_code, "must be 200",
              end='\n\n')
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


def filename_from_url(url: str) -> str:
    """
    Extracts proper Html File name from url

    :param url: url as string
    :return: filename with .html extension as string
    """
    # endpoint for urls like https://www.facebook.com/hello, file name will be hello "THE ENDPOINT"
    endpoint = url.split(sep='/')[-1]
    # for urls like https://www.facebook.com/, file name will be facebook
    return (endpoint if endpoint != "" else url.split(sep='.')[-2]) + ".html"
