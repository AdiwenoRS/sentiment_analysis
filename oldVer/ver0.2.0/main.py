import statistics
import pandas as pd
from textblob import TextBlob

# Retrieve data from csv file
datas = pd.read_csv('data.csv')
sentiments = datas.to_numpy()

# Object that will be search and process from user input
objects = []

# Text menu and user input
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
a_PolarityN = []
b_PolarityN = []
c_PolarityN = []
a_Subjectivity = []
b_Subjectivity = []
c_Subjectivity = []
a_Neutral = []
b_Neutral = []
c_Neutral = []

# Calculate polarity and subjectivity
for i in a:
    app = TextBlob(i).sentiment.polarity 
    asub = TextBlob(i).sentiment.subjectivity
    a_Subjectivity.append(asub)
    if app > 0:#
        a_polarityP.append(app)#
    elif app < 0:
        a_PolarityN.append(app)
    elif app == 0:
        a_Neutral.append(app)
        
for i in b:
    bpp = TextBlob(i).sentiment.polarity
    bsub = TextBlob(i).sentiment.subjectivity
    b_Subjectivity.append(bsub)
    if bpp > 0:
        b_polarityP.append(bpp)
    elif bpp < 0:
        b_PolarityN.append(bpp)
    elif bpp == 0:
        b_Neutral.append(bpp)
        
for i in c:
    cpp = TextBlob(i).sentiment.polarity
    csub = TextBlob(i).sentiment.subjectivity
    c_Subjectivity.append(csub)
    if cpp > 0:
        c_polarityP.append(cpp)
    elif cpp < 0:
        c_PolarityN.append(cpp)
    elif cpp  == 0:
        c_Neutral.append(cpp)

print("\nPercentage of positive Polarity")
# Prepare data
data = {
    objects[0]: a_polarityP, 
    objects[1]: b_polarityP
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
for key, mean in valid_data.items():
    percentage = mean / spp * 100
    print(f"{key} polarity percentage is {percentage:.2f}%")\

print("\nPercentage of Negative Polarity")
# Prepare data
dataN = {
    objects[0]: a_PolarityN, 
    objects[1]: b_PolarityN
}

try:
    dataN[objects[2]] = c_PolarityN
except: pass

# Initialize an empty dictionary for valid data
valid_dataN = {}

# Filter and calculate the mean for valid lists
for key, values in dataN.items():
    if any(values):  # Check if the list contains any non-zero values
        valid_dataN[key] = statistics.mean(values)  # Calculate and store the mean

# Calculate total sum of means
spn = sum(valid_dataN.values())

# Calculate and print percentages
for key, mean in valid_dataN.items():
    percentageN = mean / spn * 100
    print(f"{key} polarity percentage is {percentageN:.2f}%")

print("\nPercentage of Subjectivity")
# Prepare data
dataS = {
    objects[0]: a_Subjectivity, 
    objects[1]: b_Subjectivity
}

try:
    dataS[objects[2]] = c_Subjectivity
except: pass

# Initialize an empty dictionary for valid data
valid_dataS = {}

# Filter and calculate the mean for valid lists
for key, values in dataS.items():
    if any(values):  # Check if the list contains any non-zero values
        valid_dataS[key] = statistics.mean(values)  # Calculate and store the mean

# Calculate total sum of means
sps = sum(valid_dataS.values())

# Calculate and print percentages
for key, mean in valid_dataS.items():
    percentageS = mean / sps * 100
    print(f"{key} polarity percentage is {percentageS:.2f}%")

print("\nPercentage of Neutral")
TotalNe = [len(a_Neutral), len(b_Neutral), len(c_Neutral)]

for index in range(len(objects)):
    percentageNE = TotalNe[index] / sum(TotalNe) * 100
    print(f"{objects[index]} polarity percentage is {percentageNE:.2f}%")

print (data,dataN,dataS,TotalNe)