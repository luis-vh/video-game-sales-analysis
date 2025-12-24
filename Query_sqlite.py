import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

df = pd.read_csv('data_of_games.csv')
conn = sqlite3.connect('videogames.db')

df.to_sql('Esencial_data', conn, if_exists='replace', index=False)

cursor = conn.cursor()

cursor.execute("""
    SELECT Name ,Year FROM Esencial_data
    ORDER BY Global_Sales DESC
    LIMIT 10
""")

top_10 = cursor.fetchall()

cursor.execute("""
    SELECT Genre, ROUND(Sum(Global_Sales),2) AS total_sales FROM Esencial_data
    GROUP BY Genre
    ORDER BY total_sales DESC 
""")

most_sale_genres = cursor.fetchall()

cursor.execute("""
    SELECT Platform, ROUND(Sum(Global_Sales),2) AS total_sales FROM Esencial_data
    GROUP BY Platform
    ORDER BY total_sales DESC 
""")

most_sale_platform = cursor.fetchall()

cursor.execute("""
    SELECT Year, ROUND(SUM(NA_Sales),2) AS NA_Sales, ROUND(SUM(EU_Sales),2) AS EU_Sales,ROUND(SUM(JP_Sales),2) AS JP_Sales ,ROUND(SUM(Global_Sales),2) AS Global_Sales FROM Esencial_data
    GROUP by Year
    ORDER by Year ASC
""")

evolution_of_sales = cursor.fetchall()

df1 = pd.DataFrame(top_10 ,columns=['Name','Year'])
df2 = pd.DataFrame(most_sale_genres ,columns=['Genre','Total_sales'])
df3 = pd.DataFrame(most_sale_platform ,columns=['Platform','total_sales'])
df4 = pd.DataFrame(evolution_of_sales ,columns=['Year','NA_Sales','EU_Sales','JP_Sales','Global_Sales'])

with pd.ExcelWriter('juegos.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Top 10', index=False)
    df2.to_excel(writer, sheet_name='Most sale genres', index=False)
    df3.to_excel(writer, sheet_name='Most sale platform', index=False)
    df4.to_excel(writer, sheet_name='Evolution of sales', index=False)

df4.plot(x='Year' ,y='Global_Sales' ,kind='line', marker='o')
plt.title('Evolution of Sales')
plt.savefig('Evolution of Sales.png' ,dpi=300 ,bbox_inches='tight')