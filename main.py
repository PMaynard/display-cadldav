import vobject
from jinja2 import Template
from os import listdir
from os.path import isfile, join

# cal_location - has to be a direcotry. It will read all files with an extention .ics.

cal_location = "/home/osaka/.calendars/work.ics/"
template_location = "./index.template"
html_location = "./public_html/index.html"

events = [f for f in listdir(cal_location) if isfile(join(cal_location, f)) and f.endswith('.ics')]

cal_events = []

for e in events: 
	try: 
		cal = vobject.readOne(open(join(cal_location, e), 'rb').read())
		for ev in cal.vevent_list:
			cal_events.append(ev)
	except:
		print "> Unable to read: ", e, "\n"

events_data = ""
for event in cal_events:
	events_data += "{{\n title : \"{0}\",\n start : '{1}',\n end : '{2}'\n}},\n".format(event.getChildValue('summary'), event.getChildValue('dtstart'), event.getChildValue('dtend'))

events_data = "[" + events_data[:-2] + "]"


template = Template(open(template_location, 'rb').read())
output = open(html_location, 'w')
output.write(template.render(events_data=events_data))

