import random
import re

import requests

import config
from app import application_object_logger
from utility_methods.ignore_errors_wapper import ignore_errors_wrapper


class ProxyLoader:
    def __init__(self):
        self.proxy_object = config.DEFAULT_PROXY_DICTIONARY
        self.proxy_list_urls = config.PROXY_URL_LIST
        self.suspension_zip_token = None
        self.proxy_list_dirty = set()
        self.inn_proxy_list = set()
        self.suspension_proxy_list = set()
        self.suspension_zip_proxy_list = set()
        self.inn, self.suspension, self.suspension_zip = False, False, False

    def fetch_proxy_list(self):
        try:
            self.proxy_list_dirty.clear()
            for proxy_list_url in self.proxy_list_urls:
                [self.proxy_list_dirty.add(f"https://{response_string.split()[0]}") for response_string in requests.get(
                    proxy_list_url).text.split('\n') if re.match(r'\d+.\d+.\d+.\d+:\d+.+', response_string)]
        except Exception as e:
            application_object_logger.error(f"Не удается получить список прокси: {e.__str__()}")
            raise Exception(f"Не удается получить список прокси: {e.__str__()}")

    def filter_proxy_list(self):
        if self.proxy_list_dirty.__len__() == 0:
            raise Exception(f"Список прокси пуст. Свяжитесь с вашим администратором")
        for proxy_obj in self.proxy_list_dirty:
            self.proxy_object["https"] = proxy_obj
            with ignore_errors_wrapper():
                data = requests.post(
                    config.INN_REQUEST_URL, config.INN_DEFAULT_REQUEST_DATA, proxies=self.proxy_object,
                    timeout=config.PROXY_PING_TIMEOUT, headers=config.DEFAULT_HTTP_REQUEST_HEADERS
                )
                if data.status_code == 200:
                    self.inn_proxy_list.add(self.proxy_object['https'])
                    application_object_logger.debug(f"Proxy list sizes are: inn >> {self.inn_proxy_list.__len__()}, "
                                                    f"suspension >> {self.suspension_proxy_list.__len__()}, "
                                                    f"suspension zip >> {self.suspension_zip_proxy_list.__len__()}")
            with ignore_errors_wrapper():
                data = requests.post(
                    config.SUSPENSION_REQUEST_URL, config.SUSPENSION_DEFAULT_REQUEST_DATA, proxies=self.proxy_object,
                    timeout=config.PROXY_PING_TIMEOUT, headers=config.DEFAULT_HTTP_REQUEST_HEADERS
                )
                if data.status_code == 200:
                    self.suspension_proxy_list.add(self.proxy_object['https'])
                    if 'formToken' in data.json(): self.suspension_zip_token = data.json()['formToken']
            if self.suspension_zip_token:
                with ignore_errors_wrapper():
                    data = requests.post(
                        config.SUSPENSION_ZIP_REQUEST_URL.format(self.suspension_zip_token), proxies=self.proxy_object,
                        timeout=config.PROXY_PING_TIMEOUT, headers=config.DEFAULT_HTTP_REQUEST_HEADERS
                    )
                    if data.status_code == 200: self.suspension_zip_proxy_list.add(self.proxy_object['https'])

    def run_proxy_loader(self):
        self.fetch_proxy_list()
        self.filter_proxy_list()

    def fetch_random_proxy(self, proxy_target):
        if proxy_target == 'inn': return {"https": random.choice(list(self.inn_proxy_list))}
        if proxy_target == 'suspension': return {"https": random.choice(list(self.suspension_proxy_list))}
        if proxy_target == 'suspension_zip': return {"https": random.choice(list(self.suspension_zip_proxy_list))}

    def remove_proxy(self, proxy_target, proxy_value):
        if proxy_target == 'inn': self.inn_proxy_list.remove(proxy_value)
        if proxy_target == 'suspension': self.suspension_proxy_list.remove(proxy_value)
        if proxy_target == 'suspension_zip': self.suspension_zip_proxy_list.remove(proxy_value)
