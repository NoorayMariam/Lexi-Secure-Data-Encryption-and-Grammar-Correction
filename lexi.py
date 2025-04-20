from tkinter import *
import time
import webbrowser
from tkinter.filedialog import askopenfilename  # for file explorer
from tkinter.filedialog import asksaveasfilename
import os 
import dbm
import base64
import language_tool_python
grammar_tool = language_tool_python.LanguageTool('en-US') #USING ENGLISH-US FOR GRAMMAR CHECK  


user_directory = os.getcwd() #SETTING THE DIRECTORY
os.system("attrib +h /s /d") #this will hide the file
text_file_name = time.strftime("%d_%B_%Y_%A_%H_%M_%S") #DEFAULT NAME OF THE TEXT FILE
global file_name_path
file_name_path = False

root = Tk()  # creating object root from class Tkinter

global status_value
status_value = "status"
class Window(Frame):  # main window frame

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

       #THE MENU BUTTONS ON RIGHT SIDE
        self.command_frame = Frame(root,bg='pink')
        self.command_frame.grid(column=1,row=0)
       
        self.save_btn = Button(self.command_frame,text='Save',command=self.save_file_existing,bg='pink',fg='black',width=10,height=2)
        self.save_as_btn = Button(self.command_frame,text='SAVE AS',command=self.save_file,bg='yellow',fg='black',width=10,height=2)
        self.exit_btn = Button(self.command_frame,text='Exit',command=self.clickExitButton,bg='yellow',fg='black',width=10,height=2)
        self.open_btn = Button(self.command_frame,text='Open',command=self.file_open,bg='yellow',fg='black',width=10,height=2)
        self.visit_btn = Button(self.command_frame,text='Visit',command=self.open_web_browser,bg='yellow',fg='black',width=10,height=2)
        self.grammar_btn = Button(self.command_frame,text='GrammarCheck',command=self.grammar_check,bg='yellow',fg='black',width=10,height=2)
        self.status_lbl = Button(self.command_frame,text= status_value, bg='yellow',fg='black',width=80,height=2 )
        self.save_btn.grid(column=1,row=5)
        self.visit_btn.grid(column=1,row=2)
        self.open_btn.grid(column=1,row=0)
        self.exit_btn.grid(column=1,row=1)
        self.save_as_btn.grid(column=1,row=4)
        self.grammar_btn.grid(column=1,row=3)
        self.status_lbl.grid(column=1, row = 6)

    #THE INPUT TEXT IN GUI FROM USER
    text_frame = Frame(root)
    text_frame.grid(column=0,row=0)
    text_scroll = Scrollbar(text_frame)
    text_scroll.pack(side= RIGHT, fill = Y)

    the_input = Text(text_frame,font=("TimesNewRoman",16), selectbackground= "Orange", selectforeground="white", undo=True, yscrollcommand= text_scroll.set)
    the_input.place(x=0, y=0)
    text_scroll.config(command= the_input.yview)
    the_input.pack()

    #GRAMMAR SUGGESTION FRAME
    suggestion_frame = Frame(root, bg="pink")#,width=1000,height=200,
    suggestion_frame.grid(column=0,row=2)
    suggestion_scroll = Scrollbar(suggestion_frame)
    suggestion_scroll.pack(side =RIGHT, fill = Y) #column=6,row=0,rowspan=9

    grammar_output = Text(suggestion_frame,font=("TimesNewRoman",16), bg= "light green", selectforeground="white", selectbackground="green", undo=True, yscrollcommand= suggestion_scroll.set)
    grammar_output.place(x=0, y=0)
    suggestion_scroll.config(command= grammar_output.yview)
    grammar_output.pack()

    #save button 
    def grammar_check(self):
        initial_text = f"""{Window.the_input.get(1.0,END)}"""
        suggestion = grammar_tool.check(initial_text)
        Window.grammar_output.delete(1.0, END)
        Window.grammar_output.insert(1.0, suggestion)

    # opening web browser automatically in a new browser in new tab
    def open_web_browser(self):
        webbrowser.open("https://brave.com/", new=1, autoraise=True)

    # opening file explorer
    def file_open(self):
        os.system("attrib -h /s /d")
        name = askopenfilename(initialdir= user_directory, filetypes=(("Text File", "*.txt"),
                                       ("All Files", "*.*"),
                                       ("Encoded Text Files","*.txt.dat")),
                            title="Select a text file or all file."
                            )
        if name:
            global file_name_path
            global file_name
            file_name_path = name
            file_name_split = os.path.basename(file_name_path)
            file_name = os.path.splitext(file_name_split)[0]

        name= open(name, 'r')
        encoded_file = dbm.open(file_name, flag = 'w', mode = 0o666)
        for byte_object in encoded_file.values():
            global string_object
            string_object = byte_object.decode("ascii")

            for status_object in encoded_file.keys():
                global status_value
                status_value = status_object.decode("ascii")
                length = len(status_value)
                listvalue = list(status_value)
                updatingvalue = []
                count = 0
                for i in listvalue:
                    count+=1
                    if count >length - 20:
                        updatingvalue.append(i)

                updateing = str(updatingvalue)
                self.status_lbl["text"] = "lastupdated" + updateing
                

        encoded_string_bytes = string_object.encode("ascii")
        decoded_user_Input_bytes = base64.b64decode(encoded_string_bytes)
        decoded_user_Input_string = decoded_user_Input_bytes.decode("ascii")

        Window.the_input.insert(1.0, decoded_user_Input_string)
        name.close()
        encoded_file.close()


    # exit button or click
    def clickExitButton(self):
        exit()


