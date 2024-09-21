from google_play_scraper import app, reviews_all, Sort
import pandas as pd
import time
import json

def detail(app):
    """
    Prints detailed information about an app in a formatted JSON style.
    
    Args:
    - app (dict): A dictionary containing app details.
    """
    # Convert the app details dictionary to a JSON string with indentation for readability
    str_app_det = json.dumps(app, indent=4)
    
    # Print the formatted JSON string to the console
    print(str_app_det)


def fetch_review(package_name, country_code, delay=1000):
    """
    Fetches all reviews for a given app and country.
    
    Args:
    - package_name (str): The package name of the app (e.g., "com.miHoYo.GenshinImpact").
    - country_code (str): The country code to fetch reviews from (e.g., "id" for Indonesia).
    - delay (int): Delay in milliseconds between requests to avoid hitting rate limits.
    
    Returns:
    - list: A list of reviews.
    """
    try:
        # Fetch all reviews for the specified app and country with the given delay
        app_review = reviews_all(
            package_name,
            sleep_milliseconds=delay,
            lang="id",
            country=country_code,
            sort=Sort.MOST_RELEVANT
        )
        return app_review
    
    except Exception as e:
        # Print an error message if an exception occurs
        print(f"An error for country {country_code}: {e}")
        return []

def save_review_to_csv(review, filename):
    """
    Saves reviews to a CSV file.
    
    Args:
    - review (list): List of reviews to save.
    - filename (str): Path to the CSV file where reviews will be saved.
    """
    # Convert list of reviews to DataFrame and save to CSV
    df_reviews = pd.DataFrame(review)
    df_reviews.to_csv(filename, index=False)

def main():
    """
    Main function to fetch reviews from specified countries and save them to a CSV file.
    """
# Uncomment the following lines to show app details
# app_details = app("com.miHoYo.GenshinImpact")
# detail(app_details)

    # List of countries to fetch reviews from
    countries = ["id"]
    all_review = []

    # Loop through each country and fetch reviews
    for country in countries:
        print(f"Fetching review from country: {country}")
        reviews = fetch_review(
            package_name="com.miHoYo.GenshinImpact",
            country_code=country
        )
        print("Extending review list")
        all_review.extend(reviews)
        time.sleep(1)  # Sleep to avoid rate limits

    # Save the collected reviews to a CSV file if there are any
    if all_review:
        save_review_to_csv(all_review, "document/gi_review_id.csv")
    else:
        print("No reviews were fetched")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
