import scraperwiki           
from lxml import etree
import lxml.html           

def songs(movie):
  songs = []
  movieInfo = {}
  # print movie['movieUrl']
  if('movieUrl' in movie):
    html = scraperwiki.scrape(movie['movieUrl'])
    #print html
    root = lxml.html.fromstring(html)

    tables = root.xpath('//table[@class="infobox vevent"]')
    if (len(tables) > 0):
      image = tables[0].xpath('//img')
      if(len(image) > 0): 
        movieInfo['moviePosterUrl'] = "https:" + image[0].attrib['src']

    for table in tables:
      trs = table.cssselect('tr')
      for tr in trs:
        ths = tr.cssselect('th')
        tds = tr.cssselect('td')
  
        if(len(ths) > 0 and len(tds) > 0):
          movieInfo[ths[0].text_content().replace('\n', ' ').replace('\r', '').strip().replace(' ', '_').lower()] \
            = tds[0].text_content().strip().replace('\n', ', ').replace('\r', '').strip()

    tables = root.xpath('//table[@class="tracklist" or @class="wikitable`"]')
    for table in tables:
      trs = table.cssselect('tr')
      ths = []
      for tr in trs:
        if(tr.cssselect('td')):
          song = {}
          tds = tr.cssselect('td')
          i = 0
          if(len(tds) == len(ths)):
            for td in tds:
              song[ths[i].text_content().strip().replace('\n', ' ').replace('\r', '').replace('.', '').replace('"', '')] \
                = tds[i].text_content().strip().replace('\n', ' ').replace('\r', '').replace('.', '').replace('"', '')
              i += 1
            song = dict(movie.items() + song.items() + movieInfo.items())
            if('Title' in song):
              print song
              songs.append(song)
        else:
          if(tr.cssselect('th')):
            ths = tr.cssselect('th')
  # print songs
  return songs

def main():
  movie = { 'movieUrl': 'https://en.wikipedia.org/wiki/Nadhi_Karaiyinile' }
  print songs(movie)

if __name__ == "__main__":
    main()
