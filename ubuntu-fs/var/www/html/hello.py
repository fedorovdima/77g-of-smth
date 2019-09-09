#!/usr/bin/env python3

#print("Content-type: text/html")
#print()
#print("<h1>Hello world!</h1>")

#from flup.server.fcgi import WSGIServer
def app(environ, start_response):
  start_response('200 OK', [('Content-Type', 'text/html')])
  return('''<p>Hello world!</p>
          Wanna <a href="static/image.png">image</a>?\n''')

if __name__ == '__main__':
  from flup.server.fcgi import WSGIServer
  WSGIServer(app).run()
