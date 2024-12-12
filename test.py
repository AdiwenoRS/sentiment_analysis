import pandas as pd
import ProcessAndComparing as PAC
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

# Read data
datas = pd.read_csv('datasets/twitter_dataset.csv')
sentiments = datas.to_numpy()

# Global variables
objects = [] 
filtered_sentences = {} 
results = {} 

# Main application class
class SentimentAnalysisApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Tweet Sentiment Analysis")
        
        # Create GUI elements
        self.label = tk.Label(root, text="Choose an action:")
        self.label.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Objects", command=self.add_objects)
        self.add_button.pack(pady=5)

        self.compare_button = tk.Button(root, text="Compare Data", command=self.compare_data)
        self.compare_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Normalized Data", command=self.save_normalized_data)
        self.save_button.pack(pady=5)

        self.process_button = tk.Button(root, text="Processed Data", command=self.show_processed_data)
        self.process_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=5)

    def add_objects(self):
        user_input = simpledialog.askinteger("Input", "How many objects do you want to search? (Min 2 | Max 3)", minvalue=2, maxvalue=3)
        if user_input is not None:
            objects.clear()
            for i in range(user_input):
                obj = simpledialog.askstring("Input", f"Object {i + 1}:")
                if obj:
                    objects.append(obj)
            self.filter_and_analyze()

    def filter_and_analyze(self):
        global filtered_sentences, results
        filtered_sentences = {obj: [] for obj in objects}

        for sentence in sentiments.flatten():
            for obj in objects:
                if obj.upper() in sentence.upper():
                    filtered_sentences[obj].append(sentence)

        for obj, sentences in filtered_sentences.items():
            results[obj] = PAC.analyze_sentences(sentences)

        messagebox.showinfo("Success", "Data mining completed.")

    def compare_data(self):
        if not results:
            messagebox.showwarning("Warning", "No objects found. Please add objects to search.")
            return

        comparison_result = ""
        for obj in results:
            metrics = results[obj]
            comparison_result += f"{obj.upper()}:\n"
            comparison_result += f"Positive Polarity: {metrics[0]}\n"
            comparison_result += f"Negative Polarity: {metrics[1]}\n"
            comparison_result += f"Neutral Polarity: {metrics[2]}\n"
            comparison_result += f"Subjectivity: {metrics[3]}\n\n"
        
        messagebox.showinfo("Comparison Results", comparison_result)

    def save_normalized_data(self):
        if not filtered_sentences:
            messagebox.showwarning("Warning", "No data to save. Please analyze data first.")
            return

        data = {}
        for obj, sentences in filtered_sentences.items():
            data[obj] = sentences
            
        df = pd.DataFrame.from_dict(data, orient="index").transpose()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"Data saved to {file_path}")

    def show_processed_data(self):
        if not results:
            messagebox.showwarning("Warning", "No objects found. Please add objects to search.")
            return
        
        processed_data = ""
        for obj, metrics in results.items():
            processed_data += f"{obj.upper()}:\n"
            processed_data += f"Positive Polarity: {metrics[0]}\n"
            processed_data += f"Negative Polarity: {metrics[1]}\n"
            processed_data += f"Neutral Polarity: {metrics[2]}\n"
            processed_data += f"Subjectivity: {metrics[3]}\n\n"

        messagebox.showinfo("Processed Data", processed_data)

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentAnalysisApp(root)
    root.mainloop()