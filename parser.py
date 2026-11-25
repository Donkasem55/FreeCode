import xml.etree.ElementTree as ET

def getxml(filename):
	xml = ET.parse(filename).getroot()
	return xml

def preprocess(xml):
	ret = []
	for i in xml:
		if i.tag == "include":
			x = getxml(i.attrib["src"])
			x = preprocess(x)
			ret += x
		else:
			ret.append(i)

	return ret

def compile(xml):
	head = []
	body = []
	for i in xml:
		if i.tag == "css":
			head.append(f"<link rel=\"stylesheet\" href=\"{i.attrib["src"]}\">")
		elif i.tag == "js":
			body.append(f"<script src=\"{i.attrib["src"]}\">")
		elif i.tag == "head":
			h = compile(i)
			head += h[0]
			head += h[1]
		elif i.tag == "body":
			h = compile(i)
			body += h[0]
			body += h[1]
		else:
			h = f"<{i.tag}"
			for j in i.attrib:
				h += f" {j}=\"{i.attrib[j]}\""
			h += ">"
			f = compile(i)

			for j in f[0]:
				if i.tag not in ["a", "button"]:
					h += "\n"
				h += j
			for j in f[1]:
				if i.tag not in ["a", "button"]:
					h += "\n"
				h += j
			if i.text:
				h += i.text.replace("\n", "").replace("\t", "")
			if i.tag == "div":
				h += "\n"
			h += f"</{i.tag}>"
			body.append(h)

	return head, body

def parsefle(file):
	pped = preprocess(getxml(file))
	html = compile(pped)
	string = "<!DOCTYPE html>\n<html>\n<head>\n"
	for i in html[0]:
		string += i + "\n"
	string += "</head>\n<body>\n"
	for i in html[1]:
		string += i + "\n"
	string += "</body>\n</html>"

	return string
