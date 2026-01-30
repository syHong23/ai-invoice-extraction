# 📄 AI 기반 송장 자동 처리 시스템

Claude Sonnet 4 VLM(Vision Language Model)과 Tesseract OCR을 활용하여 송장 이미지에서 정보를 자동으로 추출하고 분석하는 비즈니스 자동화 솔루션입니다.

## 🎯 프로젝트 목적

회계/경리 업무에서 수작업으로 처리하던 송장 입력 작업을 AI로 자동화:
- **송장 이미지 → 구조화된 데이터** 자동 변환
- **여러 송장 일괄 처리** 및 통계 분석
- **거래처별, 월별 매출 통계** 자동 생성
- **Excel 리포트** 자동 생성으로 업무 효율 향상

## 🛠 기술 스택

- **VLM**: Claude Sonnet 4 (Anthropic API)
- **OCR**: Tesseract OCR
- **언어**: Python 3.8+
- **주요 라이브러리**: 
  - anthropic (Claude API)
  - pytesseract (OCR)
  - Pillow (이미지 처리)
  - pandas, openpyxl (데이터 처리)

## 📋 주요 기능

### 1. 송장 정보 자동 추출
- **기본 정보**: 송장번호, 발행일, 납부기한
- **거래처 정보**: 공급자/공급받는자 회사명, 사업자번호, 주소, 연락처
- **품목 내역**: 품목명, 수량, 단가, 금액
- **금액 정보**: 공급가액, 부가세, 합계

### 2. 일괄 처리 시스템
- 폴더 내 모든 송장 이미지 자동 스캔
- 순차적 처리 및 진행상황 표시
- 실패 건 자동 로깅

### 3. 통계 분석
- **전체 통계**: 총 매출액, 평균/최고/최저 거래액
- **거래처별 통계**: 거래처별 매출액 및 비중
- **월별 통계**: 월별 매출 추이 분석
- **Excel 리포트**: 다중 시트로 구성된 상세 리포트

### 4. VLM + OCR 하이브리드
- **VLM 우선**: Claude Sonnet 4의 강력한 Vision 이해 능력
- **OCR 보조**: 작은 글씨나 복잡한 레이아웃 보완
- **선택적 사용**: Tesseract 미설치 시 VLM만으로 작동

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/vlm_document_extraction.git
cd vlm_document_extraction

# 2. 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. Tesseract OCR 설치 (선택사항)
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr tesseract-ocr-kor
```

### 2. API 키 설정

`.env` 파일을 생성하고 Anthropic API 키를 설정:

```
ANTHROPIC_API_KEY=your_api_key_here
```

API 키는 https://console.anthropic.com/ 에서 발급받을 수 있습니다.

### 3. 샘플 송장 생성

```bash
# 10개의 샘플 송장 이미지 자동 생성
python generate_sample_invoices.py
```

### 4. 송장 일괄 처리

```bash
# 생성된 송장들을 자동으로 처리하고 통계 생성
python process_invoices.py
```

처리 완료 후 `data/output/` 폴더에서 결과 확인!

## 📁 프로젝트 구조

```
vlm_document_extraction/
├── src/
│   ├── document_processor.py    # VLM 기반 문서 처리
│   ├── ocr_handler.py           # Tesseract OCR 처리
│   └── data_extractor.py        # 데이터 변환 및 저장
├── data/
│   ├── input/                   # 송장 이미지 (invoice_*.png)
│   └── output/                  # 처리 결과 (JSON, Excel)
├── generate_sample_invoices.py  # 샘플 송장 생성기
├── process_invoices.py          # 송장 일괄 처리 메인
├── .env                         # 환경 변수 (API 키)
├── requirements.txt             # 패키지 목록
└── README.md
```

## 💡 사용 예제

### 1. 샘플 송장 생성

```python
from generate_sample_invoices import InvoiceGenerator

# 생성기 초기화
generator = InvoiceGenerator(output_dir="data/input")

# 10개의 송장 생성
generator.generate_multiple_invoices(count=10)
```

### 2. 송장 일괄 처리

```bash
# 메인 프로그램 실행
python process_invoices.py
```

**출력 예시:**
```
==================================================================
                    송장 일괄 처리 시스템
==================================================================

[1단계] 시스템 초기화
----------------------------------------------------------------------
  ✓ VLM 프로세서 초기화 완료
  ✓ OCR 핸들러 초기화 완료
  ✓ 데이터 추출기 초기화 완료

[2단계] 송장 이미지 검색
----------------------------------------------------------------------
  ✓ 발견된 송장: 10개

[3단계] 송장 처리
----------------------------------------------------------------------
  [1/10] 처리 중: invoice_001.png ✓
  [2/10] 처리 중: invoice_002.png ✓
  ...

[4단계] 통계 계산
----------------------------------------------------------------------

  📊 처리 결과
    • 총 송장 수: 10건
    • 성공: 10건
    • 실패: 0건

  💰 매출 통계
    • 총 매출액: 15,840,000원
    • 총 부가세: 1,584,000원
    • 평균 거래액: 1,584,000원
    • 최고 거래액: 3,850,000원
    • 최저 거래액: 440,000원

  🏢 거래처별 통계 (상위 5개)
    1. XYZ 코퍼레이션: 4,620,000원 (29.2%)
    2. 스마트비즈니스: 3,850,000원 (24.3%)
    3. 글로벌트레이딩: 2,970,000원 (18.8%)
    ...

