from customtkinter import *
import customtkinter
import requests
import re
import ipapi
import json



file_path = "selection.json"

all_options = ["city", "region", "country name", "latitude", "longitude"]


def resize_center(height:int, width:int, window, icon):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_height = height
    window_width = width
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    window.attributes("-topmost", True)
    window.after(197, window.focus)
    if icon == "error":
        window.after(300, lambda:window.iconbitmap("error.ico"))
    if icon == "map":
        window.after(300, lambda:window.iconbitmap("map.ico"))



def is_valid_ip(ip):
    ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

    if re.match(ip_pattern, ip):
        parts = ip.split('.')
        if all(0 <= int(part) <= 255 for part in parts):
            return True
        else:
            return False
    else:
        return False



app = CTk()
resize_center(400,500, app, "map")
app.title(" application")
app.resizable(False, False)
label = CTkLabel(master = app, text = "Please enter IP adress", font = ("Helvetica", 24))
label.pack(pady = 60)

uppercase = CTkFont("Kozuka Gothic Pr6N R", 24, "bold")


def submit():
    #disable submit button

    submitbtn.configure(state = DISABLED)
    selectoptions.configure(state = DISABLED)
    #get the entry
    submitted_entry = entry.get()


    # define close function
    def close():
        error_window.destroy()
        error_window.update()
        submitbtn.configure(state = NORMAL)
        selectoptions.configure(state = NORMAL)
    # check if entry contains anything
    

    # Example usage
    ip_address = submitted_entry  # Replace with the IP address you want to lookup
    location_info = ipapi.location(ip_address)
    # Check if IP is valid
    if is_valid_ip(ip_address):
        result = ipapi.location(ip_address)
        result_window = CTkToplevel(app,fg_color="#141414")
        def enablebtns():
            result_window.destroy()
            submitbtn.configure(state = NORMAL)
            selectoptions.configure(state = NORMAL)
        result_window.protocol("WM_DELETE_WINDOW", enablebtns)
        result_window.title(f"Result of {ip_address}")
        result_window.resizable(False,False)
        resize_center(350, 600, result_window, "map")

        def close():
            submitbtn.configure(state = NORMAL)
            selectoptions.configure(state = NORMAL)
            result_window.destroy()
            result_window.update()
        try:
            if result["error"]:
                def enablebtns():
                    submitbtn.configure(state = NORMAL)
                    selectoptions.configure(state = NORMAL)
                error_label = CTkLabel(master = result_window,text = "ERROR", font = uppercase, text_color="red")
                error_label.place(relx = 0.5, rely = 0.3, anchor = CENTER)
                error_label2 = CTkLabel(master = result_window, text = "This IP is reserved!")
                error_label2.place(relx=0.5, rely=0.5, anchor = CENTER)
                closebutton = CTkButton(master = result_window ,text = "Close", corner_radius=30, fg_color="#4B0000", border_width=2, border_color="#CF0000", hover_color="#CF0000", command = close)
                closebutton.place(relx =0.5, rely = 0.8, anchor = CENTER) 
                result_window.protocol("WM_DELETE_WINDOW", enablebtns)
        except:
            label = CTkLabel(master = result_window, text = f"Result of {ip_address}", fg_color="#AA4AFF", corner_radius=10, font = uppercase)
            label.pack(pady = 10)
            latitude = result["latitude"]
            longitude = result["longitude"]
            url = f"https://www.google.com/maps/place/{latitude},{longitude}"
            # Load the JSON file
            with open(file_path) as f:
                data = json.load(f)
            # Iterate over the key-value pairs and print keys where the value is true
            true_values = [key for key, value in data.items() if value is True]
            # Iterate over the key-value pairs in conditions
            for key, value in data.items():
                if value is True:
                    # Check if the key exists in the data and print its value if it does
                    if key in result:
                        label = CTkLabel(master = result_window, text = f"{key}: {result[key]}", font=("Helvetica", 20))
                        label.pack(pady = 10)
            label = CTkLabel(master = result_window, text = url, font=("helvetica", 20))
            label.pack(pady = 10)
            
    else:
        # Make error window
        def enablebtns():
            error_window.destroy()
            selectoptions.configure(state = NORMAL)
            submitbtn.configure(state = NORMAL)
        error_window = customtkinter.CTkToplevel(app)
        error_window.overrideredirect(False)
        error_window.title("Error")
        error_window.resizable(False, False)
        resize_center(110, 200, error_window, "error")
        error_window.protocol('WM_DELETE_WINDOW', enablebtns)
        error_frame = CTkFrame(master = error_window, fg_color="#430000", border_color="#CF0000", border_width=2)
        error_frame.pack()

        # Make text label
        error_message = customtkinter.CTkLabel(master = error_frame, text = "Please enter a valid IP-Adress!", text_color="red")
        error_message.pack(pady = 20)

        # add close button
        close_button = customtkinter.CTkButton(master = error_frame, corner_radius=30, text="Close", text_color="white", command = close, fg_color="#4B0000", border_width=2, border_color="#CF0000", hover_color="#CF0000")
        close_button.pack(pady = 10, padx = 30)

    #clear entry 
    entry.delete(0, END)


