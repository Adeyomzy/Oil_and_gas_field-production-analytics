import pandas as pd
import numpy as np
from datetime import datetime
import random
import os

# Settings
np.random.seed(42)
random.seed(42)

# Output directory
DATA_DIR = 'Data'
os.makedirs(DATA_DIR, exist_ok=True)

print("=" * 90)
print("GENERATING NIGERIAN OIL & GAS DATASET (CSV EXPORT)")
print("=" * 90)
print()

# 1. Fields dimension table
fields = {
    'Field_ID': ['F001', 'F002', 'F003', 'F004', 'F005'],
    'Field_Name': ['Umutu Field', 'Koluama Field', 'Tombo Field', 'Nembe Field', 'Oguta Field'],
    'Region': ['Niger Delta'] * 5,
    'Discovery_Year': [1988, 1992, 1995, 2003, 2008],
    'Development_Stage': ['Production'] * 5,
    'Maturity_Level': ['Mature', 'Mature', 'Developed', 'Developing', 'Development'],
    'Operator': ['Shell Nigeria', 'ExxonMobil Nigeria', 'Chevron Nigeria', 'Total E&P Nigeria', 'Shell Nigeria']
}
df_field = pd.DataFrame(fields)
df_field.to_csv(os.path.join(DATA_DIR, 'dim_field.csv'), index=False)
print("dim_field.csv written.")

