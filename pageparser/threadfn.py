import requests
import json
from pageparser.parseutil import CustomParser

def parse_endpoint(name, url=None):
    '''
        IF it's a tuple then it's a threaded call from the controller 
        and we need to unpack it. 
    '''
    if isinstance(name, tuple):
        if len(name) != 2:
            raise Exception("Incorrect argument count...")
        url = name[1]
        name = name[0]

    r = requests.get(url)
    
    return_result = r.status_code
    if r.status_code == 200:
        parser = CustomParser()
        content = r.content.decode("utf-8") 
        parser.feed(content)

    return {'name' : name, 'target' : url, 'content' : { 'images' : parser.images , 'data' : parser.data , 'links' : parser.embedded_links} }
