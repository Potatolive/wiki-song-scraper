import urllib2
import traceback
import scraperwiki           
from lxml import etree
import songs as songGetter
import lxml.html           
import json

def movies(moviesUrl):
  movies = []
  songs = []

  html = scraperwiki.scrape(moviesUrl)
  root = lxml.html.fromstring(html)
  tables = root.xpath('//table[@class="wikitable"]')
  for table in tables:
    trs = table.cssselect('tr')
    title = -1
    director = -1
    cast = -1
    genre = -1
    producer = -1
    for tr in trs:
      ths = tr.cssselect('th')
      i = 0
      if(len(ths) > 0):
        for th in ths:
          if(th.text_content() == "Title"):
            title = i
          # if(th.text_content() == "Director"):
          #   director = i
          # if(th.text_content() == "Cast"):
          #   cast = i
          # if(th.text_content() == "Genre"):
          #   genre = i
          # if(th.text_content() == "Producer"):
          #   producer = i
          i += 1
      else:        
        tds = tr.cssselect('td')

        shiftRight = -1
        for td in tds:
          if('rowspan' in td.attrib):
            shiftRight += 1

        rowContent = {}
        if(title >= 0): 
          if(title + shiftRight < len(tds)):
            rowContent['MovieTitle'] = tds[title + shiftRight].text_content()
            anchors = tds[title + shiftRight].cssselect('a')
            for anchor in anchors:
              rowContent['MovieUrl'] = "https://en.wikipedia.org" + anchor.attrib['href']
        print rowContent
        # if(director >= 0): 
        #   rowContent['director'] = tds[director + shiftRight].text_content()
        # if(cast >= 0): 
        #   rowContent['cast'] = tds[cast + shiftRight].text_content()
        # if(genre >= 0 and len(tds) > genre): 
        #   rowContent['genre'] = tds[genre + shiftRight].text_content()
        # if(producer >= 0): 
        #   rowContent['producer'] = tds[producer + shiftRight].text_content()
        # print rowContent
        movies.append(rowContent)

        try:
          mSongs = songGetter.songs(rowContent)
          if(mSongs != None):
            songs += mSongs
        
        except urllib2.HTTPError as err:
          pass
        except Exception as e:
          print rowContent
          print e
          print traceback.format_exc()
          pass
  return songs

def main():
  songs = movies("https://en.wikipedia.org/wiki/List_of_Tamil_films_of_2017")
  with open('songs.json', 'w') as f:
    f.write(json.dumps(songs))

if __name__ == "__main__":
    main()
