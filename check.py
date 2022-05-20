from datetime import date

if __name__ == "__main__":
    today = date.today()
    oldMacList = pd.read_csv(today + '.csv')
    dictionary = pd.read_csv('./InfoWeb/localStorage.csv')
    print(macList)
    print("---------------  MERGE ----------------")
    result = pd.merge(dictionary, macList, on='ip')
    print(result)