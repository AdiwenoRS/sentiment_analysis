import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ProcessAndComparingGUI as PAC # Import ProcessAndComparingGUI.py


# Read data
datas = pd.read_csv('datasets/twitter_dataset.csv')
sentiments = datas.to_numpy()
objects, filtered_sentences, results = [], {}, {}
LARGE_FONT= ("Verdana", 24)  

# Option 1
def addObjectsAndDataMining():
    if objects != []: # Check if objects is not empty. If it so, clear all necessary variable
        objects.clear()
        filtered_sentences.clear()
        results.clear()

    userInput = simpledialog.askstring("input", "How many objects you want to search? Min 2 | Max 3:")
    
    if userInput == "3" or userInput == "2": # Check if user input is valid
        for i in range(int(userInput)): # Add objects
            objectInput = simpledialog.askstring("input", "Object " + str(i + 1) + ":")
            objects.append(objectInput)
        # Filter sentences for each object
        print("Data mining started...")
        for obj in objects: 
            filtered_sentences[obj] = []

        for sentence in sentiments.flatten(): 
            for obj in objects: # Search for each object in each sentence
                if obj.upper() in sentence.upper():
                    filtered_sentences[obj].append(sentence) # Add sentence to list based on object
                #else: # Check if there is no data
                    
        for obj, sentence in filtered_sentences.items():
            if sentence == []:
                messagebox.showerror("NO DATA", "There is no data for " + obj)
                objects.clear()
                filtered_sentences.clear()
                return

        for obj, sentences in filtered_sentences.items(): # Analyze sentences and store to results
            results[obj] = PAC.analyze_sentences(sentences)
                        
        print("Done")
        messagebox.showinfo("SUCCESS", "Objects added")
        
        
# Option 3
def normalizedAndProcessedData():
    if objects == []: # Check if objects is empty
        messagebox.showerror("NO OBJECTS", "Please do \"add objects and data mining\".")
    else:
        data1, data2, data3, files, allData = {}, {}, {}, [], []
        
        PAC.calculateToTable(filtered_sentences, data1, data2, data3, objects) # Process
        
        if len(objects) > 1 : # Add first and second file
            file1 = "classified_sentiments/table1.csv"
            file2 = "classified_sentiments/table2.csv"
            allData.append(data1)
            allData.append(data2)
            files.append(file1)
            files.append(file2)
        if len(objects) == 3: # Add third file if there are 3 objects
            file3 = "classified_sentiments/table3.csv"
            allData.append(data3)
            files.append(file3)
                    
        for data, file in zip(allData, files):
                df = pd.DataFrame.from_dict(data, orient="index") # Convert dictionary to table
                df = df.transpose() # Allow N/A data in columns         
                df.to_csv((file), index=False) # Save to csv
                print(file)
                messagebox.showinfo("SUCCESS", f"All data was saved to {file}")

# What we do here is populate this tuple with all of the possible pages to our application.
# This will load all of these pages for us. Within our __init__ method, we're calling StartPage 
# to show first, but later we can call upon show_frame to raise any other frame/window that we please.     
# Refrence = https://pythonprogramming.net/change-show-new-frame-tkinter/
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title("Tweet Sentiment Analysis")
        width= self.winfo_screenwidth() 
        height= self.winfo_screenheight()
        #setting tkinter window size
        self.geometry("%dx%d" % (width, height))
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Page starts here
# Every page is a class that inherits from tk.Frame
# From the start page, we can go to the page one by calling show_frame
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.configure(background='white')
        label = tk.Label(self, text="TWEET SENTIMENT ANALYSIS", font=LARGE_FONT, background='white')
        label.pack(pady=10,padx=10)

        label_name = tk.Label(self, text="\n\nChoose an action:\n", background='white')
        label_name.pack(pady=5)

        # Button menu
        add_button = tk.Button(self, text="Add objects and data mining", command=addObjectsAndDataMining, background='#D4F6FF')
        add_button.config(width=30, height=2)
        add_button.pack(pady=5)

        compare_button = tk.Button(self, text="Compare Data", command=lambda: controller.show_frame(PageOne), background='#D4F6FF')
        compare_button.config(width=30, height=2)
        compare_button.pack(pady=5)

        save_button = tk.Button(self, text="Normalized and processed data", command=normalizedAndProcessedData, background='#D4F6FF')
        save_button.config(width=30, height=2)
        save_button.pack(pady=5)

        exit_button = tk.Button(self, text="Exit", command=self.quit, background='#FFDDAE')
        exit_button.config(width=30, height=2)
        exit_button.pack(pady=5)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='white')
        label = tk.Label(self, text="Compare Data", font=LARGE_FONT, background='white')
        label.pack(pady=10,padx=10)
        
        self.canvas = None

        # Option 2
        def compare():
            if objects == []: # Check if objects is empty
                messagebox.showerror("NO OBJECTS", "Please do \"add objects and data mining\".")
            else:  
                if self.canvas: # if "canvas" variable True, destroy
                    self.canvas.get_tk_widget().destroy()
                    self.canvas = None
                fig = matplotlib.figure.Figure(figsize=(15,5))
                # Add Legends on the left side
                ax = fig.add_subplot(100, 1000, 1)
                ax.pie([20, 30, 50]) 
                ax.legend([objects[i].upper() + "-" +str(len(filtered_sentences[objects[i]])) for i in range(len(objects))])
                
                percentages = {0: [], 1: [], 2: [], 3: []}
                title = ["Positivity", "Negativity", "Neutrality", "Subjectivity"]
                
                for i in range(len(objects)):
                    percentages[0].append(PAC.calculate_percentage(results, 0, "positive")[objects[i].upper()]["percentage"])
                    percentages[1].append(PAC.calculate_percentage(results, 1, "negative")[objects[i].upper()]["percentage"])
                    percentages[2].append(PAC.calculate_percentageNeutral(results, "neutral")[objects[i].upper()]["percentage"])
                    percentages[3].append(PAC.calculate_percentage(results, 3, "subjectivity")[objects[i].upper()]["percentage"])
                    
                for obj, percentage in percentages.items():
                    ax = fig.add_subplot(1, 4, obj+1)
                    ax.pie(percentage) 
                    ax.legend([str(percentage[i])+"%" for i in range(len(percentage))])
                    circle = matplotlib.patches.Circle((0,0), 0.7, facecolor='white')
                    ax.add_patch(circle)
                    ax.set_title(title[obj])
                print(percentages)

                self.canvas = FigureCanvasTkAgg(fig, master=self)
                self.canvas.get_tk_widget().pack()
                self.canvas.draw()   
        
        def clear_canvas(): # function to clear "canvas" variable
            if self.canvas: # if "canvas" variable True
                self.canvas.get_tk_widget().destroy()
                self.canvas = None

        label1 = tk.Label(self, text="Press \"Run/Update\" button to see compared data or update new data.\nPress \"Clear\" button to clear canvas if data wont update.", background='white')
        label1.pack(pady=10)
        
        # Create a Button to trigger the update
        update_button = tk.Button(self, text="Run/Update", command=compare, background='#D4F6FF')
        update_button.config(width=30, height=2)
        update_button.pack(pady=10)
        
        clear_button = tk.Button(self, text="Clear", command=clear_canvas, background='#C6E7FF')
        clear_button.config(width=30, height=2)
        clear_button.pack(pady=10)
        
        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage), background='#FFDDAE')
        button1.config(width=30, height=2)
        button1.pack()


print("Waiting for input...")
# Start
if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()