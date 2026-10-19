"""Offline structural and HTTP checks; no browser or live venue assertions."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
ROOT = Path(__file__).resolve().parent
class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []; self.links = []; self.frames = []; self.styles = []; self.articles = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a': self.links.append(a)
        if tag == 'iframe': self.frames.append(a)
        if tag == 'link' and a.get('rel') == 'stylesheet': self.styles.append(a['href'])
        if tag == 'article' and a.get('class') == 'stop': self.articles.append(a['id'])
html = (ROOT / 'index.html').read_text()
p = SiteParser(); p.feed(html)
assert len(p.ids) == len(set(p.ids)), 'Duplicate IDs'
assert p.articles == [f'stop-{n}' for n in range(1,8)]
for a in p.links:
    href = a['href']
    if href.startswith('#') and href != '#': assert href[1:] in p.ids, href
    if a.get('target') == '_blank': assert 'noopener' in a.get('rel','')
    if '://' in href: assert urlparse(href).scheme == 'https'
for file in p.styles: assert (ROOT / file).is_file()
assert len(p.frames) == 1 and p.frames[0]['name'] == 'tour-map'
pins = [a for a in p.links if a.get('target') == 'tour-map']
assert len(pins) == 7
for a in pins:
    q = parse_qs(urlparse(a['href']).query)
    lat, lon = map(float,q['marker'][0].split(','))
    west,south,east,north = map(float,q['bbox'][0].split(','))
    assert west < lon < east and south < lat < north
    assert 55.94 < lat < 55.97 and -3.23 < lon < -3.18
route = next(a for a in p.links if 'route-link' in a.get('class',''))
q = parse_qs(urlparse(route['href']).query)
assert q['destination'] == ['Gaucho Edinburgh']
assert len(q['waypoints'][0].split('|')) == 5
assert '19:00' in html.split('id="stop-7"')[1].split('</article>')[0]
assert (ROOT / '.nojekyll').is_file()
css = (ROOT / 'styles.css').read_text()
assert '@media print' in css and 'prefers-reduced-motion' in css and ':focus-visible' in css
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT.parent),**kwargs)
    def log_message(self,*args): pass
server = ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread = Thread(target=server.serve_forever,daemon=True); thread.start()
try:
    base = f'http://127.0.0.1:{server.server_port}/{ROOT.name}/'
    for path,content_type in [('', 'text/html'),('styles.css','text/css')]:
        with urlopen(base+path) as response:
            assert response.status == 200
            assert content_type in response.headers['Content-Type']
            assert response.read()
finally:
    server.shutdown(); server.server_close(); thread.join()
print('PASS: 7 ordered stops, 7 valid map pins, links/anchors, Gaucho finale, Pages subpath HTTP, print/accessibility CSS hooks.')
