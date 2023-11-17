import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import requests

# personalize page headers and icon
st.set_page_config(

    page_title= ' Financial Dashboard',
    page_icon= '📈'

)

# hide streamlit humberger
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Use Yahoo Api to make requests

import requests
import urllib

class YFinance:
# identifiant of user 
    user_agent_key = "User-Agent"
    user_agent_value = ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/58.0.3029.110 Safari/537.36")
    
    def __init__(self, ticker):
        self.yahoo_ticker = ticker

    def __str__(self):
        return self.yahoo_ticker

    def _get_yahoo_cookie(self):
        cookie = None

        headers = {self.user_agent_key: self.user_agent_value}
        response = requests.get("https://fc.yahoo.com",
                                headers=headers,
                                allow_redirects=True)

        if not response.cookies:
            raise Exception("Failed to obtain Yahoo auth cookie.")
#obtention of coockie 
        cookie = list(response.cookies)[0]

        return cookie
# obtention of crumb token to avoid cross site request forgeryS

    def _get_yahoo_crumb(self, cookie):
        crumb = None

        headers = {self.user_agent_key: self.user_agent_value}

        crumb_response = requests.get(
            "https://query1.finance.yahoo.com/v1/test/getcrumb",
            headers=headers,
            cookies={cookie.name: cookie.value},
            allow_redirects=True,
        )
        crumb = crumb_response.text

        if crumb is None:
            raise Exception("Failed to retrieve Yahoo crumb.")

        return crumb

    @property
# function that will retrieve data from yahoo finance 
    def info(self):
        # Yahoo modules doc informations :
        # https://cryptocointracker.com/yahoo-finance/yahoo-finance-api
        cookie = self._get_yahoo_cookie()
        crumb = self._get_yahoo_crumb(cookie)
        info = {}
        ret = {}

        headers = {self.user_agent_key: self.user_agent_value}

        yahoo_modules = ("assetProfile,"  # longBusinessSummary
                         "summaryDetail,"
                         "financialData,"
                         "indexTrend,"
                         "defaultKeyStatistics")

        url = ("https://query1.finance.yahoo.com/v10/finance/"
               f"quoteSummary/{self.yahoo_ticker}"
               f"?modules={urllib.parse.quote_plus(yahoo_modules)}"
               f"&ssl=true&crumb={urllib.parse.quote_plus(crumb)}")

        info_response = requests.get(url,
                                     headers=headers,
                                     cookies={cookie.name: cookie.value},
                                     allow_redirects=True)

        info = info_response.json()
        info = info['quoteSummary']['result'][0]

        for mainKeys in info.keys():
            for key in info[mainKeys].keys():
                if isinstance(info[mainKeys][key], dict):
                    try:
                        ret[key] = info[mainKeys][key]['raw']
                    except (KeyError, TypeError):
                        pass
                else:
                    ret[key] = info[mainKeys][key]

        return ret
    

#

c1,c2= st.columns([3,7])

title = """

        <h1  style='text-align: center;'> Financial Dashboard </h1>
      
"""

st.markdown(title, unsafe_allow_html= True )



from PIL import Image
img = Image.open("yahoo.png")

c2.image(img, caption='Data Source')



# render data from html page

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

ticker_list= tickers['Symbol']
col1,col2,col3, col4 = st.columns(4)



data = col1.selectbox( 'Select Ticker',options= ticker_list)
sd = col2.date_input('Enter start date', datetime.today().date()-timedelta(days=30))

fd = col3.date_input('Enter en date',datetime.today().date())

if col4.button("Download Data"):
       # Trigger an update 
       df= yf.download(data, sd, fd, progress= False)
       st.write(df)

    

# method to get info from yahoo
def getinfo(data):

    return YFinance(data).info

# method display company info 
def company_info():
   info = getinfo(data)
   company_info ={
   "📍 Address": info.get("address1", "Not provided"),
       "🏙 City": info.get('city', 'Not provided'),
       "🌎 Country": info.get('country', 'not provided'),
       "📞 Phone": info.get('phone', 'Not provided'),
       "👨🏼‍💼 Sectorkey": info.get('sectorKey', 'Not provided')
   }
  
   keys= [ "📍 Address","🏙 City","🌎 Country","📞 Phone","👨🏼‍💼 Sectorkey"]
   for i in keys:     
       value = company_info[i]
       st.write( i ,':', value)

    
# Render data of specific ticker 
def render(data,interval, sd ,fd,):
            
            df = yf.Ticker(data).history(interval=interval, start= sd, end= fd)
            df.reset_index(inplace=True)
            df['Date'] = df['Date'].dt.date
            return df

# render business summary




def rendersummary():
    info = getinfo(data)
    inf= {

        'BusinessSummary': info.get('longBusinessSummary', 'Not provided')
    } 
    value= inf['BusinessSummary']

    return  st.write(f'Summary {value}')


     

