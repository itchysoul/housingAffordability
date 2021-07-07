from IncomeToHousingDataFrame import IncomeToHousingData
import matplotlib.pyplot as plt


def main():
    data = IncomeToHousingData()
    idaho_data = data.states.states['ID'].data

    fig, ax = plt.subplots()
    plt.title("Idaho Housing Affordability")
    ax.plot(idaho_data['HousingExpense % of income'], color='blue')
    ax.set_ylabel("Housing Expense as % of income", color='black')
    ax.plot(idaho_data['Revised HousingExpense % of income'], color='red')

    plt.show()

    fig.savefig('housing_affordability40Year.jpg',
                format='jpeg',
                dpi=100,
                bbox_inches='tight')

    idaho_data.to_csv('Idaho.csv')


if __name__ == '__main__':
    main()

