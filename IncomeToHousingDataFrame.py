
import pickle
import pandas
import pandas as pd
from fredapi import Fred
from StatesDataObject import States
from auth import Auth

fred = Fred(api_key=Auth.fred_key)


class IncomeToHousingData:
    states = None
    mortgage_rates = None

    def __init__(self):
        self.states = States()
        self.mortgage_rates = fred.get_series('MORTGAGE30US')
        self.mortgage_rates = pd.DataFrame(self.mortgage_rates, columns=['30yrRate'])
        self.mortgage_rates['30yrRate'] = self.mortgage_rates['30yrRate'] / 100
        self.populate_state_mortgage_rates()
        pickle.dump(self.states, open('populatedStates.p', 'wb'))
        self.states.calculate_housing_expense()

    def populate_state_mortgage_rates(self):
        self.states.set_mortgage_rates(self.mortgage_rates)

    def get_housing_burden_variance(self):
        cols = {}
        for state in self.states.states.values():
            cols[state.abbrev] = state.data['HousingExpense % of income']
        state_expense_data = pd.DataFrame(cols)
        return state_expense_data

