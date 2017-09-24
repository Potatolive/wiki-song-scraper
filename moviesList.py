import scraperwiki           
from lxml import etree
import movies as movieGetter
import lxml.html           
import json

def main():
  for i in range(1999, 2018):
    songs = movieGetter.movies("https://en.wikipedia.org/wiki/List_of_Tamil_films_of_" + str(i))
    print "Year: " + str(i) + " songs downloaded " + str(len(songs))
    with open('data/songs' + str(i) + '.json', 'w') as f:
      f.write(json.dumps(songs))

if __name__ == "__main__":
    main()
