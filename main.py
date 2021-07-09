from IncomeToHousingDataFrame import IncomeToHousingData
import matplotlib.pyplot as plt
import pickle


def main():
    data = IncomeToHousingData()
    idaho_data = data.states.states['ID'].data

    fig, ax = plt.subplots()
    plt.title("Idaho Housing Affordability")
    ax.plot(idaho_data['HousingExpense % of income'], color='blue')
    ax.set_ylabel("Housing Expense as % of income", color='blue')
    ax2 = ax.twinx()
    ax2.plot(idaho_data['MedianHomePrice'], color='grey')
    ax2.set_ylabel("Median Home Price", color='grey')

    plt.show()

    fig.savefig('housing_affordability.jpg',
                format='jpeg',
                dpi=100,
                bbox_inches='tight')

    idaho_data.to_csv('Idaho.csv')

    housing_burden_by_state = data.get_housing_burden_variance()
    pickle.dump(housing_burden_by_state, open('housing_burden_by_state.p', 'wb'))

    # TODO, rotate markers and create custom legend for the highlighted states.
    plt.figure()
    for state in housing_burden_by_state.columns:
        spread = housing_burden_by_state[state].max() - housing_burden_by_state[state].min()
        if spread > 0.15:
            color = 'orange'
        elif housing_burden_by_state[state].min() < 0.14:
            color = 'green'
        elif housing_burden_by_state[state].max() > 0.40:
            color = 'red'
        else:
            color = 'grey'
        plt.plot(housing_burden_by_state.index, housing_burden_by_state[state], color=color, marker='AZ')
    plt.show()





if __name__ == '__main__':
    main()

