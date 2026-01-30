"""
OCR 처리 모듈
Tesseract를 사용하여 이미지에서 텍스트를 추출합니다.
"""

import os
import pytesseract
from PIL import Image
from typing import Optional, Dict
import platform


class OCRHandler:
    """Tesseract OCR 핸들러 클래스"""
    
    def __init__(self, tesseract_path: Optional[str] = None, lang: str = 'kor+eng'):
        """
        초기화
        
        Args:
            tesseract_path: Tesseract 실행 파일 경로 (Windows만 필요)
            lang: 인식 언어 (기본값: 한국어+영어)
        """
        self.lang = lang
        
        # Windows에서 Tesseract 경로 설정
        if platform.system() == 'Windows':
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            elif os.getenv('TESSERACT_PATH'):
                pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')
            else:
                # 기본 설치 경로 시도
                default_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                if os.path.exists(default_path):
                    pytesseract.pytesseract.tesseract_cmd = default_path
    
    def extract_text(self, image_path: str, preprocessing: bool = True) -> str:
        """
        이미지에서 텍스트 추출
        
        Args:
            image_path: 이미지 파일 경로
            preprocessing: 전처리 적용 여부
            
        Returns:
            추출된 텍스트
        """
        try:
            # 이미지 로드
            image = Image.open(image_path)
            
            # 전처리 (선택사항)
            if preprocessing:
                image = self._preprocess_image(image)
            
            # OCR 실행
            text = pytesseract.image_to_string(image, lang=self.lang)
            
            return text.strip()
            
        except Exception as e:
            print(f"OCR 오류: {str(e)}")
            return ""
    
    def extract_data(self, image_path: str) -> Dict:
        """
        이미지에서 구조화된 데이터 추출
        
        Args:
            image_path: 이미지 파일 경로
            
        Returns:
            OCR 데이터 딕셔너리
        """
        try:
            image = Image.open(image_path)
            
            # 상세 데이터 추출
            data = pytesseract.image_to_data(
                image, 
                lang=self.lang, 
                output_type=pytesseract.Output.DICT
            )
            
            return data
            
        except Exception as e:
            print(f"OCR 데이터 추출 오류: {str(e)}")
            return {}
    
    def extract_with_boxes(self, image_path: str) -> list:
        """
        텍스트와 바운딩 박스 정보 추출
        
        Args:
            image_path: 이미지 파일 경로
            
        Returns:
            [(text, x, y, w, h, conf), ...] 리스트
        """
        try:
            image = Image.open(image_path)
            
            data = pytesseract.image_to_data(
                image, 
                lang=self.lang, 
                output_type=pytesseract.Output.DICT
            )
            
            results = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                if text:  # 빈 텍스트 제외
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    conf = data['conf'][i]
                    
                    results.append((text, x, y, w, h, conf))
            
            return results
            
        except Exception as e:
            print(f"박스 추출 오류: {str(e)}")
            return []
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        이미지 전처리
        
        Args:
            image: PIL Image 객체
            
        Returns:
            전처리된 이미지
        """
        # 그레이스케일 변환
        if image.mode != 'L':
            image = image.convert('L')
        
        # 해상도 향상 (너무 작은 경우)
        width, height = image.size
        if width < 1000 or height < 1000:
            scale_factor = max(1000 / width, 1000 / height)
            new_size = (int(width * scale_factor), int(height * scale_factor))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def get_available_languages(self) -> list:
        """
        사용 가능한 언어 목록 반환
        
        Returns:
            언어 코드 리스트
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            print(f"언어 목록 조회 오류: {str(e)}")
            return []
    
    def check_tesseract_installation(self) -> bool:
        """
        Tesseract 설치 확인
        
        Returns:
            설치 여부
        """
        try:
            version = pytesseract.get_tesseract_version()
            print(f"Tesseract 버전: {version}")
            return True
        except Exception as e:
            print(f"Tesseract가 설치되지 않았거나 경로가 잘못되었습니다: {str(e)}")
            return False
