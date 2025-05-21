import wget
import pdfplumber
import json
import os


class DoterraPriceListParser:
    def __init__(self, url, pdf_filename="price-list.pdf", output_filename="products.json"):
        """
        Parameters
        ----------
        url : str
            URL of the PDF file to download and parse
        pdf_filename : str, optional
            Name of the PDF file to store locally. Defaults to "price-list.pdf"
        output_filename : str, optional
            Name of the JSON file to output. Defaults to "products.json"

        Attributes
        ----------
        products : list
            List of product dictionaries
        """

        self.url = url
        self.pdf_filename = pdf_filename
        self.output_filename = output_filename
        self.products = []

    def download_pdf(self):
        print(f"Downloading latest PDF from {self.url}...")
        # Download the file even if it exists
        if os.path.exists(self.pdf_filename):
            os.remove(self.pdf_filename)
        wget.download(self.url, self.pdf_filename)
        print("\nDownload complete.")

    def parse_pdf(self):
        print("Parsing PDF...")
        with pdfplumber.open(self.pdf_filename) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Remove irrelevant rows
                        if row == ['Продукт', 'Единица', 'PV', 'Points', 'Retail (€)', 'Whls (€)']:
                            continue
                        if None in row or len(row) != 6:
                            continue
                        
                        # TODO: move the function outside the loop!
                        def parse_float(value):
                            value = value.strip().replace(",", ".")
                            return None if value in {"-", ""} else float(value)

                        self.products.append({
                            'product': row[0].strip(),
                            'unit': row[1].strip(),
                            'pv': parse_float(row[2]),
                            'points': parse_float(row[3]),
                            'retail': parse_float(row[4]),
                            'wholesale': parse_float(row[5])
                        })
        print(f"Parsed {len(self.products)} products.")

    def save_to_json(self):
        with open(self.output_filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=4)
        print(f"Saved to {self.output_filename}.")

    def run(self):
        self.download_pdf()
        self.parse_pdf()
        self.save_to_json()
