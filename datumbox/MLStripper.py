import HTMLParser

class MLStripper(HTMLParser.HTMLParser):
    def __init__(self):
    self.reset()
    self.fed = []
    
    def handle_data(self, d):
    	self.fed.append(d)
    
    def get_fed_data(self):
        return ''.join(self.fed)
