import pandas as pd
import ProcessAndComparing as PAC

# Read data
datas = pd.read_csv('data.csv')
sentiments = datas.to_numpy()

# Get user input
print("Tweet Sentiment Analysis")
objects = []

# Get user input
try:
    userInput = int(input("How many objects you want to search? Min 2 | Max 3: "))
except:
    print("Invalid input. Please enter a number between 2 and 3.")
    exit()
if userInput < 2 or userInput > 3:
    print("Invalid input. Please enter a number between 2 and 3.")
    exit()

# Add input to objects
for i in range(userInput):
    objects.append(input(f"Object {i + 1}: "))

# Filter sentences for each object
filtered_sentences = {}
for obj in objects:
    filtered_sentences[obj] = []
    
for sentence in sentiments.flatten():
    for obj in objects:
        if obj.upper() in sentence.upper():
            filtered_sentences[obj].append(sentence)

# All results anylized stored here
results = {}
for obj, sentences in filtered_sentences.items():
    results[obj] = PAC.analyze_sentences(sentences)
        
# Print results
PAC.calculate_percentage(results, 0, "Positive Polarity")
PAC.calculate_percentage(results, 1, "Negative Polarity")
PAC.calculate_percentage(results, 3, "Subjectivity")
PAC.calculate_percentageNeutral(results)

# Debugging output
print("\nDetailed Data:")
for obj, metrics in results.items():
    print(f"\n{obj}:")
    print(f"Positive Polarity: {metrics[0]}")
    print(f"Negative Polarity: {metrics[1]}")
    print(f"Neutral Polarity: {metrics[2]}")
    print(f"Subjectivity: {metrics[3]}")
