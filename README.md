# 📄 AI-Powered Invoice Extraction System

Automated invoice data extraction system using **OpenAI GPT-4o Vision** and optional OCR for business automation.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Project Overview

Automates invoice data entry for accounting/finance teams:
- **Invoice Image → Structured Data** extraction
- **Batch processing** with statistics generation
- **Sales analytics** by customer & month
- **Automated Excel reports** for business insights

## 🛠 Tech Stack

- **VLM**: OpenAI GPT-4o Vision API
- **OCR**: Tesseract OCR (optional)
- **Language**: Python 3.8+
- **Libraries**: 
  - `openai` (GPT-4o Vision API)
  - `pytesseract` (OCR - optional)
  - `Pillow` (Image processing)
  - `pandas`, `openpyxl` (Data processing)

## 📋 Key Features

### 1. Invoice Information Extraction
- **Basic Info**: Invoice number, issue date, due date
- **Party Details**: Supplier/buyer company name, tax ID, address, contact
- **Line Items**: Description, quantity, unit price, amount
- **Financial**: Subtotal, tax, total amount

### 2. Batch Processing System
- Auto-scan all invoice images in folder
- Sequential processing with progress tracking
- Automatic error logging

### 3. Statistical Analysis
- **Overall Stats**: Total sales, avg/max/min transaction amounts
- **By Customer**: Sales breakdown and percentage by buyer
- **By Month**: Monthly sales trends
- **Excel Reports**: Multi-sheet detailed reports

### 4. VLM + OCR Hybrid (Optional)
- **VLM Primary**: Powerful vision understanding with GPT-4o
- **OCR Support**: Tesseract for small text or complex layouts
- **Flexible**: Works with VLM only if OCR not installed

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/syHong23/ai-invoice-extraction.git
cd ai-invoice-extraction

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Optional: Install Tesseract OCR
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

### 2. API Key Setup

Create `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Get API key from: https://platform.openai.com/api-keys

### 3. Generate Sample Invoices

```bash
python generate_sample_invoices.py
```

This creates 10 sample invoice images in `data/input/`

### 4. Process Invoices

```bash
python process_invoices.py
```

Check results in `data/output/`

## 📁 Project Structure

```
ai-invoice-extraction/
├── src/
│   ├── document_processor.py    # VLM-based processing
│   ├── ocr_handler.py           # Tesseract OCR
│   └── data_extractor.py        # Data conversion & export
├── data/
│   ├── input/                   # Invoice images (invoice_*.png)
│   └── output/                  # Results (JSON, Excel)
├── generate_sample_invoices.py  # Sample invoice generator
├── process_invoices.py          # Batch processing main
├── .env                         # Environment variables (API key)
├── requirements.txt             # Package dependencies
└── README.md
```

## 💡 Usage Examples

### Generate Custom Invoices

```python
from generate_sample_invoices import InvoiceGenerator

generator = InvoiceGenerator(output_dir="data/input")
generator.generate_multiple_invoices(count=10)
```

### Direct API Usage

```python
from document_processor import DocumentProcessor
from src.data_extractor import DataExtractor

# Initialize
doc_processor = DocumentProcessor()
data_extractor = DataExtractor()

# Process invoice
result = doc_processor.process_document(
    image_path="data/input/invoice_001.png",
    document_type="invoice"
)

# Save results
data_extractor.save_invoice_to_excel(result, "invoice_result")
```

### Output Example

```bash
======================================================================
    Invoice Batch Processing System (OpenAI GPT-4o Vision)
======================================================================

[Step 3] Processing Invoices
----------------------------------------------------------------------
  [1/10] Processing: invoice_001.png ✓
  [2/10] Processing: invoice_002.png ✓
  ...

[Step 4] Calculating Statistics
----------------------------------------------------------------------
  📊 Processing Results
    • Total invoices: 10
    • Successful: 10
    • Failed: 0

  💰 Sales Statistics
    • Total sales: $37,873.00
    • Total tax: $3,443.00
    • Average transaction: $3,787.30

  🏢 Top 5 Buyers
    1. XYZ Enterprises: $17,545.00 (46.3%)
    2. Smart Business Group: $13,013.00 (34.4%)
    ...

