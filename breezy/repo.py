from typing import Any
import os

from seleniumwire import webdriver
from seleniumwire.request import Request
from selenium.webdriver.chrome.options import Options
import requests


def get_driver() -> webdriver.Chrome:
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


def get_request(report_url: str) -> Request:
    driver = get_driver()

    driver.get("https://app.breezy.hr/signin")

    email = driver.find_element_by_xpath('//*[@id="email_address-2"]')
    email.send_keys(os.getenv('BREEZY_EMAIL'))

    password = driver.find_element_by_xpath('//*[@id="password-2"]')
    password.send_keys(os.getenv('BREEZY_PWD'))

    login = driver.find_element_by_xpath(
        '//*[@id="wf-form-Inclusive-Mini-Course"]/div[4]/div/input'
    )
    login.click()

    request = driver.wait_for_request("api/config", timeout=240)

    driver.quit()

    return request


def get_data(request: Request):
    with requests.get(
        "https://app.breezy.hr/api/company/dd4c90bcaaf1/reports/overview",
        params={
            "date_range": "customRange",
            "start_date": "2022-04-01",
            "end_date": "2022-04-15",
        },
        headers=request.headers,
    ) as r:
        res = r.json()
        return res


def transform(res: dict[str, Any]) -> list[dict]:
    return [
        {
            "date": key,
            **value["data"],
        }
        for key, value in res["candidates"]["volume_history"].items()
    ]
