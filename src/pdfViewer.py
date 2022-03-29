#Import the required Libraries
from operator import contains
import PyPDF2
from click import password_option
import fitz
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from pdf2image import convert_from_path
from diff import findPattern
import mytkPDFViewer as pdf
import os
import fnmatch 

password_dict={

}

file_dict={

}


#Create an instance of tkinter frame
win= Tk()
win.geometry("768x1024")
win.title('Simple PDF Viewer')

# Creating the frame for PDF Viewer
pdf_frame = Frame(win)
pdf_frame.pack(fill=BOTH,expand=1)

# Adding Scrollbar to the PDF frame
scrol_y = Scrollbar(pdf_frame,orient=VERTICAL)

# Setting the scrollbar to the right side
scrol_y.pack(side=RIGHT,fill=Y)

# set global variable v2
global pdf_frame2,zoomDPI,zoomDPIdefault,file
pdf_frame2 = None
zoomDPI,zoomDPIdefault=72,72

#Define a function to clear the frame
def clear_frame():
   for widgets in pdf_frame.winfo_children():
      widgets.destroy()

def choose_file():
    return filedialog.askopenfilename(title="Select a PDF", filetypes=(("PDF Files","*.pdf"),("All Files","*.*")))

#Define a function to open the pdf file
def open_pdf():
   global file,pdf_frame2
   
   if pdf_frame.winfo_exists():
      clear_frame()
      pdf.ShowPdf().img_object_li.clear()

   file=choose_file()
   if file:  
        try:
            open_pdf= fitz.open(file)
            open_pdf[0]
            v1 = pdf.ShowPdf()

            # Adding pdf location and width and height.
            pdf_frame2 = v1.pdf_view(pdf_frame,
                        pdf_location = file, 
                        width = 1500, height = 2000, zoomDPI=zoomDPIdefault)
      
        except ValueError as ve:
            password=check_password(file)
            file= decrypt_pdf(file,password)
            v1 = pdf.ShowPdf()

            # Adding pdf location and width and height.
            pdf_frame2 = v1.pdf_view(pdf_frame,
                        pdf_location = file, 
                        width = 1500, height = 2000, zoomDPI=zoomDPIdefault)

        # Placing Pdf in my gui.
        pdf_frame2.pack()

        mainloop()

def check_password(filename):

    f_name= os.path.basename(filename)
    
    for pattern in password_dict.keys():
        if  fnmatch.fnmatch(f_name, pattern):
            return password_dict[pattern]
    else: 
        return simpledialog.askstring(title="Password",
                                        prompt="Input the password:",  show='*')

def save_password(filepath,password):
    print("filepath in save password " + filepath)
    f_name= os.path.basename(filepath)
    print("f_name in save password " + f_name)

    print("password dict")
    print(password_dict)
    print("file  dict")
    print(file_dict)

    for elem in file_dict:
        pattern = findPattern(f_name, elem)
        print(pattern)
        if pattern is not None:
            password_dict[pattern]=password
    file_dict[os.path.basename(f_name)]=password


def decrypt_pdf(filename,password):
    new_pdf_file = '/var/tmp/test.pdf'
    pdf_reader = PyPDF2.PdfFileReader(filename)
    pdf_writer = PyPDF2.PdfFileWriter()

    pdf_reader.decrypt(password)
    try:
        for page in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page))
        
        save_password(filename,password)

    except PyPDF2.utils.PdfReadError:
        messagebox.showinfo(title='Failed', message='Incorrect Password!')
        clear_frame()

    result = open(new_pdf_file, 'wb')
    pdf_writer.write(result)
    result.close()
    return new_pdf_file

# Define function to Quit the window
def quit_app():
    print("password dict")
    print(password_dict)
    print("file  dict")
    print(file_dict)
    win.destroy()


def zoomIn():
    try:
        global zoomDPI,file,pdf_frame2
        zoomDPI=int(zoomDPI*1.5)

        if pdf_frame2: # if old instance exists, destroy it first
            pdf_frame2.destroy()
        v1 = pdf.ShowPdf() 
        
        # clear the image list # this corrects the bug inside tkPDFViewer module
        v1.img_object_li.clear()
        
        # Adding pdf location and width and height. 
        pdf_frame2 = v1.pdf_view(pdf_frame,
                    pdf_location = file, 
                    width = 1500, height = 2000, zoomDPI=zoomDPI)
        
        # Placing Pdf inside gui
        pdf_frame2.pack()
        mainloop()
    
    except:
        pass
    
def zoomOut():
    try:
        global zoomDPI,pdf_frame2,file
        zoomDPI=int(zoomDPI*0.5)

        if pdf_frame2: # if old instance exists, destroy it first
            pdf_frame2.destroy()
        
        # creating object of ShowPdf from tkPDFViewer. 
        v1 = pdf.ShowPdf() 
        
        # clear the image list # this corrects the bug inside tkPDFViewer module
        v1.img_object_li.clear()
        pdf.ShowPdf().img_object_li.clear()

        # Adding pdf location and width and height. 
        pdf_frame2=v1.pdf_view(pdf_frame,pdf_location = file, zoomDPI=zoomDPI)
        
        # Placing Pdf inside gui
        pdf_frame2.pack()
        mainloop()
    except:
        pass

def zoomRestore():
    try:
        global zoomDPI,zoomDPIdefault,pdf_frame2,file
        zoomDPI=zoomDPIdefault
        # messagebox.showinfo( "Hello Python", "Hello World")
        if pdf_frame2: # if old instance exists, destroy it first
            pdf_frame2.destroy()
        
        # creating object of ShowPdf from tkPDFViewer. 
        v1 = pdf.ShowPdf() 
        
        # clear the image list # this corrects the bug inside tkPDFViewer module
        v1.img_object_li.clear()
        
        # Adding pdf location and width and height. 
        pdf_frame2=v1.pdf_view(pdf_frame,pdf_location = file, zoomDPI=zoomDPI)
        
        # Placing Pdf inside gui
        pdf_frame2.pack()
        mainloop()
    except:
        pass



# Create a Menu
my_menu= Menu(win)
win.config(menu=my_menu)

# Add dropdown to the Menus
file_menu=Menu(my_menu,tearoff=False)
edit_menu=Menu(my_menu,tearoff=False)

my_menu.add_cascade(label="File",menu= file_menu)
my_menu.add_cascade(label="Edit",menu= edit_menu)

file_menu.add_command(label="Open",command=open_pdf)
file_menu.add_command(label="Clear",command=clear_frame)
file_menu.add_command(label="Quit",command=quit_app)

edit_menu.add_command(label="ZoomIn",command=zoomIn)
edit_menu.add_command(label="ZoomOut",command=zoomOut)
edit_menu.add_command(label="ZoomRestore",command=zoomRestore)


win.mainloop()