# 2. Dates dimension table
start_date = '2010-01-01'
end_date = '2024-12-31'
dates = pd.date_range(start=start_date, end=end_date, freq='D')
df_date = pd.DataFrame({
    'Date': dates,
    'Year': dates.year,
    'Quarter': 'Q' + ((dates.month - 1) // 3 + 1).astype(str),
    'Month': dates.month,
    'Month_Name': dates.strftime('%B'),
    'Day_of_Week': dates.dayofweek + 1,
    'Day_of_Week_Name': dates.strftime('%A'),
    'Week_of_Year': dates.isocalendar().week,
    'Day_of_Year': dates.dayofyear
})
df_date.to_csv(os.path.join(DATA_DIR, 'dim_date.csv'), index=False)
print("dim_date.csv written.")

# 3. Reservoirs dimension table
reservoirs = []
reservoirs_by_field = {}
reservoir_counter = 1
for _, field in df_field.iterrows():
    field_id = field['Field_ID']
    reservoirs_by_field[field_id] = []
    num_res = 2  # two reservoirs per field
    for i in range(1, num_res + 1):
        res_id = f"RSV{reservoir_counter:03d}"
        reservoirs_by_field[field_id].append(res_id)
        reservoirs.append({
            'Reservoir_ID': res_id,
            'Field_ID': field_id,
            'Reservoir_Name': f"{field['Field_Name'].split()[0]} Reservoir {i}",
            'Fluid_Type': random.choices(['Oil', 'Gas', 'Condensate'], weights=[0.85, 0.1, 0.05])[0],
            'Depth_ft': random.randint(6500, 11500)
        })
        reservoir_counter += 1
df_reservoir = pd.DataFrame(reservoirs)
df_reservoir.to_csv(os.path.join(DATA_DIR, 'dim_reservoir.csv'), index=False)
print("dim_reservoir.csv written.")

# 4. Wells dimension table
wells = []
well_bore_types = ['Vertical', 'Deviated', 'Horizontal']
field_abbr = {'F001': 'UMU', 'F002': 'KOL', 'F003': 'TOM', 'F004': 'NEM', 'F005': 'OGU'}
for idx, field in df_field.iterrows():
    field_id = field['Field_ID']
    operator = field['Operator']
    discovery_year = field['Discovery_Year']
    field_name = field['Field_Name']
    abbr = field_abbr[field_id]
    num_wells = random.randint(8, 10)
    for well_num in range(1, num_wells+1):
        well_letter = chr(64 + ((well_num - 1) % 2 + 1))
        well_id = f"{abbr}-{well_num:03d}{well_letter}"
        well_name = f"{field_name.split()[0]}-{well_num:03d}{well_letter}"
        spud_year = random.randint(discovery_year, 2020)
        depth_meters = random.randint(2400, 4300)
        api_gravity = round(random.uniform(31.0, 34.0), 1)
        well_bore_type = random.choice(well_bore_types)
        well_type = random.choices(['Oil Producer', 'Gas Producer', 'Injector'], weights=[0.85, 0.1, 0.05])[0]
        status_rand = random.random()
        if status_rand < 0.65:
            status = 'Active'
        elif status_rand < 0.90:
            status = 'Shut-in'
        else:
            status = 'Abandoned'
        status_change_year = random.randint(2010, 2024)
        status_change_month = random.randint(1, 12)
        status_change_day = random.randint(1, 28)
        status_change_date = f"{status_change_year}-{status_change_month:02d}-{status_change_day:02d}"
        comp_year = min(spud_year + random.randint(0, 2), 2024)
        comp_month = random.randint(1, 12)
        comp_day = random.randint(1, 28)
        completion_date = datetime(comp_year, comp_month, comp_day)
        lift_method = random.choices(['Natural Flow', 'ESP', 'Gas Lift'], weights=[0.5, 0.3, 0.2])[0]
        reservoir_id = random.choice(reservoirs_by_field[field_id])
        wells.append({
            'Well_ID': well_id,
            'Field_ID': field_id,
            'Reservoir_ID': reservoir_id,
            'Well_Name': well_name,
            'Well_Type': well_type,
            'Well_Bore_Type': well_bore_type,
            'Completion_Date': completion_date,
            'Lift_Method': lift_method,
            'Spud_Year': spud_year,
            'Depth_Meters': depth_meters,
            'API_Gravity': api_gravity,
            'Status': status,
            'Status_Change_Date': status_change_date,
            'Operator': operator
        })
df_well = pd.DataFrame(wells)
df_well.to_csv(os.path.join(DATA_DIR, 'dim_well.csv'), index=False)
print("dim_well.csv written.")

# 5. fact_well_daily_production
production_records = []
total_wells = len(df_well)
counter = 0
for well_idx, well in df_well.iterrows():
    counter += 1
    if counter % 5 == 0:
        print(f"      Processing well {counter}/{total_wells}")
    well_id = well['Well_ID']
    field_id = well['Field_ID']
    reservoir_id = well['Reservoir_ID']
    operator = well['Operator']
    spud_year = well['Spud_Year']
    status = well['Status']
    well_bore_type = well['Well_Bore_Type']
    base_API = well['API_Gravity']
    prod_start = datetime(spud_year + 1, 1, 1)
    status_change = pd.to_datetime(well['Status_Change_Date'])
    for date_idx, date_row in df_date.iterrows():
        current_date = pd.to_datetime(date_row['Date'])
        if current_date < prod_start:
            continue
        if status == 'Abandoned' and current_date > status_change:
            continue
        is_producing = False
        if status == 'Active':
            is_producing = True
        elif status == 'Shut-in':
            is_producing = random.random() < 0.15
        else:
            is_producing = False
        if is_producing:
            prod_status = 'Producing'
            if well_bore_type == 'Vertical':
                base_prod = random.uniform(200, 500)
            elif well_bore_type == 'Deviated':
                base_prod = random.uniform(250, 600)
            else:
                base_prod = random.uniform(350, 800)
            production_hours = random.uniform(20, 24)
            daily_variation = random.gauss(1.0, 0.08)
            daily_production = max(base_prod * daily_variation, 10)
            days_since_spud = (current_date.year - spud_year) * 365
            base_water_cut = min(10 + (days_since_spud / 365) * 2, 70)
            daily_water_cut = max(min(base_water_cut + random.gauss(0, 3), 95), 5)
            base_gor = random.uniform(800, 2000)
            daily_gor = max(base_gor + random.gauss(0, 100), 100)
            FTHP = round(random.uniform(450, 1200), 1)
            FLP = round(random.uniform(200, 700), 1)
            MFP = round(random.uniform(180, 650), 1)
            CasingPress = round(random.uniform(500, 1300), 1)
            SepPressure = round(random.uniform(120, 250), 1)
            SepTemp = round(random.uniform(85, 110), 1)
            ChokeSize = random.choice([24, 28, 32, 38])
            API_Gravity = base_API
            BSW = daily_water_cut
            TEST_GROSS_BLPD = daily_production + random.uniform(-10, 10)
            TEST_NET_BOPD = TEST_GROSS_BLPD * (1 - BSW / 100)
            TEST_GAS_MMSCF = (TEST_NET_BOPD * daily_gor) / 1_000_000
            TEST_WATER_BBL = TEST_GROSS_BLPD * (BSW / 100)
        else:
            if status == 'Shut-in':
                prod_status = 'Shut-in'
            else:
                prod_status = 'Abandoned'
            production_hours = 0
            daily_production = 0
            daily_water_cut = 0
            daily_gor = 0
            BSW = 0
            TEST_GROSS_BLPD = 0
            TEST_NET_BOPD = 0
            TEST_GAS_MMSCF = 0
            TEST_WATER_BBL = 0
            if status == 'Shut-in':
                FTHP = round(random.uniform(100, 400), 1)
                FLP = round(random.uniform(50, 200), 1)
                MFP = round(random.uniform(40, 180), 1)
                CasingPress = round(random.uniform(200, 600), 1)
                SepPressure = 0
                SepTemp = 0
                ChokeSize = 0
            else:
                FTHP = 0
                FLP = 0
                MFP = 0
                CasingPress = 0
                SepPressure = 0
                SepTemp = 0
                ChokeSize = 0
            API_Gravity = base_API
        production_records.append({
            'Date': date_row['Date'],
            'Field_ID': field_id,
            'Reservoir_ID': reservoir_id,
            'Well_ID': well_id,
            'Operator': operator,
            'Production_Status': prod_status,
            'Production_Time_Hours': round(production_hours, 1),
            'FTHP_psi': FTHP,
            'FLP_psi': FLP,
            'MFP_psi': MFP,
            'CasingPressure_psi': CasingPress,
            'SeparatorPressure_psi': SepPressure,
            'SeparatorTemp_F': SepTemp,
            'CHOKE_64': ChokeSize,
            'API_Gravity': API_Gravity,
            'Daily_Production_BLPD': round(daily_production, 2),
            'BSW_percent': round(BSW, 2),
            'GOR_scf_bbl': round(daily_gor, 1),
            'TestGross_BLPD': round(TEST_GROSS_BLPD, 2),
            'TestNet_BOPD': round(TEST_NET_BOPD, 2),
            'TestGas_MMSCFD': round(TEST_GAS_MMSCF, 4),
            'TestWater_BBL': round(TEST_WATER_BBL, 2),
            'Water_Cut_Percent': round(BSW, 2),
            'Oil_Production_BOPD': None,
            'Water_Production_BWPD': None,
            'Gas_Production_MMSCFD': None,
            'Water_Cut_Calc_percent': None,
            'GOR_Calc_scf_bbl': None,
            'Cumulative_Oil_Production_bbl': None,
            'Cumulative_Gas_Production_scf': None,
            'Cumulative_Water_Production_bbl': None,
            'Produced_Water_Cut_percent': None,
            'Days_On_Production': None,
            'Production_Decline_Rate_percent': None
        })
df_production = pd.DataFrame(production_records)
df_production.to_csv(os.path.join(DATA_DIR, 'fact_well_daily_prod.csv'), index=False)
print("fact_well_daily_prod.csv written.")

# 6. fact_field_creaming_curve (metadata only, metrics empty)
field_creaming_rows = []
for _, fld in df_field.iterrows():
    field_creaming_rows.append({
        'Field_ID': fld['Field_ID'],
        'Field_Name': fld['Field_Name'],
        'Discovery_Year': fld['Discovery_Year'],
        'Region': fld['Region'],
        'Operator': fld['Operator'],
        'Cumulative_Oil_Production_bbl': None,
        'Cumulative_Gas_Production_scf': None,
        'Cumulative_Water_Production_bbl': None,
        'Peak_Production_BOPD': None,
        'Peak_Production_Year': None,
        'Average_Production_BOPD': None,
        'Production_Life_Years': None,
        'Rank_by_Discovery_Year': None
    })
df_field_creaming = pd.DataFrame(field_creaming_rows)
df_field_creaming.to_csv(os.path.join(DATA_DIR, 'fact_field_creaming_curve.csv'), index=False)
print("fact_field_creaming_curve.csv written.")

print("\nAll CSVs written to the Data folder.")
print("=" * 90)
print("FORMULAS for CALCULATED COLUMNS (to calculate yourself):")
print("Oil_Production_BOPD:           = [Daily_Production_BLPD]*(100-[Water_Cut_Percent])/100")
print("Water_Production_BWPD:         = [Daily_Production_BLPD]*[Water_Cut_Percent]/100")
print("Gas_Production_MMSCFD:         = [Oil_Production_BOPD]*[GOR_scf_bbl]/1,000,000")
print("Water_Cut_Calc_percent:        = [Water_Production_BWPD]/([Oil_Production_BOPD]+[Water_Production_BWPD])*100")
print("GOR_Calc_scf_bbl:              = [Gas_Production_MMSCFD]*1,000,000/[Oil_Production_BOPD]")
print("Cumulative_Oil_Production_bbl: = SUM([Oil_Production_BOPD]) OVER (by Well ordered by Date)")
print("Cumulative_Water_Production_bbl: = SUM([Water_Production_BWPD]) OVER (by Well ordered by Date)")
print("Cumulative_Gas_Production_scf:   = SUM([Gas_Production_MMSCFD]*1,000,000) OVER (by Well ordered by Date)")
print("Produced_Water_Cut_percent:    = [Cumulative_Water_Production_bbl]/([Cumulative_Oil_Production_bbl]+[Cumulative_Water_Production_bbl])*100")
print("Days_On_Production:            = COUNTIF([Production_Status]=\"Producing\") (for the Well up to current date)")
print("Production_Decline_Rate_percent: = ([Oil_Production_BOPD]-[Prior_Day_Oil_Production_BOPD])/[Prior_Day_Oil_Production_BOPD]*100")
print("=" * 90)
print("SUCCESS! All CSVs are ready in the Data folder.\n")