Processing Complete!
```

## 📊 Output Format

### Excel Report (4 Sheets)

#### 1. All Invoices
| Invoice Number | Issue Date | Supplier | Buyer | Total |
|---|---|---|---|---|
| INV-2024-001 | 2024-01-15 | ABC Corporation | XYZ Enterprises | $16,500 |
| INV-2024-002 | 2024-01-20 | TechSolutions Inc | Global Trading Co | $8,800 |

#### 2. Statistics
| Metric | Value |
|---|---|
| Total Invoices | 10 invoices |
| Total Sales | $378,730.00 |
| Average Transaction | $37,873.00 |

#### 3. By Buyer
| Buyer | Total Sales | Percentage |
|---|---|---|
| XYZ Enterprises | $175,450.00 | 46.3% |
| Smart Business Group | $130,130.00 | 34.4% |

#### 4. By Month
| Month | Sales | Count |
|---|---|---|
| 2025-11 | $103,950.00 | 2 |
| 2025-12 | $169,510.00 | 4 |

### JSON Output

```json
{
  "invoice_number": "INV-2024-001",
  "issue_date": "2024-01-15",
  "due_date": "2024-02-14",
  "supplier": {
    "company_name": "ABC Corporation",
    "tax_id": "123-45-67890",
    "address": "123 Tech Valley Rd, San Francisco, CA 94102",
    "contact": "+1-415-123-4567"
  },
  "buyer": {
    "company_name": "XYZ Enterprises",
    "tax_id": "098-76-54321",
    "address": "111 Commerce St, New York, NY 10001",
    "contact": "+1-212-987-6543"
  },
  "items": [
    {
      "description": "Laptop Computer",
      "quantity": 5,
      "unit_price": 2000,
      "amount": 10000
    }
  ],
  "subtotal": 15000,
  "tax": 1500,
  "total": 16500,
  "currency": "USD"
}
```

## 🔧 Performance

### Processing Speed
- **10 invoices**: ~1-2 minutes (with API calls)
- **Cost**: ~$0.10-0.20 for 10 invoices (GPT-4o-mini)

### Accuracy
- **Invoice extraction**: 95%+ accuracy on clear images
- **VLM advantage**: Understands context, handles various layouts

## 📈 Future Improvements

- [ ] PDF invoice support (direct processing)
- [ ] Web interface (Streamlit/Gradio)
- [ ] Automatic invoice template detection
- [ ] Email attachment auto-processing
- [ ] ERP system integration API
- [ ] Duplicate invoice detection
- [ ] Multi-language invoice support

## 🎯 Use Cases

### 1. Accounting Team Automation
- Auto-process invoices from email
- Generate Excel for accounting software
- Month-end reconciliation reports

### 2. Procurement Data Management
- Bulk archive purchase invoices
- Track spending by supplier
- Budget vs. actual analysis

### 3. Sales Analytics
- Auto-aggregate issued invoices
- Customer sales breakdown
- Monthly/quarterly sales trends

## 🐛 Troubleshooting

### API Key Not Found
```bash
# Check .env file exists
type .env

# Verify OPENAI_API_KEY is set
```

### Tesseract Not Found (Optional)
```bash
# Set path in .env (Windows)
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Rate Limiting
```python
# Add delay for large batches
import time
for image in images:
    result = process_document(image)
    time.sleep(1)
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 👤 Author

**SY Hong**
- GitHub: [@syHong23](https://github.com/syHong23)
- Email: sungyeon.hong17@gmail.com
- Portfolio: [ai-invoice-extraction](https://github.com/syHong23/ai-invoice-extraction)

## 🙏 Acknowledgments

- OpenAI GPT-4o Vision API
- Tesseract OCR Project
- Python Community

## 📮 Contributing

Issues and pull requests are welcome!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Built with ❤️ for automated business workflows**
