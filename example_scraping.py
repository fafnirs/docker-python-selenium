import json
from pathlib import Path

from bs4 import BeautifulSoup

def main():
  """
  メイン関数
  """

  prepareJsonDirectory()

  html = getHtml('google.html')
  soup = parseHtml(html)

  scrapedDict = scrape(soup)
  writeJson(scrapedDict, 'google.json')

  print('Finished')

def prepareJsonDirectory():
  """
  ./json/ ディレクトリを作成する
  """

  jsonDir = Path(Path.cwd()).joinpath('json')
  if not jsonDir.exists():
    jsonDir.mkdir()
    print('Create JSON Directory')
  else:
    print('JSON Directory is already exists')

def getHtml(fileName):
  """
  HTML ファイルを読み込んで中身を返す

  Parameters
  ----------
  fileName : str
    読み込むファイル名

  Returns
  -------
  html : str
    HTML ソース文字列
  """

  file = Path(Path.cwd()).joinpath('html').joinpath(fileName)
  html = file.read_text(encoding = 'utf-8')
  return html

def parseHtml(html):
  """
  BeautifulSoup でパースする

  Parameters
  ----------
  html : str
    HTML ソース文字列

  Returns
  -------
  soup : BeautifulSoup
    BeautifulSoup オブジェクト
  """

  soup = BeautifulSoup(html, 'html.parser')
  return soup

def scrape(soup):
  """
  スクレイピングして結果を Dict で返す

  Parameters
  ----------
  soup : BeautifulSoup
    BeautifulSoup オブジェクト

  Returns
  -------
  scrapedDict : dict
    スクレイピング結果を格納した辞書
  """

  # 辞書 (Dict) を用意する
  # 格納順序を保持する場合は 'import collections' し 'collections.OrderedDict()' で初期化する
  scrapedDict = {}

  # CSS セレクタ指定で要素を1つ取得してみる : select() を使うと CSS セレクタで取得できる
  scrapedDict['my_text'] = soup.select('a')[0].string
  print('my_text')
  print('  ' + scrapedDict['my_text'])

  # p 要素を全て取得してみる
  elements = soup.find_all('a')
  # リストを宣言する
  elementList = []
  print('a_elements')
  # 配列の長さを取得してループすることで index を取得する
  # index が不要なら 'for element in elements:' としても良い
  for index in range(len(elements)):
    element = elements[index]
    paragraphString = element.string
    print(f'  [{index}] : {paragraphString}')
    elementList.append(paragraphString)
  # 辞書に格納する
  scrapedDict['a_elements'] = elementList

  return scrapedDict

def writeJson(scrapedDict, fileName):
  """
  辞書を JSON に変換して書き出す

  Parameters
  ----------
  scrapedDict : dict
    辞書
  fileName : str
    保存ファイル名
  """

  jsonFile = Path(Path.cwd()).joinpath('json').joinpath(fileName)
  with jsonFile.open('w', encoding = 'utf-8', newline = None) as file:
    # Unicode 出力しないようにする
    json.dump(scrapedDict, file, indent = 2, ensure_ascii = False)

# 本ファイルをインポートした時に main() 関数が実行されないようにする
if __name__ == '__main__':
  main()