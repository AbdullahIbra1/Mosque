from tkinter import *
import sqlite3
from database import*
from tkinter import messagebox
import folium
import webbrowser 
from ttkwidgets.autocomplete import AutocompleteEntry

main=Tk()
main.title("Mosque Managment System")
main.geometry('1000x300')
main.resizable(False, False)

conn=Db('Mosque.db','mosques')

l1=Label(main,text='ID',font=('Arial',14))
l1.place(relx=0.05,rely=0.1,anchor=CENTER)
t1=Text(main,height=1,width=15)
t1.place(relx=0.13,rely=0.06)
l2=Label(main,text='Type',font=('Arial',14))
l2.place(relx=0.05,rely=0.3,anchor=CENTER)
type=['mosque','masjed','jamee']
val=StringVar(main)
val.set(type[0])
o1=OptionMenu(main,val,*type)
o1.place(relx=0.13,rely=0.23,width=130)
l3=Label(main,text='Coordinates',font=('Arial',14))
l3.place(relx=0.06,rely=0.5,anchor=CENTER)
t2=Text(main,height=1,width=15)
t2.place(relx=0.13,rely=0.46)
l4=Label(main,text='Name',font=('Arial',14))
l4.place(relx=0.35,rely=0.1,anchor=CENTER)

names=[]
data=conn.Display_All()
for i in data:
    names.append(i[1])

t3 = AutocompleteEntry(
    
    width=14, 
    font=('Arial', 12),
    completevalues=names
    )

t3.place(relx=0.4,rely=0.06)




l5=Label(main,text='Address',font=('Arial',14))
l5.place(relx=0.35,rely=0.31,anchor=CENTER)

t4=Text(main,height=1,width=15)
t4.place(relx=0.4,rely=0.26)


l6=Label(main,text='Imam_name',font=('Arial',14))
l6.place(relx=0.33,rely=0.49,anchor=CENTER)

t5=Text(main,height=1,width=15)
t5.place(relx=0.4,rely=0.46)



lb=Listbox(main,width=70,height=17)
lb.place(relx=0.55,rely=0.05)

sb=Scrollbar(main)
sb.pack(side=RIGHT,fill=BOTH)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)




def display():
    lb.delete(0, END)
    lb.insert(END, ' ___________________________________________________________')
    col=['|  ID                                     ','|  NAME:                         ','|  TYPE:                            ','|  ADDRESS:                    ','|  COORDENATES:         ','|  IMAM_NAME:             ']
    data=conn.Display_All()
    for i in data:
        for j in range(6):
            lb.insert(END,col[j]+str(i[j]))
            
        lb.insert(END, '\n|___________________________________________________________')
        
        
        
        
def search():
    global names
    name=t3.get()
    
    if name=='':
        messagebox.showerror('ERROR',"Please enter a name first")
        return
    lb.delete(0, END)
    data=conn.search(name)   
    if len(data)==0:
        messagebox.showerror('ERROR',"No entry found having the name '"+name+"'")
        return
    
    lb.insert(END, ' ___________________________________________________________')
    col=['|  ID                                     ','|  NAME:                         ','|  TYPE:                            ','|  ADDRESS:                    ','|  COORDENATES:         ','|  IMAM_NAME:             ']
    for i in data:
        for j in range(6):
            lb.insert(END,col[j]+str(i[j]))
            
        lb.insert(END, '\n|___________________________________________________________')
        
   


def addEntry():
    mosque=Db("Mosque.db",'mosques')
    entry=[t1.get("1.0",'end-1c'),t3.get(),val.get(),t4.get("1.0",'end-1c'),t2.get("1.0",'end-1c'),t5.get("1.0",'end-1c')]
    data=conn.Display_All()
    for i in data:
        if str(i[0]) == str(entry[0]):
            messagebox.showerror("ERROR",'ID is taken')
            return   
    for i in entry:
        if i=='':
            messagebox.showerror("ERROR",'Please fill out all fields')
            return
    mosque.Insert(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5])
    messagebox.showinfo("entry added","The entery has been successfully added")       
    

def deleteEntry():
    
    id=t1.get("1.0",'end-1c')
    if id=='':
        messagebox.showerror("ERROR",'ID must be entered first')
        return
    
    data=conn.Display_All()
    for i in data:
        if str(i[0]) == id :
            conn.Delete(id)
            messagebox.showinfo('successful',"Entry have been deleted")
            return
    messagebox.showwarning('No entry',"No entry with an id '"+id+"'")
        
        

def updateImam():
    name=t3.get()
    imam_name= t5.get("1.0",'end-1c')
    if imam_name=='':
        messagebox.showerror("ERROR",'Please enter the new imam name')
        return
    if name=='':
        messagebox.showerror("ERROR",'Please enter mosque name')
        return
    conn.update_Imam(imam_name,name)
    search()
    messagebox.showinfo("Imam name updted","The imam name has been successfully updated")


def findOnMap():
    data=conn.Display_All()
    name=t3.get()
    for i in data:
        if t3.get()==i[1]:   
            co=i[4]
            xy=co.split(',')
            x=float(xy[0])
            y=float(xy[1])
            displayOnMap(x,y,name)

    
def displayOnMap(x,y,name):
    m = folium.Map(location=[x, y], zoom_start=20, tiles="OpenStreetMap")

    tooltip = "Click me!"

    folium.Marker(
    [x, y], popup="<i>"+name+"</i>", tooltip=tooltip
    ).add_to(m)

    m.save("index.html")

    webbrowser.open("index.html")



b1=Button(main,text='Display All',width=15,height=2 ,command=display)
b1.place(relx=0.13,rely=0.65)

b2=Button(main,text='Search By Name',width=15,height=2,command=search)

b2.place(relx=0.25,rely=0.65)

b3=Button(main,text='Update Entry',width=15,height=2,command=updateImam)
b3.place(relx=0.37,rely=0.65)


b4=Button(main,text='Add Entry',width=15,height=2,command=addEntry)
b4.place(relx=0.13,rely=0.8)



b5=Button(main,text='Delete Entry',width=15,height=2,command=deleteEntry)
b5.place(relx=0.25,rely=0.8)


b4=Button(main,text='Display On Map',width=15,height=2,command=findOnMap)
b4.place(relx=0.37,rely=0.8)











main.mainloop()