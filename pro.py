import pandas as pd 
import numpy as np 
import plotly.express as px 
import streamlit as st
import datetime as dt

st.markdown("<h3 style='text-align: center;'>Welcome To Our Application</h3>", unsafe_allow_html=True)


df=pd.read_csv(r"D:\Streamlit\v6\fact_table.csv")
df1=pd.read_csv(r"D:\Streamlit\v6\customers_table.csv")
df2=pd.read_csv(r"D:\Streamlit\v6\monthly_store_targets.csv")
df3=pd.read_csv(r"D:\Streamlit\v6\products_table.csv")
df4=pd.read_csv(r"D:\Streamlit\v6\sales_persons_table.csv")

# df.info()
df['Order Date']=pd.to_datetime(df["Order Date"])
df.insert(6,"orders",(df['Quantity Sold']) - (df['Quantity Returned']))

# df1.info()
df1['Date of Birth']=pd.to_datetime(df1["Date of Birth"])
df1.insert(5,"Birthday",df1['Date of Birth'].dt.year)
df1.drop(columns=['Date of Birth'],axis=1,inplace=True)
df1.insert(1,"FullName",df1['First Name']+" " +df1["Last Name"])
df1.drop(columns=(['First Name','Last Name' ]),inplace=True)


df2['Month']=pd.to_datetime(df2["Month"])


df3.insert(5,"Profit",(df3['Sales Price']) - (df3['Cost Price']))


df4['Date of Birth']=pd.to_datetime(df4["Date of Birth"])
df4.insert(4,"Birth year",df4['Date of Birth'].dt.year)



# df fact_table.csv 
# df1 customers_table.csv
# df2 monthly_store_targets.csv
# df3 products_table.csv
# df4 sales_persons_table.csv

df = df.join(df1.set_index('Customer ID'), on='Customer ID')
df = df.join(df3.set_index('Product ID'), on='Product ID')


df.drop(columns=(['Sales Person ID','Customer ID','Product ID']),inplace=True)
df['Month']=df['Order Date'].dt.month_name()
df.isna().sum()

length=st.slider("Select the number of the row",min_value=5,step=1,value=5)
multi=st.multiselect("Select the columns that you want to sea it",df.columns.to_list(),
                     default=df.columns.to_list())
st.write(df[:length][multi])


# df.to_excel('E:\\data analysis\\projects part 2\\v20\\Excel Sales Dashboard.xlsx')

df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')

start_date=df['Order Date'].min()
end_date=df['Order Date'].max()

col1,col2=st.columns(2)
with col1:
    date1=pd.to_datetime(st.date_input("Satrt Date",value=start_date))
with col2:
    date2=pd.to_datetime(st.date_input("End Date",value=end_date))
    

df=df[(df['Order Date'] >=date1 ) & (df['Order Date'] <=date2)]    

st.sidebar.header("Select the Filters")

month=st.sidebar.multiselect("Select the month ",df['Month'].unique())
Payment_Method=st.sidebar.multiselect("Select the Payment Method ",df['Payment Method'].unique())
Location=st.sidebar.multiselect("Select the Location ",df['Location'].unique())
Category=st.sidebar.multiselect("Select the Category ",df['Category'].unique())




# month Payment_Method Location Category 

if not month and not Payment_Method and not Location and not Category:
    df=df
    
elif  not month and not Payment_Method and not Location:
    df=df[df['Category'].isin(Category)]    
     
elif  not month and not Payment_Method and not Category:
    df=df[df['Location'].isin(Location)]
    
elif  not month and not Location and not Category:
    df=df[df['Payment Method'].isin(Payment_Method)]
    
elif  not Payment_Method and not Location and not Category:
    df=df[df['Month'].isin(month)]
    
    
    
    

# month Payment_Method Location Category 
elif month and Payment_Method:
    df=df[df['Payment Method'].isin(Payment_Method) & df['Month'].isin(month)]
    
elif month and Location:
    df=df[df['Location'].isin(Location) & df['Month'].isin(month)]

elif month and Category:
    df=df[df['Month'].isin(month) & df['Category'].isin(Category)] 
    
       
elif Payment_Method and Location:
    df=df[df['Payment Method'].isin(Payment_Method) & df['Location'].isin(Location)] 

elif Payment_Method and Category:
    df=df[df['Payment Method'].isin(Payment_Method) & df['Category'].isin(Category)] 

elif Location and Category:
    df=df[df['Location'].isin(Location) & df['Category'].isin(Category)] 
    



# month Payment_Method Location Category 
elif  month :
    df=df['Month'].isin(month)
    
elif  Payment_Method :
    df=df['Payment Method'].isin(Payment_Method)
    
elif  Location :
    df=df['Location'].isin(Location)
    
elif  Category :
    df=df['Category'].isin(Category) 
            
else :
    df=df[df['Month'].isin(month) & df['Payment Method'].isin(Payment_Method)& df['Locatione'].isin(Location)& df['Category'].isin(Category) & df['Category'].isin(Category)]

Quantity=df['Quantity Sold'].sum()
Quantity = "{:,.2f}".format(Quantity)

Returned=df['Quantity Returned'].sum()
Returned = "{:,.2f}".format(Returned)

