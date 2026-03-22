"""
Create PRISM real data Excel files based on specifications.
This script generates:
1. _h_batch_production_data.xlsx - 60 batches (T001-T060)
2. _h_batch_process_data.xlsx - 211 rows for T001 across 8 phases
"""
import numpy as np
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

# =============================================================================
# 1. PRODUCTION DATA - 60 batches
# =============================================================================

# Top 5 Golden Batches specs from real data
GOLDEN_BATCHES = {
    'T051': {'Dissolution_Rate': 81.2, 'Hardness': 135.0, 'Friability': 0.29, 'Content_Uniformity': 98.5},
    'T020': {'Dissolution_Rate': 82.3, 'Hardness': 132.0, 'Friability': 0.32, 'Content_Uniformity': 97.8},
    'T031': {'Dissolution_Rate': 83.8, 'Hardness': 128.0, 'Friability': 0.35, 'Content_Uniformity': 97.2},
    'T005': {'Dissolution_Rate': 85.1, 'Hardness': 125.0, 'Friability': 0.38, 'Content_Uniformity': 96.5},
    'T042': {'Dissolution_Rate': 84.5, 'Hardness': 124.0, 'Friability': 0.37, 'Content_Uniformity': 96.8},
}

# Parameter ranges for realistic pharma manufacturing
PARAM_RANGES = {
    'Granulation_Time': (10, 90),
    'Binder_Amount': (2.0, 8.0),
    'Drying_Temp': (45, 75),
    'Drying_Time': (20, 60),
    'Compression_Force': (8.0, 20.0),
    'Machine_Speed': (25, 110),
    'Lubricant_Conc': (0.5, 2.5),
    'Moisture_Content': (2.0, 6.0),
    'Tablet_Weight': (180, 220),
    'Hardness': (100, 140),
    'Friability': (0.25, 0.55),
    'Disintegration_Time': (2, 8),
    'Dissolution_Rate': (75.0, 87.0),
    'Content_Uniformity': (94.0, 99.0),
}

# Generate 60 batches
batch_ids = [f'T{i:03d}' for i in range(1, 61)]
production_data = []

for batch_id in batch_ids:
    if batch_id in GOLDEN_BATCHES:
        # Use exact golden batch specs
        dissolution = GOLDEN_BATCHES[batch_id]['Dissolution_Rate']
        hardness = GOLDEN_BATCHES[batch_id]['Hardness']
        friability = GOLDEN_BATCHES[batch_id]['Friability']
        uniformity = GOLDEN_BATCHES[batch_id]['Content_Uniformity']
        
        # Parameters tuned for golden batches
        row = {
            'Batch_ID': batch_id,
            'Granulation_Time': np.random.uniform(35, 55),
            'Binder_Amount': np.random.uniform(4.5, 6.5),
            'Drying_Temp': np.random.uniform(58, 65),
            'Drying_Time': np.random.uniform(35, 48),
            'Compression_Force': np.random.uniform(14.0, 17.0) if batch_id == 'T051' else np.random.uniform(13.0, 16.0),
            'Machine_Speed': np.random.uniform(55, 75),
            'Lubricant_Conc': np.random.uniform(1.2, 1.8),
            'Moisture_Content': np.random.uniform(3.5, 4.5),
            'Tablet_Weight': np.random.uniform(195, 205),
            'Hardness': hardness,
            'Friability': friability,
            'Disintegration_Time': np.random.uniform(3.5, 5.5),
            'Dissolution_Rate': dissolution,
            'Content_Uniformity': uniformity,
        }
    else:
        # Regular batches with realistic variation
        row = {
            'Batch_ID': batch_id,
            'Granulation_Time': np.random.uniform(*PARAM_RANGES['Granulation_Time']),
            'Binder_Amount': np.random.uniform(*PARAM_RANGES['Binder_Amount']),
            'Drying_Temp': np.random.uniform(*PARAM_RANGES['Drying_Temp']),
            'Drying_Time': np.random.uniform(*PARAM_RANGES['Drying_Time']),
            'Compression_Force': np.random.uniform(*PARAM_RANGES['Compression_Force']),
            'Machine_Speed': np.random.uniform(*PARAM_RANGES['Machine_Speed']),
            'Lubricant_Conc': np.random.uniform(*PARAM_RANGES['Lubricant_Conc']),
            'Moisture_Content': np.random.uniform(*PARAM_RANGES['Moisture_Content']),
            'Tablet_Weight': np.random.uniform(*PARAM_RANGES['Tablet_Weight']),
            'Hardness': np.random.uniform(*PARAM_RANGES['Hardness']),
            'Friability': np.random.uniform(*PARAM_RANGES['Friability']),
            'Disintegration_Time': np.random.uniform(*PARAM_RANGES['Disintegration_Time']),
            'Dissolution_Rate': np.random.uniform(*PARAM_RANGES['Dissolution_Rate']),
            'Content_Uniformity': np.random.uniform(*PARAM_RANGES['Content_Uniformity']),
        }
    
    production_data.append(row)

