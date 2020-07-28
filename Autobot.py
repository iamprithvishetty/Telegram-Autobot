import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError,UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from threading import Thread
import asyncio
import time
import random
import traceback
import csv

LARGE_FONT=("Verdana",12)

#CHANGE PAGE VARIABLES
file_name = "data.csv" #FILE WITH MAIN NO
temp_list1=list() #FILE TO RETRIEVE DATA from data.csv
value=0
####

#MAIN PAGE VARIABLE
Press_check=0

#########ADD PAGEEEE#########

#ADDING NO TO CSV FILE
def add_main(phone, id, hash, value):
    global file_name, temp_list1
    if value == 0:
        fieldname = ["Phone_No", "Api_Id", "Api_Hash","Verification"]
        with open(file_name, "a", newline='') as csvfile:
            Writer = csv.DictWriter(csvfile, fieldnames=fieldname)
            # Writer.writeheader()
            Writer.writerow({"Phone_No": phone, "Api_Id": id, "Api_Hash": hash,"Verification": "Not Verified"})
        with open(file_name, "r") as csvfile:
            reader2 = csv.DictReader(csvfile)
            temp_list1 = list()
            for row in reader2:
                temp_list1.append(row)

#UPDATE NOS
def update_main(phone,id,hash,value):
    global file_name,temp_list1
    if value==1:
        with open(file_name, "r") as csvfile:
            reader1 = csv.DictReader(csvfile)
            fieldname = ['Phone_No', 'Api_Id', 'Api_Hash','Verification']
            temp_list = list()
            for row in reader1:
                if row["Phone_No"] == phone:
                    row["Api_Id"] = id
                    row["Api_Hash"] = hash
                    row["Verification"]="Not Verified"
                temp_list.append(row)

        with open(file_name, "w+", newline='') as csvfile:
            writer1 = csv.DictWriter(csvfile, fieldnames=fieldname)
            writer1.writeheader()
            writer1.writerows(temp_list)

        with open(file_name, "r") as csvfile:
            reader2 = csv.DictReader(csvfile)
            temp_list1 = list()
            for row in reader2:
                temp_list1.append(row)
    print("update_main",temp_list1)

#DELETE NOS
def delete_main(phone,value):
    global file_name,temp_list1
    if value==2:
        with open(file_name, "r") as csvfile:
            reader1 = csv.DictReader(csvfile)
            fieldname = ['Phone_No', 'Api_Id', 'Api_Hash','Verification']
            temp_list = list()
            for row in reader1:
                if row["Phone_No"] == phone:
                    continue
                temp_list.append(row)

        with open(file_name, "w+", newline='') as csvfile:
            writer1 = csv.DictWriter(csvfile, fieldnames=fieldname)
            writer1.writeheader()
            writer1.writerows(temp_list)

        with open(file_name, "r") as csvfile:
            reader2 = csv.DictReader(csvfile)
            temp_list1 = list()
            for row in reader2:
                temp_list1.append(row)

#Setting Value for add,update,delete i.e selection
def clicked(value1):
    global value
    value=value1

#Currently Selected item
def selectItem():
    global main_list,treetime,Phone,Id,Hash
    curItem = treetime.focus()
    print(treetime.item(curItem))
    main_list=treetime.item(curItem)["values"]
    print(main_list)
    Phone.delete(0,len(Phone.get()))
    Id.delete(0, len(Id.get()))
    Hash.delete(0, len(Hash.get()))
    Phone.insert(0,"+"+str(main_list[0]))
    Id.insert(0,main_list[1])
    Hash.insert(0,main_list[2])

def tree_start():
    global treetimestart

####START PAGE
def wait():
    global Press_check
    while Press_check!=1:
        time.sleep(1)
    Press_check=0

def Press():
    global Press_check
    Press_check=1

def Update_MainPage():
    global countstart,treetimestart,temp_list1
    for i in range(1, countstart):
        treetimestart.delete(str(i))
    countstart = 1
    for i in range(0, len(temp_list1)):
        treetimestart.insert("", "end", str(countstart), text=str(countstart), value=(
            temp_list1[len(temp_list1) - countstart]["Phone_No"],
            temp_list1[len(temp_list1) - countstart]["Api_Id"],
            temp_list1[len(temp_list1) - countstart]["Api_Hash"],
            temp_list1[len(temp_list1) - countstart]["Verification"]))
        countstart = countstart + 1

