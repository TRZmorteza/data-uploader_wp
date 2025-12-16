import pandas as pd
import re

df = pd.read_excel("data.xls")

print("Columns:", df.columns.tolist())

# regex for Persian/English letters + spaces + () + -
pattern = re.compile(r'(\w+(\s+)?)+', re.UNICODE)
# regex for integers only
p = re.compile(r'^\d+$', re.UNICODE)
names = []
p_list = []
car_type=[]
TARGET_COL = "شرح کالا"

for index, row in df.iterrows():
    text = str(row[TARGET_COL]).strip()
    carT = str(row['مدل خودرو']).strip()
    price = str(row['قيمت فروش']).strip()

    if pattern.match(carT):
        car_type.append(carT)
    
    if p.match(price):
        p_list.append(price)
    
    if pattern.match(text):
        names.append(text)

print("\nDetected names:", len(names))
print("\ncar type:", len(car_type))
print("Detected prices:", len(p_list))

# write all names + prices together
with open('res.txt', 'a', encoding='utf-8') as f:
    for name, price,brand in zip(names, p_list,car_type):
        f.write(f"name:{name} , ||price:{price},||brand:{brand}\n")
