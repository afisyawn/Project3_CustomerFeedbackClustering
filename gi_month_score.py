import pandas as pd

def calculate_monthly_score(file_path, output_file, threshold=3):
    # Read the dataset
    cleaned_data = pd.read_csv(file_path)
    
    # Convert the 'at' column to datetime format
    cleaned_data["date"] = pd.to_datetime(cleaned_data['at'])
    
    # Determine favorable reviews based on the threshold
    cleaned_data["favorable"] = cleaned_data["score"] > threshold
    
    # Extract year and month from the date column
    cleaned_data["year"] = cleaned_data["date"].dt.year
    cleaned_data["month"] = cleaned_data["date"].dt.month
    
    # Group by year and month, and calculate total and favorable reviews
    score_month_mean = cleaned_data.groupby(by=["year", "month"]).agg(
        favorable_reviews=("favorable", "sum"),
        total_reviews=("score", "size")
    )
    
    # Calculate the percentage of favorable reviews
    score_month_mean["percentage"] = (score_month_mean["favorable_reviews"] / score_month_mean["total_reviews"]) * 100
    
    # Save the results to a CSV file
    score_month_mean.to_csv(output_file)
    
    print(f"Monthly score data saved to {output_file}")

# Example usage:
calculate_monthly_score("document/gi_review_id.csv", "document/gi_score_month.csv")