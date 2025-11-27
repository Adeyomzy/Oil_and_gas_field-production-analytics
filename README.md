# Oil & Gas Field Production Analytics Dashboard

### Dashboard Link : [Power BI Dashboard](https://app.powerbi.com/groups/me/reports/)

## Problem Statement

This dashboard helps oil and gas operators understand their field and well performance better. It provides insights into production trends, field maturity analysis, and creaming curve visualization for exploration success. Through comprehensive production metrics and discovery analytics, operators can identify underperforming assets, optimize production strategies, and make informed decisions about future exploration investments.

The dashboard enables operators to:
- Track cumulative oil, gas, and water production across fields and wells
- Monitor production decline rates and identify intervention opportunities
- Analyze discovery success through creaming curve visualization
- Compare field performance across different regions and operators
- Evaluate well performance by completion type, lift method, and reservoir characteristics
- Understand the relationship between discovery size and timing to guide exploration strategy

By visualizing production data alongside discovery metrics, operators can prioritize capital allocation, schedule workovers, and identify optimal drilling locations within mature fields.

### Key Features

- **Creaming Curve Analysis**: Visualize cumulative discoveries over time to understand exploration maturity
- **Production Performance**: Track daily and cumulative production metrics (oil, gas, water)
- **Field Comparison**: Compare performance across multiple fields and operators
- **Well Analytics**: Analyze well performance by type, completion method, and lift mechanism
- **Decline Analysis**: Monitor production decline rates and forecast future performance
- **Pressure & Operational Metrics**: Track FTHP, FLP, choke settings, and separator conditions

---

## Data Model

The dashboard is built on a star schema with the following structure:

### Dimension Tables:
- **dim_date**: Date dimension with year, quarter, month, week attributes (2010-2024)
- **dim_field**: Field master data including discovery year, operator, region, and discovery volumes
- **dim_well**: Well master data with completion details, lift method, API gravity, and well type
- **dim_reservoir**: Reservoir information with depth and fluid type

### Fact Tables:
- **fact_well_daily_prod**: Daily production data with operational parameters (pressure, temperature, choke, production rates)
- **fact_field_creaming_curve**: Cumulative discovery metrics by field and discovery sequence

### Key Metrics Available:
- Oil Production (BOPD, Cumulative BBL)
- Gas Production (MMSCFD, Cumulative SCF)
- Water Production (BWPD, Cumulative BBL)
- Water Cut (%)
- Gas-Oil Ratio (SCF/BBL)
- Production Decline Rate (%)
- Discovery Volumes (Oil MMBBL, Gas BCF, Total MMBOE)
- Operational Metrics (FTHP, FLP, Separator Pressure/Temperature, Choke Size, API Gravity)

---

## Steps Followed

### Data Preparation & Modeling

- **Step 1**: Loaded multiple data sources into Power BI Desktop:
  - Daily well production data (fact_well_daily_prod.xlsx)
  - Field dimension (dim_field.csv)
  - Well dimension (dim_well.csv)
  - Reservoir dimension (dim_reservoir.csv)
  - Date dimension (dim_date.csv)
  - Field creaming curve data (fact_field_creaming_curve.csv)

- **Step 2**: Opened Power Query Editor and performed data quality checks:
  - Enabled "column distribution", "column quality" & "column profile" options
  - Set column profiling to analyze entire dataset
  - Validated data types for all columns (dates, decimals, integers)

- **Step 3**: Data Transformation in Power Query:
  - Handled null values in production metrics (excluded from calculations)
  - Created calculated columns for derived metrics:
    - Oil_Production_BOPD = Daily_Production_BLPD * (100 - Water_Cut_Percent) / 100
    - Water_Production_BWPD = Daily_Production_BLPD * Water_Cut_Percent / 100
    - Gas_Production_MMSCFD = Oil_Production_BOPD * GOR_scf_bbl / 1,000,000
  - Standardized field and well identifiers for relationship mapping

- **Step 4**: Established relationships in the data model:
  - fact_well_daily_prod[Date] → dim_date[Date] (Many-to-One)
  - fact_well_daily_prod[Well_ID] → dim_well[Well_ID] (Many-to-One)
  - fact_well_daily_prod[Field_ID] → dim_field[Field_ID] (Many-to-One)
  - dim_well[Reservoir_ID] → dim_reservoir[Reservoir_ID] (Many-to-One)
  - fact_field_creaming_curve[Field_ID] → dim_field[Field_ID] (Many-to-One)

### Dashboard Design & Visualizations

- **Step 5**: Selected appropriate theme for oil & gas industry (professional dark/corporate theme)

