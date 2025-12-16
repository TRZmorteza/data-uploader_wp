import pandas as pd
import re

def extract_data(file_path="data.xls"):
    """
    Extracts names, car types (brands), and prices from an Excel file.
    Returns a list of dictionaries: data_to_upload.
    """
    df = pd.read_excel(file_path)
    print("Columns:", df.columns.tolist())

    # regex for Persian/English letters + spaces + () + -
    text_pattern = re.compile(r'(\w+(\s+)?)+', re.UNICODE)
    # regex for integers only (prices)
    number_pattern = re.compile(r'^\d+$', re.UNICODE)

    names = []
    prices = []
    car_types = []

    TARGET_COL = "شرح کالا"

    for index, row in df.iterrows():
        text = str(row[TARGET_COL]).strip()
        carT = str(row['مدل خودرو']).strip()
        price = str(row['قيمت فروش']).strip()

        if text_pattern.match(text):
            names.append(text)

        if text_pattern.match(carT):
            car_types.append(carT)

        if number_pattern.match(price):
            prices.append(price)

    # Make sure all lists have the same length
    min_len = min(len(names), len(prices), len(car_types))
    names = names[:min_len]
    prices = prices[:min_len]
    car_types = car_types[:min_len]

    # Create list of dictionaries
    data_to_upload = [
        {"name": n, "brand": b, "price": p}
        for n, b, p in zip(names, car_types, prices)
    ]

    return data_to_upload


if __name__ == "__main__":
    data = extract_data("data.xls")
    print(f"Total items to upload: {len(data)}")
    if int(input('all:1 or first 5:2\n'))==1:
        for item in data:  # print all
            print(item)
    else:
        for item in data[:5]:  # print first 5 items as preview
            print(item)
