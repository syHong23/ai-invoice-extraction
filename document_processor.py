"""
Document Processing with OpenAI GPT-4o Vision
Extracts structured data from invoice images using GPT-4o Vision API.
"""

import os
import base64
from typing import Dict, Any, Optional
from pathlib import Path
from openai import OpenAI
from PIL import Image
import json


class DocumentProcessor:
    """GPT-4o Vision based document processor"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize
        
        Args:
            api_key: OpenAI API key (reads from env if None)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Cost-effective option
    
    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64
        
        Args:
            image_path: Image file path
            
        Returns:
            base64 encoded string
        """
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if needed
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Optimize image size (max 2000x2000)
            max_size = (2000, 2000)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to temp and encode
            temp_path = "temp_image.jpg"
            img.save(temp_path, format='JPEG', quality=85)
            
            with open(temp_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            os.remove(temp_path)
            
        return image_data
    
    def extract_with_vlm(
        self, 
        image_path: str, 
        extraction_prompt: str,
        use_ocr_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract information using GPT-4o Vision
        
        Args:
            image_path: Document image path
            extraction_prompt: Extraction instructions
            use_ocr_text: OCR text (optional, not used with Vision)
            
        Returns:
            Extracted information dictionary
        """
        image_data = self.encode_image(image_path)
        
        # Construct message
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": extraction_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
        
        # API call
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2000,
                temperature=0
            )
            
            # Extract response text
            result_text = response.choices[0].message.content
            
            # Parse JSON
            try:
                # Remove code blocks if present
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw text
                result = {"raw_text": result_text}
            
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def process_document(
        self,
        image_path: str,
        document_type: str,
        ocr_handler: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Process document
        
        Args:
            image_path: Document image path
            document_type: Document type (invoice, receipt, contract, etc.)
            ocr_handler: OCR handler (not used with Vision API)
            
        Returns:
            Extracted information
        """
        # Get prompt based on document type
        prompts = {
            "invoice": self._get_invoice_prompt(),
            "receipt": self._get_receipt_prompt(),
            "contract": self._get_contract_prompt(),
            "business_card": self._get_business_card_prompt(),
            "id_card": self._get_id_card_prompt()
        }
        
        prompt = prompts.get(document_type, self._get_generic_prompt())
        
        # Extract with VLM
        result = self.extract_with_vlm(image_path, prompt)
        
        return result
    
    def _get_invoice_prompt(self) -> str:
        """Invoice extraction prompt"""
        return """Analyze this invoice image and extract the following information in JSON format:

{
  "invoice_number": "Invoice number",
  "issue_date": "Issue date (YYYY-MM-DD)",
  "due_date": "Due date (YYYY-MM-DD)",
  "supplier": {
    "company_name": "Supplier company name",
    "address": "Supplier address",
    "tax_id": "Tax ID number",
    "contact": "Contact information"
  },
  "buyer": {
    "company_name": "Buyer company name",
    "address": "Buyer address",
    "tax_id": "Tax ID number",
    "contact": "Contact information"
  },
  "items": [
    {
      "description": "Item description",
      "quantity": quantity (number),
      "unit_price": unit price (number),
      "amount": total amount (number)
    }
  ],
  "subtotal": subtotal amount (number),
  "tax": tax amount (number),
  "total": total amount (number),
  "currency": "Currency code"
}

Use null for missing fields. Return ONLY the JSON, no additional text."""

    def _get_receipt_prompt(self) -> str:
        """Receipt extraction prompt"""
        return """Analyze this receipt image and extract the following information in JSON format:

{
  "store_name": "Store name",
  "store_address": "Store address",
  "store_phone": "Store phone number",
  "transaction_date": "Transaction date/time (YYYY-MM-DD HH:MM:SS)",
  "receipt_number": "Receipt number",
  "items": [
    {
      "name": "Item name",
      "quantity": quantity (number),
      "unit_price": unit price (number),
      "total_price": total price (number)
    }
  ],
  "subtotal": subtotal (number),
  "tax": tax (number),
  "discount": discount (number),
  "total": total (number),
  "payment_method": "Payment method",
  "card_number": "Masked card number",
  "currency": "Currency code"
}

Use null for missing fields. Return ONLY the JSON, no additional text."""

    def _get_contract_prompt(self) -> str:
        """Contract extraction prompt"""
        return """Analyze this contract image and extract the following information in JSON format:

{
  "contract_title": "Contract title",
  "contract_number": "Contract number",
  "contract_date": "Contract date (YYYY-MM-DD)",
  "effective_date": "Effective date (YYYY-MM-DD)",
  "expiry_date": "Expiry date (YYYY-MM-DD)",
  "party_a": {
    "name": "Party A name",
    "representative": "Representative",
    "address": "Address",
    "contact": "Contact"
  },
  "party_b": {
    "name": "Party B name",
    "representative": "Representative",
    "address": "Address",
    "contact": "Contact"
  },
  "contract_amount": contract amount (number),
  "payment_terms": "Payment terms",
  "key_terms": ["Key term 1", "Key term 2"],
  "special_notes": "Special notes"
}

Use null for missing fields. Return ONLY the JSON, no additional text."""

    def _get_business_card_prompt(self) -> str:
        """Business card extraction prompt"""
        return """Analyze this business card image and extract the following information in JSON format:

{
  "name": "Name",
  "company": "Company name",
  "position": "Position/Title",
  "department": "Department",
  "email": "Email",
  "phone": "Phone number",
  "mobile": "Mobile number",
  "fax": "Fax number",
  "address": "Address",
  "website": "Website"
}

Use null for missing fields. Return ONLY the JSON, no additional text."""

    def _get_id_card_prompt(self) -> str:
        """ID card extraction prompt"""
        return """Analyze this ID card image and extract the following information in JSON format:

{
  "document_type": "Document type",
  "id_number": "ID number (partially masked)",
  "name": "Name",
  "date_of_birth": "Date of birth (YYYY-MM-DD)",
  "issue_date": "Issue date (YYYY-MM-DD)",
  "expiry_date": "Expiry date (YYYY-MM-DD)",
  "issuing_authority": "Issuing authority",
  "address": "Address"
}

Mask sensitive information for privacy. Use null for missing fields. Return ONLY the JSON, no additional text."""

    def _get_generic_prompt(self) -> str:
        """Generic document extraction prompt"""
        return """Analyze this document image and extract key information in structured JSON format.
Identify the document type and extract all relevant information.

{
  "document_type": "Document type",
  "key_information": {
    // Document-specific key information
  }
}

Return ONLY the JSON, no additional text."""
