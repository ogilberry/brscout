##import base64
import urllib.request

#user information - add your own
devid = ""
devkey = ""
iv = ""
memberid = ""

baseurl = "http://api.blackoutrugby.com/"
request = "rk&start=20000" #refer to the docs, you don't need the &r= part here

# suffix with member details
request = request + "&memberid=" + memberid

# construct full request URL
url = baseurl + "?d=" + devid + "&dk=" + devkey + "&r=" + request + "&json=1"
print(url)

# issue request
u = urllib.request.urlopen(url)

# read data, returns as a string
data = u.read()