- **Step 6**: Created KPI Cards for key metrics:
  - Total Oil Production (MMBBL)
  - Total Gas Production (BCF)
  - Total Water Production (MMBBL)
  - Active Wells Count
  - Average Daily Oil Production (BOPD)
  - Average Water Cut (%)
  - Number of Fields
  - Total Discovery Volumes (MMBOE)

- **Step 7**: Built Production Trend Visualizations:
  - Line chart showing oil, gas, and water production over time
  - Area chart displaying cumulative production by field
  - Column chart comparing production by operator
  - Stacked bar chart showing production by well type (vertical, horizontal, deviated)

- **Step 8**: Developed Creaming Curve Analysis:
  - Line chart plotting cumulative discovery (MMBOE) vs. discovery rank
  - Scatter plot showing discovery size by discovery year
  - Bar chart displaying top fields by discovery volume
  - Timeline visualization of major discoveries

- **Step 9**: Added Interactive Slicers:
  - Date range slicer (Year, Quarter, Month)
  - Field multi-select slicer
  - Operator slicer
  - Well Type slicer (Oil Producer, Gas Producer, Injector)
  - Well Bore Type slicer (Vertical, Horizontal, Deviated)
  - Production Status slicer (Active, Shut-in, Abandoned)
  - Lift Method slicer (Natural Flow, ESP, Gas Lift)
  - Region slicer

- **Step 10**: Created Well Performance Analysis:
  - Table showing top producing wells with key metrics
  - Gauge charts for pressure metrics (FTHP, FLP, Casing Pressure)
  - Scatter plot: API Gravity vs. Production Rate
  - Heat map: Well performance by completion date and reservoir

- **Step 11**: Built Decline Analysis Section:
  - Line chart showing production decline curves by well
  - Calculated field for decline rate: 
    ```DAX
    Decline_Rate = 
    VAR PrevProd = CALCULATE([Total Oil Production], DATEADD(dim_date[Date], -1, MONTH))
    VAR CurrentProd = [Total Oil Production]
    RETURN
    IF(PrevProd <> 0, (CurrentProd - PrevProd) / PrevProd * 100, BLANK())
    ```
  - Moving average trend line for decline forecasting

- **Step 12**: Added Field Maturity Classification:
  - Created calculated column in dim_field:
    ```DAX
    Maturity_Classification = 
    VAR YearsProducing = YEAR(TODAY()) - dim_field[Discovery_Year]
    RETURN
    SWITCH(
        TRUE(),
        YearsProducing >= 25, "Mature",
        YearsProducing >= 15, "Developed",
        YearsProducing >= 5, "Developing",
        "New"
    )
    ```
  - Donut chart showing field distribution by maturity level

- **Step 13**: Created Operational Metrics Dashboard Page:
  - Gauge visuals for real-time pressure monitoring
  - Line chart for separator temperature trends
  - Scatter plot: Choke size vs. Production rate
  - Table with well test results (TestGross, TestNet, TestGas, TestWater)

- **Step 14**: Designed Report Header & Branding:
  - Added company logo placeholder
  - Inserted text boxes for report title and description
  - Applied consistent color scheme (blues/greens for production, reds for alerts)
  - Added navigation buttons between pages

### DAX Measures Created

- **Step 15**: Total Production Measures:
  ```DAX
  Total Oil Production (BBL) = SUM(fact_well_daily_prod[Oil_Production_BOPD])
  
  Total Gas Production (SCF) = SUM(fact_well_daily_prod[Gas_Production_MMSCFD]) * 1000000
  
  Total Water Production (BBL) = SUM(fact_well_daily_prod[Water_Production_BWPD])
  
  Average Water Cut % = AVERAGE(fact_well_daily_prod[Water_Cut_Percent])
  ```

- **Step 16**: Cumulative Production Measures:
  ```DAX
  Cumulative Oil Production = 
  CALCULATE(
      [Total Oil Production (BBL)],
      FILTER(
          ALL(dim_date[Date]),
          dim_date[Date] <= MAX(dim_date[Date])
      )
  )
  ```

- **Step 17**: Well Count Measures:
  ```DAX
  Active Wells = 
  CALCULATE(
      DISTINCTCOUNT(dim_well[Well_ID]),
      dim_well[Status] = "Active"
  )
  
  Total Wells = DISTINCTCOUNT(dim_well[Well_ID])
  
  % Active Wells = DIVIDE([Active Wells], [Total Wells], 0) * 100
  ```

- **Step 18**: Discovery Metrics:
  ```DAX
  Total Discovery Oil (MMBBL) = SUM(dim_field[Discovery_Oil_MMBBL])
  
  Total Discovery Gas (BCF) = SUM(dim_field[Discovery_Gas_BCF])
  
  Total Discovery BOE (MMBOE) = SUM(dim_field[Discovery_Total_MMBOE])
  
  Average Discovery Size = AVERAGE(dim_well[Discovery_Total_MMBOE])
  ```

