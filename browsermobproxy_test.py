from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import psutil
import traceback
import json

def terminate_browsermob_processes(proxy, server):
    proxy.close()
    server.stop()

    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['name', 'cmdline'])
            if process_info.get('name') in ('java', 'java.exe'):
                for cmd_info in process_info.get('cmdline'):
                    if cmd_info == '-Dapp.name=browsermob-proxy':
                        process.kill()
        except psutil.NoSuchProcess:
            pass

def prepareDirectory():
    """
    ./imageUrlList/ ディレクトリを作成する
    """
    htmlDir = Path(Path.cwd()).joinpath('imageUrlList')
    if not htmlDir.exists():
        htmlDir.mkdir()
        print('Create imageUrlList Directory')
    else:
        print('imageUrlList Directory is already exists')

def writePagelist(pageSource, fileName):
    """
    urlリストをファイル出力する。
    """
    htmlFile = Path(Path.cwd()).joinpath('imageUrlList').joinpath(fileName)
    with htmlFile.open('w', encoding = 'utf-8', newline = '\n') as file:
        file.writelines(pageSource)

if __name__ == '__main__':

    # BrowserMob Proxyのインストールパス
    proxy_path = './browsermob-proxy-2.1.4/bin/browsermob-proxy'

    # BrowserMob ProxyがListenするポート番号 (デフォルト: 8080)
    proxy_ooptions = {'port': 60000}

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')

    try:
        server = Server(proxy_path, options=proxy_ooptions)
        server.start()
        proxy = server.create_proxy()

        # Google Analyticsが利用するURLをblacklistに入れてアクセス解析タグを除外する
        proxy.blacklist('https?:\/\/www\.google-analytics\.com\/analytics\.js', 404)
        proxy.blacklist('https?:\/\/www\.googletagmanager\.com\/gtag\/js\?id=UA-.*', 404)

        options.add_argument('--proxy-server={0}'.format(proxy.proxy))

        driver = webdriver.Chrome(options=options)

        # HTTP(S)通信の内容も取得したい場合
        proxy.new_har('smcc', options={'captureHeaders': True})

        driver.get('https://www.smbc-card.com/nyukai/loan/special.jsp')
        print(driver.title)

        # 通信内容を表示
        #print(proxy.har)

        # Harを出力
        jsonFile = Path(Path.cwd()).joinpath('json').joinpath('loan_special.json')
        with jsonFile.open('w', encoding = 'utf-8', newline = None) as file:
            # Unicode 出力しないようにする
            json.dump(proxy.har, file, indent = 2, ensure_ascii = False)

        imageUrlList =[]
        # Harからurlのみを抽出
        for ent in proxy.har['log']['entries']:
            #print(ent['request']['url'])
            imageUrlList.append(ent['request']['url'])

        # ファイル出力
        prepareDirectory()
        writePagelist(imageUrlList, 'loan_special.txt')
        print(imageUrlList)

        # ブラウザのログを取得して表示
        #log = driver.get_log('browser')
        #print(log)

    except:
        traceback.print_exc()

    finally:
        driver.quit()

        # BrowserMob Proxyの関連プロセスを完全に停止する処理
        terminate_browsermob_processes(proxy, server)