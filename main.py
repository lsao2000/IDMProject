import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror, askokcancel
import threading
import os
from tkinter import PhotoImage
import PIL.Image as PILIMAGE





class Interface() :
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.window = ctk.CTk()
        # self.window.protocol("WM_DELETE_WINDOW",self.close_window)
        self.window.geometry("900x600")
        self.window.resizable(width=False, height=False)
        self.window.title("IDM DOWNLOADER FREE")
        self.window.iconbitmap(self.window, 'assets/icon.ico')
       
    def responsive(self, fram):
        # Make the app responsive horizontally
        fram.columnconfigure(0, weight=1)
        fram.columnconfigure(1, weight=1)
        fram.columnconfigure(2, weight=1)
        fram.columnconfigure(3, weight=1)
        fram.columnconfigure(4, weight=1)
        fram.columnconfigure(5, weight=1)
        fram.columnconfigure(6, weight=1)
        fram.columnconfigure(7, weight=1)
        fram.columnconfigure(8, weight=1)
        fram.columnconfigure(9, weight=1)
        fram.columnconfigure(10, weight=1)
        fram.columnconfigure(11, weight=1)
        fram.columnconfigure(12, weight=1)
        # Make the app responsive vertically
        fram.rowconfigure(0, weight=1)
        fram.rowconfigure(1, weight=1)
        fram.rowconfigure(2, weight=1)
        fram.rowconfigure(3, weight=1)
        fram.rowconfigure(4, weight=1)
        fram.rowconfigure(5, weight=1)
        fram.rowconfigure(6, weight=1)
        fram.rowconfigure(7, weight=1)
        fram.rowconfigure(8, weight=1)
        fram.rowconfigure(9, weight=1)
        fram.rowconfigure(10, weight=1)

    def functionality(self):
        self.responsive(self.window)
        logo = ctk.CTkImage(dark_image=PILIMAGE.open(os.path.join('assets/logo.png')),size=(150, 100))
        label = ctk.CTkLabel(self.window, image=logo, text='')
        label.grid(row=2, column=3)
        label_Donwnload = ctk.CTkLabel(self.window,
                                       text="IDM DOWNLOADER FREE",
                                       font=("OCR A Extended", 50, "bold"),
                                       text_color="white")
        label_Donwnload.grid(row=2, column=5)
        label_url = ctk.CTkLabel(self.window,
                                 text="Enter The URL ",
                                 font=("OCR A Extended", 30, "bold"),
                                 text_color="white")
        label_url.grid(row=4, column=3, columnspan=3)
        self.Entry_url = ctk.CTkEntry(self.window,
                                 font=('OCR A Extended', 20, "bold"),
                                 width=700,
                                 height=40)
        self.Entry_url.grid(row=5, column=2, columnspan=7)
        self.choisse = ctk.CTkOptionMenu(self.window,
                                    fg_color="red",
                                    values=["MP3", "MP4"],
                                    font=("OCR A Extended", 20, "bold"),
                                    dropdown_fg_color="gray25",
                                    dropdown_font=("OCR A Extended", 15, "bold"),
                                    button_color="red",
                                    button_hover_color="#BC0000",
                                    width=150,
                                    height=40,
                                    dropdown_hover_color="#BC0000",
                                    command=lambda x : self.displayResolution())
        self.choisse.grid(row=5, column=9)
        self.resolution = ttk.Combobox(self.window,
                                       width=10)
        self.search_Resolution = ctk.CTkButton(self.window,
                                               text="Search quality",
                                               font=("OCR A Extended", 12, "bold"),
                                               fg_color="red",
                                               hover_color="#BC0000",
                                               width=150,
                                               command=self.searchThread)
        self.progress_label = ctk.CTkLabel(self.window, 
                                           text="")
        self.progress_label.grid(row=7, column=5)
        self.progress_bar = ttk.Progressbar(self.window,
                                       orient="horizontal",
                                       length=450,
                                       mode="determinate")
        self.progress_bar.grid(row=8, column=2, columnspan=8)
        self.download_Btn = ctk.CTkButton(self.window,
                                     text="DOWNLOAD",
                                     font=("OCR A Extended", 15, "bold"),
                                     fg_color="red",
                                     height=40,
                                     hover_color="#BC0000",
                                     command=self.downloadThread)
        self.download_Btn.grid(row=9, column=5)
    
    def displayResolution(self):
        if self.choisse.get() == "MP4":
            self.search_Resolution.grid(row=6, column=4, columnspan= 2)
            self.resolution.grid(row=6, column=6, columnspan=2)
        else :
            self.resolution.grid_forget()
            self.search_Resolution.grid_forget()

    # This method for asking the user if he realy want to close the window
    def close_window(self):
        if askokcancel(title='Close', message="Do you want to close the IDM DOWNLOADER"):
            self.window.destroy()
    
    def searchResolution(self):
        link = self.Entry_url.get()
        if link == "":
            showerror(title="Error", message="Provide the video link please!")
        else :
            try :
                video = YouTube(link)
                resolutions = []
                for i in video.streams.filter(file_extension='mp4'):
                    resolutions.append(i.resolution)
                # update the resolution after click search quality
                self.resolution.configure(values=resolutions)
                showinfo(title="Search Complete", message="chosse the quality of the video you want to download ")

            except :
                showerror(title="Error", message="An error occurred while searching for video resolutions!\n'\
                'Below might be the causes\n->Unstable internet connection\n->Invalid link")

    def Download(self):
        link = self.Entry_url.get()
        progress = self.progress_bar
        progress_label = self.progress_label
        window = self.window
        if link == "":
            showerror(title="Error", message="Please enter the URL")
        else:
            if self.choisse.get() == "MP4" :
                try : 
                    resolution = self.resolution.get()
                    if resolution == "" :
                        showerror(title="Error", message="None is an invalid video resolution!!\n'\
                    'Please select a valid video resolution")
                    else:
                        try:
                            def on_progress(stream, chunk, bytes_remaining):
                                total_size = stream.filesize
                                
                                def get_formated_size(total_size, factor=10, suffix='B'):
                                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                                        if total_size < factor:
                                            return f"{total_size:.2f}{unit}{suffix}"
                                        total_size /= factor
                                    return f"{total_size:.2f}Y{suffix}"
                                
                                formatted_size = get_formated_size(total_size)
                                bytes_download = total_size - bytes_remaining
                                percentage_completed = round(bytes_download / total_size * 100)
                                progress['value'] = percentage_completed
                                progress_label.configure(text= str(percentage_completed) + "%, File size:" + formatted_size)
                                window.update()
                            video = YouTube(link, on_progress_callback=on_progress)
                            video.streams.filter(res=resolution).first().download()
                            showinfo(title="Download Complete", message="Video has been downloaded successfully. ")
                            progress_label.configure(text="")
                            progress["value"] = 0
                        except:
                            showerror(title='Download Error', message="Failed to download video for this resolution")
                            progress_label.configure(text="")
                            progress["value"] = 0
                except :
                    showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the video\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                     'Make sure you have stable internet connection and the video link is valid')
                    # ressetting the progress bar and the progress label
                    progress_label.config(text='')
                    progress['value'] = 0
                    
            else : 
                try :
                    
                    def on_progress( stream, bytes_remaining):
                        total_size = stream.filesize
                        
                        def get_formatted_size(total_size, factor=1024, suffix='B'):
                            for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                                if total_size < factor:
                                    return f"{total_size:.2f}{unit}{suffix}"
                                total_size /= suffix
                            return f"{total_size:.2f}Y{suffix}"

                        formatted_size = get_formatted_size(total_size)
                        bytes_downloaded = total_size - bytes_remaining
                        percentage_completed = round(bytes_downloaded / total_size * 100)
                        progress['value'] = percentage_completed
                        progress_label.configure(text=str(percentage_completed))
                        window.update()
                    audio = YouTube(link, on_progress_callback=on_progress)
                    output = audio.streams.get_audio_only().download()
                    base, ext = os.path.splitext(output)
                    new_file = base + ".mp3"
                    os.rename(output, new_file)
                    showinfo(title="Download Complete", message="MP3 has been downloaded successfully.")
                    self.progress_label.configure(text="")
                    self.progress_bar['value'] = 0
                except:
                    showerror(title='Download Error', message='An error occurred while trying to ' \
                        'download the MP3\nThe following could ' \
                        'be the causes:\n->Invalid link\n->No internet connection\n'\
                        'Make sure you have stable internet connection and the MP3 link is valid')
                    # ressetting the progress bar and the progress label
                    self.progress_label.configure(text='')
                    self.progress_bar['value'] = 0
    # This function to search all the quality that are available
    def searchThread(self):
        t1 = threading.Thread(target=self.searchResolution)
        t1.start()

    def downloadThread(self):
        t1 = threading.Thread(target=self.Download)
        t1.start()

    def showInterface(self):
        self.window.mainloop()

class Program(Interface):
    def __init__(self):
        Interface.__init__(self)

program = Program()
program.functionality()
program.showInterface()
