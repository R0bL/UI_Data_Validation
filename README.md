# UI Data Validation - Field Mapping Tools

This repository contains tools for validating and mapping data fields in the AllSci web application.

## Files

### 1. `test_load_times.ipynb`
Performance testing notebook that measures load times for the clinical trials atlas using Playwright.

**Features:**
- Downloads and analyzes parquet files from CloudFront
- Measures cold load (no cache) and warm load (with cache) times
- Provides bottleneck analysis for resource loading
- Compares performance across environments (Production, Staging)

**Usage:**
```bash
jupyter notebook test_load_times.ipynb
```

### 2. `selenium_field_mapper.ipynb` ⭐ NEW
Comprehensive Selenium-based HTML parser that maps all data fields in the application.

**Features:**
- Automatically logs into the application
- Scans specified pages and extracts all data fields
- Identifies field types: metadata, buttons, dates, tables, etc.
- Generates CSS selectors for each field
- Creates detailed field mapping reports
- Exports data to CSV and JSON formats

**What it Maps:**

1. **Metadata Fields**
   - Conditions
   - Intervention/Treatment
   - Study Type
   - Phase
   - Enrollment
   - And more...

2. **Button Metrics**
   - Citation counts
   - Any buttons with aria-labels containing data

3. **Date Fields**
   - Year fields (e.g., "2025")
   - Full date fields
   - Fields with calendar icons

4. **Table Data**
   - All table headers and sample data
   - Multi-column data extraction

5. **Data Attributes**
   - Elements with `data-testid`
   - Elements with `data-field`
   - Elements with `data-value`

**Output:**

The notebook generates three types of outputs:

1. **Field Mapping CSV** (`field_mapping_YYYYMMDD_HHMMSS.csv`)
   - Complete list of all fields with metadata
   - Columns: environment, page_url, page_title, category, label, value, selector, element_type, has_data, scan_timestamp

2. **Field Mapping JSON** (`field_mapping_YYYYMMDD_HHMMSS.json`)
   - Same data in JSON format for programmatic access

3. **Validation Report CSV** (`validation_report_YYYYMMDD_HHMMSS.csv`)
   - Simplified report for validation purposes
   - Columns: Page, Category, Field Label, Has Data, Sample Value, CSS Selector

**Usage:**

1. Install dependencies:
```bash
pip install selenium beautifulsoup4 pandas
```

2. Update configuration in the notebook:
   - Set your login credentials
   - Add pages you want to scan
   - Adjust wait times if needed

3. Run the notebook:
```bash
jupyter notebook selenium_field_mapper.ipynb
```

4. The notebook will:
   - Launch Chrome browser (visible by default)
   - Login to the application
   - Navigate through specified pages
   - Extract all fields
   - Generate mapping reports

**Example Output:**

```
Field Mapping Summary:
Total fields: 156

Fields by category:
metadata          45
button_metric     12
date              8
table            35
data_testid      56

Fields with data: 142
Fields without data: 14

Page Coverage:
explore/clinical-trials    85 fields
trial/NCT12345678         71 fields
```

## Configuration

### Selenium Field Mapper Configuration

```python
# Add or remove pages to scan
URLS_TO_SCAN = {
    "Production": {
        "login": "https://app.allsci.com/?login=true",
        "pages": [
            "https://app.allsci.com/explore/clinical-trials",
            "https://app.allsci.com/another-page",  # Add more pages
        ]
    }
}

# Adjust detection patterns
FIELD_PATTERNS = {
    'metadata': {
        'selector': 'div#metadata-content h1',
        'pattern': r'^([^:]+):\\s*(.+)$'
    },
    # Add custom patterns for your specific fields
}
```

## Field Detection Logic

The field mapper uses multiple strategies to identify fields:

1. **Label-Value Pairs**: Detects patterns like "Label: Value"
2. **CSS Selectors**: Uses specific selectors for known components
3. **Semantic HTML**: Identifies fields based on semantic structure
4. **Data Attributes**: Extracts elements with data-* attributes
5. **Context Analysis**: Uses surrounding elements for context

## CSS Selector Generation

Each field is assigned a unique CSS selector for:
- Automated testing
- UI validation
- Data extraction scripts
- Element location in tests

Example selectors generated:
```css
div#metadata-content > h1:nth-of-type(1)
button[aria-label="Total citations"]
span.flex.flex-row.items-center
```

## Extending the Field Mapper

To add custom field detection:

1. Create a new extraction function:
```python
def extract_custom_fields(driver):
    fields = []
    # Your custom logic here
    return fields
```

2. Add it to the extraction pipeline in `extract_all_fields_from_page()`:
```python
print("    - Extracting custom fields...")
all_fields.extend(extract_custom_fields(driver))
```

## Troubleshooting

**Issue: Login fails**
- Verify credentials are correct
- Check if manual CAPTCHA is required
- Increase `ELEMENT_WAIT` timeout

**Issue: Fields not detected**
- Check if page is fully loaded (increase `PAGE_LOAD_WAIT`)
- Verify CSS selectors in `FIELD_PATTERNS`
- Add custom detection logic for specific fields

**Issue: Browser crashes**
- Run in headless mode: `scan_application(URLS_TO_SCAN, headless=True)`
- Reduce number of pages scanned
- Increase system resources

## Requirements

```
selenium>=4.0.0
beautifulsoup4>=4.9.0
pandas>=1.3.0
jupyter>=1.0.0
playwright>=1.40.0  # For test_load_times.ipynb
nest-asyncio>=1.5.0  # For test_load_times.ipynb
```

## License

Internal use only - AllSci Corporation
