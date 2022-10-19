from http.client import FORBIDDEN
from ascii_graph import Pyasciigraph
from ascii_graph.colordata import vcolor
from ascii_graph import colors
import argparse
from ast import arg

# obsluga argumentow
parser = argparse.ArgumentParser()
parser.add_argument('file_name')
parser.add_argument('-w', '--number_of_words', default=10)
parser.add_argument('-l', '--number_of_letters', default=0)
parser.add_argument('-i', '--ignore_words', nargs='*', default=[])
parser.add_argument('-c', '--contain_string', default='')


args = parser.parse_args()

file_name = args.file_name
num_of_words = int(args.number_of_words)
num_of_letters = int(args.number_of_letters)
ignored_words = args.ignore_words
contains = args.contain_string

slownik = {}

# otwieramy plik
with open(file_name, 'r', encoding="utf8") as f:
    for line in f:
        for word in line.strip().split(' '):
            # pozbycie sie znakow specjalnych
            word = word.replace(',', '')
            word = word.replace('?', '')
            word = word.replace('.', '')
            word = word.replace('!', '')
            word = word.replace('"', '')
            word = word.replace(';', '')
            word = word.replace(':', '')
            word = word.replace('(', '')
            word = word.replace(')', '')

            # nie zapisujemy slow ktore sa za krotkie LUB sa slowami podanymi jako zakazane
            if len(word) < num_of_letters:
                continue
            
            # nie rozumiem czemu to nie dziala 
            # if any(word == forbidden for forbidden in ignored_words):
            #    continue
            
            # pozbycie sie wielkich liter
            word = word.lower()
            # sprawdzamy czy znalezione slowo zawiera podany ciag znakow
            if not (contains in word):
                continue
            # zliczanie slow w slowniku (jesli slowo nie wystepuje dopisujemy je z wartoscia 1)
            if word in slownik:
                slownik[word] += 1
            else:
                if not(any(word == forbidden for forbidden in ignored_words)): #tutaj smiga, ale jak probowalem ifa z continue to slowo wykluczone nadal sie przesligiwalo ale w mniejszej liczbie wystapien.
                    slownik[word] = 1
                

# sortujemy slowa od najczesciej wystepujacych
hist = dict(sorted(slownik.items(), key=lambda x: x[1], reverse=True))

# przycinamy do wymaganej liczby slow
final_hist = (list(hist.items())[:num_of_words])

# rysujemy histogram
graph = Pyasciigraph()
pattern = [colors.Gre, colors.Pur, colors.Yel, colors.Red, colors.Cya]
data = vcolor(final_hist, pattern)
for line in graph.graph("Histogram of word's frequency", data):
    print(line)
