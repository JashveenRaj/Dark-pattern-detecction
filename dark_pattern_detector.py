from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/run':
            # Execute your Python code here
            subprocess.run(["python", "your_script.py"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Python code executed successfully')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
