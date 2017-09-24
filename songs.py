import scraperwiki           
from lxml import etree
import lxml.html
import uuid

def songs(movie):
  songs = []
  movieInfo = {}
  # print movie['movieUrl']
  if('MovieUrl' in movie):
    html = scraperwiki.scrape(movie['MovieUrl'])
    #print html
    root = lxml.html.fromstring(html)

    tables = root.xpath('//table[@class="infobox vevent"]')
    if (len(tables) > 0):
      image = tables[0].xpath('//img')
      if(len(image) > 0): 
        movieInfo['MoviePosterUrl'] = "https:" + image[0].attrib['src']

    for table in tables:
      trs = table.cssselect('tr')
      for tr in trs:
        ths = tr.cssselect('th')
        tds = tr.cssselect('td')
  
        if(len(ths) > 0 and len(tds) > 0):
          tagName = getTagName(ths[0].text_content())
          if(tagName <> None):
            movieInfo[tagName] \
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
              tagName = getTagName(ths[i].text_content())
              if(tagName <> None):
                song[tagName] \
                  = tds[i].text_content().strip().replace('\n', ' ').replace('\r', '').replace('.', '').replace('"', '')
              i += 1
            song = dict(movie.items() + song.items() + movieInfo.items())
            if('Title' in song):
              song["UniqueId"] = str(uuid.uuid4())
              print(song)
              songs.append(song)
        else:
          if(tr.cssselect('th')):
            ths = tr.cssselect('th')
  # print songs
  return songs

def getTagName(headerContent):
  tagName =  headerContent.strip().replace('\n', ' ').replace('\r', '').replace('.', '').replace('"', '').lower()
  
  tags = [
    { "key": "lyrics", "value":"Lyrics" },
    { "key": "no", "value":"NoInTheMovie" },
    { "key": "starring", "value":"Starring" },
    { "key": "music_by", "value":"MusicBy" },
    { "key": "written_by", "value":"WrittenBy" },
    { "key": "singers", "value":"Singers" },
    { "key": "movieurl", "value":"MovieUrl" },
    { "key": "cinematography", "value":"Cinematography" },
    { "key": "produced_by", "value":"ProducedBy" },
    { "key": "language", "value":"Language" },
    { "key": "movietitle", "value":"MovieTitle" },
    { "key": "release_date", "value":"ReleaseDate" },
    { "key": "edited_by", "value":"EditedBy" },
    { "key": "title", "value":"Title" },
    { "key": "box_office", "value":"BoxOffice" },
    { "key": "movieposterurl", "value":"MoviePosterUrl" },
    { "key": "production_company", "value":"ProductionCompany" },
    { "key": "directed_by", "value":"DirectedBy" }
  ]

  for tag in tags:
    if(tag["key"] == tagName): 
      return tag["value"]

  return None

def main():
  movie = { 'movieUrl': 'https://en.wikipedia.org/wiki/Bogan_(film)' }
  print songs(movie)

if __name__ == "__main__":
    main()
