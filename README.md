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

### 2. `application_crawler.ipynb` 🚀 RECOMMENDED
**Full Application Crawler** - Automatically discovers and maps the entire application structure.

This is the most comprehensive tool that crawls the entire application to build a complete sitemap and field mapping.

**Features:**
- **Automatic Page Discovery**: Starts from seed URLs and automatically discovers all pages
- **Intelligent Crawling**: Follows links from list pages to detail pages
- **Tab Detection**: Automatically detects and clicks through tabs (Works, Hypotheses, Patents, etc.)
- **Complete Sitemap**: Builds a tree structure of the entire application
- **Comprehensive Field Mapping**: Extracts all fields from every page and tab
- **Relationship Mapping**: Shows how pages are connected (list → detail → tabs)
- **Multiple Export Formats**: CSV, JSON, and human-readable sitemap

**How it Works:**

1. **Search Queries** → Start with search terms (e.g., "covid", "cancer")
2. **Click Search Tabs** → Navigate through Hypotheses, Articles, Clinical Trials, Grants, Researchers tabs
3. **Extract Filters** → Map filter fields (Publication Year, Researcher, Source, etc.)
4. **Sample Results** → Collect sample detail pages from each search tab (5 per tab by default)
5. **Follow to Details** → Navigate to detail pages (e.g., `/clinical-trial/ASC-CT-...`)
6. **Detect Detail Tabs** → Find and click tabs on detail pages (Overview, Works, Hypotheses, Patents)
7. **Extract All Fields** → Map all data fields from every page and tab
8. **Build Structure** → Create complete sitemap showing relationships

**Example Structure Discovered:**

```
📄 /search?query=covid (Search Results)
   Type: search_results | Fields: 67 (filters + metrics) | Search Tabs: 5

   Search Tabs Clicked:
   ├─ Hypotheses (177.9K results)
   ├─ Articles (1.2M results)
   ├─ Clinical Trials (20.1K results) → Sampled 5 trials
   ├─ Grants (11.8K results)
   └─ Researchers (635 results)

   Filters Extracted:
   ├─ Publication Year (2025, 2024, 2023, 2022, 2021...)
   ├─ Researcher (viroj wiwanitkit, giuseppe lippi...)
   └─ Source (PLOS One, Cureus, Scientific Reports...)

   📄 /clinical-trial/ASC-CT-0000000174586-1.0-1745776457 (Detail Page)
      Type: clinical_trial_detail | Fields: 89 | Tabs: Overview, Works, Hypotheses, Patents

      Detail Page Tabs:
      ├─ Overview → Metadata fields (Conditions, Intervention, Phase, Enrollment...)
      ├─ Works → Related works table
      ├─ Hypotheses → Related hypotheses
      └─ Patents → Related patents

      📄 /work/ASC-WK-... (Linked Work)
         Type: work_detail | Fields: 156
```

**Configuration:**

```python
# Search queries - starting points
SEARCH_QUERIES = [
    "covid",        # Discovers: hypotheses, articles, trials, grants, researchers
    "cancer",       # Different search for broader coverage
    "diabetes",     # Another search term
]

# Search result tabs to explore
SEARCH_RESULT_TABS = [
    'Hypotheses',
    'Articles',
    'Clinical Trials',
    'Grants',
    'Researchers',
]

# Crawl limits
MAX_PAGES_TO_CRAWL = 50  # Total pages to crawl
MAX_RESULTS_PER_SEARCH_TAB = 5  # Sample detail pages per search tab
MAX_DEPTH = 3  # How deep to crawl from detail pages
```

**Output Files:**

1. **`field_mapping_full_YYYYMMDD_HHMMSS.csv`**
   - All fields from all pages with full metadata
   - Columns: page_url, page_type, tab_name, category, label, value, selector, has_data

2. **`page_structure_YYYYMMDD_HHMMSS.csv`**
   - Summary of all crawled pages
   - Columns: url, page_type, title, depth, num_tabs, tabs, num_fields, num_links