def authorize():
    global temp_list1,Input_label,Input,treetimestart,countstart
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)
    count=0
    print(temp_list1)

    for user in temp_list1:
        try:
            print(user)
            if user["Verification"]=="Not Verified":
                client = TelegramClient(user["Phone_No"], user["Api_Id"], user["Api_Hash"],loop=loop1)
                client.connect()
                if not client.is_user_authorized():
                    client.send_code_request(user["Phone_No"])
                    Input_label['text']="Enter OTP: \n"+user["Phone_No"]
                    wait()
                    try:
                        client.sign_in(Phone,Input.get())
                        temp_list1[count]["Verification"]="Verified"
                        write_verify(user["Phone_No"])

                    except:
                        print("Error Encountered")
                        Input_label['text'] = "Error Encountered"
                    Input.delete(0,'end')
                    Input_label['text']="Hey :"

                else:
                    temp_list1[count]["Verification"] = "Verified"
                    write_verify(user["Phone_No"])
                    print("client is connected")
                client.disconnect()
            print(countstart)
            for i in range(1,countstart):
                treetimestart.delete(str(i))
            countstart=1
            for i in range(0, len(temp_list1)):
                treetimestart.insert("", "end",str(countstart), text=str(countstart), value=(
                    temp_list1[len(temp_list1) - countstart]["Phone_No"],
                    temp_list1[len(temp_list1) - countstart]["Api_Id"],
                    temp_list1[len(temp_list1) - countstart]["Api_Hash"],
                    temp_list1[len(temp_list1) - countstart]["Verification"]))
                countstart = countstart + 1
            count=count+1
        except:
            print("Couldn't connect")
            count=count+1

def write_verify(phone):
    global file_name
    with open(file_name, "r") as csvfile:
        reader1 = csv.DictReader(csvfile)
        fieldname = ['Phone_No', 'Api_Id', 'Api_Hash','Verification']
        temp_list = list()
        for row in reader1:
            if row["Phone_No"] == phone:
                row["Verification"]="Verified"
            temp_list.append(row)

    with open(file_name, "w+", newline='') as csvfile:
        writer1 = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer1.writeheader()
        writer1.writerows(temp_list)

    with open(file_name, "r") as csvfile:
        reader2 = csv.DictReader(csvfile)
        temp_list1 = list()
        for row in reader2:
            temp_list1.append(row)

####PAGE EXPORT

def export_data_change():
    global temp_list1,Phone_Options,variable
    phone_no_list = list()
    for phone in range(0, len(temp_list1)):
        if temp_list1[phone]["Verification"] == "Verified":
            phone_no_list.append(temp_list1[phone]["Phone_No"])
    Phone_Options['menu'].delete(0, 'end')
    print(phone_no_list)
    for phone in phone_no_list:
        Phone_Options['menu'].add_command(label=phone, command=tk._setit(variable, phone))




def Fetch_Groups():
    global count_group,treetimegroup,Phone_Options,variable,client_list,groups,list_groups
    try:
        loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        list_groups=list()
        Selected_No=variable.get()
        for i in range(0,len(temp_list1)):
            if temp_list1[i]["Phone_No"]== Selected_No:
                client_list=temp_list1[i]
                break
        client = TelegramClient(client_list["Phone_No"], client_list["Api_Id"], client_list["Api_Hash"],loop=loop1)
        client.connect()
        chats = []
        last_date = None
        chunk_size = 200
        groups = []

        result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)
        for chat in chats:
            groups.append(chat)

        #print('Choose a group to scrape members from:')
        i = 1
        for g in groups:
            g_list=[str(i),str(g.id),str(g.title)]
            #print(str(i) + '-' + str(g.id))
            list_groups.append(g_list)
            i += 1
        print(list_groups)
        for i in range(1, count_group):
            treetimegroup.delete(str(i))
        count_group = 1
        for i in range(0, len(list_groups)):
            treetimegroup.insert("", "end", str(count_group), text=str(count_group), value=(
                list_groups[i][1],
                list_groups[i][2]))
            count_group = count_group + 1
            client.disconnect()
    except:
        client.disconnect()
    finally:
        print("")


