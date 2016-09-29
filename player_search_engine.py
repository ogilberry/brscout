"""Scouting Tool for Blackoutrugby.com (C) 
Made by Jordan Ogilvy, September 2015
"""

import json
import urllib.request
from stack import stack
import time 
import datetime
import operator
import requests		
import math
import os
		
class scouted_player:
	#an object that describes the details of a BR player
	def __init__(self, player_data_dict):
		self.name = player_data_dict["name"]
		self.csr = int(player_data_dict["csr"]) #a string
		self.nationality = player_data_dict["nationality"]
		self.age = int(player_data_dict["age"]) #a string? not sure
		self.weight = int(player_data_dict["weight"])
		self.height = int(player_data_dict["height"])
		self.id = player_data_dict["id"]
		self.birthday = "R{0}D{1}".format(player_data_dict["birthday"][0:2], player_data_dict["birthday"][3])
			
	def fix_name(self):
		#change \\ to \ so unicode encoding with escaped characters will work
		self.name=bytes(self.name, "utf-8").decode("unicode_escape")
	
	def __repr__(self):
		return self.name + ", ID: " + self.id
		
	def __str__(self):
		return self.name

class Results:
	#an object that makes accessing and changing the scouted_list list from another file possible
	def __init__(self):
		self.scouted_list = []
	
def api_make_request(request_str):
	#makes  a request to the br api with the specified request, in the form &r=request_str.
	#examples for request str are m, p&teamid=xxxxx, must be a string
	#returns a string, data, in json format which contains information for a python type
	baseurl = "http://api.blackoutrugby.com"
	# construct full request URL
	url = "/?d=" + devid + "&dk=" + devkey + "&r=" + request_str + "&memberid=" + memberid + "&json=1"
	# issue request
	r = connection.get(baseurl + url)
	# read data, returns as a string
	r = str(r.text)
	return r

def json_to_python_object(data):
	#takes data, a string with proper json formatting, and converts to a python type, such as
	#a dict or list. returns the new object, and tries to clean up any incorrect formatting in
	#the input string.

	#Sometimes, some fields will contain strings with invalid json formatting
	#This tries to fix it, but may not work in all scenarios
	try:
		data = json.loads(data)
	except ValueError:
		#a common error was \uxxxx characters having the \ escaped as \\ from previous processing, making it unloadable
		acceptable_chars = "/\\bfnrtu" #only characters allowed to follow a \
		for i in range(0, len(data) - 1):
			if len(data) == i + 1:
				break
			if data[i] == "\\" and data[i+1] not in acceptable_chars:
				data = data[:i] + data[i+1:]
				data = json.loads(data)
	return data		
		
def request_team_dict(teamid):
	#returns a dictionary containing information for every player in the team
	#teamid must be a string
	request = "p&teamid=" + teamid 
	data = api_make_request(request)
	data = json_to_python_object(data)
	return data
	
def request_teamids(starting_ranking, teamid_stack):
	#gets the teamids of 100 teams, in order of increasing world ranking from the integer/string starting_ranking. #starting_ranking must be changed outside of this function
	#returns nothing, but MODIFIES the stack teamid_stack, pushing the next 100 team ids from the rankings onto it
	#Should only be called from update_database
	#Stops modifying the teamid_stack when it reaches the bot teams, which it checks by seeing if the ranking points is equal to 25. 
	request = "rk&start=" + str(starting_ranking)
	data = api_make_request(request)
	data = json_to_python_object(data)
		
	#add the team ids to the stack, UNLESS it is a bot team. (bot teams have ranking points of 25.0000)
	for ranking, team_info in data['rankings'].items():
		if not team_info['points'] == '25':
			teamid_stack.push(team_info['id'])
			
	return data
	
