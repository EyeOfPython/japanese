'''
Created on 04.08.2014

@author: Tobias Ruck
'''

from http.server import SimpleHTTPRequestHandler
from urllib import parse
import random

class JapaneseWebServer(SimpleHTTPRequestHandler):
    
    enc = "utf-8"
    account = None
    
    def do_GET(self):
        r = []
        self.build_head(r)
        request = parse.urlparse(self.path)
        path = request.path
        query = parse.parse_qs(request.query)
        if path.startswith('/syllables'):
            self.view_syllables(r, query)
        if path.startswith('/letters'):
            self.view_letters(r, query)
        self.build_body(r)
        
        encoded = '\n'.join(r).encode(self.enc)
        self.send_headers(encoded)
        self.wfile.write(encoded)
        
    def view_table(self, table, r):
        a = 0
        r.append('<table>')
        for t in table:
            if a == 0:
                r.append('<tr>')
            r.append('<td>%s</td>' % (t,))
                
            a = (a+1) % 12
            if a == 0:
                r.append('</tr>')
        r.append('</table>')
        
    def view_syllables(self, r, q):
        s = ['n', 'wa', 'ra', 'ma', 'ha', 'ta', 'na', 'sa', 'ka', 'ya', 'a',
                  'wi', 'ri', 'mi', 'hi', 'chi','ni', 'shi','ki',       'i',
                        'ru', 'mu', 'fu', 'tsu','nu', 'su', 'ku', 'yu', 'u',
                  'we', 're', 'me', 'he', 'te', 'ne', 'se', 'ke',       'e',
                  'wo', 'ro', 'mo', 'ho', 'to', 'no', 'so', 'ko', 'yo', 'o']
        random.shuffle(s)
        self.view_table(s, r)
        
    def view_letters(self, r, q):
        a = list("アイウエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヰヱヲン")
        b = list("あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわゐゑをん")

        random.shuffle(a)
        random.shuffle(b)
        self.view_table(a, r)
        r.append('<p/>')
        self.view_table(b, r)
        
    def build_head(self, r):
        title = 'Overview' 
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % self.enc)
        r.append('''
<style>
td { border: 1px solid grey; 
     padding: 2px; }
.block { float: left; width: 300px; }
</style>
'''
                 )
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n')
        
    def build_body(self, r):
        r.append('\n</body>\n</html>\n')
        
    def send_headers(self, text):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % self.enc)
        self.send_header("Content-Length", str(len(text)))
        self.end_headers()

if __name__ == '__main__':
    import socketserver
    
    port = 4444
    
    Handler = JapaneseWebServer
    httpd = socketserver.TCPServer(("", port), Handler)
    print("Serve at port", port)
    httpd.serve_forever()