def ScrapeMembers():
    global client_list,group_list_pos,groups,list_groups,group_input
    try:
        target_group = groups[group_list_pos]
        loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        client = TelegramClient(client_list["Phone_No"], client_list["Api_Id"], client_list["Api_Hash"], loop=loop1)
        client.connect()
        #group_input.delete(0, last="end")
        #group_input.insert(0,'Fetching Members...' )
        print('Fetching Members...')
        all_participants = []
        all_participants = client.get_participants(target_group, aggressive=True)
        #group_input.delete(0, last="end")
        #group_input.insert(0, 'Saving In file...')
        print('Saving In file...')
        with open(group_input.get()+".csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
            for user in all_participants:
                if user.username:
                    username = user.username
                else:
                    username = ""
                if user.first_name:
                    first_name = user.first_name
                else:
                    first_name = ""
                if user.last_name:
                    last_name = user.last_name
                else:
                    last_name = ""
                name = (first_name + ' ' + last_name).strip()
                writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
        group_input.delete(0, last="end")
        group_input.insert(0, 'Members scraped successfully.')
        print('Members scraped successfully.')
        client.disconnect()
    except:
        client.disconnect()
        group_input.delete(0, last="end")
        group_input.insert(0, "Couldn't Fetch")
        print("Couldn't Fetch")

###ADD PAGE

def import_data_change():
    global temp_list1,Phone_Options_Add,variable_Add
    phone_no_list = list()
    for phone in range(0, len(temp_list1)):
        if temp_list1[phone]["Verification"] == "Verified":
            phone_no_list.append(temp_list1[phone]["Phone_No"])
    Phone_Options_Add['menu'].delete(0, 'end')
    print(phone_no_list)
    for phone in phone_no_list:
        Phone_Options_Add['menu'].add_command(label=phone, command=tk._setit(variable_Add, phone))

def Fetch_Groups_Add():
    global count_group_add,treetimegroup_add,Phone_Options_Add,variable_Add,client_list_add,groups_add,list_groups_add,time_select_lower,time_select_upper
    try:
        loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(loop1)
        list_groups_add=list()
        Selected_No=variable_Add.get()
        for i in range(0,len(temp_list1)):
            if temp_list1[i]["Phone_No"]== Selected_No:
                client_list_add=temp_list1[i]
                break
        client = TelegramClient(client_list_add["Phone_No"], client_list_add["Api_Id"], client_list_add["Api_Hash"],loop=loop1)
        client.connect()
        chats = []
        last_date = None
        chunk_size = 200
        groups_add = []

        result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)
        for chat in chats:
            groups_add.append(chat)
        #print('Choose a group to scrape members from:')
        i = 1
        for g in groups_add:
            g_list=[str(i),str(g.id),str(g.title)]
            #print(str(i) + '-' + str(g.id))
            list_groups_add.append(g_list)
            i += 1
        print(list_groups_add)
        for i in range(1, count_group_add):
            treetimegroup_add.delete(str(i))
        count_group_add = 1
        for i in range(0, len(list_groups_add)):
            treetimegroup_add.insert("", "end", str(count_group_add), text=str(count_group_add), value=(
                list_groups_add[i][1],
                list_groups_add[i][2]))
            count_group_add = count_group_add + 1
            client.disconnect()
    except:
        try:
            client.disconnect()
        except:
            print('Error Encountered')