- **Step 19**: Production Performance Indicators:
  ```DAX
  Production per Well (BOPD) = 
  DIVIDE([Total Oil Production (BBL)], [Active Wells], 0)
  
  GOR Average = AVERAGE(fact_well_daily_prod[GOR_scf_bbl])
  
  Peak Production = MAX(fact_well_daily_prod[Oil_Production_BOPD])
  ```

- **Step 20**: Time Intelligence Measures:
  ```DAX
  YTD Oil Production = 
  TOTALYTD([Total Oil Production (BBL)], dim_date[Date])
  
  Prior Year Oil Production = 
  CALCULATE(
      [Total Oil Production (BBL)],
      SAMEPERIODLASTYEAR(dim_date[Date])
  )
  
  YoY Growth % = 
  DIVIDE(
      [Total Oil Production (BBL)] - [Prior Year Oil Production],
      [Prior Year Oil Production],
      0
  ) * 100
  ```

### Final Steps

- **Step 21**: Applied row-level security (RLS) for operator-specific access (if required)

- **Step 22**: Created bookmarks for key views and insights

- **Step 23**: Added drill-through functionality:
  - From field view to well-level details
  - From production trends to specific well analysis

- **Step 24**: Optimized dashboard performance:
  - Aggregated daily data to monthly where appropriate
  - Disabled auto date/time to reduce model size
  - Set incremental refresh for fact tables

- **Step 25**: Published dashboard to Power BI Service with scheduled refresh

---

## Dashboard Pages

### Page 1: Executive Summary
- KPI cards with total production metrics
- Production trend over time (oil, gas, water)
- Top 5 fields by production
- Field maturity distribution
- Operator performance comparison

### Page 2: Creaming Curve Analysis
- Cumulative discovery vs. rank chart
- Discovery timeline by field
- Discovery size distribution
- Regional discovery comparison
- Exploration success metrics

### Page 3: Well Performance
- Well production ranking table
- Production by well type and completion method
- Lift method effectiveness analysis
- Well status distribution
- API gravity vs. production scatter plot

### Page 4: Operational Metrics
- Pressure monitoring (FTHP, FLP, Separator)
- Temperature trends
- Choke settings analysis
- GOR and water cut trends
- Well test results comparison

### Page 5: Decline Analysis
- Production decline curves
- Decline rate by field and well
- Forecasted production
- Intervention opportunity identification

---

## Sample Insights

Based on the data analysis, the following insights can be derived:

### [1] Production Overview

**Total Production Statistics:**
- Total Oil Production: Calculated from daily BOPD aggregated across all wells
- Total Gas Production: Derived from GOR and oil production rates
- Total Water Production: Based on water cut percentages
- Active Wells: Count of wells with "Active" status

**Field Performance:**
- Umutu Field (F001): Mature field operated by Shell Nigeria since 1988
- Koluama Field (F002): Mature field operated by ExxonMobil Nigeria since 1992
- Tombo Field (F003): Developed field operated by Chevron Nigeria since 1995
- Nembe Field (F004): Developing field operated by Total E&P Nigeria since 2003
- Oguta Field (F005): Development stage field operated by Shell Nigeria since 2008

### [2] Discovery Analysis (Creaming Curve)

**Major Discoveries:**
1. Umutu Field: 225 MMBOE discovered in 1988 (largest discovery)
2. Koluama Field: 47 MMBOE discovered in 1992
3. Tombo Field: 83 MMBOE discovered in 1995

**Discovery Trends:**
- Early discoveries (1988-1995) show largest reserve additions
- Creaming curve indicates basin maturity with declining discovery sizes
- Later discoveries (2003-2008) show smaller field sizes typical of mature exploration

### [3] Well Statistics

**Well Distribution by Type:**
- Oil Producers: Majority of wells
- Gas Producers: Used for gas cap management or gas field development
- Injectors: For pressure maintenance and enhanced recovery

**Completion Methods:**
- Vertical wells: Traditional completions, primarily in early field development
- Horizontal wells: Used for improved reservoir contact and higher productivity
- Deviated wells: For accessing reservoirs under restricted surface locations

**Lift Mechanisms:**
- Natural Flow: Wells with sufficient reservoir pressure
- ESP (Electric Submersible Pump): Most common artificial lift for liquid loading
- Gas Lift: Used in wells with high GOR or gas availability

### [4] Operational Parameters

**Average Metrics:**
- API Gravity: Ranges from 31-34° (medium to light crude oil)
- Water Cut: Increases over field life (typical waterflood response)
- GOR: Monitored for gas cap encroachment or solution gas drive
- Flowing Pressures: Decline over time indicating reservoir depletion