tab1 ,tab2 , tab3 , tab4 = st.tabs(['Company Profile', 'Company Summary', ' Data', 'Compare stocks '])


# tab 1 that will render info
with tab1:

    company_info()

# tab 2 render company summary

with tab2:

    rendersummary()

# Tab3 allow user to display charts of stocks 
with tab3:

    st.sidebar.subheader('Chart Color Selector')
    col1, col2, col3 = st.columns(3)
    chart_type = col1.selectbox("Select Chart Type", ["Candlestick Chart", "Line Chart"], key="tab2_chart_type")
    duration = col2.selectbox('Select Duration', ['None', '1mo', '3mo', '6mo', 'YTD', '1y', '3y', '5y', 'max'], key="tab2_duration")
    time_interval = col3.selectbox("Select Time Interval", ["1d", "1mo", "3mo"], key="tab2_time_interval")
    df =render(data,time_interval, sd ,fd)

    color =st.sidebar.radio('Select Bar color', ('Red', 'Green','Yellow', 'Orange'))

    if color == 'Red':  
            para= 'rgba(255, 0, 0, 0.5)'
    
    elif color == 'Green':
        
            para='rgba(0, 255, 0, 0.5)'

    elif color=='Orange':
            
            para= 'rgba(255, 165, 0, 0.5)'
    else:
         
            para= 'rgba(255, 255, 0, 0.5)'
        
    import plotly.graph_objects as go
    import pandas as pd
    
    
   # To differentiate between selecting the duration and using start/end dates
    if duration == 'None':
        duration = None
    
    # if user selected a ticker 

    if data:
        stock_price = None
    # use duration as parameter
        if duration:
            historical_data = yf.Ticker(data).history(period=duration, interval=time_interval)
            stock_price = pd.DataFrame(historical_data)
            stock_price.reset_index(inplace=True)
    # use interval as parameter
        else:
            stock_price = render(data, time_interval, sd, fd)

         # Show data table
        show_data = st.checkbox("Show Data Table")
    
        if show_data:
             st.write('**Stock Price Data**')
             st.dataframe(stock_price, hide_index=True, use_container_width=True)

         
        if stock_price is not None:
          # dipslay different charts               
            fig = go.Figure()
               # candlesticks chart
            if chart_type == "Candlestick Chart":
                fig.add_trace(go.Candlestick(
                    x=stock_price['Date'],
                    open=stock_price['Open'],
                    high=stock_price['High'],
                    low=stock_price['Low'],
                    close=stock_price['Close'],
                    name='CandleStick',
                    yaxis='y1'
                ))
            else:  # Line Chart
                    fig.add_trace(go.Scatter(
                        x=stock_price['Date'],
                        y=stock_price['Close'], 
                        mode='lines', 
                        name='Close Price',
                        yaxis= 'y1'
                        ))
                    
                # Add volume bar chart
            fig.add_trace(go.Bar(x=stock_price['Date'],
                                     y=stock_price['Volume'],
                                     name='Volume',
                                     yaxis='y2',
                                     marker=dict(color= para)
                                     )
                              )
                
            
            # Update layout based on time interval selected
            fig.update_layout(
                title=f'{data} Stock Price',
                xaxis_title='Date',
                xaxis_rangeslider_visible=False,
                yaxis=dict(title='Close Price', side='left'),
                yaxis2=dict(title='Volume', side='right', overlaying='y'),
                annotations=[
                    dict(
                        text="Select 'CandleStick'/'Close Price' or Volume to display one of them or select both.",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=1.1,
                        y=1.3,
                        bordercolor="#c7c7c7",
                        font=dict(size=10),
                        )
                            ],
                legend=dict(
                        x=0.5,  
                        y=1.25
                           )
                            )


            st.plotly_chart(fig, use_container_width=True)

    


    header = """

        <h1  style='text-align: center;'> Stocks Indicators Mean </h1>
      
    """

    st.markdown(header, unsafe_allow_html= True )

    

    k1 ,k2 , k3 ,k4 = st.columns(4)

    mean = stock_price['High'].mean()
    mean1 = stock_price['Low'].mean()
    mean2 = stock_price['Open'].mean()
    mean3 = stock_price['Close'].mean()
    k1.metric('High Stock Mean',mean)

    k2.metric('Low Stock Mean', mean1)

    k3.metric('Open Stock Mean', mean2)

    k4.metric('Close Stock Mean', mean3)

with tab4:
     
     text = st.text_input(' Enter companty Tickers separated by dash -')
     
     st.subheader('Line Chart comparison between different companies  stocks')

     if text is not None:
         
         li = text.split('-')
         df = yf.download(li , start= sd , end =fd)
         
         st.line_chart(df['Close'])

     

     