def Add_Groups():
    global client_list_add, group_list_pos, groups_add, list_groups, group_input, list_groups_add,time_select_lower,time_select_upper,users,Clear_Added,Clear_Disabled,Error_label,users_full,file_add
    Clear_Added_list=[]
    Clear_Disabled_list=[]
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)
    client = TelegramClient(client_list_add["Phone_No"], client_list_add["Api_Id"], client_list_add["Api_Hash"],
                            loop=loop1)
    client.connect()
    target_group = groups_add[int(group_list_pos_add)]
    #print(target_group)
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
    n=0
    for user in users:
        n += 1
        if n % 50 == 0:
            time.sleep(900)
        try:
            print("Adding {}".format(user['id']))
            Error_label['text']="Adding {"+str(user['id'])+"}\n"

            user_to_add = InputPeerUser(user['id'], user['access_hash'])

            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("Waiting for "+time_select_lower.get()+" - "+time_select_upper.get() +"Seconds...")
            Error_label['text'] = "Waiting for "+time_select_lower.get()+" - "+time_select_upper.get() +"Seconds..."
            time.sleep(random.randrange(int(time_select_lower.get()), int(time_select_upper.get())))
            Clear_Added_list.append(user)
            Error_label['text'] = "Added : "+str(user['id'])
        except PeerFloodError:
            Error_label['text']="Getting Flood Error from telegram. Script is stopping now.\n Please try again after some time."
            print("Getting Flood Error from telegram.\n Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            Error_label['text']="The user's privacy settings do not allow you to do this.\n Skipping."
            print("The user's privacy settings do not allow you to do this. Skipping.")
            Clear_Disabled_list.append(user)
        except:
            traceback.print_exc()
            Error_label['text'] = "Unexpected Error"
            print("Unexpected Error")
            continue

    print("Clear dis",Clear_Disabled.get(),"Clear add",Clear_Added.get())

    print(Clear_Added_list)
    print(Clear_Disabled_list)

    if Clear_Added.get()==1 and Clear_Disabled.get()==0:
        for user_check in Clear_Added_list:
            if user_check in users_full:
                users_full.remove(users_full.index(user_check))
        for user_check in Clear_Disabled_list:
            if user_check in users_full:
                users_full.remove(users_full.index(user_check))



    if Clear_Added.get()==0 and Clear_Disabled.get()==1:
        for user_check in Clear_Disabled_list:
            if user_check in users_full:
                users_full.remove(users_full.index(user_check))

    if Clear_Added.get()==1 and Clear_Disabled.get()==0:
        for user_check in Clear_Added_list:
            if user_check in users_full:
                users_full.remove(users_full.index(user_check))

    with open(file_add, "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in users_full:
            writer.writerow([user["username"], user["id"], user["access_hash"], user["name"],user["group_name"],user["group_id"]])

    client.disconnect()




class Telegram(tk.Tk):

    def __init__(self,*args,**kwargs):

        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self,"Telegram")
        tk.Tk.geometry(self,"830x600")
        #tk.Tk.iconbitmap(self,default="")

        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand="True")
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames={}

        #LOAD THE CSV FILE FIRST
        with open(file_name, "r") as csvfile:
            reader2 = csv.DictReader(csvfile)
            for row in reader2:
                temp_list1.append(row)

        for F in (StartPage,PageOne,PageTwo,PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)



    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        global Input_label,Input
        Change_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="CHANGE", font=("Courier", "10", "bold"),
                                  command=lambda: controller.show_frame(PageOne))
        Change_button.grid(row=0, column=0,padx=50,pady=25,ipadx=5,ipady=5)
        Export_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="EXPORT", font=("Courier", "10", "bold"),
                                  command=lambda: [controller.show_frame(PageTwo),export_data_change()])
        Export_button.grid(row=0, column=1,ipadx=5,ipady=5,padx=160)
        Import_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="ADD USERS", font=("Courier", "10", "bold"),
                                  command=lambda: [controller.show_frame(PageThree),import_data_change()])
        Import_button.grid(row=0, column=2,ipadx=5,ipady=5)

        Input_label=tk.Label(self,text="Hey :",font=("Courier", "12", "bold"))
        Input_label.grid(row=4,column=0)
        Input = tk.Entry(self, width=50, borderwidth=5, bg="#5ba6b0", fg="black", font="Calibri 15 bold")
        Input.grid(row=4, column=1, columnspan=1, padx=5, pady=25, ipadx=5, ipady=5)
        Enter_Button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                 fg="black", text="ENTER", font=("Courier", "10", "bold"), command=lambda:[Press(),StartPage.tree_change1(self)])
        Enter_Button.grid(row=4, column=2, padx=5, pady=25)
        Verify_Button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                 fg="black", text="VERIFY", font=("Courier", "10", "bold"),command=lambda:Thread(target=authorize).start())
        Verify_Button.grid(row=5, column=1, padx=5, pady=25)
        self.tree_change1()

    def tree_change1(self):
        global treetimestart,countstart
        treetimestart= ttk.Treeview(self)
        try:
            treetimestart.destroy()
            treetimestart = ttk.Treeview(self)
            treetimestart["columns"] = ("PHONE NO", "API KEY", "API HASH","VERIFICATION")

            treetimestart.column("#0", width=40, minwidth=30)
            treetimestart.column("PHONE NO", width=100, minwidth=100)
            treetimestart.column("API KEY", width=150, minwidth=150)
            treetimestart.column("API HASH", width=200, minwidth=200)
            treetimestart.column("VERIFICATION",width=50,minwidth=50)

            treetimestart.heading("#0", text="id", anchor=tk.W)
            treetimestart.heading("PHONE NO", text="Phone No", anchor=tk.W)
            treetimestart.heading("API KEY", text="API Keys", anchor=tk.W)
            treetimestart.heading("API HASH", text="API Hash", anchor=tk.W)
            treetimestart.heading("VERIFICATION", text="Verification", anchor=tk.W)
            countstart = 1
            for i in range(0, len(temp_list1)):
                treetimestart.insert("", "end",str(countstart) ,text=str(countstart), value=(
                    temp_list1[len(temp_list1) - countstart]["Phone_No"], temp_list1[len(temp_list1) - countstart]["Api_Id"],
                    temp_list1[len(temp_list1) - countstart]["Api_Hash"],temp_list1[len(temp_list1) - countstart]["Verification"]))
                countstart = countstart + 1

            treetimestart.grid(row=1, column=0, columnspan=3, padx=2, pady=2, sticky=tk.NSEW)
            Scrollbarstart = tk.Scrollbar(self, orient="vertical", command=treetimestart.yview)
            treetimestart.configure(yscroll=Scrollbarstart.set)
            Scrollbarstart.grid(row=1, column=3,sticky="nse")
        except:
            print("Error encountered")




