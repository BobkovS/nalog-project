import base64

import requests

import config
from app import application_object
from utility_methods.response_objects import Inn, Suspension


class NalogWorker:
    def __init__(self):
        self.error_count = 0
        self.answer_object = None
        self.inn_request_url = config.INN_REQUEST_URL
        self.suspension_request_url = config.SUSPENSION_REQUEST_URL
        self.suspension_zip_request_url = config.SUSPENSION_ZIP_REQUEST_URL

    @staticmethod
    def fetch_response_errors(json):
        error_dict = {}
        if 'ERRORS' in json:
            for errors in json['ERRORS']:
                for value in json['ERRORS'][errors]:
                    error_dict.update({errors: value})
        if 'captcha' in error_dict:
            return {}
        return error_dict

    def increase_error_count(self):
        self.error_count = self.error_count + 1

    def fetch_inn_request(self, request_json, proxy):
        nalog_data = requests.post(
            self.inn_request_url, proxies=proxy, data=request_json, timeout=config.INN_REQUEST_TIMEOUT
        ).json()
        if self.fetch_response_errors(nalog_data):
            self.answer_object.errors = self.fetch_response_errors(nalog_data)
            return self.answer_object
        code = nalog_data["code"] if "code" in nalog_data else -1
        if code == 1 or code == 0:
            self.answer_object.inn = nalog_data["inn"] if code == 1 else -1
            return self.answer_object

    def fetch_inn(self, request_json):
        self.answer_object = Inn(None, None)
        while True:
            proxy = application_object.proxy_loader.fetch_random_proxy(proxy_target="inn")
            try:
                self.fetch_inn_request(request_json, proxy)
            except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.ReadTimeout) as e:
                self.increase_error_count()
                application_object.proxy_loader.remove_proxy(proxy_target='inn', proxy_value=proxy['https'])
                if self.error_count > config.INN_REQUEST_MAX_ERROR_COUNT:
                    self.answer_object.errors = e.__str__()
                    return self.answer_object
            if self.answer_object.errors:
                return self.answer_object
            if self.answer_object.inn is None:
                continue
            if self.answer_object.inn == -1:
                self.answer_object.inn = None
                self.answer_object.errors = "ИНН на заданные паспортные данные не найден"
                return self.answer_object
            return self.answer_object

    def fetch_suspension_request(self, request_json, proxy):
        nalog_data = requests.post(
            self.suspension_request_url, proxies=proxy, data=request_json, timeout=config.SUSPENSION_REQUEST_TIMEOUT
        ).json()
        if self.fetch_response_errors(nalog_data):
            self.answer_object.errors = self.fetch_response_errors(nalog_data)
            return self.answer_object
        self.answer_object.zip = nalog_data['formToken'] if 'formToken' in nalog_data else -1
        self.answer_object.mark = 0 if 'rows' in nalog_data else 1

    def fetch_suspension(self, request_json):
        self.answer_object = Suspension(None, None, None)
        while True:
            proxy = application_object.proxy_loader.fetch_random_proxy(proxy_target="suspension")
            try:
                self.fetch_suspension_request(request_json, proxy)
            except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.ReadTimeout) as e:
                self.increase_error_count()
                application_object.proxy_loader.remove_proxy(proxy_target='suspension', proxy_value=proxy['https'])
                if self.error_count > config.SUSPENSION_REQUEST_MAX_ERROR_COUNT:
                    self.answer_object.errors = e.__str__()
                    return self.answer_object
            if self.answer_object.zip == -1 or self.answer_object.zip is None:
                continue
            self.error_count = 0
            self.download_suspension_zip()
            return self.answer_object

    def download_suspension_zip(self):
        while True:
            proxy = application_object.proxy_loader.fetch_random_proxy(proxy_target="suspension_zip")
            try:
                suspension_zip_data = requests.get(
                    self.suspension_zip_request_url.format(self.answer_object.zip), proxies=proxy,
                    timeout=config.SUSPENSION_ZIP_REQUEST_TIMEOUT
                )
                self.answer_object.zip = str(base64.b64encode(suspension_zip_data.content), 'UTF-8')
                break
            except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.ReadTimeout) as e:
                self.increase_error_count()
                application_object.proxy_loader.remove_proxy(proxy_target='suspension_zip', proxy_value=proxy['https'])
                if self.error_count > config.SUSPENSION_ZIP_REQUEST_MAX_ERROR_COUNT:
                    self.answer_object.errors = e.__str__()
                    return self.answer_object
