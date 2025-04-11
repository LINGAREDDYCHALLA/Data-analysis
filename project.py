import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("C:\\Users\\HP\\Downloads\\file (7).csv")
print(df.info()) 
print(df.describe())
print(df.head())
print(df.tail())
print(df.isnull().sum()) 
df=df.drop(columns="published_timestamp")
def convert_to_minutes(duration):
    try:
        duration = duration.lower().strip()
        if 'hour' in duration:
            return float(duration.split()[0]) * 60
        elif 'min' in duration:
            return float(duration.split()[0])
        else:
            return 0
    except:
        return np.nan
df['content_duration'] = df['content_duration'].astype(str).apply(convert_to_minutes)
df['price'] = df['price'].replace('Free', '0')            
df['price'] = df['price'].replace('[\$,]', '', regex=True)  
df['price'] = df['price'].astype(float)                  
df=df.drop_duplicates()
print(df.duplicated().sum())

price_engagement = df.groupby('price')[['num_subscribers', 'num_reviews']].mean().reset_index()
plt.figure(figsize=(13, 6))
sns.lineplot(data=price_engagement, x='price', y='num_subscribers', label='Average Subscribers')
sns.lineplot(data=price_engagement, x='price', y='num_reviews', label='Average Reviews')
plt.title('Average Engagement by Course Price')
plt.xlabel('Price')
plt.ylabel('Average Count')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

df_cleaned = df[['price', 'num_subscribers', 'num_reviews', 'num_lectures', 'content_duration']]
corr = df_cleaned.corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap of Udemy Course Features')
plt.tight_layout()
plt.show()

top_courses = df.sort_values(by='num_subscribers', ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x='num_subscribers', y='course_title', data=top_courses, palette='coolwarm')
plt.title('Top 10 Courses by Subscribers')
plt.xlabel('Subscribers')
plt.ylabel('Course Title')
plt.tight_layout()
plt.show()

price_vs_subs = df.groupby('price')['num_subscribers'].mean().reset_index()
price_vs_subs = price_vs_subs.sort_values(by='price')
plt.figure(figsize=(10, 6))
plt.plot(price_vs_subs['price'], price_vs_subs['num_subscribers'], marker='o', color='teal')
plt.title('Average Subscribers by Course Price')
plt.xlabel('Price (USD)')
plt.ylabel('Average Number of Subscribers')
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='subject', y='num_reviews', palette='Set2')
plt.title('Number of Reviews by Subject')
plt.xlabel('Subject')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
