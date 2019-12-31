import uuid
from html.parser import HTMLParser

class CustomParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.script_tags = False
        self.ignore_tags = ["script", "style"]
        self.images = []
        self.embedded_links = []
        self.data = []
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        if tag in self.ignore_tags:
            self.script_tags = True
        elif tag == 'img':
            self._parseImageAttributes(attrs)
        elif tag == 'a':
            self._parseExternalLink(attrs)
        elif tag == 'video':
            print("VIDEO: ", attrs)
        else:
            # You can inspect all tags/attrs at some point, just in case there is something
            # hidden in there.
            pass 
            #print(tag,attrs)

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            self.script_tags = False

    def handle_data(self, data):
        if not self.script_tags:
            if '\n' in data:
                self.buffer.append(data)
                if len(self.buffer) > 0:
                    buffer_content = ' '.join(self.buffer)
                    cleaned_buffer = buffer_content.strip()
                    if cleaned_buffer:
                        self.data.append(cleaned_buffer)
                self.buffer = []
            else:
                self.buffer.append(data)

        '''
        if not self.script_tags:
            cleaned = data.strip()
            if cleaned:
                self.data.append(cleaned)
        '''

    def getUniqueImages(self):
        return self._getUniqueEntries(self.images)

    def getUniqueLinks(self):
        return self._getUniqueEntries(self.embedded_links)

    def _getUniqueEntries(self, sequence):
        '''
            Given a sequence, get only the unique entries adn 
            create a dictionary where the key is a uuid. 
        '''
        return_entries = {}
        if len(sequence) > 0 :
            for item in list(set(sequence)):
                uid = uuid.uuid1()
                return_entries[str(uid)] = item
        return return_entries  

    def _parseExternalLink(self, attributes):
        '''
            Attribute parser for 'a' tags (links)
        '''
        for att in attributes:
            if att[0] == 'href':
                self.embedded_links.append(att[1])

    def _parseImageAttributes(self, attributes):
        '''
            Attribute parser for 'img' tags (images). Attributes
            can be either a set or a single image.
        '''
        for att in attributes:
            if att[0] == 'srcset':
                parts = att[1].split(',')
                for part in parts:
                    self.images.append(self._stripImage(part))
                break
            if att[0] == 'src':
                self.images.append(self._stripImage(att[1]))
                break

    def _stripImage(self, image_attribute):
        '''
            From an attribute, strip off any size information at the end
            of the image entry.
        '''
        return_data = None
        stripped = image_attribute.strip()
        if ' ' in  stripped:
            img_parts = stripped.split(' ')
            return_data = img_parts[0]
        else:
            return_data = stripped
        return return_data 
