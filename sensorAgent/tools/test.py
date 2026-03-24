from .singapore_time import singapore_time
from .singapore_weather import singapore_weather
from .singapore_news import singapore_news
from .wiki_tool import wiki_tool

def test_print_all():
    #print(singapore_time())
    #print("\n" + singapore_weather())
    #print("\n" + singapore_news())
    print("\n" + wiki_tool("Artificial Intelligence"))

test_print_all()