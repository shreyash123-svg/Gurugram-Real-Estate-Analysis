import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("data of gurugram real Estate.csv")
print(df.head())

print(df.columns.tolist())
#Data cleaning
df.columns = (
    df.columns.str.strip()
    .str.replace(r'\s+', '_', regex=True)
    .str.lower()
)
if 'builder' not in df.columns and 'builder_name' in df.columns:
    df = df.rename(columns={'builder_name': 'builder'})
print(df.columns.tolist())
df=df.drop_duplicates()
df['price'] = df['price'].astype(str).str.replace(',', '').astype(float)
df['area']=df['area'].astype(str).str.replace(',','').astype(int)
df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(',', '').astype(int)
print(df['price'])
print(df['area'])
print(df['rate_per_sqft'])

#categorical columns cleaning
df['status'] = df['status'].str.strip().str.lower()

df['rera_approval']=df['rera_approval'].str.strip().str.lower().map({'approved by rera': True, 'not approved by rera': False})
print(df['rera_approval'])
df['flat_type'] = df['flat_type'].str.strip().str.lower()
df=df.drop_duplicates()
print(df.head())


#question 1: which is the costliest flat in the dataset
costliest_flat = df.loc[df['price'].idxmax()]
print(costliest_flat)


print(f"The costliest flat in the dataset is a {costliest_flat['flat_type']} located in {costliest_flat['locality']} with a price of {costliest_flat['price']}.")


#Question 2: Which locality has the highest average price?

df.groupby("locality")["price"].mean().idxmax()
highest_avg_price_locality = df.groupby("locality")["price"].mean().idxmax()
print(f"The locality with the highest average price is {highest_avg_price_locality}.")

#Question 3: Which locality has the highest rate per square foot?

df.groupby("locality")["rate_per_sqft"].mean().idxmax()
highest_rate_per_sqft_locality = df.groupby("locality")["rate_per_sqft"].mean().idxmax()
print(f"The locality with the highest rate per square foot is {highest_rate_per_sqft_locality}.")

#Question 4: Ready-to-move vs Under-construction pricing
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()
if ready_to_move_avg_price > under_construction_avg_price:
    print(f"Ready-to-move flats have a higher average price of {ready_to_move_avg_price} compared to under-construction flats with an average price of {under_construction_avg_price}.")
else:
    print(f"Under-construction flats have a higher average price of {under_construction_avg_price} compared to ready-to-move flats with an average price of {ready_to_move_avg_price}.")


#Question 5: Does RERA approval affect pricing?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
rera_not_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()
if rera_approved_avg_price > rera_not_approved_avg_price:
    print(f"RERA-approved flats have a higher average price of {rera_approved_avg_price} compared to non-RERA-approved flats with an average price of {rera_not_approved_avg_price}.")
else:
    print(f"Non-RERA-approved flats have a higher average price of {rera_not_approved_avg_price} compared to RERA-approved flats with an average price of {rera_approved_avg_price}.")


#Question 6: How does area impact price?

sns.scatterplot(data=df, x='area', y='price')
plt.title('Area vs Price')
plt.xlabel('Area (sqft)')
plt.ylabel('Price')
plt.show()

#Question 7: Which BHK configuration is most expensive?
most_expensive_bhk = df.groupby('bhk_count')['price'].mean().idxmax()
print(f"The most expensive BHK configuration is {most_expensive_bhk} BHK.")

#Question 8: Which property type is the costliest?
costliest_property_type = df.groupby('flat_type')['price'].mean().idxmax()
print(f"The costliest property type is {costliest_property_type}.")


#Question 9: Do certain builders price higher?
builders_avg_price = df.groupby('builder')['price'].mean()
most_expensive_builder = builders_avg_price.idxmax()
print(f"The builder with the highest average price is {most_expensive_builder}.")


#Question 10: Are larger homes more expensive per sqft?
sns.scatterplot(data=df, x='area', y='rate_per_sqft')
plt.title('Area vs Rate per Sqft')
plt.xlabel('Area (sqft)')
plt.ylabel('Rate per Sqft')
plt.show()
