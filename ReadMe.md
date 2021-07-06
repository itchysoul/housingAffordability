Rough TODOs and instructions

run from main.py. Currently just plots some sample data for Idaho, but this pulls the measures for all 50 states.

TODO: use the pickled data for testing



Grouped by State and PCA

Household Income / ( Median Home Price * 30-year Mortgage Rate * Formula for Monthly Mortgage Payments * 12 )

r = monthly interest rate = 30-year mortgage rate / 12
r(1+r)^(30*12)/((1+r)^(30*12)-1)

R(1+R)^30 / ((1+R)^30-1)

P = Median Home Price
H = Median Household Income
M = Median Mortgage Payments (yearly)
R = 30-year Mortgage Rate

M = P*(R*(1*R)^30 / ((1+R)^30-1))

HousingExpense = H / M


DataFeeds Needed:
30-year mortage rate (USA)
    https://fred.stlouisfed.org/series/MORTGAGE30US 1971

Median Home Price (by state)
    https://fred.stlouisfed.org/series/MEDLISPRIID eg 2017

Household Income (by state)
    https://fred.stlouisfed.org/series/MEHOINUSIDA646N eg 1984

    

Single measure: variance in Housing Expense as Share of Income