class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        global Phone,Id,Hash
        tk.Frame.__init__(self, parent)
        Check_Var = tk.IntVar()
        back_button=tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                               fg="black", text="BACK", font=("Courier", "10", "bold"),
                               command=lambda:[controller.show_frame(StartPage),Update_MainPage()])

        add_button = tk.Radiobutton(self, text="ADD", variable=Check_Var, value=0,
                                    command=lambda: clicked(Check_Var.get()))
        # add_button.pack()

        update_button = tk.Radiobutton(self, text="UPDATE", variable=Check_Var, value=1,
                                       command=lambda: clicked(Check_Var.get()))
        # update_button.pack()

        delete_button = tk.Radiobutton(self, text="DELETE", variable=Check_Var, value=2,
                                       command=lambda: clicked(Check_Var.get()))
        # delete_button.pack()

        label_phone = tk.Label(self, fg="black", text="PHONE", font=("Courier", "20", "bold italic"))
        # label_phone.pack()

        Phone = tk.Entry(self, width=50, borderwidth=5, bg="#5ba6b0", fg="black", font="Calibri 15 bold")
        # Phone.pack(ipady=3)

        label_id = tk.Label(self, fg="black", text="API_ID", font=("Courier", "20", "bold italic"))
        # label_id.pack()

        Id = tk.Entry(self, width=50, borderwidth=5, bg="#5ba6b0", fg="black", font="Calibri 15 bold")
        # Id.pack(ipady=3)

        label_hash = tk.Label(self, fg="black", text="API_HASH", font=("Courier", "20", "bold italic"))
        # label_hash.pack()

        Hash = tk.Entry(self, width=50, borderwidth=5, bg="#5ba6b0", fg="black", font="Calibri 15 bold")
        # Hash.pack(ipady=3)

        Phone_No = Phone.get()
        Api_Id = Id.get()
        Api_Hash = Hash.get()

        button_add = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                               fg="black", text="ADD", font=("Courier", "10", "bold"),
                               command=lambda: [add_main(Phone.get(), Id.get(), Hash.get(), value), tree_change()])
        # button_add.pack()

        button_update = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="UPDATE", font=("Courier", "10", "bold"),
                                  command=lambda: [update_main(Phone.get(), Id.get(), Hash.get(), value),
                                                   tree_change()])
        # button_update.pack()

        button_delete = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="DELETE", font=("Courier", "10", "bold"),
                                  command=lambda: [delete_main(Phone.get(), value), tree_change()])
        # button_delete.pack()

        button_select = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="SELECT", font=("Courier", "10", "bold"),
                                  command=lambda: selectItem())

        def tree_change():
            global treetime
            treetime = ttk.Treeview(self)
            try:
                treetime.destroy()
                treetime = ttk.Treeview(self)
                treetime["columns"] = ("PHONE NO", "API KEY", "API HASH")

                treetime.column("#0", width=40, minwidth=30)
                treetime.column("PHONE NO", width=150, minwidth=120)
                treetime.column("API KEY", width=250, minwidth=200)
                treetime.column("API HASH", width=350, minwidth=300)

                treetime.heading("#0", text="id", anchor=tk.W)
                treetime.heading("PHONE NO", text="Phone No", anchor=tk.W)
                treetime.heading("API KEY", text="API Keys", anchor=tk.W)
                treetime.heading("API HASH", text="API Hash", anchor=tk.W)
                count = 1
                for i in range(0, len(temp_list1)):
                    treetime.insert("", "end", text=str(count), value=(
                        temp_list1[len(temp_list1) - count]["Phone_No"], temp_list1[len(temp_list1) - count]["Api_Id"],
                        temp_list1[len(temp_list1) - count]["Api_Hash"]))
                    count = count + 1

                treetime.grid(row=5, column=0, columnspan=3, padx=2, pady=2, sticky=tk.NSEW)
                Scrollbar = tk.Scrollbar(self, orient="vertical", command=treetime.yview)
                treetime.configure(yscroll=Scrollbar.set)
                Scrollbar.grid(row=5, column=4, ipady=100)
            except:
                print("Error encountered")

        tree_change()
        back_button.grid(row=0, column=0, pady=10,padx=20, ipady=5,sticky="nsew")
        add_button.grid(row=0, column=1,columnspan=2,padx=50, pady=10, ipady=5,sticky="w")
        update_button.grid(row=0, column=1,columnspan=2,padx=200, pady=10, ipady=5,sticky="w")
        delete_button.grid(row=0, column=1,columnspan=2, pady=10,padx=200, ipady=5,sticky="e")
        label_phone.grid(row=1, column=0, padx=25, pady=10, ipadx=5, ipady=5)
        Phone.grid(row=1, column=1, padx=5, pady=10, ipadx=5, ipady=5)
        button_delete.grid(row=1, column=2, padx=5, pady=10, ipadx=5, ipady=5)
        label_id.grid(row=2, column=0, padx=25, pady=10, ipadx=5, ipady=5)
        Id.grid(row=2, column=1, padx=5, pady=10, ipadx=5, ipady=5)
        label_hash.grid(row=3, column=0, padx=25, pady=10, ipadx=5, ipady=5)
        Hash.grid(row=3, column=1, padx=5, pady=10, ipadx=5, ipady=10)
        button_add.grid(row=4, column=0, padx=5, pady=10, ipadx=5, ipady=5)
        button_update.grid(row=4, column=1, padx=5, pady=10, ipadx=5, ipady=5)
        button_select.grid(row=4, column=2, padx=5, pady=10, ipadx=5, ipady=5)

