import pandas as pd
import numpy as np


# Load the clean CSV created in Task 2
df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")


# --------------------------------------------------
# 1. LOAD AND EXPLORE
# --------------------------------------------------

print()
print("First 5 rows:")
print(df.head())


# Calculate average score and average comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print()
print(f"Average score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")


# --------------------------------------------------
# 2. BASIC ANALYSIS WITH NUMPY
# --------------------------------------------------

# Convert score column to NumPy array
scores = df["score"].to_numpy()

# NumPy statistics
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

highest_score = np.max(scores)
lowest_score = np.min(scores)

print()
print("--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {highest_score}")
print(f"Min score    : {lowest_score}")


# Find the category with the most stories
category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print()
print(
    f"Most stories in: {most_common_category} "
    f"({most_common_count} stories)"
)


# Find the story with the most comments
most_commented_index = df["num_comments"].idxmax()

most_commented_title = df.loc[most_commented_index, "title"]
most_commented_count = df.loc[most_commented_index, "num_comments"]

print()
print(
    f'Most commented story: "{most_commented_title}" '
    f"— {most_commented_count} comments"
)


# --------------------------------------------------
# 3. ADD NEW COLUMNS
# --------------------------------------------------

# Engagement = comments divided by score + 1
df["engagement"] = df["num_comments"] / (df["score"] + 1)


# A story is popular when its score is greater than
# the average score of all stories
df["is_popular"] = df["score"] > average_score


# --------------------------------------------------
# 4. SAVE THE RESULT
# --------------------------------------------------

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print()
print(f"Saved to {output_file}")