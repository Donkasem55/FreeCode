from wsgiref.simple_server import make_server
import sys
from parser import parsefle


if sys.argv[1:] == []:
	port = 8000
else:
	port = sys.argv[1]

def getpage(filename, path):
	html = parsefle("html/" + filename)

	return html

def getcss(filename):
	with open(f"html/{filename}") as f:
		css = f.read()
	return css

def homepage():
	page = getpage("index.xml", [])
	return page.replace("{titlesign}", "Home")

def course(path):
	
	return (f"{path}", "200 OK")

def server(environ, start_response):
	path_info = environ['PATH_INFO']
	path = path_info.split("/")
	request_method = environ['REQUEST_METHOD']
	while "" in path:
		path.remove("")

	CT = "text/html"

	if request_method == "GET":
		if path == []:
			response_body = homepage().encode("utf-8")
			status = "200 OK"
		elif path[0] == "course":
			response_body, status = course(path)
			response_body = response_body.encode("utf-8")
		elif path[-1].endswith(".css"):
			response_body = getcss(path[-1]).encode("utf-8")
			CT = "text/css"
			status = "200 OK"
		elif path[-1].endswith(".svg"):
			response_body = getcss(path[-1]).encode("utf-8")
			CT = "image/svg+xml"
			status = "200 OK"

	headers = [('Content-type', CT)]
	start_response(status, headers)
	return [response_body]

print("Starting server...")
httpd = make_server('', port, server)
print(f"Serving on port {port}...")
httpd.serve_forever()