**Production Status Distribution:**
- Active: Wells currently producing
- Shut-in: Temporarily closed for maintenance or economic reasons
- Abandoned: Permanently plugged wells

### [5] Regional & Operator Analysis

**Regional Distribution:**
- Niger Delta: Primary production region for all fields in dataset

**Operator Performance:**
- Shell Nigeria: Operating Umutu and Oguta fields
- ExxonMobil Nigeria: Operating Koluama field
- Chevron Nigeria: Operating Tombo field
- Total E&P Nigeria: Operating Nembe field

### [6] Production Trends

**Typical Patterns Observed:**
- Initial production plateau during primary recovery
- Gradual decline as reservoir pressure depletes
- Water cut increase indicating water breakthrough
- GOR changes reflecting drive mechanism transitions

### [7] Well Performance by Reservoir

**Reservoir Characteristics:**
- Multiple reservoirs per field (RSV001-RSV010)
- Depth ranges: 2,518 to 11,097 feet
- Primary fluid type: Oil
- Reservoir depletion varies by discovery date and production history

---

## Key Performance Indicators (KPIs)

The dashboard tracks the following KPIs:

✅ **Production KPIs:**
- Daily Oil Production (BOPD)
- Daily Gas Production (MMSCFD)
- Daily Water Production (BWPD)
- Cumulative Production (Oil, Gas, Water)

✅ **Efficiency KPIs:**
- Production per Active Well
- Average Water Cut %
- Average GOR (SCF/BBL)
- Well Uptime %

✅ **Asset KPIs:**
- Total Wells (Active/Shut-in/Abandoned)
- Number of Producing Fields
- Field Maturity Distribution
- Discovery Success Rate

✅ **Operational KPIs:**
- Average FTHP (psi)
- Average Separator Pressure (psi)
- Average API Gravity
- Production Decline Rate (%)

---

## Technologies Used

- **Power BI Desktop**: Dashboard development and data modeling
- **Power Query**: Data transformation and cleansing
- **DAX (Data Analysis Expressions)**: Calculated columns and measures
- **Excel**: Source data storage (fact_well_daily_prod.xlsx)
- **CSV Files**: Dimension table storage

---

## Data Sources

| File Name | Description | Type |
|-----------|-------------|------|
| fact_well_daily_prod.xlsx | Daily well production data with operational parameters | Fact Table |
| dim_field.csv | Field master data including discovery information | Dimension |
| dim_well.csv | Well master data with completion and status details | Dimension |
| dim_reservoir.csv | Reservoir information | Dimension |
| dim_date.csv | Date dimension (2010-2024) | Dimension |
| fact_field_creaming_curve.csv | Cumulative discovery data by field | Fact Table |
| Table_details.csv | Data dictionary and column definitions | Documentation |

---

## How to Use This Dashboard

1. **Open the Power BI file**: `field-production-analytics.pbix`
2. **Refresh Data**: Click "Refresh" to load the latest production data
3. **Use Slicers**: Filter by date range, field, operator, or well type
4. **Navigate Pages**: Use the navigation buttons to explore different analyses
5. **Drill Through**: Right-click on fields to drill through to well-level details
6. **Export Data**: Export underlying data for detailed analysis in Excel
7. **Set Alerts**: Configure alerts in Power BI Service for production thresholds

---

## Future Enhancements

- [ ] Integration with real-time SCADA systems for live production monitoring
- [ ] Predictive analytics for production forecasting using machine learning
- [ ] Economic analysis including opex, capex, and netback calculations
- [ ] Well intervention tracking and workover history
- [ ] Reserves estimation and booking visualization
- [ ] Environmental metrics (flaring, emissions, water disposal)
- [ ] Integration with geological maps and well logs
- [ ] Mobile app version for field operations

---

## Data Governance & Quality

- **Data Refresh**: Manual refresh from source files (can be automated in Power BI Service)
- **Data Quality**: Null values in production data are handled appropriately in calculations
- **Historical Data**: Production data from 2010 to 2024
- **Calculated Fields**: All derived metrics documented in Table_details.csv
- **Validation**: Cross-checked with well test data for accuracy

---

## Contact & Support

For questions, issues, or enhancement requests regarding this dashboard, please contact:

- **Repository**: [Oil_and_gas_field-production-analytics](https://github.com/Adeyomzy/Oil_and_gas_field-production-analytics)
- **Owner**: Adeyomzy
- **Branch**: main

---

## License

This project is part of the Oil & Gas Field Production Analytics initiative. Please refer to repository license for usage terms.

---

## Acknowledgments

Special thanks to all contributors and the oil & gas industry professionals who provided domain expertise for this analytics solution.

---

**Last Updated**: November 27, 2025

**Dashboard Version**: 1.0

**Power BI Version**: Latest Desktop Version
