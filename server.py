from urllib import parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/adminproduct.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        body = parse.unquote(body.decode('utf-8'))
        print(body)

        #conseguir la imagen
        #Generar nombre
        url = body['url'].split('=')
        print(url)
        name = body['name']
        print(name)
        #guardar la imagen
        urllib.request.urlretrieve(url, image_name)
        #redireccionar
        self.send_response(301)
        # self.send_header('Location', '/')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

# Iniciar el servidor
print('Starting server...')
server = HTTPServer(('localhost', 8080), RequestHandler)
server.serve_forever()
