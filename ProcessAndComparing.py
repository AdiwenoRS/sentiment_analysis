import statistics
from textblob import TextBlob

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

# Calculate percentages
def calculate_percentage(data_dict, metric_index, label):
    valid_data = {} # Valid data to store
    
    for obj, metrics in data_dict.items(): # Filter and calculate mean for valid data
        if metrics[metric_index]:  
            valid_data[obj] = statistics.mean(metrics[metric_index])
    total = sum(valid_data.values())
    
    # Print percentages
    print(f"\nPercentage of {label}")
    for obj, mean in valid_data.items():
        percentage = (mean / total) * 100
        print(f"{obj} {label.lower()} percentage is {percentage:.2f}%")

# Neutral percentage
def calculate_percentageNeutral(results):
    print("\nPercentage of Neutral")
    total_neutral_counts = {}
    for obj, metrics in results.items():
        total_neutral_counts[obj] = len(metrics[2])

    # Print neutral percentages
    total_neutral_sum = sum(total_neutral_counts.values())
    for obj, count in total_neutral_counts.items():
        print(f"{obj} neutral percentage is {count / total_neutral_sum * 100:.2f}%")
        
    # append total_neutral_counts to results
    # results["Neutral"] = total_neutral_counts 

