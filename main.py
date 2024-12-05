import pandas as pd
import ProcessAndComparing as PAC

# Read data
datas = pd.read_csv('data.csv')
sentiments = datas.to_numpy()
objects = [] # Objects stored here
filtered_sentences = {} # Filtered sentences stored here
results = {} # All results anylized stored here

def userChoice():
    choice = input("\nTweet Sentiment Analysis\n1. Add objects\n2. Compare data\n3. Keywords of objects\n4. Normalized data\n5. Processed data\n6. Exit\nEnter your choice: ")
    if choice == "1":
        addObjects()
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
        print("hello world")
        userChoice()
    elif choice == "4":
        if objects == []: # Check if objects is empty
            print("\nNO OBJECTS : Please add objects to search.")
            userChoice()
        else:
            for obj, sentences in filtered_sentences.items():
                print(f"\n{obj.upper()}: {sentences}")
            userChoice()
    elif choice == "5":
        if objects == []: # Check if objects is empty
            print("\nNO OBJECTS : Please add objects to search.")
            userChoice()
        else:
            for obj, metrics in results.items():
                print(f"\n{obj.upper()}:")
                print(f"Positive Polarity: {metrics[0]}")
                print(f"Negative Polarity: {metrics[1]}")
                print(f"Neutral Polarity: {metrics[2]}")
                print(f"Subjectivity: {metrics[3]}")
            userChoice()
    elif choice == "6":
        exit()
    else:
        print("\nINVALID INPUT : Please enter a number between 1 to 4.")
        userChoice()

# Add objects
def addObjects():
    userInput = str(input("How many objects you want to search? Min 2 | Max 3: "))
    
    if userInput != "3" and userInput != "2": # Check if user input is valid
        print("\nINVALID INPUT : Please enter a number between 2 and 3.")
        userChoice()
        
    for i in range(int(userInput)): # Add objects
        objects.append(input(f"Object {i + 1}: "))
    filterAndAnalyze() 

def filterAndAnalyze():
    # Filter sentences for each object
    for obj in objects: # Create empty lists for each object into dictionary
        filtered_sentences[obj] = []
        
    for sentence in sentiments.flatten(): # Iterate over each sentence
        for obj in objects: # Search for each object in each sentence
            if obj.upper() in sentence.upper():
                filtered_sentences[obj].append(sentence)
    
    for obj, sentences in filtered_sentences.items(): # Analyze sentences and store to results
        results[obj] = PAC.analyze_sentences(sentences)
    userChoice()
# Start
userChoice()
