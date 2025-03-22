import streamlit as st
import pandas as pd
import mysql.connector
from tabulate import tabulate

connection = mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "42gLBzNbmFpVnrp.root",
  password = "M4zJcGITE38JycpJ",
  database = "Retail_Order_Analysis",
)

mycursor = connection.cursor()


st.title("Retail Order Analysis")
st.subheader("Choose a Internal Mentor Query")
question = st.selectbox(
    "Select a Question",
    [
        "Find top 10 highest revenue generating products",
        "Find the top 5 cities with the highest profit margins",
        "Calculate the total discount given for each category",
        "Find the average sale price per product category",
        "Find the region with the highest average sale price",
        "Find the total profit per category",
        "Identify the top 3 segments with the highest quantity of orders",
        "Determine the average discount percentage given per region",
        "Find the product category with the highest total profit",
        "Calculate the total revenue generated per year"
    ]
)

sql_queries = {
    "Find top 10 highest revenue generating products": '''SELECT product_id, SUM(sale_price) AS total_revenue FROM order_table2 
    GROUP BY product_id ORDER BY total_revenue DESC LIMIT 10;''',
    "Find the top 5 cities with the highest profit margins":'''SELECT city, SUM(profit) AS total_profit FROM order_table1 
    JOIN order_table2 ON order_table1.order_id = order_table2.order_id GROUP BY city ORDER BY total_profit DESC LIMIT 5;''',
    "Calculate the total discount given for each category": '''SELECT category, SUM(discount_amount) AS total_discount FROM order_table1 
    JOIN order_table2 ON order_table1.order_id = order_table2.order_id GROUP BY category;''',
    "Find the average sale price per product category": '''SELECT category, AVG(sale_price) AS average_sale_price 
    FROM Retail_order_analysis.order_table2 JOIN order_table1 ON order_table2.order_id = order_table1.order_id GROUP BY category;''',
    "Find the region with the highest average sale price": '''SELECT region, AVG(sale_price) AS avg_sale_price FROM Retail_order_analysis.order_table2 
    JOIN order_table1 ON order_table2.order_id = order_table1.order_id GROUP BY region;''',
    "Find the total profit per category": '''SELECT category, sum(profit) as overall_profit FROM Retail_order_analysis.order_table2 
    JOIN order_table1 ON order_table2.order_id = order_table1.order_id GROUP BY category;''',
    "Identify the top 3 segments with the highest quantity of orders": '''SELECT segment, SUM(quantity) AS total_quantity FROM Retail_order_analysis.order_table2 
    JOIN order_table1 ON order_table2.order_id = order_table1.order_id GROUP BY segment ORDER BY total_quantity DESC LIMIT 3;''',
    "Determine the average discount percentage given per region": '''SELECT region, AVG(discount_percent) AS avg_discount_percent FROM Retail_order_analysis.order_table2 
    JOIN order_table1 ON order_table2.order_id = order_table1.order_id GROUP BY region;''',
    "Find the product category with the highest total profit": '''SELECT sub_category as product_category, SUM(profit) AS total_profit FROM Retail_order_analysis.order_table2
    GROUP BY sub_category;''',
    "Calculate the total revenue generated per year": '''SELECT YEAR(order_date) AS order_year, CONCAT('$', FORMAT(SUM(sale_price), 2))AS total_revenue
    FROM Retail_order_analysis.order_table2 JOIN order_table1 ON order_table2.order_id = order_table1.order_id GROUP BY YEAR(order_date);'''
}

st.code(sql_queries[question], language="sql")

def run_query(query):
    mycursor.execute(query)
    columns = [col[0] for col in mycursor.description]
    data = mycursor.fetchall()
    return pd.DataFrame(data, columns=columns)

if st.button("Run Query"):
    result = run_query(sql_queries[question])
    if not result.empty:
        st.write("### Result:")
        st.dataframe(result)
    else:
        st.write("No data found.")

