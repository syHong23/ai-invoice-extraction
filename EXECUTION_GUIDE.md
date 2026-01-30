# 송장 처리 프로젝트 실행 가이드

## 📌 전체 프로세스

```
1. 샘플 송장 생성
   ↓
2. 송장 일괄 처리
   ↓
3. 결과 확인 (Excel, JSON)
```

## 🚀 실행 순서

### Step 1: 프로젝트 설정

```bash
# 1. 폴더 생성
mkdir vlm_document_extraction
cd vlm_document_extraction

# 2. 가상환경
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 폴더 구조 생성
mkdir -p src data/input data/output
```

### Step 2: 파일 배치

다운로드한 파일들을 다음과 같이 배치:

```
vlm_document_extraction/
├── src/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── ocr_handler.py
│   └── data_extractor.py
├── data/
│   ├── input/
│   └── output/
├── generate_sample_invoices.py
├── process_invoices.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Step 3: 환경 변수 설정

`.env` 파일 생성:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

### Step 4: 샘플 송장 생성

```bash
python generate_sample_invoices.py
```

**예상 출력:**
```
============================================================
송장 샘플 이미지 생성 중... (총 10개)
============================================================

생성 완료: data/input/invoice_001.png
   1. INV-2024-001 - XYZ 코퍼레이션 - 1,650,000원
생성 완료: data/input/invoice_002.png
   2. INV-2024-002 - 글로벌트레이딩 - 880,000원
...

============================================================
생성 완료! data/input 폴더를 확인하세요.
============================================================
```

### Step 5: 송장 처리

```bash
python process_invoices.py
```

**예상 출력:**
```
======================================================================
                    송장 일괄 처리 시스템
======================================================================

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
  [3/10] 처리 중: invoice_003.png ✓
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

  📅 월별 통계
    2024-01: 7,920,000원 (5건)
    2024-02: 7,920,000원 (5건)

[5단계] 결과 저장
----------------------------------------------------------------------

요약 리포트 생성: data/output/invoice_summary_20240130_143025.xlsx
  ✓ JSON 파일: 10개 (data/output/invoice_*.json)
  ✓ 통계 JSON: data/output/invoice_statistics_20240130_143025.json
  ✓ 요약 Excel: data/output/invoice_summary_20240130_143025.xlsx

======================================================================
                      처리 완료!
======================================================================

📁 결과 파일 위치: data/output/
📊 Excel을 열어서 상세 통계를 확인하세요.
```

### Step 6: 결과 확인

#### Excel 파일 열기
```bash
# Windows
start data/output/invoice_summary_*.xlsx

# Mac
open data/output/invoice_summary_*.xlsx

# Linux
xdg-open data/output/invoice_summary_*.xlsx
```

#### JSON 파일 확인
```bash
# 개별 송장 JSON
cat data/output/invoice_001.json

# 통계 JSON
cat data/output/invoice_statistics_*.json
```

## 🔍 생성된 파일 구조

```
data/
├── input/
│   ├── invoice_001.png    # 생성된 송장 이미지
│   ├── invoice_002.png
│   └── ...
└── output/
    ├── invoice_001.json                      # 개별 송장 JSON
    ├── invoice_002.json
    ├── ...
    ├── invoice_summary_20240130_143025.xlsx  # 통합 Excel 리포트
    └── invoice_statistics_20240130_143025.json  # 통계 JSON
```

## ⚙️ 커스터마이징

### 송장 개수 변경

`generate_sample_invoices.py` 수정:
```python
# 10개 대신 20개 생성
generator.generate_multiple_invoices(count=20)
```

### 샘플 데이터 커스터마이징

`generate_sample_invoices.py`의 `suppliers`, `buyers`, `products` 리스트 수정:
```python
self.suppliers = [
    {"name": "내 회사", "tax_id": "123-45-67890", ...},
    # 더 추가...
]
```

### VLM만 사용 (OCR 없이)

Tesseract를 설치하지 않으면 자동으로 VLM만 사용됩니다.

## 🐛 문제 해결

### 문제 1: "송장 이미지를 찾을 수 없습니다"

**해결:**
```bash
python generate_sample_invoices.py
```

### 문제 2: "ANTHROPIC_API_KEY가 설정되지 않았습니다"

**해결:**
1. `.env` 파일이 있는지 확인
2. API 키가 올바른지 확인
3. 가상환경이 활성화되었는지 확인

### 문제 3: Tesseract 오류

**해결:**
- OCR 없이 VLM만 사용해도 됩니다
- 또는 Tesseract 설치: https://github.com/UB-Mannheim/tesseract/wiki

### 문제 4: 한글 폰트 깨짐

**해결:**
- Windows: 자동으로 `malgun.ttf` 사용
- Mac: 자동으로 `AppleSDGothicNeo` 사용
- Linux: 한글 폰트 설치 필요

## 💡 팁

1. **처리 시간**: 송장 1개당 약 5-10초 소요 (VLM API 호출)
2. **비용**: Claude Sonnet 4 API 비용 발생 (이미지당 약 $0.01-0.02)
3. **정확도**: VLM은 약 95% 이상 정확도 (샘플 송장 기준)
4. **대량 처리**: 100개 이상 처리 시 배치 처리 권장

## 📧 다음 단계

프로젝트를 GitHub에 업로드하고 포트폴리오로 활용하세요!

```bash
git init
git add .
git commit -m "Initial commit: AI Invoice Processing System"
git remote add origin https://github.com/username/vlm_document_extraction.git
git push -u origin main
```
