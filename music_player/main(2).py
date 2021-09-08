#import all the required libraries  

import tkinter as tk
import sqlite3
from tkinter import filedialog, ttk 
from PIL import Image, ImageTk
from pygame import mixer  
import time
from mutagen.mp3 import MP3


class ThemeColors:
    default_colour = "WHITE" 
    default_text = "#1a1a1a"
    default_font = ("Itim" , "14") 

    @staticmethod
    def changeTheme( object_to_change ):
        theme_colourDark = "#1a1a1a"
        theme_colourLight = "WHITE" 

        if( object_to_change.default_colour == theme_colourDark ):
            # if the active color is of Light mode change the color to dark mode colour 
            object_to_change.default_colour = theme_colourLight
            object_to_change.default_text = theme_colourDark
        else:
            #else change the color to the light mode colour 
            object_to_change.default_colour = theme_colourDark
            object_to_change.default_text = theme_colourLight

        # all the widgets need to be re-configured to see the changes
        for i in object_to_change.widgets_list:
            i.configure( background = object_to_change.default_colour, foreground= object_to_change.default_text )

        for i in object_to_change.frames_list:
            i.configure( background = object_to_change.default_colour )

#        for i in object_to_change.checkButton_list:
#            i.configure( bg = object_to_change.default_colour, activebackground = object_to_change.default_colour , fg = object_to_change.default_text, activeforeground =object_to_change.default_text )

class MusicPlayer( ThemeColors ):
    base = tk.Tk()      # initalizing the Tk window..

    folder = ""  

    dumper = []         # this list holds all the widgets that are no longer needed so that they can be destroyed( whenever needed )

    checkButton_list = []

    frames_list = [] 

    widgets_list= []    # this list holds all the widgets that are present in this app ( which is helpful for later purposes )
                        # we will add the widgets as they are created in our app to handle this widgets 
    
    songs_list = [ ]    # this will hold the songs list that will be returned by searching a song name

    def __init__(self):
        #positioning the base window and setting the icon
        self.base.configure( background = self.default_colour )
        self.base.geometry( "+10+0")
        self.base.iconbitmap( "./assets/coffee01.ico")

        self.frames_list.append( self.base ) # appending to the widgets list

        #Button
        button1 = tk.Button( self.base, text='Change Theme' , activebackground= self.default_colour , activeforeground= self.default_colour, font = self.default_font , command= lambda:ThemeColors.changeTheme(self) )
        button1.pack() 
        self.widgets_list.append( button1 ) # appending to the widgets list

        #Label
        label1 = tk.Label( self.base, text='This is the text required for testing', bg = self.default_colour , fg = self.default_text, font= self.default_font )
        label1.pack( ) 
        self.widgets_list.append( label1 )

        #checkButton
        checkButton1 = tk.Checkbutton( self.base, text= "Check this chekcbox", bg = self.default_colour, fg=  self.default_text ,activebackground = self.default_colour , activeforeground =self.default_text , font= self.default_font )
        checkButton1.pack() 
        self.widgets_list.append( checkButton1 )

        #Entry
        entry1 = tk.Entry( self.base , bg = self.default_colour , fg= self.default_colour ) 
        entry1.pack( )
        self.widgets_list.append( entry1 )

        #Scale
        scale1 =tk.Scale(  self.base , bg = self.default_colour, fg  = self.default_text )
        scale1.pack( )
        widgets_list.append( scale1 )

        #ListBox

        #RadioButton 

        self.base.mainloop()

#starting the code
if __name__ == "__main__" : 
    m1 = MusicPlayer( )
        