df_production = pd.DataFrame(production_data)

# Calculate scores to verify T051 is highest
max_diss = df_production['Dissolution_Rate'].max()
max_fri = df_production['Friability'].max()
max_hard = df_production['Hardness'].max()
max_uniform = df_production['Content_Uniformity'].max()

df_production['Score'] = (
    (df_production['Dissolution_Rate'] / max_diss) * 0.30 +
    (1 - df_production['Friability'] / max_fri) * 0.30 +
    (df_production['Content_Uniformity'] / max_uniform) * 0.20 +
    (df_production['Hardness'] / max_hard) * 0.20
)

# Verify T051 has highest score
top_batch = df_production.loc[df_production['Score'].idxmax(), 'Batch_ID']
print(f"Production data created: {len(df_production)} batches")
print(f"Top scoring batch: {top_batch} (score: {df_production['Score'].max():.3f})")
print(f"T051 score: {df_production[df_production['Batch_ID']=='T051']['Score'].values[0]:.3f}")

# Drop Score column as it's computed in the app
df_production_output = df_production.drop(columns=['Score'])

# =============================================================================
# 2. PROCESS DATA - Multiple batches across 8 phases
# =============================================================================

# Phase definitions with real power and vibration stats (golden reference)
PHASES = [
    {'name': 'Preparation', 'duration': 15, 'power_mean': 2.19, 'power_std': 0.3, 'vib_mean': 0.094, 'vib_std': 0.02},
    {'name': 'Granulation', 'duration': 35, 'power_mean': 15.12, 'power_std': 2.0, 'vib_mean': 2.539, 'vib_std': 0.4},
    {'name': 'Drying', 'duration': 45, 'power_mean': 24.21, 'power_std': 3.0, 'vib_mean': 1.825, 'vib_std': 0.3},
    {'name': 'Milling', 'duration': 25, 'power_mean': 36.01, 'power_std': 4.0, 'vib_mean': 8.066, 'vib_std': 1.2},
    {'name': 'Blending', 'duration': 20, 'power_mean': 12.53, 'power_std': 1.5, 'vib_mean': 3.172, 'vib_std': 0.5},
    {'name': 'Compression', 'duration': 40, 'power_mean': 44.65, 'power_std': 4.5, 'vib_mean': 5.344, 'vib_std': 0.8},
    {'name': 'Coating', 'duration': 25, 'power_mean': 20.19, 'power_std': 2.5, 'vib_mean': 2.057, 'vib_std': 0.35},
    {'name': 'Quality_Testing', 'duration': 15, 'power_mean': 4.77, 'power_std': 0.6, 'vib_mean': 0.490, 'vib_std': 0.08},
]

total_duration = sum(p['duration'] for p in PHASES)
print(f"\nTotal batch duration: {total_duration} minutes per batch")

# Generate process data for ALL 60 batches
# Each batch gets slight variation in phase profiles based on its production quality
# Golden batches stay close to reference; poor batches deviate more
process_rows = []