orders=df['orders'].sum()
orders = "{:,.2f}".format(orders)


Sales_Price=df['Sales Price'].sum().round(2)
Sales_Price = "{:,.2f}".format(Sales_Price)

Cost_Price=df['Cost Price'].sum().round(2)
Cost_Price = "{:,.2f}".format(Cost_Price)

Profit=df['Profit'].sum().round(2)
Profit = "{:,.2f}".format(Profit)


st.markdown("""
        <style>
        .metric-label {
            font-size: 18px;
            color: #4CAF50;  /* Change color here */
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #FF5722;  /* Change color here */
        }
        </style>
        """, unsafe_allow_html=True)

col01, col02, col03 = st.columns(3)
with col01:
    st.markdown(f"""
    <div class="metric-label">Total Quantity </div>
    <div class="metric-value">{Quantity}</div>
    </br>
    </br>
    """, unsafe_allow_html=True)

with col02:
    st.markdown(f"""
    <div class="metric-label">Total Returned orders </div>
    <div class="metric-value">{Returned}</div>
    </br>
    </br>
    """, unsafe_allow_html=True)

with col03:
    st.markdown(f"""
    <div class="metric-label">Total of orders </div>
    <div class="metric-value">{orders}</div>
    </br>
    </br>
    """, unsafe_allow_html=True)




col01, col02, col03 = st.columns(3)
with col01:
    st.markdown(f"""
    <div class="metric-label">Total Sales </div>
    <div class="metric-value">{Sales_Price}</div>
    </br>
    </br>
    """, unsafe_allow_html=True)

with col02:
    st.markdown(f"""
    <div class="metric-label">Total Cost </div>
    <div class="metric-value">{Cost_Price}</div>
    </br>
    </br>
    """, unsafe_allow_html=True)

with col03:
    st.markdown(f"""
    <div class="metric-label">Total of Profit</div>
    <div class="metric-value">{Profit}</div>
    </br>
    </br>
    """, unsafe_allow_html=True)
    

col1,col2=st.columns(2)
with col1:
    xx=st.selectbox("Select the column in X axis",df.select_dtypes(include=['object', 'string']).columns)
    
with col2:    
    y=st.selectbox("Select the column in X axis",df.select_dtypes(include=np.int64).columns)


x=df.groupby(by=xx,as_index=False)[y].sum()

fig = px.bar(
    x, 
    x=xx, 
    y=y, 
    color=xx,  
    text=y     
)
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(width=1200,  # Width of the chart
    height=400,  # Height of the chart
    margin=dict(t=5, b=30, l=50, r=30),xaxis_tickangle=60)
st.plotly_chart(fig, use_container_width=False)



col1,col2=st.columns(2)
with col1:
        with st.expander(" Top 10 Customer buys "):
            region = df.groupby(by='FullName',as_index=False)['Profit'].sum().sort_values(by='Profit', ascending=False).head(10)
            st.write()
            csv = region.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file') 

with col2:
        with st.expander("Top 10 Category make profit"):
            q2 = df.groupby(by='Category', as_index=False)['Profit'].sum().sort_values(by='Profit', ascending=False).head(10)
            st.write()
            csv = q2.to_csv(index = False).encode('utf-8')
            st.download_button("Download city", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file') 



st.markdown(
"""
<h1 style='text-align: center;'>Table contain view of Profit</h1>
""",
unsafe_allow_html=True
)

import plotly.figure_factory as ff
with st.expander("Summary_Table"):
    top = df.groupby(by=['FullName','Location','Category','Payment Method'])[['Sales Price','Cost Price','Profit']].sum().round(3).reset_index().sort_values(by=['Sales Price','Cost Price','Profit'], ascending=False).head(30)
    fig = ff.create_table(top, colorscale = "Cividis")
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,  # Adjust height to fit content
        font=dict(size=12)  # Reduce font size
    )
    st.plotly_chart(fig, use_container_width=True)


st.markdown(
"""
<h1 style='text-align: center;'>Hierarchical view of Profit TreeMap</h1>
""",
unsafe_allow_html=True
)
fig3 = px.treemap(df, path = ["Location","Category"], values = "Profit",hover_data = ["Profit"],
                color = "Category")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)



q2 = df.groupby(by='Month')['Profit'].sum().sort_values(ascending=False).reset_index()
st.markdown(
    """
    <h5 style='text-align: center;'>Total Profit by Month</h5>

    """,
    unsafe_allow_html=True
)
fig = px.area(q2, x='Month', y='Profit')       
st.plotly_chart(fig, use_container_width=True)

st.markdown("Monthly Profit Table")
st.dataframe(q2)



st.markdown(
    """
    <h5 style='text-align: center;'>Total Profit by Gender</h5>

    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    xx = st.selectbox(
        "Select the column in X axis", 
        df.select_dtypes(include=['object', 'string']).columns,
        key='x_column'
    )

with col2:
    y = st.selectbox(
        "Select the column in Y axis", 
        df.select_dtypes(include=np.int64).columns,
        key='y_column'
    )


gender_profit = df.groupby(xx, as_index=False)[y].sum()

fig = px.pie(gender_profit, names=xx, values=y)
st.plotly_chart(fig)













