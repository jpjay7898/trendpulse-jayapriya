import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# Load the analysed data from Task 3
df = pd.read_csv("data/trends_analysed.csv")


# Create the outputs folder if it does not already exist
os.makedirs("outputs", exist_ok=True)


# --------------------------------------------------
# CHART 1: TOP 10 STORIES BY SCORE
# --------------------------------------------------

# Sort stories by score and select the top 10
top_stories = df.sort_values("score", ascending=False).head(10).copy()


# Shorten long titles so they fit nicely on the chart
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)


# Create horizontal bar chart
plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

# Put the highest score at the top
plt.gca().invert_yaxis()

plt.tight_layout()

# Save before showing the chart
plt.savefig("outputs/chart1_top_stories.png")

plt.show()
plt.close()


# --------------------------------------------------
# CHART 2: STORIES PER CATEGORY
# --------------------------------------------------

# Count stories in each category
category_counts = df["category"].value_counts()


# Create bar chart
plt.figure(figsize=(8, 6))

# Give each bar a different colour
plt.bar(
    category_counts.index,
    category_counts.values,
    color=plt.cm.tab10(np.arange(len(category_counts)))
)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()

# Save before showing the chart
plt.savefig("outputs/chart2_categories.png")

plt.show()
plt.close()


# --------------------------------------------------
# CHART 3: SCORE VS COMMENTS
# --------------------------------------------------

plt.figure(figsize=(10, 6))


# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]


# Plot popular stories
plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)


# Plot non-popular stories
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)


plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")

plt.legend()

plt.tight_layout()

# Save before showing the chart
plt.savefig("outputs/chart3_scatter.png")

plt.show()
plt.close()


# --------------------------------------------------
# BONUS: COMBINED DASHBOARD
# --------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

fig.suptitle("TrendPulse Dashboard", fontsize=18)


# Dashboard Chart 1
axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].invert_yaxis()


# Dashboard Chart 2
axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=plt.cm.tab10(np.arange(len(category_counts)))
)

axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")
axes[0, 1].set_title("Stories per Category")


# Dashboard Chart 3
axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)

axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].set_title("Score vs Comments")
axes[1, 0].legend()


# Use the fourth space for a simple summary
axes[1, 1].axis("off")

axes[1, 1].text(
    0.5,
    0.5,
    f"Total Stories: {len(df)}\n"
    f"Average Score: {df['score'].mean():.2f}\n"
    f"Average Comments: {df['num_comments'].mean():.2f}",
    ha="center",
    va="center",
    fontsize=14
)


plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the dashboard
plt.savefig("outputs/dashboard.png")

plt.show()
plt.close()


print()
print("All charts created successfully!")
print("Saved files:")
print("  outputs/chart1_top_stories.png")
print("  outputs/chart2_categories.png")
print("  outputs/chart3_scatter.png")
print("  outputs/dashboard.png")