#Learner Queries
st.subheader("Choose a Learner Query")
question1 = st.selectbox(
    "Select a Question",
    [
        "Find the top 5 state with the highest phone sales",
        "Find the product which has highest profit",
        "Categorize the profit of each product category",
        "Find the number of shipping mode as categorized",
        "Find the products in different shipping mode",
        "Find the highest product which is ordered",
        "Find the profit from the Table product",
        "Find the sales quantity of paper in san fransisco",
        "Find the postal code & city of top 5 sales in Art order",
        "Check how much accessories have been purchased by Consumer"
    ]
)

sql_queries1 = {
    "Find the top 5 state with the highest phone sales": '''SELECT state, SUM(quantity) AS total_phone_sales
    FROM Retail_order_analysis.order_table2 JOIN order_table1 ON order_table2.order_id = order_table1.order_id 
    WHERE sub_category = 'Phones' GROUP BY state ORDER BY total_phone_sales DESC LIMIT 5;''',
    "Find the product which has highest profit": '''SELECT product_id, SUM(profit) AS total_profit 
    FROM Retail_order_analysis.order_table2 GROUP BY product_id order by total_profit DESC LIMIT 1;''',
    "Categorize the profit of each product category": '''SELECT sub_category, SUM(profit) AS total_profit, 
    CASE
    WHEN SUM(profit) > 25000 then 'High Profit'
    WHEN SUM(profit) > 10000 then 'Medium Profit'
    ELSE 'Low Profit' END AS profit_category FROM Retail_order_analysis.order_table2 GROUP BY sub_category order by total_profit;''',
    "Find the number of shipping mode as categorized": '''SELECT ship_mode, COUNT(*) AS mode_count FROM Retail_order_analysis.order_table1 
    GROUP BY ship_mode;''',
    "Find the products in different shipping mode": '''SELECT ship_mode, COUNT(DISTINCT product_id) AS product_count 
    FROM Retail_order_analysis.order_table1 JOIN Retail_order_analysis.order_table2 ON order_table1.order_id = order_table2.order_id
    GROUP BY ship_mode;''',
    "Find the highest product which is ordered": '''SELECT category as product, SUM(quantity) AS total_quantity FROM Retail_order_analysis.order_table2
    JOIN Retail_order_analysis.order_table1 ON order_table2.order_id = order_table1.order_id 
    GROUP BY category ORDER BY total_quantity DESC LIMIT 1;''',
    "Find the profit from the Table product": '''SELECT sub_category as product, SUM(profit) AS total_profit FROM Retail_order_analysis.order_table2 
    WHERE sub_category = 'Tables' GROUP BY sub_category;''',
    "Find the sales quantity of paper in san fransisco": '''SELECT sub_category as product, SUM(quantity) AS Total_quantity
    FROM Retail_order_analysis.order_table2 JOIN Retail_order_analysis.order_table1 ON order_table2.order_id = order_table1.order_id
    WHERE sub_category = 'Paper' AND city = 'San Francisco';''',
    "Find the postal code & city of top 5 sales in Art order": '''SELECT postal_code, city, SUM(quantity) AS Total_quantity 
    FROM Retail_order_analysis.order_table2 JOIN Retail_order_analysis.order_table1 ON order_table2.order_id = order_table1.order_id 
    WHERE sub_category = 'Art' GROUP BY postal_code, city ORDER BY Total_quantity DESC LIMIT 5;''',
    "Check how much accessories have been purchased by Consumer": '''SELECT segment, COUNT(*) sub_category FROM Retail_order_analysis.order_table2 
    JOIN Retail_order_analysis.order_table1 ON order_table2.order_id = order_table1.order_id WHERE segment = 'Consumer' AND sub_category = 'Accessories';'''
}

st.code(sql_queries1[question1], language="sql")

def run_query1(query):
    mycursor.execute(query)
    columns = [col[0] for col in mycursor.description]
    data = mycursor.fetchall()
    return pd.DataFrame(data, columns=columns)

if st.button("Run Query", key="predefined_query"):
    result = run_query(sql_queries1[question1])
    if not result.empty:
        st.write("### Result:")
        st.dataframe(result)
    else:
        st.write("No data found.")
