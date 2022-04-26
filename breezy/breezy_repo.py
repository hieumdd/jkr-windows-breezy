from typing import Any, Callable
import os
from urllib.parse import urljoin

from seleniumwire import webdriver
from seleniumwire.request import HTTPHeaders
from selenium.webdriver.chrome.options import Options
import requests

BASE_URL = "https://app.breezy.hr/api/company/dd4c90bcaaf1/"


def _get_driver() -> webdriver.Chrome:
    chrome_options = Options()
    if os.getenv("PYTHON_ENV") == "prod":
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if os.getenv("PYTHON_ENV") == "dev":
        driver = webdriver.Chrome("./chromedriver", options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(20)
    return driver


def get_headers() -> HTTPHeaders:
    driver = _get_driver()

    driver.get("https://app.breezy.hr/signin")

    email = driver.find_element_by_xpath('//*[@id="email_address-2"]')
    email.send_keys(os.getenv("BREEZY_EMAIL"))

    password = driver.find_element_by_xpath('//*[@id="password-2"]')
    password.send_keys(os.getenv("BREEZY_PWD"))

    login = driver.find_element_by_xpath(
        '//*[@id="wf-form-Inclusive-Mini-Course"]/div[4]/div/input'
    )
    login.click()

    request = driver.wait_for_request("api/config", timeout=240)

    driver.quit()

    return request.headers


def get_api(uri: str, params_fn: Callable[[], dict[str, Any]]):
    def _get(headers: HTTPHeaders):
        with requests.get(
            urljoin(BASE_URL, uri),
            params=params_fn(),
            headers=headers,
        ) as r:
            res = r.json()
            return res

    return _get
