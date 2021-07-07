import pandas as pd
from fredapi import Fred
from state_abbreviations import state_codes
from auth import Auth
from concurrent.futures import ThreadPoolExecutor


fred = Fred(api_key=Auth.fred_key)


class State:
    median_home_prices = None
    median_household_incomes = None
    mortgage_rates = None
    abbrev = None
    data: pd.DataFrame = pd.DataFrame()

    def __init__(self, abbrev):
        self.abbrev = abbrev

    def __repr__(self):
        return f'{self.abbrev}_prices:{len(self.median_home_prices)}_incomes:{len(self.median_household_incomes)}'

    def fetch_home_prices(self):
        self.median_home_prices = fred.get_series(f'MEDLISPRI{self.abbrev}')
        self.median_home_prices = pd.DataFrame(self.median_home_prices, columns=['MedianHomePrice'])

    def fetch_income(self):
        self.median_household_incomes = fred.get_series(f'MEHOINUS{self.abbrev}A646N')
        self.median_household_incomes = pd.DataFrame(self.median_household_incomes, columns=['MedianIncome'])

    def set_mortgage_rates(self, mortgage_rates: pd.DataFrame):
        self.mortgage_rates = mortgage_rates

    def build_raw_data_frame(self):
        assert self.mortgage_rates is not None
        assert self.median_household_incomes is not None
        assert self.median_home_prices is not None

        self.median_household_incomes = self.median_household_incomes.resample('1d').interpolate('linear')

        self.data = pd.merge_asof(self.median_home_prices, self.median_household_incomes,
                                  left_index=True, right_index=True,
                                  tolerance=pd.Timedelta(value=32, unit='days'))
        self.data = pd.merge_asof(self.data, self.mortgage_rates,
                                  left_index=True, right_index=True,
                                  tolerance=pd.Timedelta(value=26, unit='days'))
        self.data.loc[:, 'MedianIncome'].interpolate(method='spline', order=1, limit_direction='both', inplace=True)


    def calculate_housing_expense(self):
        self.build_raw_data_frame()
        self.data['HousingExpense $'] = self.data['MedianHomePrice']
        self.data['HousingExpense $'] *= self.data['30yrRate'] * (1 + self.data['30yrRate']) ** 30
        self.data['HousingExpense $'] /= (1 + self.data['30yrRate']) ** 30 - 1
        self.data['HousingExpense % of income'] = self.data['HousingExpense $'] / self.data['MedianIncome']


class States:
    states = {}

    def __init__(self):
        for state in state_codes:
            self.states[state] = State(state)
        self.populate_income_home_price_ratio_data()

    def __repr__(self):
        return f'{len(self.states)} states'

    @staticmethod
    def _fetch_data(state):
        state.fetch_home_prices()
        state.fetch_income()
        print(f'{state.abbrev} populated')

    def populate_income_home_price_ratio_data(self):
        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(self._fetch_data, self.states.values())

    def set_mortgage_rates(self, mortgage_rates: pd.DataFrame):
        for state in self.states.values():
            state.set_mortgage_rates(mortgage_rates)

    def calculate_housing_expense(self):
        for state in self.states.values():
            state.calculate_housing_expense()