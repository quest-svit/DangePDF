#Import the required Libraries
from operator import contains
import PyPDF2
from click import password_option
import fitz
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from pdf2image import convert_from_path
from encrypt_utils import EncryptUtils
from pattern import find_pattern
import mytkPDFViewer as pdf
import os
import fnmatch 
import sys
import sql_utils


#Create an instance of tkinter frame
win= Tk()
win.geometry("768x1024")
win.title('Dange PDF Viewer')

# Creating the frame for PDF Viewer
pdf_frame = Frame(win)
pdf_frame.pack(fill=BOTH,expand=1)

# Adding Scrollbar to the PDF frame
scrol_y = Scrollbar(pdf_frame,orient=VERTICAL)

# Setting the scrollbar to the right side
scrol_y.pack(side=RIGHT,fill=Y)

# set global variables
global pdf_frame2, zoomDPI, zoomDPIdefault, file
pdf_frame2 = None
zoomDPI, zoomDPIdefault=72,72
file = None
sql_utils=sql_utils.SqlUtils()
TMP_FOLDER="/var/tmp/"

def clear_frame():
    ''' Define a function to clear the frame '''

    for widgets in pdf_frame.winfo_children():
        widgets.destroy()

def choose_file():
    return filedialog.askopenfilename(title="Select a PDF", filetypes=(("PDF Files","*.pdf"),("All Files","*.*")))

def open_pdf(filename=None):
    '''Function to open the pdf file '''

    global file, pdf_frame2
   
    if pdf_frame.winfo_exists():
        clear_frame()
        pdf.ShowPdf().img_object_li.clear()

    if filename is None:
        file=choose_file()
    else:
        file=filename

    if file:
        try:
            open_pdf= fitz.open(file)
            open_pdf[0]  # IF file is encrypted then this line will throw ValueError
            pdf_frame2=display_pdf_file()

        except ValueError:
            password=check_password(file)
            file= decrypt_pdf(file,password)
            pdf_frame2=display_pdf_file()

        # Placing Pdf in my gui.
        pdf_frame2.pack()

    mainloop()

def display_pdf_file():
    global file, pdf_frame

    return pdf.ShowPdf().pdf_view(pdf_frame,
                        pdf_location = file, 
                        width = 1500, height = 2000, zoomDPI=zoomDPIdefault)

def check_password(filename):

    f_name= os.path.basename(filename)
    
    for pattern in sql_utils.get_all_patterns():
        if  fnmatch.fnmatch(f_name, pattern):
            return sql_utils.get_password_for_pattern(pattern)
    else: 
        return simpledialog.askstring(title="Password",
                                        prompt="Input the password:",  show='*')

def save_password(filepath,password):
    f_name= os.path.basename(filepath)

    for elem in sql_utils.get_all_filenames():
        pattern = find_pattern(f_name, elem)
        
        if pattern is not None:
            sql_utils.insert_into_pattern(pattern,password)
    sql_utils.insert_into_file(os.path.basename(f_name),password)


def decrypt_pdf(filename,password):
    new_pdf_file = TMP_FOLDER+EncryptUtils.random_filename_generator()+".pdf"
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
file_menu.add_command(label="Close",command=clear_frame)
file_menu.add_command(label="Quit",command=quit_app)

edit_menu.add_command(label="ZoomIn",command=zoomIn)
edit_menu.add_command(label="ZoomOut",command=zoomOut)
edit_menu.add_command(label="ZoomRestore",command=zoomRestore)

    
if len(sys.argv) == 2:
    filename = os.getcwd()+ "/" + sys.argv[1]
else:
    filename = None

open_pdf(filename)

win.mainloop()
