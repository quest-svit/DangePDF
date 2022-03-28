#Import the required Libraries
import PyPDF2
from tkinter import *
from tkinter import filedialog
from pdf2image import convert_from_path
import mytkPDFViewer as pdf

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

#Define a function to clear the frame
def clear_frame():
   for widgets in pdf_frame.winfo_children():
      widgets.destroy()

#Define a function to open the pdf file
def open_pdf():

   global file,pdf_frame2
   
   if pdf_frame.winfo_exists():
      clear_frame()
      pdf.ShowPdf().img_object_li.clear()

   file= filedialog.askopenfilename(title="Select a PDF", filetypes=(("PDF Files","*.pdf"),("All Files","*.*")))
   if file:
      v1 = pdf.ShowPdf()
      
      # Adding pdf location and width and height.
      pdf_frame2 = v1.pdf_view(pdf_frame,
                     pdf_location = file, 
                     width = 1500, height = 2000)
      
      # Placing Pdf in my gui.
      pdf_frame2.pack()
      mainloop()

# Define function to Quit the window
def quit_app():
   win.destroy()


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

win.mainloop()
