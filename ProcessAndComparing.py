import statistics
from textblob import TextBlob
import pandas as pd

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
    valid_data = {} # mean valid data 
    sentimentTotal = {}
    
    for obj, metrics in data_dict.items(): # Filter and calculate mean for valid data
        if metrics[metric_index]:  
            valid_data[obj] = statistics.mean(metrics[metric_index])
            sentimentTotal[obj] = len(metrics[metric_index])
    total = sum(valid_data.values())
    
    # Print percentages
    print(f"\nPercentage of {label}")
    for obj, mean in valid_data.items():
        percentage = (mean / total) * 100
        print(f"{obj.upper()} {label.lower()} percentage is {percentage:.2f}% from {sentimentTotal[obj]} sentiments")

# Neutral percentage
def calculate_percentageNeutral(results):
    print("\nPercentage of Neutral")
    total_neutral_counts = {}
    for obj, metrics in results.items():
        total_neutral_counts[obj] = len(metrics[2])

    # Print neutral percentages
    total_neutral_sum = sum(total_neutral_counts.values())
    for obj, count in total_neutral_counts.items():
        print(f"{obj.upper()} neutral percentage is {count / total_neutral_sum * 100:.2f}% from {total_neutral_counts[obj]} sentiments")

def calculateToTable(filtered_sentences, data1, data2, objects):
    for obj, sentences in filtered_sentences.items():
        if obj == objects[0]:
            data1[obj] = sentences
            data1['P Positive'], data1['P Negative'], data1['P Neutral'], data1['Subjectivity'] = [], [], [], []
            for sentence in sentences:
                sentiment = TextBlob(sentence).sentiment
                polarity = sentiment.polarity
                data1['Subjectivity'].append(sentiment.subjectivity)
                if polarity > 0:
                    data1["P Positive"].append(polarity)
                    data1["P Negative"].append(None)
                    data1['P Neutral'].append(None)
                elif polarity < 0:
                    data1['P Negative'].append(polarity)
                    data1["P Positive"].append(None)
                    data1['P Neutral'].append(None)
                else:
                    data1["P Neutral"].append(polarity)    
                    data1["P Negative"].append(None)
                    data1['P Positive'].append(None)

        elif obj == objects[1]:
            data2[obj] = sentences
            data2['P Positive'], data2['P Negative'], data2['P Neutral'], data2['Subjectivity'] = [], [], [], []
            for sentence in sentences:
                sentiment = TextBlob(sentence).sentiment
                polarity = sentiment.polarity
                data2['Subjectivity'].append(sentiment.subjectivity)
                if polarity > 0:
                    data2["P Positive"].append(polarity)
                    data2["P Negative"].append(None)
                    data2['P Neutral'].append(None)
                elif polarity < 0:
                    data2['P Negative'].append(polarity)
                    data2["P Positive"].append(None)
                    data2['P Neutral'].append(None)
                else:
                    data2["P Neutral"].append(polarity)    
                    data2["P Negative"].append(None)
                    data2['P Positive'].append(None)
        
