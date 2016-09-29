"""A GUI Application for scouting players in Blackout Rugby.
Made by Jordan Ogilvy, 17/09/2015
"""
	
import player_search_engine
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
import threading
import time

class scouting_tool(tk.Tk):
	def __init__(self, parent):
		tk.Tk.__init__(self, parent)
		self.root = parent
		#create the gui
		self.draw_search_panel()
		self.draw_results_panel()
		#variable for the maximum number of results the gui will display in one search
		self.max_results = 300
		
		#set the ttk theme/style
		s = ttk.Style()
		s.theme_use('vista')
			
	def draw_search_panel(self):
		#initialise the grid implementation
		self.grid()
		
		#the panel which holds the search & update buttons, and all the search field entry boxes
		self.search_field_panel = tk.Frame(self.root, height=310, width=80)
		self.search_field_panel.pack(side='left', fill='both', expand=0, padx=5)
		
		#button that updates the database. Date of last update is shown below it
		self.empty_block0 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block0.grid(row=1, column=1, columnspan=3)
		self.update_button = ttk.Button(self.search_field_panel, text = "Update Database")
		self.update_button.grid(row=2, column=1, columnspan=3)
		self.update_button.bind("<Button-1>", lambda event: self.draw_update_popup())
		self.last_update = tk.Label(self.search_field_panel, text = "Last updated " + player_search_engine.days_ago + " days ago")
		self.last_update.grid(row=3, column=1, columnspan=3)
		self.empty_block1 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block1.grid(row=4, column=1, columnspan=3)
		
		#button that begins the search with the current field entries, then shows the result
		self.search_button = ttk.Button(self.search_field_panel, text = "Search")
		self.search_button.grid(row=5, column=1, columnspan=3)
		self.search_button.bind("<ButtonRelease-1>", self.search)
		self.search_button.bind("<Return>", self.search)
		self.empty_block2 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block2.grid(row=6, column=1, columnspan=3)
		
		#search fields for nationality
		self.nat_label = tk.Label(self.search_field_panel, text="Nationality: ")
		self.nat_label.grid(row=7, column=1, columnspan=2)
		self.nat_options = ["Any","AR","AU","BE","BR","CA","CL","HR","CZ","EN","FR","GE","DE","HK","IE","IT","CI","JP","KE","NA","NL","NZ","PI","PL","PT","RO","RU","SL","ZA","KR","ES","US","UY","WA","ZW"]
		self.nat_list = ttk.Combobox(self.search_field_panel, width=5)
		self.nat_list['values'] = self.nat_options
		self.nat_list.current(0)
		self.nat_list.grid(row =7, column=3, pady=3)
		
		#checkbox and text for including dual nationality players, wrapped in a frame
		self.dual_check_frame = tk.Frame(self.search_field_panel)
		self.dual_check_frame.grid(row=8, column=1, columnspan=3)
		self.dual_label = tk.Label(self.dual_check_frame, text="Include Dual Nationality:")
		self.dual_label.pack(side='left')
		self.include_dual_nat = tk.BooleanVar()
		self.dual_check = ttk.Checkbutton(self.dual_check_frame, variable=self.include_dual_nat)
		self.dual_check.pack(side='right')
		self.empty_block2 = tk.Frame(self.search_field_panel, width = 150, height = 4)
		self.empty_block2.grid(row=9, column=1, columnspan=3)
		
		#checkbox for U20 eligibility
		self.u20_check_frame = tk.Frame(self.search_field_panel)
		self.u20_check_frame.grid(row=10, column=1, columnspan=3)
		self.u20_label = tk.Label(self.u20_check_frame, text="Eligible for U20:")
		self.u20_label.pack(side='left')
		self.check_u20_eligible = tk.BooleanVar()
		self.u20_check = ttk.Checkbutton(self.u20_check_frame, variable=self.check_u20_eligible)
		self.u20_check.pack(side='right')
		self.empty_block6 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block6.grid(row=11, column=1, columnspan=3)
		
		#search fields for csr
		self.min_csr_label = tk.Label(self.search_field_panel, text="Min CSR")
		self.min_csr_label.grid(row=12, column=1)
		self.max_csr_label = tk.Label(self.search_field_panel, text="Max CSR")
		self.max_csr_label.grid(row=12, column=3)
		self.min_csr_box = ttk.Entry(self.search_field_panel, width=8)
		self.min_csr_box.grid(row=13, column=1)
		self.max_csr_box = ttk.Entry(self.search_field_panel, width=8)
		self.max_csr_box.grid(row=13, column=3)
		
		#search fields for age
		self.empty_block3 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block3.grid(row=14, column=1, columnspan=3)
		self.min_age_label = tk.Label(self.search_field_panel, text="Min Age")
		self.min_age_label.grid(row=15, column=1)
		self.max_age_label = tk.Label(self.search_field_panel, text="Max Age")
		self.max_age_label.grid(row=15, column=3)
		self.min_age_box = ttk.Entry(self.search_field_panel, width=8)
		self.min_age_box.grid(row=16, column=1)
		self.max_age_box = ttk.Entry(self.search_field_panel, width=8)
		self.max_age_box.grid(row=16, column=3)
		
		#search fields for height
		self.empty_block4 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block4.grid(row=17, column=1, columnspan=3)
		self.min_height_label = tk.Label(self.search_field_panel, text="Min Height (cm)")
		self.min_height_label.grid(row=18, column=1)
		self.max_height_label = tk.Label(self.search_field_panel, text="Max Height")
		self.max_height_label.grid(row=18, column=3)
		self.min_height_box = ttk.Entry(self.search_field_panel, width=8)
		self.min_height_box.grid(row=19, column=1)
		self.max_height_box = ttk.Entry(self.search_field_panel, width=8)
		self.max_height_box.grid(row=19, column=3)
		
		#search fields for weight
		self.empty_block5 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block5.grid(row=20, column=1, columnspan=3)
		self.min_weight_label = tk.Label(self.search_field_panel, text="Min Weight (kg)")
		self.min_weight_label.grid(row=21, column=1)
		self.max_weight_label = tk.Label(self.search_field_panel, text="Max Weight")
		self.max_weight_label.grid(row=21, column=3)
		self.min_weight_box = ttk.Entry(self.search_field_panel, width=8)
		self.min_weight_box.grid(row=22, column=1)
		self.max_weight_box = ttk.Entry(self.search_field_panel, width=8)
		self.max_weight_box.grid(row=22, column=3)
		self.empty_block5 = tk.Frame(self.search_field_panel, width = 150, height = 8)
		self.empty_block5.grid(row=23, column=1, columnspan=3)
		
	def draw_results_panel(self):
		#create the results field, where the matching players will appear.
		#A frame to hold everything
		self.result_panel = tk.Frame(self.root)
		self.result_panel.pack(expand=0, pady=2)
		#create the header,a hard coded canvas, which will have the relevant data listed below it
		self.result_header = tk.Canvas(self.result_panel,width=492, height=19, borderwidth=0)
		self.result_header.grid(row=1, sticky='wne')
		
		self.name_column_width = 240
		self.csr_column_width = 70
		self.age_column_width = 51
		self.height_column_width = 65
		self.weight_column_width = 65
		self.name_columnx = 0 #x position of the left side of that fields column
		self.csr_columnx = self.name_columnx+self.name_column_width
		self.age_columnx = self.csr_columnx+self.csr_column_width
		self.height_columnx = self.age_columnx+self.age_column_width
		self.weight_columnx = self.height_columnx+self.height_column_width
		self.sort_direction = 'descending'
		
		self.header_font = ("TKDefaultFont", 10, "bold")
		
		self.name_header = self.result_header.create_rectangle(self.name_columnx,2,self.csr_columnx,20,activefill = 'grey')
		self.name_text = self.result_header.create_text(self.name_columnx+self.name_column_width//2,10, text="Name", anchor = "center", font=self.header_font)
		#self.result_header.tag_bind(self.name_header, "<Enter>", lambda event: self.cursor_enter_header(self.name_header), add = '+')
		self.result_header.tag_bind(self.name_text, "<Enter>", lambda event: self.cursor_enter_header(self.name_header), add = '+')
		self.result_header.tag_bind(self.name_text, "<Leave>", lambda event: self.cursor_leave_header(self.name_header), add = '+')
		self.result_header.tag_bind(self.name_header, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('name'), add='+')
		self.result_header.tag_bind(self.name_text, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('name'), add='+')
										
		self.csr_header = self.result_header.create_rectangle(self.csr_columnx,2,self.csr_columnx+self.csr_column_width,20, activefill = 'grey')
		self.csr_text = self.result_header.create_text(self.csr_columnx+self.csr_column_width//2,10, text="CSR", anchor = "center", font=self.header_font)
		#self.result_header.tag_bind(self.csr_header, "<Enter>", lambda event: self.cursor_enter_header(self.csr_header), add = '+')
		self.result_header.tag_bind(self.csr_text, "<Enter>", lambda event: self.cursor_enter_header(self.csr_header), add = '+')
		self.result_header.tag_bind(self.csr_text, "<Leave>", lambda event: self.cursor_leave_header(self.csr_header), add = '+')
		self.result_header.tag_bind(self.csr_header, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('csr'), add='+')
		self.result_header.tag_bind(self.csr_text, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('csr'), add='+')
										
		self.age_header = self.result_header.create_rectangle(self.age_columnx,2,self.age_columnx+self.age_column_width,20, activefill = 'grey')
		self.age_text = self.result_header.create_text(self.age_columnx+self.age_column_width//2,10, text="Age", anchor = "center", font=self.header_font)
		#self.result_header.tag_bind(self.age_header, "<Enter>", lambda event: self.cursor_enter_header(self.age_header), add = '+')
		self.result_header.tag_bind(self.age_text, "<Enter>", lambda event: self.cursor_enter_header(self.age_header), add = '+')
		self.result_header.tag_bind(self.age_text, "<Leave>", lambda event: self.cursor_leave_header(self.age_header), add = '+')
		self.result_header.tag_bind(self.age_header, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('age'), add='+')
		self.result_header.tag_bind(self.age_text, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('age'), add='+')
										
		self.height_header = self.result_header.create_rectangle(self.height_columnx,2,self.height_columnx+self.height_column_width,20, activefill = 'grey')
		self.height_text = self.result_header.create_text(self.height_columnx+self.height_column_width//2,10, text="Height", anchor = "center", font=self.header_font)
		#self.result_header.tag_bind(self.height_header, "<Enter>", lambda event: self.cursor_enter_header(self.height_header), add = '+')
		self.result_header.tag_bind(self.height_text, "<Enter>", lambda event: self.cursor_enter_header(self.height_header), add = '+')
		self.result_header.tag_bind(self.height_text, "<Leave>", lambda event: self.cursor_leave_header(self.height_header), add = '+')
		self.result_header.tag_bind(self.height_header, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('height'), add='+')
		self.result_header.tag_bind(self.height_text, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('height'), add='+')
										
		self.weight_header = self.result_header.create_rectangle(self.weight_columnx,2,self.weight_columnx+self.weight_column_width,20, activefill = 'grey')
		self.weight_text = self.result_header.create_text(self.weight_columnx+self.weight_column_width//2,10, text="Weight", anchor = "center", font=self.header_font)
		#self.result_header.tag_bind(self.weight_header, "<Enter>", lambda event: self.cursor_enter_header(self.weight_header), add = '+')
		self.result_header.tag_bind(self.weight_text, "<Enter>", lambda event: self.cursor_enter_header(self.weight_header), add = '+')
		self.result_header.tag_bind(self.weight_text, "<Leave>", lambda event: self.cursor_leave_header(self.weight_header), add = '+')
		self.result_header.tag_bind(self.weight_header, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('weight'), add='+')
		self.result_header.tag_bind(self.weight_text, "<ButtonRelease-1>", lambda event: self.draw_sort_arrow('weight'), add='+')
		
		#create the scrollbar for the next canvas, which display the rows of matched players
		self.scrollbar = ttk.Scrollbar(self.result_panel)
		self.scrollbar.grid(row=2, column=1, sticky='ns')
		#create the canvas that shows the actual results of the search, connected to scrollbar
		self.result_table = tk.Canvas(self.result_panel, width=492, height=350,borderwidth=0,\
										yscrollcommand=self.scrollbar.set, scrollregion=[0,0,0,350])
		self.result_table.grid(row=2, sticky='wn')
		#configurate the scrollbar
		self.scrollbar.config(command=self.result_table.yview)
		
		#There is a problem where everything in the header canvas is offset by 2 pixels to the right
		#compared to the table canvas, so this is a quick fix
		self.result_header.addtag_all('all')
		self.result_header.move('all',2,0)
	
	def draw_sort_arrow(self, header_str):
		#draws a triangle pointing up or down depending on self.sort_direction, which is either 'ascending' or 'descending' in the 
		#column denoted by header_str
		
		arrow_xpos_dict = {'name': (self.name_columnx, self.name_column_width), 'csr': (self.csr_columnx, self.csr_column_width), 'age': (self.age_columnx, self.age_column_width), 'height': (self.height_columnx, self.height_column_width), 'weight': (self.weight_columnx, self.weight_column_width)}
		
		#co ordinates for middle of the arrow/triangle, relative to the result_header canvas, triangle is equilateral
		x = arrow_xpos_dict[header_str][0] + arrow_xpos_dict[header_str][1] - 5
		y = 10 #int(self.result_header.cget('height'))//2
		side_length = 7
		
		#remove any previously drawn arrow, if there is one
		self.result_header.delete('arrow')
		
		#draw a new arrow
		if self.sort_direction == 'ascending':
			self.sort_direction = 'descending'
			#create down arrow if sorting direction is ascending
			self.result_header.create_polygon(x-side_length/2, y+side_length/2, x+side_length/2, y+side_length/2, x, y-side_length/2, fill = 'black', tag='arrow')
		else:
			self.sort_direction = 'ascending'
			#create up arrow if sorting direction is ascending
			self.result_header.create_polygon(x-side_length/2, y-side_length/2, x+side_length/2, y-side_length/2, x, y+side_length/2, fill = 'black', tag='arrow')
			
		#call the actual sorting function then redraw the results
		player_search_engine.sort_by_field(header_str, self.sort_direction)
		self.draw_found_players()
		
	def cursor_enter_header(self, header_object):	
		self.result_header.itemconfig(header_object, fill = 'grey')
		
	def cursor_leave_header(self, header_object):
		self.result_header.itemconfig(header_object, fill = 'SystemButtonFace')
	
	def draw_update_popup(self):
		self.update_popup = tk.Toplevel()
		self.update_popup.wm_resizable(False, False)
		self.update_warning = tk.Label(self.update_popup, text="Are you sure you wish to update? Updating can take \nbetween 30 - 60 minutes, depending on the speed \nof your computer and internet connection.\n\nYou will be able to let BR Scout run in the background \nwhile using your computer normally.", justify = 'left')
		self.update_warning.grid(row=1, column=1, padx = 10, pady=10)
		
		self.popup_button_frame = tk.Frame(self.update_popup) 
		self.popup_button_frame.grid(row=2, column=1)
		
		
		self.update_ok_button = ttk.Button(self.popup_button_frame, text="Ok", width=10, command=self.begin_update)
		self.update_ok_button.pack(side='left', padx=5, pady=10)
		
		self.update_cancel_button = ttk.Button(self.popup_button_frame, text="Cancel", command=lambda: self.update_popup.destroy(), width=10)
		self.update_cancel_button.pack(side='right', padx=5, pady=10)
		
	def begin_update(self):
		#updates the database via player_search_engine
		self.popup_button_frame.destroy()
		#start the update thread
		self.update_thread = updateThread()
		self.update_thread.start()
		#change the popup window to one showing the update is in progress
		self.update_warning.destroy()
		self.update_warning = tk.Label(self.update_popup, text="Update in progress. Please do not exit BR scout at this \ntime. Feel free to continue using your computer.", justify = 'center')
		self.update_warning.grid(row=1, column=1, padx = 10, pady=10)
		#create the progressbar
		self.update_progress = ttk.Progressbar(self.update_popup, orient='horizontal', mode='indeterminate', length=200)
		self.update_progress.grid(row=2, columnspan = 2, pady=10)
		self.update_progress.start(20)

	def draw_found_players(self):
		#displays a row showing the details of a player for every found player
		
		#clear the results tables
		self.result_table.delete("all")
		self.result_table.create_text(int(self.result_table.cget('width'))//2,int(self.result_table.cget('height'))//2, text="Searching...")
		self.update()
		
		self.result_table.delete("all") #remove the 'searching...' text first
		
		#Draw the matched players and configure the scrollbar (below)
		
		#if no results are found, show a no results found message.
		if len(player_search_engine.results.scouted_list) == 0:
			self.draw_no_players_found()
			self.result_table.config(scrollregion=[0,0,446,0])
			
		#if too many results are found, only show the first self.max_results of them (default 300)
		elif len(player_search_engine.results.scouted_list)>self.max_results:
			shortened_list = player_search_engine.results.scouted_list[:self.max_results]
			self.draw_too_many_popup()
			self.result_table.config(scrollregion=[0,0,446,len(shortened_list)*20])
			for i in range(len(shortened_list)):
				self.draw_player_info(i)
		#otherwise amount of results is fine
		else:
			for i in range(len(player_search_engine.results.scouted_list)):
				self.draw_player_info(i)
				self.result_table.config(scrollregion=[0,0,446,len(player_search_engine.results.scouted_list)*20])
				
	def draw_player_info(self, scouted_list_index):
		#draws one row displaying the information of a specified player from the scouted_list on the results_table canvas
		
		#alternate the background colour on every listing, to make reading easier
		if scouted_list_index%2 == 0:
			back = 'white'
		else:
			back = 'lightgrey'
		
		#create the listing rectangle, 20 is the height of each result row
		top_y = scouted_list_index*20
		bottom_y = top_y + 20
		self.result_table.create_rectangle(0,top_y,self.weight_columnx+self.weight_column_width,\
											bottom_y, fill=back, outline=back)
		#add the lines that separate each data field column
		self.result_table.create_line(self.csr_columnx,top_y,self.csr_columnx,bottom_y + 1, fill='darkgrey')
		self.result_table.create_line(self.age_columnx,top_y,self.age_columnx,bottom_y + 1, fill='darkgrey')
		self.result_table.create_line(self.height_columnx,top_y,self.height_columnx,bottom_y + 1, fill='darkgrey')
		self.result_table.create_line(self.weight_columnx,top_y,self.weight_columnx,bottom_y + 1, fill='darkgrey')
	
		#get the player object. Is a custom class containing all attributes such as name, csr, etc
		player = player_search_engine.results.scouted_list[scouted_list_index]
		#draw/print the players information in the appropriate columns
		textid = self.result_table.create_text(self.name_columnx+5, (top_y+bottom_y)//2, anchor='w', \
												text=player.name, activefill='blue', font=("TKDefaultFont", 9))
		self.result_table.create_text(self.csr_columnx+8, (top_y+bottom_y)//2, anchor='w', text=player.csr)
		self.result_table.create_text(self.age_columnx+19, (top_y+bottom_y)//2, anchor='w', text=player.age)
		self.result_table.create_text(self.height_columnx+23, (top_y+bottom_y)//2, anchor='w', text=player.height)
		self.result_table.create_text(self.weight_columnx+23, (top_y+bottom_y)//2, anchor='w', text=player.weight)
		
		#create the hyperlinked name text
		self.result_table.tag_bind(textid,"<ButtonRelease-1>", lambda event: self.click_name(player.id), add="+")
		self.result_table.tag_bind(textid,"<Enter>", lambda event: self.enter_name(textid), add="+")
		self.result_table.tag_bind(textid,"<Leave>", lambda event: self.leave_name(textid), add="+")
		
	def draw_no_players_found(self):
		#draws a message to the results canvas if no matching players are found
		self.result_table.create_text(int(self.result_table.cget('width'))//2,int(self.result_table.cget('height'))//2, text="No Players Found.")
		
	def draw_too_many_popup(self):
		#creates a pop up window explaining that the search criteria returned too many results
		self.too_many_popup = tk.Toplevel()
		self.too_many_message = tk.Label(self.too_many_popup, text="Too many results found. Only showing the first {0}. \n Try narrowing your search criteria.".format(str(self.max_results)), justify = 'center')
		self.too_many_message.pack(padx=10, pady=10, side='top')
		#window destroys on pressing ok
		ok_button = ttk.Button(self.too_many_popup, text= "Ok", width=10, command=lambda: self.too_many_popup.destroy())
		ok_button.pack(side='bottom', pady=10)
		
	def enter_name(self, name_object):
		#changes the cursor when it hovers over a players name in the results
		super(scouting_tool, self).config(cursor="hand2")
		self.result_table.itemconfig(name_object, font=("TKDefaultFont", 9, "underline"))
	
	def leave_name(self, name_object):
		#changes the cursor when it moves from a players name to any other part of the gui
		super(scouting_tool, self).config(cursor="")
		self.result_table.itemconfig(name_object, font=("TKDefaultFont", 9))
		super(scouting_tool, self).wm_attributes("-topmost", 0)
		
	def click_name(self, playerid):
		#opens the player's br page when its name is clicked, the browser opens behind the gui but clicking the browser will bring it to the front.
		super(scouting_tool, self).wm_attributes("-topmost", 1)
		webbrowser.open("http://www.blackoutrugby.com/game/club.squad.php#player=" + playerid, new=2, autoraise=False)
	
	def get_entry_box_data(self, entry_box, default_value):
		#retrieves the input from the specified entry_box, and returns it. If the entry box is empty, it assigns a specified default value
		if entry_box.get().strip() == "":
			return default_value
		else:
			return int(entry_box.get().strip())	
	
	def search(self, event):
		#gets the input from all the search fields, applies them to the search engine settings,
		#and searches the database using them. Then displays all matching players
		#get the nationality from the combobox
		player_search_engine.target_nationality = self.nat_list.get()
		player_search_engine.include_dual_nat = self.include_dual_nat.get()
		#get bool for searching only U20 eligible players
		player_search_engine.check_u20_eligibility = self.check_u20_eligible.get()
		
		#get the inputs from the entry boxes. Pass a default value to use if the box is empty.
		player_search_engine.min_csr = self.get_entry_box_data(self.min_csr_box, 0)
		player_search_engine.max_csr = self.get_entry_box_data(self.max_csr_box, 999999)
		
		player_search_engine.min_age = self.get_entry_box_data(self.min_age_box, 17)
		player_search_engine.max_age = self.get_entry_box_data(self.max_age_box, 80)
		
		player_search_engine.min_height = self.get_entry_box_data(self.min_height_box, 140)
		player_search_engine.max_height = self.get_entry_box_data(self.max_height_box, 230)
		
		player_search_engine.min_weight = self.get_entry_box_data(self.min_weight_box, 60)
		player_search_engine.max_weight = self.get_entry_box_data(self.max_weight_box, 160)
		
		#remove the sorting direction arrow
		self.result_header.delete('arrow')
		
		#search the database on another thread so the gui doesnt freeze
		self.search_thread = searchThread()
		self.search_thread.start()
	
	def search_done_check(self): 
		#called regularly to check if the search thread is completed
		
		#if the search is completed, display the results
		if self.search_thread.done_event.is_set(): 
			self.draw_found_players() 
		#otherwise update the gui and check if the search thread is finished in 100 ms 
		else:
			self.after(100, self.search_done_check)
			self.update()

	def update_done_check(self): 
		#checks if the update thread is finished
		
		#if it is finished, change the popup window to one explaining the updating is finished which destroys when ok is pressed
		if self.update_thread.done_event.is_set(): 
			self.update_warning.destroy()
			self.update_progress.destroy()
			
			self.update_complete = tk.Label(self.update_popup, text="Database updated.", justify = 'left')
			self.update_complete.grid(row=1, column=1, padx = 10, pady=10)
			self.update_complete_button = ttk.Button(self.update_popup, text="Ok", width=10, command=self.update_popup.destroy)
			self.update_complete_button.grid(row=2, column=1, pady=10)
			self.last_update.destroy()
			self.last_update = tk.Label(self.search_field_panel, text = "Last updated " + player_search_engine.days_ago + " days ago")
			self.last_update.grid(row=3, column=1, columnspan=3)
			self.update()
			
		#else check is 100 ms and keep the gui alive	
		else:
			self.after(100, self.update_done_check)
			self.update()
			
class searchThread(threading.Thread):
	#thread object for searching, so the search doesnt block the gui
	def __init__(self):
		threading.Thread.__init__(self)
		self.done_event = threading.Event()

	def run(self):
		#start checking if the thread is finished
		app.search_done_check()
		#do the search
		player_search_engine.search_database()	
		#tell the object the search is done
		self.done_event.set()
	
class updateThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.done_event = threading.Event()

	def run(self):
		#start the check for completion of the thread
		app.update_done_check()
		#update the database
		player_search_engine.update_database()
		#tell thread object the update is finished
		self.done_event.set()

if __name__=="__main__":		
	app = scouting_tool(None)
	app.title("BR Scout")
	app.wm_resizable(False, False)
	app.mainloop()