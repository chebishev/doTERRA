import wget
import pdfplumber
import json
import os
import re


class DoterraPriceListParser:
    def __init__(self, url, pdf_filename="price-list.pdf", output_filename="products.json"):
        """
        Initialize a DoterraPriceListParser object.

        :param url: The URL to download the PDF from.
        :param pdf_filename: The name of the PDF file to download. Defaults to 'price-list.pdf'.
        :param output_filename: The name of the JSON file to output. Defaults to 'products.json'.
        :return: None
        """

        self.url = url
        self.pdf_filename = pdf_filename
        self.output_filename = output_filename
        self.products = []

    def download_pdf(self):
        """
        Downloads the latest PDF from the specified URL.

        If a file with the same name already exists, it is removed to ensure 
        the latest version is downloaded. The PDF is downloaded to the local 
        system using the provided URL and saved with the specified filename.
        """

        print(f"Downloading latest PDF from {self.url}...")
        if os.path.exists(self.pdf_filename):
            os.remove(self.pdf_filename)  # Always fetch latest version
        wget.download(self.url, self.pdf_filename)
        print("\nDownload complete.")

    @staticmethod
    def clean_name(name):
        """Clean a product name by removing trademark and registered symbols, and
        normalizing unusual characters."""

        name = re.sub(r"[™®]", "", name)
        name = name.replace("ō", "o").replace("–", "-")
        name = name.replace("\n", " ")
        return name.strip()

    @staticmethod
    def parse_float(value):
        """Convert numeric strings to float, normalizing separators and handling empty strings."""

        value = value.strip().replace(",", ".")
        return None if value in {"-", ""} else float(value)

    @staticmethod
    def normalize_unit(unit):
        # Ensure number and unit are separated by a space
        unit = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", unit)
        unit = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", unit)
        return " ".join(unit.split())

    def parse_pdf(self):
        print("Parsing PDF...")
        current_context = None

        with pdfplumber.open(self.pdf_filename) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Skip header
                        if row == ['Продукт', 'Единица', 'PV', 'Points', 'Retail (€)', 'Whls (€)']:
                            continue

                        if row is None or len(row) != 6:
                            # Detect section headers (context)
                            if row and any("Pack" in cell or "Enrolment" in cell or "Kit" in cell for cell in row if cell):
                                context_candidates = [cell.strip() for cell in row if cell and any(c.isalpha() for c in cell)]
                                if context_candidates:
                                    current_context = context_candidates[0]
                            continue

                        # Skip rows with missing mandatory fields
                        if row[0] is None or row[1] is None:
                            continue

                        product_data = {
                            'product': self.clean_name(row[0]),
                            'unit': self.normalize_unit(row[1]),
                            'pv': self.parse_float(row[2]),
                            'points': self.parse_float(row[3]),
                            'retail': self.parse_float(row[4]),
                            'wholesale': self.parse_float(row[5]),
                        }

                        if current_context:
                            product_data['context'] = current_context

                        self.products.append(product_data)


        print(f"Parsed {len(self.products)} products.")

    def save_to_json(self):
        """
        Saves the parsed products to a JSON file.

        The file is written with UTF-8 encoding and indentation of 4 spaces.
        """

        with open(self.output_filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=4)
        print(f"Saved to {self.output_filename}.")

    def run(self):
        """
        Downloads the price list PDF, parses it and saves the products to a JSON file.
        
        This method calls download_pdf, parse_pdf and save_to_json in sequence.
        """

        self.download_pdf()
        self.parse_pdf()
        self.save_to_json()



if __name__ == "__main__":
    # Create an instance of the class with default pdf_filename: "price-list.pdf" and output_filename: "products.json"
    parser = DoterraPriceListParser(
        url="https://media.doterra.com/bg/bg/forms/price-list.pdf"
    )
    parser.run()
