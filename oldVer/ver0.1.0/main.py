from textblob import TextBlob
import statistics
import pandas as pd

datas = pd.read_csv('data.csv')
sentiments = datas.to_numpy()

# Object that will be search and process from user input
objects = []

# Text menu
print("Tweet Sentiment Analysis")
userInput = int(input("How many objects you want to search? Min 2 | Max 3: "))
if userInput < 2 or userInput > 3:
    print("Invalid input. Please enter a number between 2 and 3.")
    exit()
else:
    for select in range(userInput):
        objects.append(input(f"Object {select + 1}: "))
    

# Initialize result lists
a = []
b = []
c = []

# Iterate over each statement
for i in sentiments:
    for sentence in i:
        if objects[0].upper() in sentence.upper():  # Check if "a" is in the sentence
            a.append(sentence)  # Add the sentence to the result list
        if objects[1].upper() in sentence.upper():  
            b.append(sentence)
        try:  
            if objects[2].upper() in sentence.upper():  
                c.append(sentence)        
        except: pass       

# Initialize polarity lists
a_polarityP = []
b_polarityP = []    
c_polarityP = []

# Calculate polarity
for i in a:
    app = TextBlob(i).sentiment.polarity
    if app > 0:
        a_polarityP.append(app)
for i in b:
    bpp = TextBlob(i).sentiment.polarity
    if bpp > 0:
        b_polarityP.append(bpp)
for i in c:
    cpp = TextBlob(i).sentiment.polarity
    if cpp > 0:
        c_polarityP.append(cpp)
        
# Prepare data
data = {
    objects[0]: a_polarityP, 
    objects[1]: b_polarityP, 
}
try:
    data[objects[2]] = c_polarityP
except: pass

# Initialize an empty dictionary for valid data
valid_data = {}

# Filter and calculate the mean for valid lists
for key, values in data.items():
    if any(values):  # Check if the list contains any non-zero values
        valid_data[key] = statistics.mean(values)  # Calculate and store the mean

# Calculate total sum of means
spp = sum(valid_data.values())

# Calculate and print percentages
print("Percentage of positive Polarity")
for key, mean in valid_data.items():
    percentage = mean / spp * 100
    print(f"{key} polarity percentage is {percentage:.2f}%")
    