def update_database():
	#this is a very big function and a very time consuming function.
	#requests the team id of every team in the world via the rankings, 
	#then requests the information of every player in each team,
	#And creates one dictionary containing every team, which is a dictionary containing all of its players
	#The dictionary is then saved locally as a json file. The function returns None
	#from 0-120 seconds, make a request once every 3 seconds as requested in the api docs
	#from 120-240 seconds, make a request every 1 seconds
	#from 240+ seconds, request at will. This gives the br servers time to adjust to the large load
	current_ranking_index = 0
	ranking_request_string = "rk&start=" + str(current_ranking_index)
	teamid_stack = stack()
	unsuccessful_teamid_stack = stack()
	#these two variables will be used to check if all of the team ids have been collected
	#if they are the same number, no more teams are being added, therefore we are finished collecting
	previous_number_teams = None
	current_number_teams = 0
	
	database_dict = {}
	
	#timing controls
	can_request = True
	finished = False
	request_interval = 3 #time in seconds between each request to the API
	time_zero = time.clock() #start the clock
	start = time_zero
	
	print("starting while loop: " + str(time.ctime()))
	while not finished:
		end = time.clock()
		time_since_request = end-start
		total_time = end - time_zero
		
		if 120<total_time<240:
			request_interval = 1
		elif total_time>240:
			request_interval = 0
		
		if time_since_request >= request_interval:
			can_request = True
			start = time.clock()
			
		#If we haven't yet got every teams id, make one request for more
		if can_request and previous_number_teams != current_number_teams:
			print("requesting ids from rankings: " + str(time.ctime()))
			request_teamids(current_ranking_index, teamid_stack)
			#the api can only return 100 teams per request from the rankings
			current_ranking_index = current_ranking_index + 100
			can_request = False
			previous_number_teams = current_number_teams
			current_number_teams = teamid_stack.size()
		
		#if we have every team id, and have not processed all of them yet, request their players' information
		elif can_request and not teamid_stack.is_empty():
			current_teamid = teamid_stack.pop()
			try:
				print("requesting team dict: " + str(time.ctime()))
				current_team_dict = request_team_dict(current_teamid)
				database_dict[current_teamid] = current_team_dict
			except:
				print("Error adding team ID " + current_teamid + " team information dictionary on attempt 1")
				unsuccessful_teamid_stack.push(current_teamid)
				
			can_request = False
		#else everything must be finished, so exit the loop	
		elif can_request:
			print("exiting first while loop: " + str(time.ctime()))
			finished = True
			
	#Try to add the unsuccessful teamids again
	print("adding unsuccessful team ids: " + str(time.ctime()))
	for i in range(2,10):
		unsuccessful_teamid_stack = attempt_add_unsuccessful_teams(unsuccessful_teamid_stack, i)
		
	#once the database is finished, save it to the computer
	print("exited second while loop, starting file write: " + str(time.ctime()))
	with open("player_database.json", 'w') as fp:
		json.dump(database_dict, fp)
		fp.close()
		print("Database updated.")
	print("finished writing database file: " + str(time.ctime()))
		
	#change the date of the last update variable to today
	last_update, days_ago = update_last_update()
	days_ago = get_last_update()
	update_br_date()
	last_update_brtime = get_last_brdate()
	
def attempt_add_unsuccessful_teams(team_stack, attempt_no):
	#attempt to add the team info from the given team id in the team stack to the database, print error if not successful
	#returns a stack of team ids that were not successful, for another attempt
	new_stack = stack()
	while not team_stack.is_empty():
		current_id = team_stack.pop()
		try:
			current_team_dict = request_team_dict(current_id)
			database_dict[current_id] = current_team_dict
		except:
			new_stack.push(current_id)
			print("Error adding team ID {0} team information on attempt number {1}".format(str(current_id), str(attempt_no)))
			
	return new_stack
		
def load_database_dict():
	#Load the database dictionary from the lcoal json file and return it as a python dictionary.
	#Every key in the database is a teamid, whos value is a dictionary of all of that
	#teams players ids as keys, which have all the players information as another dictionary.
	with open("player_database.json", 'r') as fp:
		data = json.load(fp)
		fp.close()
	return data	

