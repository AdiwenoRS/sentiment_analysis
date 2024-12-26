import pandas as pd
import ProcessAndComparing as PAC
import time

# Read data
datas = pd.read_csv('datasets/training.1600000.processed.noemoticon.csv')

# Choose a column that contain text from the dataset you want to analyze by changing the number
# 1 means select the second column (indexing starts at 0). : means select all rows.
sentiments = datas.iloc[:, 5].to_numpy()

objects, filtered_sentences, results, splittedSentences = [], {}, {}, {}

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
            # Calculate percentage
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
                
            print(f"\nData was saved to:")
            
            for data, file in zip(allData, files):
                    df = pd.DataFrame.from_dict(data, orient="index") # Convert dictionary to table
                    df = df.transpose() # Allow N/A data in columns         
                    df.to_csv((file), index=False) # Save to csv
                    print(file)

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

def record_time(function): # Count mining process time
    def wrap(*args, **kwargs):
        start_time = time.time()
        function_return = function(*args, **kwargs)
        
        print(f"\nData mining done. Time taken: {round(time.time() - start_time, 2)} seconds")
        return function_return
    return wrap

@record_time # Start record filterAndAnalyze() process time
def filterAndAnalyze():
    
    # Filter sentences for each object
    for obj in objects: 
        filtered_sentences[obj] = []
        
    for sentence in sentiments.flatten(): 
        for obj in objects: # Search for each object in each sentence
            if obj.upper() in sentence.upper():
                filtered_sentences[obj].append(sentence) # Add sentence to list based on object

    smallest = len(filtered_sentences[objects[0]])
    for obj, sentence in filtered_sentences.items():
        if len(sentence) < smallest:
            smallest = len(sentence)

    for obj, sentence in filtered_sentences.items():
        filtered_sentences[obj] = sentence[:smallest]
    
    for obj, sentence in filtered_sentences.items():
            if sentence == []:
                objects.clear()
                filtered_sentences.clear()
                
                print(f"\nNO DATA : There is no data for {obj}")
                return 
    
    for obj, sentences in filtered_sentences.items(): # Analyze sentences and store to results
        results[obj] = PAC.analyze_sentences(sentences)
    
# Start
if __name__ == "__main__":
    userChoice()