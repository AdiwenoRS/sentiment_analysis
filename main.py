import pandas as pd
import ProcessAndComparing as PAC
import time
from textblob import TextBlob

# Read data
datas = pd.read_csv('twitter_dataset.csv')
sentiments = datas.to_numpy()
objects = [] 
filtered_sentences = {} 
results = {} 
splittedSentences = {} 

def userChoice():
    choice = input("\nTweet Sentiment Analysis\n1. Add objects and data mining\n2. Compare data\n3. Normalized and processed data\n4. Exit\nEnter your choice: ")
    if choice == "1":
        if objects != []: # Check if objects is not empty. If it so, clear all necessary variable
            objects.clear()
            filtered_sentences.clear()
            results.clear()
            splittedSentences.clear()
        addObjects()
        userChoice()
    elif choice == "2":
        if objects == []: # Check if objects is empty
            print("\nNO OBJECTS : Please add objects to search.")
            userChoice()
        else:    
            print("-" * 50)
            PAC.calculate_percentage(results, 0, "Positive Polarity")
            PAC.calculate_percentage(results, 1, "Negative Polarity")
            PAC.calculate_percentage(results, 3, "Subjectivity")
            PAC.calculate_percentageNeutral(results)
            print("\n", "-" * 50)
        userChoice()
    elif choice == "3":
        if objects == []: # Check if objects is empty
            print("\nNO OBJECTS : Please add objects to search.")
            userChoice()
        else:
            data1 = {}
            data2 = {}
            file1 = "filtered_sentences_table1.csv"
            file2 = "filtered_sentences_table2.csv"
            
            PAC.calculateToTable(filtered_sentences, data1, data2, objects)
            df1 = pd.DataFrame.from_dict(data1, orient="index") # Convert dictionary to table
            df1 = df1.transpose() # allow N/A data in row         
            df1.to_csv((file1), index=False) # Save to csv
            df2 = pd.DataFrame.from_dict(data2, orient="index") # Convert dictionary to table
            df2 = df2.transpose() # allow N/A data in row         
            df2.to_csv((file2), index=False) # Save to csv

            print(f"\nData was saved to {file1} and {file2}")
            userChoice()
    elif choice == "4":
        exit()
    else:
        print("\nINVALID INPUT : Please enter a number between 1 to 4.")
        userChoice()

# Add objects
def addObjects():
    userInput = str(input("How many objects you want to search? Min 2 | Max 3: "))
    
    if userInput != "3" and userInput != "2": # Check if user input is valid
        print("\nINVALID INPUT : Please enter a number between 2 and 3.")
        addObjects()
        
    for i in range(int(userInput)): # Add objects
        objects.append(input(f"Object {i + 1}: "))
        
    filterAndAnalyze() 

def record_time(function): 
    def wrap(*args, **kwargs):
        start_time = time.time()
        function_return = function(*args, **kwargs)
        
        print(f"\nData mining done. Time taken: {round(time.time() - start_time, 2)} seconds")
        return function_return
    return wrap

@record_time # Start record filterAndAnalyze() process time
def filterAndAnalyze():
    # Filter sentences for each object
    for obj in objects: # Create empty lists for each object into dictionary
        filtered_sentences[obj] = []
        
    for sentence in sentiments.flatten(): # Iterate over each sentence
        for obj in objects: # Search for each object in each sentence
            if obj.upper() in sentence.upper():
                filtered_sentences[obj].append(sentence) # Add sentence to list based on object
    
    for obj, sentences in filtered_sentences.items(): # Analyze sentences and store to results
        results[obj] = PAC.analyze_sentences(sentences)
    
# Start
if __name__ == "__main__":
    userChoice()