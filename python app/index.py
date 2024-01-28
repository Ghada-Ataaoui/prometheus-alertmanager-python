from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import Counter,Histogram, start_http_server
import time
from random  import randint

hostName = "localhost"
serverPort = 8080

c = Counter('python_http_requests', 'counter for http requests')
h = Histogram('python_request_latency_seconds', 'latency',buckets=["1","2","3"])

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        start_time = time.time()
        c.inc()
        time.sleep(randint(0,3))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Python App</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>welcome to our python app</h1>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        h.observe(time.time()-start_time)


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    start_http_server(8000)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")