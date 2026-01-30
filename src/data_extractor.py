"""
데이터 추출 및 변환 모듈
추출된 정보를 Excel, JSON 등 다양한 형식으로 저장합니다.
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class DataExtractor:
    """데이터 추출 및 변환 클래스"""
    
    def __init__(self, output_dir: str = "data/output"):
        """
        초기화
        
        Args:
            output_dir: 출력 디렉토리 경로
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_as_json(self, data: Dict[str, Any], filename: str) -> str:
        """
        데이터를 JSON 파일로 저장
        
        Args:
            data: 저장할 데이터
            filename: 파일명 (확장자 제외)
            
        Returns:
            저장된 파일 경로
        """
        filepath = self.output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"JSON 저장 완료: {filepath}")
        return str(filepath)
    
    def save_invoice_to_excel(
        self, 
        invoice_data: Dict[str, Any], 
        filename: str
    ) -> str:
        """
        송장 데이터를 Excel로 저장
        
        Args:
            invoice_data: 송장 데이터
            filename: 파일명 (확장자 제외)
            
        Returns:
            저장된 파일 경로
        """
        filepath = self.output_dir / f"{filename}.xlsx"
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 기본 정보 시트
            info_data = {
                '항목': [
                    '송장번호', '발행일', '납부기한', 
                    '판매자', '구매자', '소계', '세금', '총액', '통화'
                ],
                '내용': [
                    invoice_data.get('invoice_number', ''),
                    invoice_data.get('issue_date', ''),
                    invoice_data.get('due_date', ''),
                    invoice_data.get('seller', {}).get('company_name', ''),
                    invoice_data.get('buyer', {}).get('company_name', ''),
                    invoice_data.get('subtotal', 0),
                    invoice_data.get('tax', 0),
                    invoice_data.get('total', 0),
                    invoice_data.get('currency', 'KRW')
                ]
            }
            df_info = pd.DataFrame(info_data)
            df_info.to_excel(writer, sheet_name='기본정보', index=False)
            
            # 품목 시트
            items = invoice_data.get('items', [])
            if items:
                df_items = pd.DataFrame(items)
                df_items.to_excel(writer, sheet_name='품목내역', index=False)
        
        print(f"Excel 저장 완료: {filepath}")
        return str(filepath)
    
    def save_receipts_to_excel(
        self, 
        receipts: List[Dict[str, Any]], 
        filename: str
    ) -> str:
        """
        여러 영수증 데이터를 하나의 Excel로 저장
        
        Args:
            receipts: 영수증 데이터 리스트
            filename: 파일명 (확장자 제외)
            
        Returns:
            저장된 파일 경로
        """
        filepath = self.output_dir / f"{filename}.xlsx"
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 전체 요약 시트
            summary_data = []
            for i, receipt in enumerate(receipts, 1):
                summary_data.append({
                    '번호': i,
                    '상점명': receipt.get('store_name', ''),
                    '거래일시': receipt.get('transaction_date', ''),
                    '총액': receipt.get('total', 0),
                    '결제수단': receipt.get('payment_method', ''),
                    '통화': receipt.get('currency', 'KRW')
                })
            
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='전체요약', index=False)
            
            # 개별 영수증 시트
            for i, receipt in enumerate(receipts, 1):
                items = receipt.get('items', [])
                if items:
                    df_items = pd.DataFrame(items)
                    sheet_name = f'영수증{i}'[:31]  # Excel 시트명 길이 제한
                    df_items.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"Excel 저장 완료: {filepath}")
        return str(filepath)
    
    def save_contract_to_excel(
        self, 
        contract_data: Dict[str, Any], 
        filename: str
    ) -> str:
        """
        계약서 데이터를 Excel로 저장
        
        Args:
            contract_data: 계약서 데이터
            filename: 파일명 (확장자 제외)
            
        Returns:
            저장된 파일 경로
        """
        filepath = self.output_dir / f"{filename}.xlsx"
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 기본 정보 시트
            party_a = contract_data.get('party_a', {})
            party_b = contract_data.get('party_b', {})
            
            info_data = {
                '항목': [
                    '계약서 제목', '계약 번호', '계약일', '효력발생일', '만료일',
                    '갑 당사자', '갑 대표자', '갑 연락처',
                    '을 당사자', '을 대표자', '을 연락처',
                    '계약금액', '지불조건'
                ],
                '내용': [
                    contract_data.get('contract_title', ''),
                    contract_data.get('contract_number', ''),
                    contract_data.get('contract_date', ''),
                    contract_data.get('effective_date', ''),
                    contract_data.get('expiry_date', ''),
                    party_a.get('name', ''),
                    party_a.get('representative', ''),
                    party_a.get('contact', ''),
                    party_b.get('name', ''),
                    party_b.get('representative', ''),
                    party_b.get('contact', ''),
                    contract_data.get('contract_amount', 0),
                    contract_data.get('payment_terms', '')
                ]
            }
            df_info = pd.DataFrame(info_data)
            df_info.to_excel(writer, sheet_name='계약정보', index=False)
            
            # 주요 조항 시트
            key_terms = contract_data.get('key_terms', [])
            if key_terms:
                df_terms = pd.DataFrame({
                    '번호': range(1, len(key_terms) + 1),
                    '조항': key_terms
                })
                df_terms.to_excel(writer, sheet_name='주요조항', index=False)
        
        print(f"Excel 저장 완료: {filepath}")
        return str(filepath)
    
    def create_summary_report(
        self, 
        documents: List[Dict[str, Any]], 
        document_type: str,
        filename: str = None
    ) -> str:
        """
        여러 문서의 요약 리포트 생성
        
        Args:
            documents: 문서 데이터 리스트
            document_type: 문서 유형
            filename: 파일명 (None일 경우 자동 생성)
            
        Returns:
            저장된 파일 경로
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{document_type}_summary_{timestamp}"
        
        filepath = self.output_dir / f"{filename}.xlsx"
        
        # 문서 유형별 요약 데이터 생성
        if document_type == "invoice":
            summary_data = self._summarize_invoices(documents)
        elif document_type == "receipt":
            summary_data = self._summarize_receipts(documents)
        elif document_type == "contract":
            summary_data = self._summarize_contracts(documents)
        else:
            summary_data = self._summarize_generic(documents)
        
        # Excel 저장
        df = pd.DataFrame(summary_data)
        df.to_excel(filepath, index=False)
        
        print(f"요약 리포트 저장 완료: {filepath}")
        return str(filepath)
    
    def _summarize_invoices(self, invoices: List[Dict]) -> List[Dict]:
        """송장 요약"""
        summary = []
        for inv in invoices:
            summary.append({
                '송장번호': inv.get('invoice_number', ''),
                '발행일': inv.get('issue_date', ''),
                '판매자': inv.get('seller', {}).get('company_name', ''),
                '구매자': inv.get('buyer', {}).get('company_name', ''),
                '총액': inv.get('total', 0),
                '통화': inv.get('currency', 'KRW'),
                '상태': '처리완료'
            })
        return summary
    
    def _summarize_receipts(self, receipts: List[Dict]) -> List[Dict]:
        """영수증 요약"""
        summary = []
        for rec in receipts:
            summary.append({
                '상점명': rec.get('store_name', ''),
                '거래일시': rec.get('transaction_date', ''),
                '총액': rec.get('total', 0),
                '결제수단': rec.get('payment_method', ''),
                '통화': rec.get('currency', 'KRW')
            })
        return summary
    
    def _summarize_contracts(self, contracts: List[Dict]) -> List[Dict]:
        """계약서 요약"""
        summary = []
        for con in contracts:
            summary.append({
                '계약번호': con.get('contract_number', ''),
                '계약일': con.get('contract_date', ''),
                '갑': con.get('party_a', {}).get('name', ''),
                '을': con.get('party_b', {}).get('name', ''),
                '계약금액': con.get('contract_amount', 0),
                '만료일': con.get('expiry_date', '')
            })
        return summary
    
    def _summarize_generic(self, documents: List[Dict]) -> List[Dict]:
        """일반 문서 요약"""
        summary = []
        for i, doc in enumerate(documents, 1):
            summary.append({
                '번호': i,
                '문서유형': doc.get('document_type', 'Unknown'),
                '처리일시': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '상태': '완료'
            })
        return summary
    
    def load_json(self, filepath: str) -> Dict[str, Any]:
        """
        JSON 파일 로드
        
        Args:
            filepath: JSON 파일 경로
            
        Returns:
            데이터 딕셔너리
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
