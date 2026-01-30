"""
Batch Invoice Processing with OpenAI GPT-4o Vision
Processes multiple invoice images and generates sales statistics.
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import glob
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Use OpenAI DocumentProcessor
from document_processor import DocumentProcessor
from src.data_extractor import DataExtractor


def process_single_invoice(image_path: str, doc_processor):
    """
    Process a single invoice
    
    Args:
        image_path: Invoice image path
        doc_processor: DocumentProcessor instance
        
    Returns:
        Extracted invoice data
    """
    print(f"  Processing: {os.path.basename(image_path)}", end="")
    
    invoice_data = doc_processor.process_document(
        image_path=image_path,
        document_type="invoice",
        ocr_handler=None
    )
    
    if "error" not in invoice_data:
        print(f" ✓")
    else:
        print(f" ✗ Error")
    
    return invoice_data


def calculate_statistics(invoices: list) -> dict:
    """
    Calculate invoice statistics
    
    Args:
        invoices: List of invoice data
        
    Returns:
        Statistics dictionary
    """
    if not invoices:
        return {}
    
    # Basic statistics
    total_amount = sum(inv.get('total', 0) for inv in invoices)
    total_tax = sum(inv.get('tax', 0) for inv in invoices)
    avg_amount = total_amount / len(invoices) if len(invoices) > 0 else 0
    
    # Statistics by buyer
    buyer_stats = {}
    for inv in invoices:
        buyer_name = inv.get('buyer', {}).get('company_name', 'Unknown')
        buyer_stats[buyer_name] = buyer_stats.get(buyer_name, 0) + inv.get('total', 0)
    
    # Monthly statistics
    monthly_stats = {}
    for inv in invoices:
        issue_date = inv.get('issue_date', '')
        if issue_date:
            try:
                month = issue_date[:7]  # YYYY-MM
                monthly_stats[month] = monthly_stats.get(month, 0) + inv.get('total', 0)
            except:
                pass
    
    return {
        'total_invoices': len(invoices),
        'total_amount': total_amount,
        'total_tax': total_tax,
        'avg_amount': avg_amount,
        'max_amount': max((inv.get('total', 0) for inv in invoices), default=0),
        'min_amount': min((inv.get('total', 0) for inv in invoices), default=0),
        'buyer_stats': buyer_stats,
        'monthly_stats': monthly_stats
    }


def create_summary_excel(invoices: list, stats: dict, output_path: str):
    """
    Create summary Excel file
    
    Args:
        invoices: List of invoice data
        stats: Statistics information
        output_path: Output file path
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # 1. All invoices list
        invoice_list = []
        for inv in invoices:
            invoice_list.append({
                'Invoice Number': inv.get('invoice_number', ''),
                'Issue Date': inv.get('issue_date', ''),
                'Due Date': inv.get('due_date', ''),
                'Supplier': inv.get('supplier', {}).get('company_name', ''),
                'Buyer': inv.get('buyer', {}).get('company_name', ''),
                'Subtotal': inv.get('subtotal', 0),
                'Tax': inv.get('tax', 0),
                'Total': inv.get('total', 0),
                'Currency': inv.get('currency', 'USD')
            })
        
        df_invoices = pd.DataFrame(invoice_list)
        df_invoices.to_excel(writer, sheet_name='All Invoices', index=False)
        
        # 2. Overall statistics
        stats_data = {
            'Metric': [
                'Total Invoices',
                'Total Sales',
                'Total Tax',
                'Average Transaction',
                'Highest Transaction',
                'Lowest Transaction'
            ],
            'Value': [
                f"{stats['total_invoices']} invoices",
                f"${stats['total_amount']:,.2f}",
                f"${stats['total_tax']:,.2f}",
                f"${stats['avg_amount']:,.2f}",
                f"${stats['max_amount']:,.2f}",
                f"${stats['min_amount']:,.2f}"
            ]
        }
        df_stats = pd.DataFrame(stats_data)
        df_stats.to_excel(writer, sheet_name='Statistics', index=False)
        
        # 3. Statistics by buyer
        buyer_data = []
        for buyer, amount in sorted(stats['buyer_stats'].items(), 
                                    key=lambda x: x[1], reverse=True):
            buyer_data.append({
                'Buyer': buyer,
                'Total Sales': amount,
                'Percentage': round(amount / stats['total_amount'] * 100, 2) if stats['total_amount'] > 0 else 0
            })
        
        df_buyers = pd.DataFrame(buyer_data)
        df_buyers.to_excel(writer, sheet_name='By Buyer', index=False)
        
        # 4. Monthly statistics
        monthly_data = []
        for month, amount in sorted(stats['monthly_stats'].items()):
            monthly_data.append({
                'Month': month,
                'Sales': amount,
                'Count': sum(1 for inv in invoices 
                           if inv.get('issue_date', '').startswith(month))
            })
        
        if monthly_data:
            df_monthly = pd.DataFrame(monthly_data)
            df_monthly.to_excel(writer, sheet_name='By Month', index=False)
    
    print(f"\nSummary report generated: {output_path}")


