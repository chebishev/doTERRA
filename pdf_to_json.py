import pdfplumber
import json

products = []
with pdfplumber.open("price-list.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if row == ['Продукт', 'Единица', 'PV', 'Points', 'Retail (€)', 'Whls (€)']:
                    continue
                if None in row:
                    continue
                if len(row) == 6:
                    products.append({
                        'product': row[0],
                        'unit': row[1],
                        'pv': row[2],
                        'points': row[3],
                        'retail': row[4],
                        'wholesale': row[5]
                    })

with open('products.json', 'w') as f:
    json.dump(products, f, indent=4)
