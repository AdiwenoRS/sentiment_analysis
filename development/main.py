import statistics
import pandas as pd
from textblob import TextBlob

# Read data
datas = pd.read_csv('data.csv')
sentiments = datas.to_numpy()

# Get user input
print("Tweet Sentiment Analysis")
objects = []
userInput = int(input("How many objects you want to search? Min 2 | Max 3: "))
if userInput < 2 or userInput > 3:
    print("Invalid input. Please enter a number between 2 and 3.")
    exit()

for i in range(userInput):
    objects.append(input(f"Object {i + 1}: "))

# Filter sentences for each object
filtered_sentences = {obj: [] for obj in objects}
for sentence in sentiments.flatten():
    for obj in objects:
        if obj.upper() in sentence.upper():
            filtered_sentences[obj].append(sentence)

# Analyze polarity, subjectivity, and neutrality
def analyze_sentences(sentences):
    positive, negative, neutral, subjectivity = [], [], [], []
    for sentence in sentences:
        sentiment = TextBlob(sentence).sentiment
        polarity = sentiment.polarity
        subjectivity.append(sentiment.subjectivity)
        if polarity > 0:
            positive.append(polarity)
        elif polarity < 0:
            negative.append(polarity)
        else:
            neutral.append(polarity)
    return positive, negative, neutral, subjectivity

results = {}
for obj, sentences in filtered_sentences.items():
    results[obj] = analyze_sentences(sentences)

# Calculate percentages
def calculate_percentage(data_dict, metric_index, label):
    valid_data = {}
    
    # Filter and calculate mean for valid data
    for obj, metrics in data_dict.items():
        if metrics[metric_index]:  
            valid_data[obj] = statistics.mean(metrics[metric_index])
    total = sum(valid_data.values())
    
    # Print percentages
    print(f"\nPercentage of {label}")
    for obj, mean in valid_data.items():
        percentage = (mean / total) * 100
        print(f"{obj} {label.lower()} percentage is {percentage:.2f}%")
# Print results
calculate_percentage(results, 0, "Positive Polarity")
calculate_percentage(results, 1, "Negative Polarity")
calculate_percentage(results, 3, "Subjectivity")

# Neutral percentage
print("\nPercentage of Neutral")
total_neutral_counts = {obj: len(metrics[2]) for obj, metrics in results.items()}
total_neutral_sum = sum(total_neutral_counts.values())
for obj, count in total_neutral_counts.items():
    print(f"{obj} neutral percentage is {count / total_neutral_sum * 100:.2f}%")

# Debugging output
print("\nDetailed Data:")
print(results)
