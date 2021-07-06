from IncomeToHousingDataFrame import IncomeToHousingData
import matplotlib.pyplot as plt


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

if __name__ == '__main__':
    main()
