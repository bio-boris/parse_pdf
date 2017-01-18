#!/usr/bin/env python
import os
import time
import subprocess
from Tkinter import *
from ttk import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from tkMessageBox import *


import time
import threading

class Application:
    def __init__(self, master):
        self.master = master
        frame = Frame(master,width=800,height=200)
        frame.pack()

        #Select PDF button
        self.select_pdf_btn = Button(frame, text="Select PDF File", command=self.selectPDF,width=25)
        self.select_pdf_btn.grid(row=0)
        #Select Watermark button
        self.watermark_pdf_btn = Button(frame, text="WaterMark PDF File", command=self.start_thread,width=25)
        self.watermark_pdf_btn.grid(row=1)
        self.watermark_pdf_btn['state'] = 'disable'
        #View Logfile Watermark button
        self.viewLogfile_btn = Button(frame, text="View log.txt", command=self.viewLogFile,width=25)
        self.viewLogfile_btn.grid(row=2)
        #self.viewLogfile_btn['state'] = 'disable'
        
        #Labels
        self.pdf_in_filepath = StringVar()
        self.pdf_in_filepath.set("Selected Filepath:")
        self.pdf_out_filepath = StringVar()
        self.pdf_out_filepath.set("Output File:")
        self.watermark = StringVar()
        self.watermark.set("Ready...")
        self.filename = None;
      
        #Files
        self.outfile = "none"
        self.log = "log.txt"


        self.pdfFilePathLabel = Label(frame,textvariable=self.pdf_in_filepath).grid(row=0,column=1)
        self.pdfFilePathLabel2 = Label(frame,textvariable=self.pdf_out_filepath).grid(row=1,column=1)
        self.pdfFilePathLabel3 = Label(frame,textvariable=self.watermark).grid(row=4,column=0)
    
       
        self.progbar = Progressbar(frame,maximum=4, mode='indeterminate')
        self.progbar.grid(row=5)


    def successPopup(self):
        showinfo("Success","Generated file '" + self.outfile + "'")

    def noLogPopup(self):
        showinfo("No Log", self.log + " not found")


    def viewLogFile(self):
        if(not os.path.isfile(self.log)):
            return self.noLogPopup()

        with open (self.log, "r") as myfile:
            log=myfile.read()

        Dialog1 = Toplevel()
        Dialog1.geometry("500x400")
        scrollbar = Scrollbar(Dialog1)
        scrollbar.pack(side=RIGHT, fill=Y)
        text = Text(Dialog1, wrap=WORD)#yscrollcommand=scrollbar.set)
        text.insert(INSERT,log)
        text.pack()
        scrollbar.config(command=text.yview)

        Dialog1.update_idletasks()
        w = Dialog1.winfo_screenwidth()
        h = Dialog1.winfo_screenheight()
        size = tuple(int(_) for _ in Dialog1.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        Dialog1.geometry("%dx%d+%d+%d" % (size + (x, y))) 


    #Feature: Select only PDFS
    def selectPDF(self):
        filename = askopenfilename()
        if(not filename.endswith(".pdf")):
            self.pdf_in_filepath.set("That's not a PDF!")
        elif(len(filename) > 1):
            self.pdf_in_filepath.set("Selected Filepath:"  + str(filename))
            self.outfile = str(os.path.basename(filename) + ".watermarked.pdf"  ) 
            self.pdf_out_filepath.set("Output File: " + self.outfile )
            self.filename = filename
            self.watermark_pdf_btn['state'] = 'normal'


    def processPDF(self):
        fp = self.filename
        command = "python pdf_watermark.py " + str(fp) + " > " + self.log
        result =subprocess.check_output( command,  shell=True )
        

    def start_thread(self):
        self.watermark.set("Working...")
        self.watermark_pdf_btn['state'] = 'disable'
        self.progbar.start()
        self.secondary_thread = threading.Thread(target=self.processPDF)
        self.secondary_thread.start()
        #Check in 50 ms to see if the thread has finished
        self.master.after(50, self.check_thread)

    def check_thread(self):
        if self.secondary_thread.is_alive():
            self.master.after(50, self.check_thread)
        else:
            self.watermark_pdf_btn['state'] = 'normal'
            self.viewLogfile_btn['state'] = 'normal'
            self.watermark.set("Done")
            self.successPopup()
            self.progbar.stop()  
    
def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y))) 


root = Tk()
root.title("Select PDF for Watermarks")
root.geometry("800x200")
#center(root)
app = Application(root)
#center(root)
root.mainloop()
