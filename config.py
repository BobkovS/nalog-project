import os

NALOG_URL = os.environ.get('NALOG_URL') or 'https://service.nalog.ru/'
INN_REQUEST_URL, SUSPENSION_REQUEST_URL = f"{NALOG_URL}inn-proc.do", f"{NALOG_URL}bi2-proc.json"
SUSPENSION_ZIP_REQUEST_URL = f"{NALOG_URL}bi-pdf.do?" + "token={}"

PROXY_URL_LIST = os.environ.get('PROXY_URL_LIST') or [
    'https://spys.me/proxy.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'
]

INN_DEFAULT_REQUEST_DATA = {
    "fam": "Бобков", "nam": "Сергей", "otch": "Алексеевич", "bdate": "16.08.1996", "bplace": "Пермь",
    "doctype": "21", "docno": "57 16 485247", "docdt": "14.09.2016", "captcha": "", "captchaToken": "", "c": "innMy"
}

SUSPENSION_DEFAULT_REQUEST_DATA = {
    'requestType': 'FINDPRS', 'innPRS': "590204405510", 'bikPRS': "043601829", 'fileName': '', 'bik': '', 'kodTU': '',
    'dateSAFN': '', 'bikAFN': '', 'dateAFN': '', 'fileNameED': '', 'captcha': '', 'captchaToken': ''
}

DEFAULT_HTTP_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
}

DEFAULT_PROXY_DICTIONARY = {
    "https": "https://0.0.0.0:8080"
}

PROXY_PING_TIMEOUT, MINIMAL_PROXY_COUNT = 1, 10
INN_REQUEST_TIMEOUT, SUSPENSION_REQUEST_TIMEOUT, SUSPENSION_ZIP_REQUEST_TIMEOUT = 5, 5, 5
INN_REQUEST_MAX_ERROR_COUNT, SUSPENSION_REQUEST_MAX_ERROR_COUNT, SUSPENSION_ZIP_REQUEST_MAX_ERROR_COUNT = 20, 20, 20