처리 완료!
```

### 3. Python 코드로 직접 사용

```python
from src.document_processor import DocumentProcessor
from src.ocr_handler import OCRHandler
from src.data_extractor import DataExtractor

# 초기화
doc_processor = DocumentProcessor()
ocr_handler = OCRHandler()
data_extractor = DataExtractor()

# 송장 처리
result = doc_processor.process_document(
    image_path="data/input/invoice_001.png",
    document_type="invoice",
    ocr_handler=ocr_handler
)

# 결과 저장
data_extractor.save_invoice_to_excel(result, "invoice_result")
```

## 📊 결과 예시

### Excel 리포트 구성

생성되는 Excel 파일은 4개의 시트로 구성됩니다:

#### 1. 전체송장 시트
| 송장번호 | 발행일 | 납부기한 | 공급자 | 공급받는자 | 공급가액 | 부가세 | 합계 |
|---------|--------|---------|--------|-----------|---------|-------|------|
| INV-2024-001 | 2024-01-15 | 2024-02-14 | ABC 주식회사 | XYZ 코퍼레이션 | 1,500,000 | 150,000 | 1,650,000 |
| INV-2024-002 | 2024-01-20 | 2024-02-19 | 테크솔루션즈 | 글로벌트레이딩 | 800,000 | 80,000 | 880,000 |

#### 2. 전체통계 시트
| 항목 | 값 |
|------|-----|
| 총 송장 수 | 10건 |
| 총 매출액 | 15,840,000원 |
| 총 부가세 | 1,584,000원 |
| 평균 거래액 | 1,584,000원 |

#### 3. 거래처별통계 시트
| 거래처 | 거래액 | 비중(%) |
|--------|--------|---------|
| XYZ 코퍼레이션 | 4,620,000 | 29.2 |
| 스마트비즈니스 | 3,850,000 | 24.3 |

#### 4. 월별통계 시트
| 월 | 거래액 | 건수 |
|----|--------|------|
| 2024-01 | 7,920,000 | 5 |
| 2024-02 | 7,920,000 | 5 |

### JSON 출력 예시

```json
{
  "invoice_number": "INV-2024-001",
  "issue_date": "2024-01-15",
  "due_date": "2024-02-14",
  "supplier": {
    "company_name": "ABC 주식회사",
    "tax_id": "123-45-67890",
    "address": "서울시 강남구 테헤란로 123",
    "contact": "02-1234-5678"
  },
  "buyer": {
    "company_name": "XYZ 코퍼레이션",
    "tax_id": "098-76-54321",
    "address": "서울시 종로구 세종대로 111",
    "contact": "02-9876-5432"
  },
  "items": [
    {
      "description": "노트북 컴퓨터",
      "quantity": 5,
      "unit_price": 200000,
      "amount": 1000000
    },
    {
      "description": "모니터",
      "quantity": 10,
      "unit_price": 50000,
      "amount": 500000
    }
  ],
  "subtotal": 1500000,
  "tax": 150000,
  "total": 1650000,
  "currency": "KRW"
}
```

## 🔧 성능 최적화

### VLM과 OCR 조합 전략

1. **VLM Only**: 간단한 문서, 레이아웃이 명확한 경우
2. **OCR + VLM**: 복잡한 문서, 작은 글씨, 많은 텍스트
3. **OCR Only**: 단순 텍스트 추출만 필요한 경우

### 이미지 전처리

```python
# OCR 정확도 향상을 위한 이미지 전처리
ocr_handler = OCRHandler()
result = ocr_handler.extract_text(
    image_path="document.png",
    preprocessing=True  # 그레이스케일, 해상도 최적화
)
```

## 📈 향후 개선 계획

- [ ] PDF 송장 직접 처리 (이미지 변환 없이)
- [ ] 웹 인터페이스 추가 (Streamlit)
- [ ] 송장 양식 자동 감지
- [ ] 이메일 첨부 송장 자동 처리
- [ ] ERP 시스템 연동 API
- [ ] 중복 송장 자동 감지
- [ ] 송장 검증 (금액 계산 확인)
- [ ] 다국어 송장 지원

## 🎯 실무 활용 시나리오

### 1. 경리팀 업무 자동화
- 이메일로 받은 송장 자동 처리
- 회계 프로그램 입력용 Excel 생성
- 월말 정산 리포트 자동 생성

### 2. 구매팀 데이터 관리
- 구매 송장 일괄 아카이빙
- 거래처별 구매 내역 추적
- 예산 대비 실적 분석

### 3. 영업팀 매출 분석
- 발행 송장 자동 집계
- 고객사별 매출 통계
- 월별/분기별 매출 트렌드

## 🐛 트러블슈팅

### Tesseract 인식 안 됨

```python
# Windows에서 경로 직접 지정
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### API 호출 제한

```python
# 대량 처리 시 딜레이 추가
import time
for image in images:
    result = process_document(image)
    time.sleep(1)  # 1초 대기
```

### 한글 인식 오류

```bash
# 한글 언어팩 설치 확인
tesseract --list-langs

# 없으면 설치
# Windows: Tesseract 설치 시 Korean 체크
# Linux: sudo apt-get install tesseract-ocr-kor
```

## 📝 라이선스

MIT License

## 👤 개발자

- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com

## 🙏 감사의 말

- Anthropic Claude API
- Tesseract OCR
- Python 커뮤니티

## 📮 문의 및 기여

이슈나 PR은 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
