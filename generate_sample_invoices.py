"""
Invoice Sample Image Generator
Automatically generates realistic invoice images using Python PIL.
"""

from PIL import Image, ImageDraw, ImageFont
import random
from datetime import datetime, timedelta
import os


class InvoiceGenerator:
    """Invoice image generator class"""
    
    def __init__(self, output_dir="data/input"):
        """
        Initialize the generator
        
        Args:
            output_dir: Output directory path
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Image settings
        self.width = 800
        self.height = 1100
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.header_color = (41, 128, 185)
        self.line_color = (200, 200, 200)
        
        # Sample data
        self.suppliers = [
            {"name": "ABC Corporation", "tax_id": "123-45-67890", 
             "address": "123 Tech Valley Rd, San Francisco, CA 94102", "tel": "+1-415-123-4567"},
            {"name": "TechSolutions Inc", "tax_id": "234-56-78901", 
             "address": "456 Innovation Ave, Austin, TX 78701", "tel": "+1-512-234-5678"},
            {"name": "Digital Systems Ltd", "tax_id": "345-67-89012", 
             "address": "789 Enterprise Blvd, Seattle, WA 98101", "tel": "+1-206-345-6789"},
        ]
        
        self.buyers = [
            {"name": "XYZ Enterprises", "tax_id": "098-76-54321", 
             "address": "111 Commerce St, New York, NY 10001", "tel": "+1-212-987-6543"},
            {"name": "Global Trading Co", "tax_id": "987-65-43210", 
             "address": "222 Market Plaza, Chicago, IL 60601", "tel": "+1-312-876-5432"},
            {"name": "Smart Business Group", "tax_id": "876-54-32109", 
             "address": "333 Financial Ave, Boston, MA 02101", "tel": "+1-617-765-4321"},
            {"name": "Future Technologies", "tax_id": "765-43-21098", 
             "address": "444 Silicon Way, San Jose, CA 95101", "tel": "+1-408-654-3210"},
        ]
        
        self.products = [
            "Laptop Computer", "Monitor", "Keyboard", "Mouse", "Printer",
            "Software License", "Server Equipment", "Network Switch",
            "Office Desk", "Office Chair", "Consulting Service", "Maintenance Service"
        ]
    
    def generate_invoice_data(self, invoice_number):
        """
        Generate invoice data
        
        Args:
            invoice_number: Invoice number
            
        Returns:
            Invoice data dictionary
        """
        # Generate date (within last 6 months)
        days_ago = random.randint(0, 180)
        issue_date = datetime.now() - timedelta(days=days_ago)
        due_date = issue_date + timedelta(days=30)
        
        # Select parties
        supplier = random.choice(self.suppliers)
        buyer = random.choice(self.buyers)
        
        # Generate items (2-5 items)
        num_items = random.randint(2, 5)
        items = []
        
        for _ in range(num_items):
            product = random.choice(self.products)
            quantity = random.randint(1, 20)
            unit_price = random.choice([100, 200, 300, 500, 1000, 
                                       1500, 2000, 5000, 10000])
            amount = quantity * unit_price
            
            items.append({
                "description": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "amount": amount
            })
        
        # Calculate totals
        subtotal = sum(item["amount"] for item in items)
        tax = int(subtotal * 0.1)  # 10% tax
        total = subtotal + tax
        
        return {
            "invoice_number": f"INV-2024-{invoice_number:03d}",
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "supplier": supplier,
            "buyer": buyer,
            "items": items,
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        }
    
    def draw_invoice(self, data, filename):
        """
        Draw invoice image
        
        Args:
            data: Invoice data
            filename: Output filename
        """
        # Create image
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Font settings (default font)
        try:
            # Windows
            font_large = ImageFont.truetype("arial.ttf", 32)
            font_medium = ImageFont.truetype("arial.ttf", 20)
            font_small = ImageFont.truetype("arial.ttf", 14)
            font_tiny = ImageFont.truetype("arial.ttf", 12)
        except:
            try:
                # Mac
                font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
                font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
                font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
                font_tiny = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
            except:
                # Default font
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
                font_tiny = ImageFont.load_default()
        
        y = 30
        
        # Header
        draw.rectangle([30, y, self.width - 30, y + 60], fill=self.header_color)
        draw.text((self.width // 2, y + 30), "TAX INVOICE", 
                 fill=(255, 255, 255), font=font_large, anchor="mm")
        y += 80
        
        # Invoice number and dates
        draw.text((50, y), f"Invoice #: {data['invoice_number']}", 
                 fill=self.text_color, font=font_medium)
        draw.text((50, y + 30), f"Issue Date: {data['issue_date']}", 
                 fill=self.text_color, font=font_small)
        draw.text((50, y + 50), f"Due Date: {data['due_date']}", 
                 fill=self.text_color, font=font_small)
        y += 90
        
        # Separator
        draw.line([30, y, self.width - 30, y], fill=self.line_color, width=2)
        y += 20
        
        # Supplier information
        draw.text((50, y), "[SUPPLIER]", fill=self.header_color, font=font_medium)
        y += 30
        supplier = data['supplier']
        draw.text((50, y), f"Company: {supplier['name']}", 
                 fill=self.text_color, font=font_small)
        y += 25
        draw.text((50, y), f"Tax ID: {supplier['tax_id']}", 
                 fill=self.text_color, font=font_tiny)
        y += 20
        draw.text((50, y), f"Address: {supplier['address']}", 
                 fill=self.text_color, font=font_tiny)
        y += 20
        draw.text((50, y), f"Tel: {supplier['tel']}", 
                 fill=self.text_color, font=font_tiny)
        y += 35
        
        # Buyer information
        draw.text((50, y), "[BUYER]", fill=self.header_color, font=font_medium)
        y += 30
        buyer = data['buyer']
        draw.text((50, y), f"Company: {buyer['name']}", 
                 fill=self.text_color, font=font_small)
        y += 25
        draw.text((50, y), f"Tax ID: {buyer['tax_id']}", 
                 fill=self.text_color, font=font_tiny)
        y += 20
        draw.text((50, y), f"Address: {buyer['address']}", 
                 fill=self.text_color, font=font_tiny)
        y += 20
        draw.text((50, y), f"Tel: {buyer['tel']}", 
                 fill=self.text_color, font=font_tiny)
        y += 35
        
        # Separator
        draw.line([30, y, self.width - 30, y], fill=self.line_color, width=2)
        y += 20
        
        # Items table header
        draw.rectangle([30, y, self.width - 30, y + 30], fill=(240, 240, 240))
        draw.text((50, y + 15), "Description", fill=self.text_color, font=font_small, anchor="lm")
        draw.text((400, y + 15), "Qty", fill=self.text_color, font=font_small, anchor="mm")
        draw.text((520, y + 15), "Unit Price", fill=self.text_color, font=font_small, anchor="mm")
        draw.text((680, y + 15), "Amount", fill=self.text_color, font=font_small, anchor="mm")
        y += 30
        
        # Items list
        for item in data['items']:
            draw.line([30, y, self.width - 30, y], fill=self.line_color, width=1)
            y += 10
            
            # Item description (truncate if too long)
            desc = item['description']
            if len(desc) > 20:
                desc = desc[:20] + "..."
            
            draw.text((50, y), desc, fill=self.text_color, font=font_tiny)
            draw.text((400, y), f"{item['quantity']:,}", 
                     fill=self.text_color, font=font_tiny, anchor="mm")
            draw.text((520, y), f"${item['unit_price']:,}", 
                     fill=self.text_color, font=font_tiny, anchor="mm")
            draw.text((680, y), f"${item['amount']:,}", 
                     fill=self.text_color, font=font_tiny, anchor="mm")
            y += 25
        
        # Bottom separator
        draw.line([30, y, self.width - 30, y], fill=self.line_color, width=2)
        y += 30
        
        # Totals
        draw.text((450, y), "Subtotal:", fill=self.text_color, font=font_small)
        draw.text((680, y), f"${data['subtotal']:,}", 
                 fill=self.text_color, font=font_small, anchor="mm")
        y += 30
        
        draw.text((450, y), "Tax (10%):", fill=self.text_color, font=font_small)
        draw.text((680, y), f"${data['tax']:,}", 
                 fill=self.text_color, font=font_small, anchor="mm")
        y += 30
        
        # Total (emphasized)
        draw.rectangle([430, y - 5, self.width - 30, y + 35], 
                      outline=self.header_color, width=2)
        draw.text((450, y + 15), "TOTAL:", fill=self.header_color, 
                 font=font_medium, anchor="lm")
        draw.text((680, y + 15), f"${data['total']:,}", 
                 fill=self.header_color, font=font_medium, anchor="mm")
        
        # Save image
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath, quality=95)
        print(f"Generated: {filepath}")
        
        return filepath
    
    def generate_multiple_invoices(self, count=10):
        """
        Generate multiple invoices
        
        Args:
            count: Number of invoices to generate
            
        Returns:
            List of generated file paths
        """
        print(f"\n{'='*60}")
        print(f"Generating Invoice Samples... (Total: {count})")
        print(f"{'='*60}\n")
        
        filepaths = []
        
        for i in range(1, count + 1):
            # Generate data
            data = self.generate_invoice_data(i)
            
            # Generate image
            filename = f"invoice_{i:03d}.png"
            filepath = self.draw_invoice(data, filename)
            filepaths.append(filepath)
            
            # Print brief info
            print(f"  {i:2d}. {data['invoice_number']} - "
                  f"{data['buyer']['name']} - "
                  f"${data['total']:,}")
        
        print(f"\n{'='*60}")
        print(f"Generation complete! Check {self.output_dir} folder.")
        print(f"{'='*60}\n")
        
        return filepaths


def main():
    """Main function"""
    # Initialize generator
    generator = InvoiceGenerator(output_dir="data/input")
    
    # Generate 10 invoices
    filepaths = generator.generate_multiple_invoices(count=10)
    
    # Statistics
    print("Generated Invoice List:")
    for i, path in enumerate(filepaths, 1):
        print(f"  {i}. {os.path.basename(path)}")


if __name__ == "__main__":
    main()
