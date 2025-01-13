import customtkinter as ctk
import tkinter as tk
import os, shutil
from tkinter import filedialog
class App(ctk.CTk):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)

        # Configure spacing for borders
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        #self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(7, weight=1)# new
        self.grid_rowconfigure(8, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        
        self.title("File Manager")
        self.geometry("850x550")

         

        self.CustomDirectoryFrame = DirectoryStructure(self)
        self.CustomDirectoryFrame.grid( row=1, column=0, columnspan=5, rowspan=7, padx=30, pady=10, sticky='nsew')

        # get target path = 
        self.request_current_path= ctk.CTkButton(self, text="Select Folder where files reside", command=self.select_current_path)
        self.request_current_path.grid(row=1, column=5, sticky='s', pady=20)

        self.request_target_path= ctk.CTkButton(self, text="Select Folder where you wish to move files", command=self.select_output_path)
        self.request_target_path.grid(row=1, column=5, pady=20)


        # could place inside a label to include label and entry, or could just use columns
        self.startswithEntry = ctk.CTkEntry(self, placeholder_text= "Starts with...")
        self.startswithEntry.grid(row=3, column=5, sticky='n', pady=10)

        self.endswithEntry = ctk.CTkEntry(self, placeholder_text="Ends with...")
        self.endswithEntry.grid(row=3, column=5 , pady=10)

        optionsNofStr = ["0","1", "2", "3"]
        # option 1, 2,3 how many strs contained or similar + # checkbox of exact or similar
        self.NstrContained = ctk.CTkOptionMenu(self, values=optionsNofStr, command=self.str_containers)
        self.NstrContained.set("Number of str contained")
        self.NstrContained.grid(row=4, column=5)
        

        # Search Button 
        self.searchButton = ctk.CTkButton(self, text='search', command=self.search_files)
        self.searchButton.grid(row=7, column=5, sticky ='n')

        # Move Button 
        self.moveButton = ctk.CTkButton(self, text='move', command=self.move_files)
        self.moveButton.grid(row=7, column=5)
        



    def move_files(self):
        if hasattr(self, 'final_selected_items'):
            if hasattr(self, 'output_path'):
                if os.path.exists(self.output_path):
                    dest_paths = []
                    for i, f in enumerate(self.final_selected_items):
                        basename = os.path.basename(f) 
                        dest_path = os.path.join(self.output_path, basename)
                        if dest_path in dest_paths:
                            base_name, extension = os.path.splitext(basename)
                            dest_path = f"{base_name}({i}){extension}"
                            print("An item already has that name")
                            print(f"File had been renamed to: {dest_path}")
                        shutil.move(f, dest_path)
                        dest_paths.append(dest_path)
                        print(f"file{f} -> ")
                        print(f"---->{dest_path}")
                        print(" ")
                    print("Items have been Moved!")
                    self.CustomDirectoryFrame.kill_all_children() 
                else:
                    self.warning = tk.Message(self, text="Your destination path does not exist")
                    self.warning.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            else:
                self.warning = tk.Message(self, text="No selected items")
                self.warning.grid(row=0, column=0, padx=10, pady=10, sticky="w")
           
        else:
            self.warning = tk.Message(self, text="No selected items")
            self.warning.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # could implement for custom stuff but i doubt i have time so just basic moving
    
        # add a clean button to clean selection
    def search_files(self):
        str_contained = []
        startswith = None
        endswith = None
        if hasattr(self, 'str_container_holder'):
            if len(self.str_container_holder) > 0:
                for c in self.str_container_holder:
                    str_contained.append(c.get())

        if self.startswithEntry.get():
            startswith = self.startswithEntry.get()
        
        if self.endswithEntry.get():
            endswith = self.endswithEntry.get()

        if any([str_contained, startswith,endswith]):

            selected_items = self.search_file(str_contained =str_contained, startswith=startswith,endswith=endswith)
            # delete all children labels
            self.CustomDirectoryFrame.kill_all_children() 
            self.CustomDirectoryFrame.add_to_visible_stack(selected_items)
            print(f"{len(selected_items)} selected items")
            print("Selected items: ")
            self.final_selected_items = selected_items
            for item in selected_items:
                print(item)
        else:
            self.warning = tk.Message(self, text="No criteria selected everything will be moved to the selected folder")
            self.warning.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    def search_file(self, **kwargs):
         
         
        selected_items = self.traverse_and_list(self.current_path)
        for key, val in kwargs.items():
            if val:
                # works with AND not customed for OR operations
                if key == 'startswith': 
                    selected_items = [p for p in  selected_items if os.path.basename(p).startswith(val)]    

                if key == 'endswith':
                    selected_items = [p for p in selected_items if os.path.basename(p).endswith(val)]

                if key == 'str_contained':
                    for s in val:
                        selected_items = [p for p in selected_items if s in os.path.basename(p)]
        return selected_items
    

    def select_current_path(self):
        self.current_path = filedialog.askdirectory(title="Select a Folder")
        if self.current_path:
            str_lst = self.print_directory(self.current_path)
            
            self.CustomDirectoryFrame.add_to_visible_stack(str_lst)
        else:
            self.warning = ctk.Message(self, text="No path selected")
            return 

    def str_containers(self, ncontainers):
    
        if not hasattr(self, 'str_container_holder'):
            self.str_container_holder = []
        # Create or destroy containers
        if len(self.str_container_holder) < int(ncontainers):
            for c in range(int(ncontainers) - len(self.str_container_holder)):
                container = ctk.CTkEntry(self, placeholder_text="string contained")
                container.grid(row=5 + c, column=5)
                self.str_container_holder.append(container) 
        else:
            n = len(self.str_container_holder) - int(ncontainers)
            for _ in range(n):
                container = self.str_container_holder.pop()
                container.destroy()


    def traverse_and_list(self, root):
        stack = [(root, 0)]
        dir_list = []
        while stack:
            current_path, depth = stack.pop()
            
            dir_list.append(current_path)
            #print(f"{'    ' * depth} - {os.path.basename(current_path)}")
            if os.path.isdir(current_path):
               
                for item in os.listdir(current_path):
                    stack.append((os.path.join(current_path, item), depth + 1))
        return dir_list

    def select_output_path(self):
        self.output_path = filedialog.askdirectory(title="Select a Folder")
        # sort based on 
        # should I add to rename files??
        
        


    def print_directory(self, current_path):

        # Traverse if given path is directory
        if os.path.isdir(current_path):             
            str_lst = self.traverse_directory(current_path)
            return str_lst
            
        else:
            self.warning = ctk.Message(self, text="Selected folder is not a directory")
            return 
        
    def traverse_directory(self, root):
        stack = [(root, 0)]
        str_lst = []
        while stack:
            current_path, depth = stack.pop()
            
            
            str_temp = (f"{'      ' * depth}|-- {os.path.basename(current_path)}")
                
            str_lst.append(str_temp)
            #print(f"{'    ' * depth} - {os.path.basename(current_path)}")
            if os.path.isdir(current_path):
                str_lst[-1] = str_lst[-1] + ' /'
                for item in os.listdir(current_path):
                    stack.append((os.path.join(current_path, item), depth + 1))
            
        print("Done!")
        print("\n")
        return str_lst

    

 
# Custom class to add  directory structure
class DirectoryStructure(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.directoryFrame = ctk.CTkScrollableFrame(self,corner_radius=20)
        #needs to be added both inside and outside
        self.directoryFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
       
        # Avoid garbage collector
        self.directory_items = []
    def add_to_visible_stack(self, str_list):

        for i, txt in enumerate(str_list):
            print(txt)
            path = ctk.CTkLabel(self.directoryFrame, text=f"{txt}")
            path.grid(row=i,column=1, columnspan=3 ,padx=10, pady=0,sticky = 'w')
           
            self.directory_items.append((path))
    def kill_all_children(self):
        for _ in range(len(self.directory_items)):
            item = self.directory_items.pop()
            item.destroy()
        self.directory_items = []


if __name__ == "__main__":
    app = App()
    app.mainloop()