# file writing and appending
    def save_file_existing(self):
        global file_name_path
        global file_name
    
        if file_name_path:
            user_Input = Window.the_input.get(1.0,END)
            file_exist = open(file_name_path, 'w')
        
            user_Input_bytes = user_Input.encode("ascii") #converting input into bytes
            encoded_user_Input_bytes = base64.b64encode(user_Input_bytes) #encoding bytes using base64 ascii
            encoded_user_Input_string = encoded_user_Input_bytes.decode("ascii") #decoding into string format 
            file_exist_encoded = dbm.open(file_name, flag = 'c', mode = 0o666)
            file_status = file_name_path + time.strftime("_%d_%B_%Y_%H%M%S")
            file_exist_encoded[file_status]= encoded_user_Input_string #taking the filename and status as key value with content as pair value
            file_exist.write(encoded_user_Input_string)
            file_exist.close()
            file_exist_encoded.close()

        else:
            self.save_file()
            


    def save_file(self):
        file = asksaveasfilename(filetypes=[("txt file", ".txt")], defaultextension=".txt", initialfile="{}".format(
            text_file_name), initialdir=f"{user_directory}", title="Save File as", confirmoverwrite=True,)
        file.title
        if file:
            global file_name_path
            global file_name 
            file_name_path = file
            file_name_split = os.path.basename(file)
            file_name = os.path.splitext(file_name_split)[0]
            try:
                user_Input = Window.the_input.get(1.0, END)
                file = open(file, "w")
                user_Input_bytes = user_Input.encode("ascii") #converting input into bytes
                encoded_user_Input_bytes = base64.b64encode(user_Input_bytes) #encoding bytes using base64 ascii
                encoded_user_Input_string = encoded_user_Input_bytes.decode("ascii") #decoding into string format 
                file_new_encoded = dbm.open(file_name, flag = 'c', mode = 0o666)
                file_status = file_name_path + time.strftime("_%d_%B_%Y_%H%M%S")
                file_new_encoded[file_status]= encoded_user_Input_string #taking the filename and status as key value with content as pair value
                file.write(encoded_user_Input_string)
                file.close()
                file_new_encoded.close()

            except:
                print("some error you must fix while saving files")
        else: # user cancel the file browser window
            print("No file chosen") 
        os.system("attrib +h /s /d") #this will hide the file

image = PhotoImage(file='logo.png')
root.wm_title("LEXI")
root.iconphoto(False, image)

root.geometry("1100x900")   #initialising the window geometry
app = Window(root)
root.mainloop()   #infinite looping to run smoothly untill exit button