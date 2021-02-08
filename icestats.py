import datetime, os, time, xml.dom.minidom, urllib2 as U

mgr = U.HTTPPasswordMgrWithDefaultRealm()
uri = "http://icecast:8000/admin/stats"
mgr.add_password(None, uri, "user", "password")
os.mkdir("lock")
try:
	root = xml.dom.minidom.parseString(U.build_opener(U.HTTPBasicAuthHandler(mgr)).open(uri).read()).documentElement
	timestamp = datetime.datetime.now().isoformat() + "%+03d" % (time.timezone / 3600)
	root.setAttribute("timestamp", timestamp)
	with open("stats.xml", "r+") as f:
		f.seek(-8, 2)
		f.write(root.toxml("UTF-8") + "\n</stats>")
except Exception as e:
	pref = os.path.exists("error.log") * "\n"
	with open("error.log", "a") as f: f.write(pref + timestamp + " " + str(e))
os.rmdir("lock")
