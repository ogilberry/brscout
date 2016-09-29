##import base64
import urllib.request

#user information
devid = "722"
devkey = "IU6dmDkK9RiZ2twX"
iv = "VD1PvRq5Cm8OPioN"
memberid = "91675"

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