def search_team(team_dict):
	#Searches for matching players in ONE team.
	#Loops through every player in the specified team dictionary, and creates player objects for the
	#players who meet the search criteria, then adds them to the list of players who meet the criteria
	#creates a player object and modifies results.scouted_list, returns nothing
	for player, player_data_dict in team_dict.items():
		if player_data_dict["nationality"] == target_nationality or (player_data_dict["dualnationality"] == target_nationality and include_dual_nat == True) or target_nationality == 'Any':
			if min_weight <= int(player_data_dict["weight"]) <= max_weight:
				if min_height <= int(player_data_dict["height"]) <= max_height:
					if min_age <= int(player_data_dict["age"]) <= max_age:
						if min_csr <= int(player_data_dict["csr"]) <= max_csr:
							if check_u20_eligibility:
								#if under 20 or already turned 20 this season
								if int(player_data_dict["age"])<20 or (int(player_data_dict["age"])==20 and (int(player_data_dict["birthday"][0:2])<last_update_brtime[0] or (int(player_data_dict["birthday"][0:2])==last_update_brtime[0] and int(player_data_dict["birthday"][-1])<=last_update_brtime[1]))):
									results.scouted_list.append(scouted_player(player_data_dict))
							else:
								results.scouted_list.append(scouted_player(player_data_dict))
	
def search_database():
	#loops through every team in the database dictionary and searches them for players
	#returns nothing, modifies the list results.scouted_list with target player objects
	results.scouted_list=[]
	team_dicts = database_dict.values()
	for team in team_dicts:
		team = team['players']
		search_team(team)

def sort_by_field(field_str, sort_order):
	#sorts results.scouted_list by the specified player field(e.g. height) in either ascending or descending order 
	if sort_order == 'ascending':
			results.scouted_list = sorted(results.scouted_list, key=operator.attrgetter(field_str), reverse = True)
	else:
			results.scouted_list = sorted(results.scouted_list, key=operator.attrgetter(field_str))
		
def update_last_update(): 
	#returns datetime.date object of last update, and the days since that (which will be 0 just after updating)
	today = datetime.date.today()
	last_update = today
	return last_update, 0

def update_br_date():
	#record the date that the database was updated in terms of br time, save it to a local file for persistency
	#the request 'xx' is a nonsense request, but every call to the api always returns the current dates and br state
	xx=api_make_request("xx")
	xx = xx[xx.rfind("{"):len(xx)-1]
	date_dict = json.loads(xx)
	last_update_brtime[0] = int(date_dict["round"])
	last_update_brtime[1] = int(date_dict["day"])
	#save it in a file so it is persistent
	f = open("br_date.file", 'w')
	f.write(str(date_dict["round"]) + " " + str(date_dict["day"]))
	f.close()
	return [int(date_dict["round"]), int(date_dict["day"])]
	
def get_last_update():
	#returns a string of a number indicating how many days it has been since the last database update
	today = datetime.date.today()
	
	try:
		mtime = os.path.getmtime('player_database.json')
	except OSError:
		mtime = 0
		
	last_update = datetime.date.fromtimestamp(mtime)
	days_ago = str((today-last_update).days)
	return days_ago
	
def get_last_brdate():
	#get the date of the last database update in terms of BR time, return as a list [round, day]
	infile = open("br_date.file", 'r')
	contents = infile.read()
	infile.close()
	datelist = contents.split(" ")
	for i in range(len(datelist)):
		datelist[i] = int(datelist[i])
	return datelist

#user information needed for API requests, used in lots of functions. These should be kept secret and hidden from the user
devid = ""
devkey = ""
iv = ""
memberid = ""

#load the database_dict at the start rather than loading it every search.
database_dict = load_database_dict()

#search information initialised as integers 
#these are accessed and changed by the gui program
target_nationality = "PL"
include_dual_nat = False
check_u20_eligibility = False
min_csr = 0
max_csr =0
min_age = 0
max_age = 0
min_weight = 0
max_weight = 0
min_height = 0
max_height = 0		

#The single connection
connection = requests.Session()
				
#create the object that contains the found players
results = Results()

#the date the database was last updated, and finds the days since that date, in YYYY-MM-DD
days_ago = get_last_update()
last_update_brtime = get_last_brdate() #a list, in format of [Round, Day], integers.