def main():
    """Main function"""
    # Load environment variables
    load_dotenv()
    
    print("=" * 70)
    print("    Invoice Batch Processing System (OpenAI GPT-4o Vision)")
    print("=" * 70)
    
    # 1. Initialize handlers
    print("\n[Step 1] System Initialization")
    print("-" * 70)
    
    try:
        doc_processor = DocumentProcessor()
        print(f"  ✓ OpenAI GPT-4o Vision processor initialized (Model: {doc_processor.model})")
    except Exception as e:
        print(f"  ✗ Failed to initialize: {e}")
        print("\nMake sure OPENAI_API_KEY is set in .env file!")
        return
    
    data_extractor = DataExtractor()
    print("  ✓ Data extractor initialized")
    
    # 2. Search for invoice images
    print("\n[Step 2] Searching for Invoice Images")
    print("-" * 70)
    
    invoice_pattern = "data/input/invoice*.png"
    invoice_images = glob.glob(invoice_pattern)
    
    if not invoice_images:
        print("  ✗ No invoice images found.")
        print("\nRun this command to generate sample invoices:")
        print("  python generate_sample_invoices.py")
        return
    
    invoice_images.sort()
    print(f"  ✓ Found {len(invoice_images)} invoices")
    
    # 3. Batch process invoices
    print("\n[Step 3] Processing Invoices with GPT-4o Vision")
    print("-" * 70)
    
    all_invoices = []
    failed_count = 0
    
    for i, image_path in enumerate(invoice_images, 1):
        print(f"  [{i}/{len(invoice_images)}] ", end="")
        
        invoice_data = process_single_invoice(image_path, doc_processor)
        
        if "error" not in invoice_data:
            all_invoices.append(invoice_data)
            
            # Save JSON
            data_extractor.save_as_json(
                invoice_data, 
                f"invoice_{i:03d}"
            )
        else:
            failed_count += 1
            print(f"    Error detail: {invoice_data.get('error', 'Unknown')}")
    
    # 4. Calculate statistics
    print("\n[Step 4] Calculating Statistics")
    print("-" * 70)
    
    if not all_invoices:
        print("  ✗ No invoices processed successfully.")
        return
    
    stats = calculate_statistics(all_invoices)
    
    print(f"\n  📊 Processing Results")
    print(f"    • Total invoices: {stats['total_invoices']}")
    print(f"    • Successful: {len(all_invoices)}")
    print(f"    • Failed: {failed_count}")
    
    print(f"\n  💰 Sales Statistics")
    print(f"    • Total sales: ${stats['total_amount']:,.2f}")
    print(f"    • Total tax: ${stats['total_tax']:,.2f}")
    print(f"    • Average transaction: ${stats['avg_amount']:,.2f}")
    print(f"    • Highest transaction: ${stats['max_amount']:,.2f}")
    print(f"    • Lowest transaction: ${stats['min_amount']:,.2f}")
    
    print(f"\n  🏢 Top 5 Buyers")
    for i, (buyer, amount) in enumerate(
        sorted(stats['buyer_stats'].items(), 
               key=lambda x: x[1], reverse=True)[:5], 1
    ):
        percentage = (amount / stats['total_amount'] * 100) if stats['total_amount'] > 0 else 0
        print(f"    {i}. {buyer}: ${amount:,.2f} ({percentage:.1f}%)")
    
    if stats['monthly_stats']:
        print(f"\n  📅 Monthly Statistics")
        for month, amount in sorted(stats['monthly_stats'].items()):
            count = sum(1 for inv in all_invoices 
                       if inv.get('issue_date', '').startswith(month))
            print(f"    {month}: ${amount:,.2f} ({count} invoices)")
    
    # 5. Save results
    print("\n[Step 5] Saving Results")
    print("-" * 70)
    
    # Create summary Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = f"data/output/invoice_summary_{timestamp}.xlsx"
    create_summary_excel(all_invoices, stats, summary_path)
    
    # Save statistics JSON
    stats_path = data_extractor.save_as_json(
        stats, 
        f"invoice_statistics_{timestamp}"
    )
    
    print(f"  ✓ JSON files: {len(all_invoices)} files (data/output/invoice_*.json)")
    print(f"  ✓ Statistics JSON: {stats_path}")
    print(f"  ✓ Summary Excel: {summary_path}")
    
    print("\n" + "=" * 70)
    print("                   Processing Complete!")
    print("=" * 70)
    print(f"\n📁 Results location: data/output/")
    print(f"📊 Open the Excel file to view detailed statistics.\n")
    print(f"✅ Powered by OpenAI GPT-4o Vision API\n")


if __name__ == "__main__":
    main()
