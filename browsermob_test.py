from browsermobproxy import Server
from selenium import webdriver
import json
from pathlib import Path
import time


class GetWebPageHar:
    proxy_path = "./browsermob-proxy-2.1.4/bin/browsermob-proxy"

    def __init__(self):
        self.server = Server(str(Path(self.proxy_path).absolute()))
        self.server.start()
        self.proxy = self.server.create_proxy()

    def get_har(self, url, output_filename):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={0}".format(self.proxy.proxy))
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(chrome_options=chrome_options)

        self.proxy.new_har("google")
        driver.get(url)
        time.sleep(10)
        har_json = json.dumps(self.proxy.har, indent=4, ensure_ascii=False)
        with open(output_filename, "w") as f:
            f.write(har_json)
        driver.quit()

    def stop(self):
        self.server.stop()


if __name__ == "__main__":
    getter = GetWebPageHar()
    getter.get_har("https://www.google.com", "test_har.json")
    getter.stop()