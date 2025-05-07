import pandas as pd
# Load the dataset
df = pd.read_csv("cloud_architect_jobs_large.csv")
# Field-Level Validation
# 1. Salary Range Validation
valid_salary_range = (50000 <= df['Salary_USD']) &
(df['Salary_USD'] <= 250000)
invalid_salaries = df[~valid_salary_range]
print("Invalid Salaries:\n", invalid_salaries)
# 2. Experience Level Validation
valid_experience_levels = ['Entry-Level', 'Mid-Level', 'Senior']
invalid_experience =
df[~df['Experience_Level'].isin(valid_experience_levels)]
print("Invalid Experience Levels:\n", invalid_experience)
# 3. Skills Validation (check for common skills)
common_skills = ['DevOps', 'AWS', 'Azure', 'Kubernetes', 'GCP',
'Machine Learning']
invalid_skills = df[~df['Skills'].apply(lambda x: any(skill in x
for skill in common_skills))]
print("Invalid Skills:\n", invalid_skills)
# 4. Location Validation (check for valid format)
valid_location_format = df['Location'].str.contains(r'^[A-Za-z\s]+,\s[A-Z]{2}$')
invalid_locations = df[~valid_location_format]
print("Invalid Locations:\n", invalid_locations)
print("Data Validation Summary:")
print(f"Invalid Salaries: {len(invalid_salaries)}")
print(f"Invalid Experience Levels: {len(invalid_experience)}")
print(f"Invalid Skills: {len(invalid_skills)}")
print(f"Invalid Locations: {len(invalid_locations)}")