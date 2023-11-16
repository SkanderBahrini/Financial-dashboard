# Financial-dashboard

This project aims to create a financial dashboard containing Yahoo Finance stock information.

In this project, we used many Python libraries such as :

+ Ploltly
+ Pandas
+ Streamlit
+ Yahoo Finance

This project is composed of 4 tabs:

* Tab1: Display company info
* Tab2: Display company summary
* Tab3: Display company chart
* Tab4: Compared between companies' stocks

# ⛔ Important Notice 

If you want to retrieve data directly from Yahoo Finance you will face this problem:

![Capture d'écran 2023-11-14 112302](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/d1f82385-cdb1-4da5-85d9-7538b376d73b)



Yahoo is blocking you and does not allow data retrieval.

# 💡 Solution

To avoid this problem you need to use Yahoo Finance API:

API will provide to Yahoo Finance:

+ User-Agent: This will allow the website to authenticate the user by providing a web browser and it is version and type of operating system used.

  example: Mozilla/5.0 (Windows NT 6.1; Win64; x64)

+ Cookie: A cookie will allow the website to remember the user on each visit

+ Crumb: It is a token that will protect the user from Cross-site forgery which is a cyber attack that will execute a command on behalf of the user. By using this token we will ensure that each command executed comes from a trusted part.

Credit:[ranaroussi] (https://github.com/ranaroussi/yfinance/issues/1729)

# First step:
The client needs to enter company Ticker and the desired interval period.

![info](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/b68919e6-7cf4-4d0a-92de-e830191a68f2)

After entering the desired data the user chooses one of the 4 tabs: 

# Tab1: Company information
This section displays companies' data from phones, sectors of activity, and countries....

![ta1](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/3ad89eaf-f013-4877-ab8f-0b235c63f32c)

# Tab2: Company summary

This section will display a summary of the company:

![tab2](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/ec333e09-b4aa-4e48-bade-4709ffa2c25d)

# Tab3: Display company chart:

This  section is crucial in the app:

It will allow the user to display according to data entered in the desired chart ( Candlestick, Line chart, Bar chart) to display company stocks.

+ Candlestick + Bar charts 

![tab31](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/f01998f2-19bc-4199-b53d-7380c9287f4c)

+ Line + Bar charts
  
![tab32](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/661c7a63-f013-4a88-99fb-8a0ff74c4d6e)

+ Metrics
  
![mean](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/eecad7aa-c67f-4794-8901-d4945c65410a)

PS: The user can use the sidebar to choose the color of the bar chart.

# Tab4: Compare the company's stocks

This section allows the user to enter different Tickers and compare the stocks displayed in the line chart.

![tab](https://github.com/SkanderBahrini/Financial-dashboard/assets/74383561/2158aefd-76a1-423a-ab97-951f02636a5e)



Thank you for your attention!

Happy Coding ;)











