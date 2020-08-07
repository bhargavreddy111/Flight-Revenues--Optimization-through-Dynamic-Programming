
import streamlit as st
import numpy as np
from numpy.random import uniform, seed
from numpy import floor
from collections import namedtuple

def _tickets_sold(p, demand_level, max_qty):
    quantity_demanded = floor(max(0, demand_level-p))
    return min(quantity_demanded, max_qty)

def simulate_revenue(days_left, tickets_left, pricing_function, rev_to_date=0, demand_level_min=100, demand_level_max=200, verbose=False):
    if (days_left == 0) or (tickets_left == 0):
        if verbose:
            if (days_left == 0):
                print("The flight took off today. ")
            if (tickets_left == 0):
                print("This flight is booked full.")
            print("Total Revenue: ${:.0f}".format(rev_to_date))
        return rev_to_date
    else:
        demand_level = uniform(demand_level_min, demand_level_max)
        p = pricing_function(days_left, tickets_left, demand_level)
        q = _tickets_sold(p, demand_level, tickets_left)
        st.write("{:.0f} days before flight: "
                "Started with {:.0f} seats. "
                "Demand level: {:.0f}. "
                "Price set to ${:.0f}. "
                "Sold {:.0f} tickets. "
                "Daily revenue is {:.0f}. Total revenue-to-date is {:.0f}. "
                "{:.0f} seats remaining".format(days_left, tickets_left, demand_level, p, q, p*q, p*q+rev_to_date, tickets_left-q))
        return simulate_revenue(days_left = days_left-1,
                          tickets_left = tickets_left-q,
                          pricing_function=pricing_function,
                          rev_to_date=rev_to_date + p * q,
                          demand_level_min=demand_level_min,
                          demand_level_max=demand_level_max,
                          verbose=verbose)



st.markdown("# Price Optimization - Flight Revenues")
n_demand_levels = 11
min_demand_level = 100
max_demand_level = 200
demand_levels = np.linspace(min_demand_level, max_demand_level, n_demand_levels)

max_tickets = 200
max_days = 90
st.sidebar.subheader("Minimum price to be maintained")
min_price = st.sidebar.number_input('Enter the minimum ticket price', min_value=20, max_value=200, value=20)

# Q indices are: n_sold in day, tickets_left to start day, demand_level, days_left
Q = np.zeros([max_tickets, max_tickets, n_demand_levels, max_days])
# V indices are: n_left and n_days
V = np.zeros([max_tickets, max_days])

#%%
@st.cache
def for_loop():
    for tickets_left in range(max_tickets):
        for tickets_sold in range(tickets_left+1): # add 1 to offset 0 indexing. Allow selling all tickets
            for demand_index, demand_level in enumerate(demand_levels):
                # Never set negative prices
                price = max(demand_level - tickets_sold, min_price)
                Q[tickets_sold, tickets_left, demand_index, 0] = price * tickets_sold
        # For each demand_level, choose the optimum number to sell. Output of this is array .of size n_demand_levels
        revenue_from_best_quantity_at_each_demand_level = Q[:, tickets_left, :, 0].max(axis=0)
        # take the average, since we don't know demand level ahead of time and all are equally likely
        V[tickets_left, 0] = revenue_from_best_quantity_at_each_demand_level.mean()

    #%%
    for days_left in range(1, max_days):
        for tickets_left in range(max_tickets):
            for tickets_sold in range(tickets_left):
                for demand_index, demand_level in enumerate(demand_levels):
                    price = max(demand_level - tickets_sold, min_price)
                    rev_today = price * tickets_sold
                    Q[tickets_sold, tickets_left, demand_index, days_left] = rev_today + V[tickets_left-tickets_sold, days_left-1]
            expected_total_rev_from_best_quantity_at_each_demand_level = Q[:, tickets_left, :, days_left].max(axis=0)
            V[tickets_left, days_left] = expected_total_rev_from_best_quantity_at_each_demand_level.mean()


    return Q



def main():

    st.sidebar.subheader("Days left for the flight to take off")
    days_rmng= st.sidebar.number_input('Bookings start only 90 days before take off, enter any number between 0 to 90', min_value=0, max_value=90, value=0)
    st.sidebar.subheader("Tickets left for booking")
    tkts_rmng= st.sidebar.number_input('Enter a number, this cant exceed maximum capacity of plane which is 200',min_value=0, max_value=200, value=0)
    if st.button("RUN"):
        arr=for_loop()

        def pricing_function1(days_left, tickets_left, demand_level):
            demand_level_index = np.abs(demand_level - demand_levels).argmin()
            day_index = days_left - 1  # arrays are 0 indexed
            tickets_index = int(tickets_left)  # in case it comes in as float, but need to index with it
            relevant_Q_vals = arr[:, tickets_index, demand_level_index, day_index]
            desired_quantity = relevant_Q_vals.argmax()  # offset 0 indexing
            price = max(demand_level - desired_quantity, min_price)
            return price

        def score_me(pricing_function, sims_per_scenario=5):
            seed(0)
            Scenario = namedtuple('Scenario', 'n_days n_tickets')
            # x=st.textbox()
            s = Scenario(n_days=days_rmng, n_tickets=tkts_rmng)

            scenario_score = sum(simulate_revenue(s.n_days, s.n_tickets, pricing_function)
                                 for _ in range(sims_per_scenario)) / sims_per_scenario
            st.subheader("Ran {:.0f} flights starting {:.0f} days before flight with {:.0f} tickets. "
                  "Average revenue: ${:.0f}".format(sims_per_scenario,
                                                    s.n_days,
                                                    s.n_tickets,
                                                    scenario_score))
            return scenario_score

        score_me(pricing_function1)

#%%

main()