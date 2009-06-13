import datetime
import logging
import os

from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Map(webapp.RequestHandler):
  WIDTH = 857
  HEIGHT = 699
  
  def get(self):
    shengs = []
    for p in self.request.arguments():
      if len(p) == 2:
        shengs.append(p)

    shengs.sort()
    
    w = int(self.request.get('w', self.WIDTH))
    h = int(self.request.get('h', self.HEIGHT))
    
    cache_key = '%s&w=%s&h=%s' % ('&'.join(shengs), w, h)
    img = memcache.get(cache_key)
    if img is None:
      img = self.create_map(shengs, w, h)
      memcache.add(cache_key, img, 3600)
    
    self.write(img)
  
  def create_map(self, shengs, w, h):
    shengs = ['base'] + shengs
    img = images.composite(
      [(self.load(sheng), 0, 0, 1.0, images.TOP_LEFT) for sheng in shengs], 
      self.WIDTH, self.HEIGHT)
      
    if w != self.WIDTH or h != self.HEIGHT:
      img = images.resize(img, w, h)

    return img
  
  def write(self, img):
    self.response.headers['Content-Type'] = 'image/png'
    self.response.headers.add_header('Expires', 
      (datetime.datetime.utcnow() + datetime.timedelta(365)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
    self.response.out.write(img)
  
  def load(self, name):
    f = open('./map/%s.png' % name, 'rb')
    data = f.read()
    f.close()
    return data
    

class PrintEnvironmentHandler(webapp.RequestHandler):
  def get(self):
    for name in os.environ.keys():
      self.response.out.write("%s = %s<br />\n" % (name, os.environ[name]))
      
    for n in self.request.arguments():
      self.response.out.write("%s = %s<br />\n" % (n, self.request.get(n)))
      
application = webapp.WSGIApplication(
                                     [('/', Map),
                                     ('/env', PrintEnvironmentHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()