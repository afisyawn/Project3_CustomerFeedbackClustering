import pandas as pd

def calculate_version_score(file_path, output_file, threshold=3, favorable_threshold=4):
    # Read the dataset
    cleaned_data = pd.read_csv(file_path)
    
    # Filter scores based on the threshold
    score_data = cleaned_data["score"].where(cleaned_data["score"] > threshold, other=0)
    
    # Extract version data
    version_data = cleaned_data["reviewCreatedVersion"]
    
    # Create DataFrame for scores and versions
    score_version = pd.DataFrame({"score": score_data, "version": version_data})
    
    # Drop rows where version is NaN
    score_version = score_version.dropna(subset=["version"])
    
    # Determine if the review is favorable based on the favorable threshold
    score_version["favorable"] = score_version["score"] >= favorable_threshold
    
    # Group by version and calculate the number of favorable reviews and total reviews
    score_version_mean = score_version.groupby("version").agg(
        favorable_reviews=("favorable", "sum"),  # Count of favorable reviews (True counts as 1)
        total_reviews=("score", "size")          # Total number of reviews
    )
    
    # Calculate the Customer Satisfaction Score (CSAT) percentage
    score_version_mean["CSAT"] = (score_version_mean["favorable_reviews"] / score_version_mean["total_reviews"]) * 100
    
    # Save the results to a CSV file
    score_version_mean.to_csv(output_file)
    
    print(f"Version score data saved to {output_file}")

# Example usage:
calculate_version_score("document/gi_review_id.csv", "document/gi_score_version.csv")