for batch_id in batch_ids:
    # Calculate a quality factor from production data for this batch
    batch_row = df_production[df_production['Batch_ID'] == batch_id].iloc[0]
    # Normalise quality: 1.0 = golden, lower = worse batch
    quality_factor = (
        batch_row['Dissolution_Rate'] / df_production['Dissolution_Rate'].max() * 0.3
        + (1 - batch_row['Friability'] / df_production['Friability'].max()) * 0.3
        + batch_row['Content_Uniformity'] / df_production['Content_Uniformity'].max() * 0.2
        + batch_row['Hardness'] / df_production['Hardness'].max() * 0.2
    )
    # Deviation multiplier: golden batches get ~1.0, poor batches get up to 1.8
    deviation = 1.0 + (1.0 - quality_factor) * 3.0
    
    # Per-batch random seed for reproducibility
    rng = np.random.RandomState(hash(batch_id) % (2**31))
    
    time_counter = 0
    for phase in PHASES:
        phase_duration = phase['duration']
        rows_in_phase = phase_duration + (1 if phase['name'] in ['Drying', 'Compression'] else 0)
        
        # Scale noise by batch quality — golden batches are more consistent
        power_noise = phase['power_std'] * deviation
        vib_noise = phase['vib_std'] * deviation
        # Offset: poorer batches may have shifted means (e.g., higher power = inefficient)
        power_offset = (deviation - 1.0) * phase['power_mean'] * 0.08
        vib_offset = (deviation - 1.0) * phase['vib_mean'] * 0.12
        
        for i in range(rows_in_phase):
            time_minutes = time_counter + i
            
            power = rng.normal(phase['power_mean'] + power_offset, power_noise)
            power = max(0.5, power)
            
            vibration = rng.normal(phase['vib_mean'] + vib_offset, vib_noise)
            vibration = max(0.01, vibration)
            
            if phase['name'] == 'Drying':
                temp = rng.uniform(55, 65) + (deviation - 1.0) * 3
                humidity = rng.uniform(25, 40)
            elif phase['name'] == 'Granulation':
                temp = rng.uniform(35, 45)
                humidity = rng.uniform(40, 60)
            elif phase['name'] == 'Compression':
                temp = rng.uniform(25, 30)
                humidity = rng.uniform(30, 45)
            else:
                temp = rng.uniform(20, 40)
                humidity = rng.uniform(35, 55)
            
            row = {
                'Batch_ID': batch_id,
                'Time_Minutes': time_minutes,
                'Phase': phase['name'],
                'Temperature_C': round(temp, 2),
                'Pressure_Bar': round(rng.uniform(1.0, 3.5), 2),
                'Humidity_Percent': round(humidity, 2),
                'Motor_Speed_RPM': round(rng.uniform(800, 2500), 1),
                'Compression_Force_kN': round(rng.uniform(5.0, 25.0), 2),
                'Flow_Rate_LPM': round(rng.uniform(2.0, 15.0), 2),
                'Power_Consumption_kW': round(power, 3),
                'Vibration_mm_s': round(vibration, 4),
            }
            process_rows.append(row)
        
        time_counter += phase_duration

df_process = pd.DataFrame(process_rows)

# Verify stats
n_batches = df_process['Batch_ID'].nunique()
print(f"\nProcess data created: {len(df_process)} rows across {n_batches} batches")
print(f"Rows per batch: ~{len(df_process) // n_batches}")
print("\nGolden batch T053 power by phase:")
t053_proc = df_process[df_process['Batch_ID'] == 'T053']
for phase in PHASES:
    phase_data = t053_proc[t053_proc['Phase'] == phase['name']]['Power_Consumption_kW']
    if len(phase_data) > 0:
        print(f"  {phase['name']}: {phase_data.mean():.2f} kW (ref: {phase['power_mean']:.2f})")

# Calculate total energy for T001
t001_proc = df_process[df_process['Batch_ID'] == 'T001']
total_kwh = (t001_proc['Power_Consumption_kW'] / 60).sum()
total_co2 = total_kwh * 0.82
print(f"\nT001 batch energy: {total_kwh:.2f} kWh, CO2: {total_co2:.2f} kg")

# =============================================================================
# Save to Excel
# =============================================================================
output_dir = '/Users/karthik/Downloads/iit hyderbad prism/prism'
df_production_output.to_excel(f'{output_dir}/_h_batch_production_data.xlsx', index=False)
df_process.to_excel(f'{output_dir}/_h_batch_process_data.xlsx', index=False)

print(f"\n✅ Excel files created successfully!")
print(f"   - _h_batch_production_data.xlsx ({len(df_production_output)} rows)")
print(f"   - _h_batch_process_data.xlsx ({len(df_process)} rows)")
