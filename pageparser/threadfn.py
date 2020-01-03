import requests
import json
from pageparser.parseutil import CustomParser

def parse_endpoint(name, url=None, min_word_count = 1):
    '''
        IF it's a tuple then it's a threaded call from the controller 
        and we need to unpack it. 
    '''
    if isinstance(name, tuple):
        if len(name) != 3:
            raise Exception("Incorrect argument count...")
        url = name[1]
        min_word_count = name[2]
        name = name[0]

    r = requests.get(url)
    
    return_result = None
    if r.status_code == 200:
        parser = CustomParser()
        content = r.content.decode("utf-8") 
        parser.feed(content)
        return_result = {'name' : name, 'target' : url, 'content' : { 'images' : parser.getUniqueImages() , 'data' : parser.getPageData(min_word_count) , 'links' : parser.getUniqueLinks()} }
    else:
        return_result = {'name' : name, 'target' : url, 'content' : { 'images' : None , 'data' : None , 'links' : None} }


    return return_result
