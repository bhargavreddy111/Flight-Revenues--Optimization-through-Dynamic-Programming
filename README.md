# Flight-Revenues--Optimization-through-Dynamic-Programming
For each flight, pricing_function will be run once per (simulated) day to set that day's ticket price. The seats you don't sell today will be available to sell tomorrow, unless the flight leaves that day.
Your pricing_function is run for one flight at a time, and it takes following inputs:

Number of days until the flight (max_days = 150)
Number of seats they have left to sell (max_tickets = 200)

A variable called demand_level that determines how many tickets you can sell at any given price.
The quantity you sell at any price is:

quantity_sold = demand_level - price

Ticket quantities are capped at the number of seats available.
Your function will output the ticket price.
You learn the demand_level for each day at the time you need to make predictions for that day. For all days in the future, you only know demand_level will be drawn from the uniform distribution between 100 and 200. So, for any day in the future, it is equally likely to be each value between 100 and 200.

Kaggle Question
https://www.kaggle.com/dansbecker/airline-price-optimization-micro-challenge

Running Streamlit Demo files
Command line input :


Run the following commands respectively for seeing the results of all the simulations and seeing only best & worst simulation results.
             * streamlit run for_demo.py
              
             * streamlit run v4_fordemo.py


Description:

NO need to input data from external sources.
For loops used in the code will generate the required data
More detailed discussion on the approach followed is mentioned in Documention