class PageTwo(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        global temp_list1,count_group,treetimegroup,Phone_Options,variable,group_input,No_select_input
        back_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                fg="black", text="BACK", font=("Courier", "10", "bold"),
                                command=lambda: [controller.show_frame(StartPage)])
        back_button.grid(row=0, column=0, pady=10, padx=20, ipadx=10,ipady=5,sticky="n")
        phone_no_list=list()
        for phone in range(0,len(temp_list1)):
            if temp_list1[phone]["Verification"]=="Verified":
                phone_no_list.append(temp_list1[phone]["Phone_No"])

        variable = tk.StringVar(self)
        try:
            variable.set("Select Phone No")  # default value
            Phone_Options = tk.OptionMenu(self, variable, *phone_no_list)
        except:
            variable.set("Select Phone No")
            Phone_Options = tk.OptionMenu(self, variable, "Empty")

        Phone_Options.grid(row=0, column=4, pady=10, padx=20, ipadx=5,ipady=5,sticky="n")

        select_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                fg="black", text="SELECT", font=("Courier", "10", "bold"),
                                command=lambda: [Thread(target=Fetch_Groups).start()])
        select_button.grid(row=0, column=4, pady=100, padx=20, ipadx=10, ipady=5, sticky="n")

        count_group=1
        treetimegroup = ttk.Treeview(self)
        treetimegroup["columns"] = ("GROUP ID","GROUPS")

        treetimegroup.column("#0", width=40, minwidth=30)
        treetimegroup.column("GROUP ID", width=150, minwidth=150)
        treetimegroup.column("GROUPS", width=300, minwidth=300)

        treetimegroup.heading("#0", text="ID", anchor=tk.W)
        treetimegroup.heading("GROUP ID", text="GROUP ID", anchor=tk.W)
        treetimegroup.heading("GROUPS", text="GROUPS", anchor=tk.W)

        treetimegroup.grid(row=0, column=1, columnspan=2, padx=2, pady=10, sticky=tk.NSEW)
        Scrollbargroup = tk.Scrollbar(self, orient="vertical", command=treetimegroup.yview)
        treetimegroup.configure(yscroll=Scrollbargroup.set)
        treetimegroup.bind("<Double-1>",self.OnDoubleClick)
        Scrollbargroup.grid(row=0, column=3, pady=10, sticky="ns")

        GroupId_Label=tk.Label(self, fg="black", text="Group Selected:", font=("Courier", "10", "bold"))
        GroupId_Label.grid(row=1,column=0,pady=10,padx=10)

        group_input = tk.Entry(self, width=40, borderwidth=5, bg="#5ba6b0", fg="black", font="Calibri 15 bold")
        group_input.grid(row=1, column=1, columnspan=1, padx=5, pady=25, ipadx=5, ipady=5)

        fetch_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="FETCH", font=("Courier", "10", "bold"),
                                  command=lambda: [Thread(target=ScrapeMembers).start()])
        fetch_button.grid(row=1, column=4, pady=10, padx=20, ipadx=10, ipady=5)

    def OnDoubleClick(self,event):
        global treetimegroup,group_input,group_list_pos
        group_input.delete(0,last="end")
        sel_item = treetimegroup.focus()
        group_input.insert(0,str(treetimegroup.item(sel_item)["values"][0]))
        group_list_pos=int(treetimegroup.item(sel_item)["text"])-1
        print(group_list_pos)
        #print("you clicked on", treetimegroup.item(item, "text"))


