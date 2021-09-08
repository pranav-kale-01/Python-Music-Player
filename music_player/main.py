import sqlite3  
from tkinter import filedialog ,ttk 
import os 
from tkinter import * 
from PIL import ImageTk , Image
from pygame import mixer
from mutagen.mp3 import MP3

class MusicPlayer: 
    folder = "" 

    def __init__(self):
        global _after_function , btn1 , btn2, btn3 , btn4, btn5 , scale1

        self.theme_colour = "WHITE"
        self.flag=0  
        self.c_flag=0  
        self.dumper = []
        self.dumper_for_label = []
        _after_function = [] 
        self.class_dataMembers = [] 
        self.songs_list = [] 
        self.base = Tk() 
        self.current_song = ""
        mixer.init()
        
        #positioning the base window 
        self.base.configure(background = self.theme_colour )
        self.base.geometry( "+10+0")

        #setting the minimum width and height for the application
        self.base.wm_minsize( 1180 , 120)
        
        #adding a sidebar to hold additional settings 
        self.sidebar = LabelFrame( self.base, bg=self.theme_colour ) 
        self.sidebar.pack( fill=BOTH, side=LEFT ,expand=1, anchor="n" ,padx=0 , pady=0)
        self.sidebar.pack_propagate(0)
        
        #creating a toogle switch that will extend/contract the menuar 
        self.toggle_button = Button( self.sidebar , text="=" , font=("Itim 14") , command= self.toggle_sidebar , bg=self.theme_colour)
        self.toggle_button.grid(row=0 , sticky="nsew" , padx=5, pady=10 ,ipadx=5) 

        #adding a search button that will search the songs 
        self.search_button = Button( self.sidebar , text="S" , command= lambda :self.toggle_sidebar() , bg= self.theme_colour , font=("Itim 14") )
        self.search_bar = Entry( self.sidebar , width=30 , font=("Itim 14") , bg=self.theme_colour )

        #checking if the sidebar is contracted or expanded 
        self.search_button.grid(row=1 , sticky="nsew" , padx=5, pady=10 , ipadx=5)

        #creating a toogle switch to switch between light mode and dark mode
        self.mode_button = Button( self.sidebar , text="M" , font=("Itim 14") , command= self.switch_mode , bg=self.theme_colour)
        self.mode_button.grid(row=2, sticky="nsew" , padx=5, pady=10 , ipadx=5 ) 
        self.class_dataMembers.append( self.mode_button  )

        #creating a main frame that will hold all the songs 
        self.basic_frame = Frame(self.base ,bg=self.theme_colour, width=1100  )
        self.basic_frame.pack(expand=0, anchor="nw", side = TOP ,padx=0 , pady=0)
        self.basic_frame.pack_propagate(0) 
        
        #creating a seperate frame to hold the timeline slide 
        self.slide_frame = Frame( self.base , bg=self.theme_colour, width=1100 ) 
        self.slide_frame.pack(fill=X, expand =1, pady=0, padx=0)

        #creating a bottom frame 
        self.bottom_frame = Frame(self.base ,bg=self.theme_colour, width=1100 )
        self.bottom_frame.pack( fill=X, side=BOTTOM, expand=1, anchor ="sw")
        self.bottom_frame.pack_propagate(0)
        
        prev_img  = ImageTk.PhotoImage(Image.open("./assets/previous.png"))
        next_img  = ImageTk.PhotoImage(Image.open("./assets/forward.png"))
        pause_img = ImageTk.PhotoImage(Image.open("./assets/play_pause.png"))
        forward_n = ImageTk.PhotoImage(Image.open("./assets/forward_n.png"))
        previous_n= ImageTk.PhotoImage(Image.open("./assets/previous_n.png"))

        btn1 = Button( self.bottom_frame , image = prev_img,   font=("Itim 14"), bg=self.theme_colour , activebackground=self.theme_colour, borderwidth=0, command= self.play_prev )      
        btn2 = Button( self.bottom_frame , image = pause_img,  font=("Itim 14"), bg=self.theme_colour , activebackground=self.theme_colour, borderwidth=0, command= self.pause_and_resume )  
        btn3 = Button( self.bottom_frame , image = next_img,   font=("Itim 14"), bg=self.theme_colour , activebackground=self.theme_colour, borderwidth=0, command= self.play_next )      
        btn4 = Button( self.bottom_frame , image = previous_n, font=("Itim 14"), bg=self.theme_colour , activebackground=self.theme_colour, borderwidth=0, command= self.get_the_song_back ) 
        btn5 = Button( self.bottom_frame , image = forward_n,  font=("Itim 14"), bg=self.theme_colour , activebackground=self.theme_colour, borderwidth=0, command= self.get_the_song_ahead )

        #making a variable for Scale 
        self.var1 = DoubleVar() 
        self.var1.set(20)

        self.var2 = IntVar() 
        self.var2.set(0)
 
        scale1 = Scale( self.bottom_frame , from_ = 0 , orient=HORIZONTAL, to = 100 , variable=self.var1 ,width=10 ,bg=self.theme_colour , borderwidth=0 , length =300, background= self.theme_colour ) 
        scale1.bind("<B1-Motion>" , lambda e: mixer.music.set_volume(float(self.var1.get())/100 ) )
                
        self.scale2 = Scale( self.slide_frame , from_ = 0 , orient=HORIZONTAL, to = 100 , variable=self.var2, length=1111 ,width= 8 , bg=self.theme_colour , borderwidth=0 )
        self.scale2.bind("<ButtonRelease-1>" ,lambda e: self.change_song_playback(e , self.scale2 ) )

        #making a temporary label to set all the buttons to the correct position 
        temp = Label( self.bottom_frame ,bg=self.theme_colour )
        temp.grid(row=1,column=0 ,padx=160)
        
        btn1.grid(row=1 , column=1,padx=15 ,pady=10 ,ipady=10)
        btn2.grid(row=1 , column=3,padx=15 ,pady=10 ,ipady=10) 
        btn3.grid(row=1 , column=5,padx=15 ,pady=10 ,ipady=10) 
        btn4.grid(row=1 , column=2,padx=15 ,pady=10 ,ipady=10) 
        btn5.grid(row=1 , column=4,padx=15 ,pady=10 ,ipady=10) 

        scale1.grid(row=1 , column=6 , columnspan=10 , sticky="nsew" ,padx=20 , pady=0 ,ipadx=0 , ipady=0 )
        self.scale2.pack( fill =X ,padx=0 , pady=0)

        self.get_all_music_from_the_folder()
    
        #appneding all the used widgets to the list of datamembers 
        for _ in [ btn1 , btn2 , btn3 , btn3 , btn4 , btn5 , scale1,  self.scale2, temp ]:
            self.class_dataMembers.append( _ ) 

        self.base.mainloop()      

    def display_derrived_songs( self,event ): 
        con = sqlite3.connect("music_player_1.db")
        c = con.cursor()
        c.execute(f"SELECT song FROM MP01 where song LIKE '%{self.search_bar.get()}%' ")
        tempList = c.fetchall() 

        #clearing the previous songs menu using the songs list
        for items in self.songs_list: 
            items.destroy()

        #adding the searched songs to the menu 
        for _ in tempList:            
            lbl = Label(self.second_frame, text = _ , font=("Itim 14")  , anchor="w" , width= 118 ,pady=6 , padx=10 )
            lbl.bind("<Button-1>" , lambda e: self.getinfo(e) ) 

            if( self.c_flag == 1 ):
                lbl.configure(bg="#e3e3e3" , fg = "Black" , activeforeground = "Black" , activebackground="#e3e3e3" )
                self.c_flag= 0 

            else: 
                lbl.configure(bg=self.theme_colour , fg="BLACK" , activeforeground = "BLACK" , activebackground="WHITE" )
                self.c_flag= 1 
                
            self.class_dataMembers.append( lbl )
            self.songs_list.append( lbl )
            lbl.pack(fill=X , expand=1)
        
    def switch_mode(self):
        global scale1
        if( self.theme_colour.upper() == "WHITE" ):
            #switch to dark mode 
            self.theme_colour = "#303030"

            #switching the text of the mode-swtich button
            if(self.toggle_button['text'] != '=' ):
                self.mode_button.configure(text="Dark Mode") 

            #switching properties of other buttons and labels 
            for _ in self.class_dataMembers: 
                
                _.configure( bg=self.theme_colour,fg='White')

        else:
            #switch to light mode 
            self.theme_colour = "White"

            if(self.toggle_button['text'] != '=' ):
                self.mode_button.configure(text="Light Mode") 
            
            for _ in self.class_dataMembers: 
                _.configure( bg=self.theme_colour , fg="BLACK" )
            
        scale1.configure(background= self.theme_colour )
        
        #setting activebackground for the buttons
        for _ in [ btn1 , btn2 , btn3, btn4 , btn5 ]:
            _.configure( activebackground= self.theme_colour )
        
        #switching colours of the windows and frames 
        self.base.configure(bg=self.theme_colour )
        self.sidebar.configure(bg=self.theme_colour )
        self.toggle_button.configure(bg=self.theme_colour )
        self.basic_frame.configure(bg=self.theme_colour )
        self.slide_frame.configure(bg=self.theme_colour )
        self.bottom_frame.configure(bg=self.theme_colour )

    def toggle_sidebar( self): 
        if( self.toggle_button['text'] == '='):
            add.configure(text="Add new Songs") 
            self.toggle_button.configure(text="_______")

            if( self.theme_colour == "White"):
                self.mode_button.configure(text="Light Mode")
            else: 
                self.mode_button.configure(text="Dark Mode")

            #replacing the search button with an Entry-Label
            self.search_button.destroy()     
            self.search_bar = Entry( self.sidebar , width=15 , font=("Itim 14") )
            self.search_bar.bind("<Return>" , self.display_derrived_songs )
            self.search_bar.grid(row=1, sticky="nsew", padx=5 , pady=10 , ipadx=5 )
        else: 
            add.configure(text="+")
            self.toggle_button.configure(text="=")
            self.mode_button.configure( text="M")

            #replacing the search bar with the search button
            self.search_bar.destroy()
            self.search_button = Button( self.sidebar , text="S" , command= lambda :self.toggle_sidebar() , bg= self.theme_colour , font=("Itim 14") )
            self.search_button.grid(row=1, sticky="nsew", padx=5 , pady=10 , ipadx=5 )

    def get_the_song_back(self): 
        mixer.music.set_pos( int( self.scale2.get() ) - 10 )
        self.scale2.set( float(self.scale2.get() -10) ) 
 
    def get_the_song_ahead( self ):
        mixer.music.set_pos( int( self.scale2.get() ) + 10 )
        self.scale2.set( float(self.scale2.get() +10) ) 

    def show_time( self , scale2):
        global _after_function  
        if( self.flag == 0 ):
            scale2.set( float( scale2.get()) + 1 ) 
        if( scale2.get() == int( self._len)  ): 
            for items in _after_function: 
                scale2.after_cancel( items )    
            scale2.set(0)            
        else:
            _after_function.append( scale2.after( 1000 , lambda: self.show_time( scale2) ) )
        

    def change_song_playback( self , event , scale2 ): 
        mixer.music.pause() 
        mixer.music.set_pos( float( scale2.get() )) 
        mixer.music.unpause()
        self.flag= 0 

    def play_music(self,music): 
        global _after_function 

        #stoping all the previous after methods that were playing 
        for items in _after_function: 
            self.scale2.after_cancel( items )

        for items in self.dumper_for_label : 
            items.destroy() 

        self.current_song = music 

        cur_song = Label( self.bottom_frame , text= f"current song - {self.current_song.split('/')[-1].split('.mp3')[0]} " , font=("SegoeUI 14") , bg=self.theme_colour )
        cur_song.grid(row=2, columnspan=10 , sticky="nsew")

        self.class_dataMembers.append( cur_song )
        # get song length using mutagen 
        song_mut = MP3( music ) 
        self._len = song_mut.info.length

        self.scale2.configure(to = self._len )
        _after_function.append( self.scale2.after( 1000 , lambda : self.show_time( self.scale2) ) )
        self.scale2.set(0)

        song = mixer.music.load(music)
        mixer.music.play()
        
        mixer.music.set_volume(float(self.var1.get())/100)
        self.dumper_for_label.append(cur_song)

    def pause_and_resume(self): 
        global play_button , pause_button 
        if(self.flag==0):
            mixer.music.pause() 
            self.flag=1 
        else:
            mixer.music.unpause()
            self.flag=0 

    def play_next(self): 
        con = sqlite3.connect("music_player_1.db")
        c = con.cursor() 
        c.execute(f"""SELECT song_ID FROM MP01 WHERE song_path = "{self.current_song}" """)
        temp = c.fetchall() 
        temp = temp[0]
        for x in temp: 
            if(x != "" ):
                x = int(x)+1
                c.execute(f""" SELECT song_path FROM MP01 WHERE song_ID = '{x}' """)
                temp2 = c.fetchall()[0]
                for y in temp2:
                    self.play_music(y)

    def play_prev(self): 
        con = sqlite3.connect("music_player_1.db")
        c = con.cursor() 
        c.execute(f"""SELECT song_ID FROM MP01 WHERE song_path = "{self.current_song}" """)
        temp = c.fetchall() 
        temp = temp[0] 
        for x in temp: 
            if( x != "" ):
                x = int( x ) - 1
                c.execute(f""" SELECT song_path FROM MP01 WHERE song_ID = '{x}' """)
                temp2 = c.fetchall()[0]
                for y in temp2:
                    self.play_music(y)

    def stop(self):
        mixer.fadeout()
        mixer.music.unload()

    def Create_Table(self, main_frame):    
        #creating a srollable canvas that will show the current files               
        self.my_canvas = Canvas(main_frame ,width=1100,height=500)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1) 
        self.my_canvas.pack_propagate(0)

        # Add A Scrollbar To The Canvas
        self.vertical_scr = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.vertical_scr.pack(side=RIGHT, fill=Y , expand=1)

        self.horizontal_scr = ttk.Scrollbar( self.basic_frame, orient=HORIZONTAL, command=self.my_canvas.xview )      
        self.horizontal_scr.grid(sticky ="nsew" , columnspan=100 , padx=0 )
        self.dumper.append(self.horizontal_scr)
        
        # Configure The Canvas
        self.my_canvas.configure(yscrollcommand=self.vertical_scr.set)
        self.my_canvas.configure(xscrollcommand=self.horizontal_scr.set)
        self.my_canvas.bind('<Enter>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))

        #Using the bind method to get the scroll using the srolldown key of the mouse 
        self.my_canvas.bind_all('<MouseWheel>' , lambda e: self.on_mousewheel(e) ) 

        # Create ANOTHER Frame INSIDE the Canvas
        self.second_frame = Frame(self.my_canvas )
        self.second_frame.pack( fill=BOTH , expand=1)
 
        # Add that New frame To a Window In The Canvas
        self.my_canvas.create_window((0,0), window=self.second_frame )
    
    def get_all_music_from_the_folder(self):
        for widgets in self.dumper: 
            widgets.destroy() 

        #creating a database for permenant storing the information
        self.con = sqlite3.connect("music_player_1.db")
        self.cur = self.con.cursor()

        self.con.execute("CREATE TABLE IF NOT EXISTS MP01( song_ID INTEGER PRIMARY KEY AUTOINCREMENT , song VARCHAR(80) , title VARCHAR(20) , artist VARCHAR(20) , album VARCHAR(20) , song_path VARCHAR(200)  );")
        self.con.commit() 

        main_frame = Frame(self.basic_frame ,width=1400) 
        
        main_frame.grid( sticky=NSEW , row=2 ,column=0 , columnspan=100) 
        self.Create_Table(main_frame)

        global add 
        add = Button(self.sidebar,text="+" , command= self.add_new_music_to_the_player , font=("Itim 14") , bg= self.theme_colour  ) 
        add.grid( columnspan=20 , pady=5 ,ipadx=7 ,padx=5 , sticky="nsew")  
        self.class_dataMembers.append(add)

        self.dumper.append(add)

        self.cur.execute("SELECT song FROM MP01")
        files = self.cur.fetchall()

        for file in files: 
            for x in file:
                if(x!= "" ):   
                    lbl = Label(self.second_frame, text = x  , anchor="w" , width= 154 ,pady=6 , padx=10 )
                    lbl.bind("<Button-1>" , lambda e: self.getinfo(e) ) 
                    if( self.c_flag == 1 ):
                        lbl.configure(bg="#e3e3e3" , fg = "Black" , activeforeground = "Black" , activebackground="#e3e3e3" )
                        self.c_flag= 0 
                    else: 
                        lbl.configure(bg=self.theme_colour , fg="BLACK" , activeforeground = "BLACK" , activebackground="WHITE" )
                        self.c_flag= 1 
                    self.class_dataMembers.append(lbl)
                    self.songs_list.append( lbl )
                    lbl.pack(fill=X , expand=1)

        self.my_canvas.config( yscrollcommand = self.vertical_scr.set ) 

    def on_mousewheel(self,event): 
        self.my_canvas.yview_scroll( int( -1*(event.delta/120) ) , "units"  )

    def getinfo(self,event):
        name = event.widget.cget("text") 
        con = sqlite3.connect("music_player_1.db")
        c = con.cursor() 
        c.execute(f"""SELECT song_path FROM MP01 WHERE song = "{name}" """)
        song_path = c.fetchall()
        song_path = song_path[0]
        for x in song_path: 
            self.current_song = x
            self.play_music(x)

    def add_new_music_to_the_player(self):
        self.music_queue = [] 
        MusicPlayer.folder = filedialog.askdirectory()
        files_in_the_folder = os.listdir(MusicPlayer.folder)

        for file in files_in_the_folder:
            if( file.split('.')[-1] == "mp3" ):
                self.con.execute(f"""INSERT INTO MP01(song,song_path) VALUES("{file}" , "{MusicPlayer.folder+'/'+file}");""")
                self.music_queue.append( MusicPlayer.folder+'/'+file)
        self.con.commit() 
        self.get_all_music_from_the_folder()

if __name__ == "__main__":
    m1 = MusicPlayer()