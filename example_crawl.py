import platform
import time
from pathlib import Path

import chromedriver_binary
from selenium import webdriver

def main():
  """
  メイン関数
  """

  driver = createDriver()
  try:
    prepareHtmlDirectory()
    pageSource = getPageSource(driver, 'http://google.com/')
    print(pageSource)
    writePageSource(pageSource, 'google.html')
  except Exception as error:
    print('An error occurred', error)
  finally:
    time.sleep(1)
    driver.quit()
    print('Finished')

def createDriver():
  """
  Chrome WebDriver を生成する

  Returns
  -------
  driver : webdriver.Chrome
    WebDriver
  """

  # Chrome オプション
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_argument('--disable-gpu')
  chromeOptions.add_argument('--no-sandbox')

  # MacOS では Headless モードにすると上手く起動しなかったので避ける・executable_path の指定が必要
  if platform.system() != 'Darwin':
    print('Headless Mode')
    chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(options = chromeOptions)
  else:
    print('Normal Mode (MacOS)')
    driver = webdriver.Chrome(
      executable_path = '/usr/local/bin/chromedriver',
      options = chromeOptions
    )
  return driver

def prepareHtmlDirectory():
  """
  ./html/ ディレクトリを作成する
  """

  htmlDir = Path(Path.cwd()).joinpath('html')
  if not htmlDir.exists():
    htmlDir.mkdir()
    print('Create HTML Directory')
  else:
    print('HTML Directory is already exists')

def getPageSource(driver, url):
  """
  URL を指定してソースを取得する

  Parameters
  ----------
  driver : webdriver.Chrome
    WebDriver
  url : str
    URL

  Returns
  -------
  page_source : str
    HTML ソース
  """

  driver.get(url)
  print(f'{url} : {driver.title}')
  return driver.page_source

def writePageSource(pageSource, fileName):
  """
  ソースをファイルに書き出す

  Parameters
  ----------
  pageSource : str
    HTML ソース
  fileName : str
    保存ファイル名
  """

  htmlFile = Path(Path.cwd()).joinpath('html').joinpath(fileName)
  with htmlFile.open('w', encoding = 'utf-8', newline = '\n') as file:
    file.write(pageSource)

# 本ファイルをインポートした時に main() 関数が実行されないようにする
if __name__ == '__main__':
  main()