3. **`crawl_results_YYYYMMDD_HHMMSS.json`**
   - Complete crawl data in JSON format
   - Includes sitemap and page relationships

4. **`sitemap_YYYYMMDD_HHMMSS.txt`**
   - Human-readable application structure map

**Usage:**

```bash
jupyter notebook application_crawler.ipynb
```

**Example Output:**

```
PHASE 1: SEARCH-BASED DISCOVERY
═══════════════════════════════════════

[Search Query: 'covid']
  Performing search: 'covid'
  Extracting search result metrics...
  Extracting filter fields...
  Found 5 search result tabs: Hypotheses, Articles, Clinical Trials, Grants, Researchers
    → Clicking search tab: Clinical Trials (20.1K results)
      Found 85 detail pages, sampling 5
  ✓ Search results page: 67 fields, 25 detail pages discovered

PHASE 2: DETAIL PAGE CRAWLING
═══════════════════════════════════════
Queue: 25 pages to crawl

[5/50] Depth 1
  Crawling: /clinical-trial/ASC-CT-0000000174586-1.0-1745776457
  - Found 4 tabs: Overview, Works, Hypotheses, Patents
    → Clicking tab: Works
  ✓ Total fields extracted: 89

CRAWL SUMMARY
═══════════════════════════════════════
Total Pages: 47
Total Fields: 2,341

Pages by Type:
search_results           2
clinical_trial_detail   25
work_detail             15
patent_detail            5

Fields by Category:
search_filter          45  ← Publication Year, Researcher, Source filters
search_result_count    10  ← Tab counts (177.9K, 1.2M, 20.1K, etc.)
metadata              567  ← Conditions, Phase, Enrollment, etc.
labeled_field         892
button_metric          45
```

---

### 3. `selenium_field_mapper.ipynb`
Single-page field mapper (use `application_crawler.ipynb` for full application mapping).

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

## Which Tool Should I Use?

| Use Case | Recommended Tool |
|----------|------------------|
| **Map entire application structure** | `application_crawler.ipynb` |
| **Discover all pages and relationships** | `application_crawler.ipynb` |
| **Find all tabs/sections in detail pages** | `application_crawler.ipynb` |
| **Build comprehensive sitemap** | `application_crawler.ipynb` |
| **Map specific known pages only** | `selenium_field_mapper.ipynb` |
| **Quick field extraction from 1-2 pages** | `selenium_field_mapper.ipynb` |
| **Performance testing** | `test_load_times.ipynb` |

**TL;DR**: Use `application_crawler.ipynb` for complete application mapping. It does everything the field mapper does, plus automatic discovery.

## Configuration

### Application Crawler Configuration

```python
# Search queries - the application uses search-based navigation
SEARCH_QUERIES = [
    "covid",        # Broad medical topic
    "cancer",       # Another broad topic
    "diabetes",     # Chronic disease
    # Add more search terms to discover different data
]

# Crawl limits
MAX_PAGES_TO_CRAWL = 50  # Increase for full crawl (e.g., 200)
MAX_RESULTS_PER_SEARCH_TAB = 5  # Sample size per search tab
MAX_DEPTH = 3  # How many levels deep

# Additional URLs (optional)
ADDITIONAL_URLS = [
    "https://app.allsci.com/explore/clinical-trials",  # Atlas view
]
```

**Key Settings Explained:**

- `SEARCH_QUERIES`: Search terms to start discovery (e.g., "covid" finds 177K hypotheses, 1.2M articles, 20K trials)
- `MAX_RESULTS_PER_SEARCH_TAB`: How many detail pages to visit from each search tab (prevents crawling millions of records)
- `MAX_PAGES_TO_CRAWL`: Hard limit on total pages to prevent runaway crawling
- `MAX_DEPTH`: How many levels to follow from detail pages (detail → related work → etc.)

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