# Create a selection menu
def open_selection():
    def enablebtns():
            selection_menu.destroy()
            selectoptions.configure(state = NORMAL)
            submitbtn.configure(state = NORMAL)
    selectoptions.configure(state = DISABLED)
    submitbtn.configure(state = DISABLED)
    selection_menu = CTkToplevel(app)
    selection_menu.protocol("WM_DELETE_WINDOW", enablebtns)
    selection_menu.title("Selection Menu")
    resize_center(380,380, selection_menu, "map")
    selection_menu.resizable(False, False)
    # Add a checkbox
    checkboxframe = CTkFrame(master = selection_menu, fg_color="#29133C", border_color="#AA4AFF", border_width=2)
    checkboxframe.pack(pady = 20)
    #Save the selection
    def save_selection():
        new_json = {
            "city":cityvar.get(),
            "region":regionvar.get(),
            "country":countryvar.get(),
            "latitude":latitudevar.get(),
            "longitude":longitudevar.get()
        }
        with open(file_path, "w") as json_file:
            json.dump(new_json, json_file)

        selection_menu.destroy()
        selection_menu.update()
        selectoptions.configure(state = NORMAL)
        submitbtn.configure(state = NORMAL)


    cityvar = BooleanVar(value = False)
    citycheckbox = CTkCheckBox(master = checkboxframe,
                            variable = cityvar,
                            text = "City",
                            checkmark_color = "#29133C",
                            fg_color = "#AA4AFF",
                            border_color = "#AA4AFF",
                            border_width = 2,
                            hover = False,
                            onvalue=True,
                            offvalue=False)
    citycheckbox.pack(anchor = "n", expand = True, pady = 10, padx=60)

    regionvar = BooleanVar(value = False)
    regioncheckbox = CTkCheckBox(master = checkboxframe,
                            variable = regionvar,
                            text = "Region",
                            checkmark_color = "#29133C",
                            fg_color = "#AA4AFF",
                            border_color = "#AA4AFF",
                            border_width = 2,
                            hover = False,
                            onvalue=True,
                            offvalue=False)
    regioncheckbox.pack(anchor = "n", expand = True, pady = 10, padx=40)

    countryvar = BooleanVar(value = False)
    countrycheckbox = CTkCheckBox(master = checkboxframe,
                            variable = countryvar,
                            text = "Country",
                            checkmark_color = "#29133C",
                            fg_color = "#AA4AFF",
                            border_color = "#AA4AFF",
                            border_width = 2,
                            hover = False,
                            onvalue=True,
                            offvalue=False)
    countrycheckbox.pack(anchor = "n", expand = True, pady = 10, padx=40)
    latitudevar = BooleanVar(value = False)
    latitudecheckbox = CTkCheckBox(master = checkboxframe,
                            variable = latitudevar,
                            text = "Latitude",
                            checkmark_color = "#29133C",
                            fg_color = "#AA4AFF",
                            border_color = "#AA4AFF",
                            border_width = 2,
                            hover = False,
                            onvalue=True,
                            offvalue=False)
    latitudecheckbox.pack(anchor = "n", expand = True, pady = 10, padx=40)
    longitudevar = BooleanVar(value = False)
    longitudecheckbox = CTkCheckBox(master = checkboxframe,
                            variable = longitudevar,
                            text = "Longitude",
                            checkmark_color = "#29133C",
                            fg_color = "#AA4AFF",
                            border_color = "#AA4AFF",
                            border_width = 2,
                            hover = False,
                            onvalue=True,
                            offvalue=False)
    longitudecheckbox.pack(anchor = "n", expand = True, pady = 10, padx=40)

    submitselection = CTkButton(master = checkboxframe, text = "Update preferences", corner_radius=20, fg_color="transparent", hover_color="#AA4AFF", border_color="#AA4AFF", border_width=2, command = save_selection)
    submitselection.pack(pady = 20)
    

    
    with open(file_path)as json_file:
        data = json.load(json_file)

    if data["city"]:
        citycheckbox.select()
    if data["region"]:
        regioncheckbox.select()
    if data["country"]:
        countrycheckbox.select()
    if data["latitude"]:
        latitudecheckbox.select()
    if data["longitude"]:
        longitudecheckbox.select()

frame = CTkFrame(master = app, fg_color="#29133C", border_color="#AA4AFF", border_width=2)
frame.pack(expand = True, pady = 0)


entry = CTkEntry(master = frame, width=140, height = 28, border_color="#AA4AFF", border_width=2, placeholder_text="Enter IP")
entry.pack(anchor = "s", expand = True, padx=20, pady = 20)

submitbtn = CTkButton(master = frame, text = "Submit", corner_radius=30, fg_color="transparent", hover_color="#AA4AFF", border_color="#AA4AFF", border_width=2, command=submit, font = ("Helvetica", 14))
submitbtn.pack(anchor = "n", expand = True, padx= 30, pady=10)

selectoptions = CTkButton(master = frame, text = "Change Selection", corner_radius=30, fg_color="transparent", hover_color="#AA4AFF", border_color="#AA4AFF", border_width=2, command = open_selection)
selectoptions.pack(anchor = "n", expand = True, pady = 20)
app.mainloop()