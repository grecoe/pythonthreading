from html.parser import HTMLParser

class CustomParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.script_tags = False
        self.ignore_tags = ["script", "style"]
        self.images = []
        self.embedded_links = []
        self.data = []

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
            cleaned = data.strip()
            if cleaned:
                self.data.append(cleaned)

    def _parseExternalLink(self, attributes):
        for att in attributes:
            if att[0] == 'href':
                self.embedded_links.append(att[1])


    def _parseImageAttributes(self, attributes):
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
        return_data = None
        stripped = image_attribute.strip()
        if ' ' in  stripped:
            img_parts = stripped.split(' ')
            return_data = img_parts[0]
        else:
            return_data = stripped
        return return_data 
