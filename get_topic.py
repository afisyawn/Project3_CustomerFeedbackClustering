import pandas as pd

def save_topic_data(file_path, topic_number, output_file):
    # Read the dataset
    data = pd.read_csv(file_path)
    
    # Filter the data based on the specified topic number
    topic_data = data[["content_conc", "topic"]].copy()
    topic_data = topic_data[topic_data["topic"] == topic_number]
    
    # Save the filtered data to a CSV file
    topic_data.to_csv(output_file, index=False)
    print(f"Topic {topic_number} data saved to {output_file}")

# Example usage:
save_topic_data("document/gi_review_analized.csv", 3, "document/topic3.csv")
save_topic_data("document/gi_review_analized.csv", 5, "document/topic5.csv")
save_topic_data("document/gi_review_analized.csv", 6, "document/topic6.csv")