class PageThree(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        global Phone_Options_Add,variable_Add,count_group_add,treetimegroup_add,group_input_add,time_select_lower,time_select_upper,count_user,treetimegroup_add_users,No_select_input,Clear_Added,Clear_Disabled,Error_label
        back_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                fg="black", text="BACK", font=("Courier", "10", "bold"),
                                command=lambda: [controller.show_frame(StartPage)])
        back_button.grid(row=0, column=0, pady=10, padx=20, ipadx=10, ipady=5, sticky="n")
        phone_no_list = list()
        for phone in range(0, len(temp_list1)):
            if temp_list1[phone]["Verification"] == "Verified":
                phone_no_list.append(temp_list1[phone]["Phone_No"])

        variable_Add = tk.StringVar(self)
        try:
            variable_Add.set("Select Phone No")  # default value
            Phone_Options_Add = tk.OptionMenu(self, variable_Add, *phone_no_list)
        except:
            variable_Add.set("Select Phone No")
            Phone_Options_Add = tk.OptionMenu(self, variable_Add, "Empty")

        Phone_Options_Add.grid(row=0, column=4, pady=10, padx=20, ipadx=5, ipady=5, sticky="n")
        select_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                  fg="black", text="GET", font=("Courier", "10", "bold"),
                                  command=lambda: [Thread(target=Fetch_Groups_Add).start()])
        select_button.grid(row=0, column=4, padx=20,pady=10, ipadx=10, ipady=5, sticky="s")

        count_group_add = 1
        treetimegroup_add = ttk.Treeview(self,height=5)
        treetimegroup_add["columns"] = ("GROUP ID", "GROUPS")

        treetimegroup_add.column("#0", width=40, minwidth=30)
        treetimegroup_add.column("GROUP ID", width=168, minwidth=168)
        treetimegroup_add.column("GROUPS", width=300, minwidth=300)

        treetimegroup_add.heading("#0", text="ID", anchor=tk.W)
        treetimegroup_add.heading("GROUP ID", text="GROUP ID", anchor=tk.W)
        treetimegroup_add.heading("GROUPS", text="GROUPS", anchor=tk.W)

        treetimegroup_add.grid(row=0, column=1, columnspan=2, pady=10, sticky="n")
        Scrollbargroup_add = tk.Scrollbar(self, orient="vertical", command=treetimegroup_add.yview)
        treetimegroup_add.configure(yscroll=Scrollbargroup_add.set)
        treetimegroup_add.bind("<Double-1>", self.OnDoubleClick)
        Scrollbargroup_add.grid(row=0, column=3,pady=10, sticky="ns")

        treetimegroup_add_users=ttk.Treeview(self,height=12)
        treetimegroup_add_users["columns"]=("Users")

        treetimegroup_add_users.column('#0',width=45,minwidth=45)
        treetimegroup_add_users.column('Users', width=185, minwidth=185)

        treetimegroup_add_users.heading("#0", text="No", anchor=tk.W)
        treetimegroup_add_users.heading("Users", text="Users", anchor=tk.W)

        treetimegroup_add_users.grid(row=1, column=1,columnspan=1,padx=2, pady=1,sticky="nsew")
        count_user=1

        Scrollbargroup_add_users = tk.Scrollbar(self, orient="vertical", command=treetimegroup_add_users.yview)
        treetimegroup_add_users.configure(yscroll=Scrollbargroup_add_users.set)
        Scrollbargroup_add_users.grid(row=1, column=1, pady=3,sticky="nse",padx=4)

        User_label = tk.Label(self, text="Select Users From:", font=("Courier", "10", "bold"))
        User_label.grid(row=1, column=2, pady=10, ipadx=1, ipady=1,sticky="nw",padx=30)

        users_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                fg="black", text="USERS", font=("Courier", "8", "bold"),
                                command=lambda: [self.open_file()])
        users_button.grid(row=1, column=2, pady=8, padx=0, ipadx=1, ipady=1, sticky="ne")

        No_select_label = tk.Label(self, text="Add          Users", font=("Courier", "10", "bold"))
        No_select_label.grid(row=1, column=2, pady=70, ipadx=1, ipady=1,sticky="nw",padx=30)

        No_select_input = tk.Entry(self, width=4, borderwidth=5, bg="#5ba6b0", fg="black", font="Calibri 15 bold")
        No_select_input.grid(row=1, column=2,padx=67, pady=62, ipadx=5, ipady=5,sticky="nw")
        No_select_input.insert(0,"60")
        Time_select_label = tk.Label(self, text="Interval between     s and     s", font=("Courier", "10", "bold"))
        Time_select_label.grid(row=1, column=2,columnspan=1, pady=130, ipadx=1, ipady=1, sticky="nw")
        time_select_lower = tk.Entry(self, width=2, borderwidth=2, bg="#5ba6b0", fg="black", font="Calibri 10 bold")
        time_select_lower.grid(row=1, column=2, pady=128,padx=103, ipadx=5, ipady=5, sticky="nse",)
        time_select_lower.insert(0, "5")
        time_select_upper = tk.Entry(self, width=2, borderwidth=2, bg="#5ba6b0", fg="black", font="Calibri 10 bold")
        time_select_upper.grid(row=1, column=2, pady=128,padx=25, ipadx=5, ipady=5, sticky="nse")
        time_select_upper.insert(0, "10")

        Clear_Added = tk.IntVar()
        Clear_Disabled = tk.IntVar()
        C1 = tk.Checkbutton(self, text="Clear users added to the group", variable=Clear_Added,onvalue=1, offvalue=0, height=2,width=30,font=("Courier", "10", "bold"))
        C2 = tk.Checkbutton(self, text="Clear disabled users", variable=Clear_Disabled,onvalue=1, offvalue=0, height=2,width=30,font=("Courier", "10", "bold"))

        C1.grid(row=1,column=2,columnspan=1,pady=80,sticky="se")
        C2.grid(row=1, column=2, pady=50, sticky="sw")
        group_input_add = tk.Entry(self, width=15, borderwidth=5, bg="#5ba6b0", fg="black", font="Calibri 15 bold")
        group_input_add.grid(row=1, column=2, ipadx=5, ipady=5,sticky="s")

        Fetch_button = tk.Button(self, activebackground="#8fa1a1", activeforeground="black", bd="5", bg="white",
                                fg="black", text="ADD", font=("Courier", "10", "bold"),
                                command=lambda: [Thread(target=Add_Groups).start()])
        Fetch_button.grid(row=1, column=4, ipadx=35, ipady=5, sticky="s")

        Error_label = tk.Label(self, text="Erros will be displayed here", font=("Courier", "10", "bold"),bg="black",fg="white",height=5,bd=4,relief="raised")
        Error_label.grid(row=2, column=0, columnspan=5,padx=40,pady=20, ipadx=1, ipady=1, sticky="nsew")


    def OnDoubleClick(self,event):
        global treetimegroup_add,group_input_add,group_list_pos_add
        group_input_add.delete(0,last="end")
        sel_item = treetimegroup_add.focus()
        group_input_add.insert(0,str(treetimegroup_add.item(sel_item)["values"][0]))
        group_list_pos_add=int(treetimegroup_add.item(sel_item)["text"])-1
        print(group_list_pos_add)



    def open_file(self):
        global file_add,users,No_select_input,count_user,treetimegroup_add_users,users_full
        file_add = askopenfilename()
        print(file_add)
        users = []
        count=0
        with open(file_add, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                user['group_name'] = row[4]
                user['group_id'] = row[5]
                users.append(user)
                count=count+1
                if count==int(No_select_input.get()):
                    break
        #print(users)
        for i in range(1, count_user):
            treetimegroup_add_users.delete(str(i))
        count_user = 1
        for i in range(0, len(users)):
            treetimegroup_add_users.insert("", "end", str(count_user), text=str(count_user), value=(
                users[i]['id']))
            count_user = count_user + 1

        users_full=[]
        with open(file_add, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                #print(row)
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                user['group_name']=row[4]
                user['group_id']=row[5]
                users_full.append(user)
        #print(users_full)




class PageFour(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        back = ttk.Button(self, text="BACK", command=lambda: controller.show_frame(StartPage))
        back.pack()

app = Telegram()
app.mainloop()
