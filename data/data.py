import pandas as pd
import numpy as np
import random
from faker import Faker
import string

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

# Number of students
n_students = 50000

# Create a function to generate student IDs
def generate_student_id(i):
    return f"S{str(i+1).zfill(5)}"  # Creates IDs like S00001, S00002, etc.

# Generate student IDs
student_ids = [generate_student_id(i) for i in range(n_students)]

# Generate first and last names
first_names = [fake.first_name() for _ in range(n_students)]
last_names = [fake.last_name() for _ in range(n_students)]

# Generate realistic emails based on names
def generate_university_email(first_name, last_name, student_id):
    # Different email patterns
    patterns = [
        lambda f, l, sid: f"{f.lower()}.{l.lower()}@university.edu",
        lambda f, l, sid: f"{f[0].lower()}{l.lower()}@university.edu",
        lambda f, l, sid: f"{l.lower()}{f[0].lower()}@university.edu",
        lambda f, l, sid: f"{sid.lower()}@university.edu",
        lambda f, l, sid: f"{f.lower()}_{l.lower()}@university.edu",
        lambda f, l, sid: f"{f.lower()}{random.choice(string.digits)}@university.edu"
    ]
    
    pattern = random.choice(patterns)
    email = pattern(first_name, last_name, student_id)
    
    # Replace any non-alphanumeric characters (except @ and .)
    email = ''.join(c for c in email if c.isalnum() or c in '@._')
    
    return email

emails = [generate_university_email(first_names[i], last_names[i], student_ids[i]) for i in range(n_students)]

# Generate gender (0 for female, 1 for male, using 50/50 distribution)
genders = np.random.choice([0, 1], n_students)

# Generate ages between 18 and 30, with more weight on 18-23
ages = np.random.choice(
    range(18, 31), 
    n_students, 
    p=[0.18, 0.18, 0.18, 0.12, 0.08, 0.05, 0.05, 0.03, 0.03, 0.02, 0.02, 0.02, 0.04]
)

# MODIFIED: Generate departments (only 3 departments now)
departments = ["Computer Science", "Data Science", "Software Engineering"]

# Assign departments with varying frequencies
department_weights = [0.45, 0.25, 0.30]  # Weights for CS, DS, SE
student_departments = np.random.choice(departments, n_students, p=department_weights)

# Generate attendance percentage (normal distribution centered around 85%)
attendance = np.random.normal(85, 10, n_students)
attendance = np.clip(attendance, 40, 100)  # Cap between 40% and 100%
attendance = np.round(attendance, 1)

# Functions to generate correlated academic performance
def generate_base_performance():
    """Generate base academic performance for each student (reflecting overall academic ability)"""
    return np.random.normal(75, 15, n_students)

base_performance = generate_base_performance()

# Add correlation between attendance and performance
performance_with_attendance = base_performance + (attendance - 85) * 0.2

# Generate midterm scores (more influenced by base performance)
def generate_midterm_scores(base):
    noise = np.random.normal(0, 10, n_students)
    scores = base + noise
    return np.clip(scores, 0, 100).round(1)

midterm_scores = generate_midterm_scores(performance_with_attendance)

# Generate assignment averages (correlated with base performance)
def generate_assignment_scores(base):
    noise = np.random.normal(0, 8, n_students)
    scores = base + noise
    return np.clip(scores, 40, 100).round(1)

assignment_avg = generate_assignment_scores(performance_with_attendance)

# Generate quiz averages (slightly more variable)
def generate_quiz_scores(base):
    noise = np.random.normal(0, 12, n_students)
    scores = base + noise
    return np.clip(scores, 30, 100).round(1)

quiz_avg = generate_quiz_scores(performance_with_attendance)

# Generate participation scores (0-10)
def generate_participation_scores(base):
    # Convert base performance (0-100) to participation (0-10)
    base_scaled = base / 10
    noise = np.random.normal(0, 1.5, n_students)
    scores = base_scaled + noise
    return np.clip(scores, 0, 10).round(1)

participation_scores = generate_participation_scores(base_performance)

# Generate project scores (correlated with base performance)
def generate_project_scores(base):
    noise = np.random.normal(0, 9, n_students)
    scores = base + noise
    return np.clip(scores, 40, 100).round(1)

project_scores = generate_project_scores(performance_with_attendance)

# Generate study hours per week (normally distributed, slight correlation with performance)
def generate_study_hours(base):
    # Higher performing students tend to study more, but with significant variance
    base_contribution = (base - 75) / 10  # Convert to -2.5 to 2.5 scale
    mean_hours = 12 + base_contribution   # Center around 12 hours
    noise = np.random.normal(0, 4, n_students)
    hours = mean_hours + noise
    return np.clip(hours, 1, 30).round(1)  # Between 1 and 30 hours

study_hours = generate_study_hours(base_performance)

# MODIFIED: Generate extracurricular activities as binary (1: Yes, 0: No)
# Distribution: 70% Yes, 30% No
extracurricular_participation = np.random.choice([1, 0], n_students, p=[0.7, 0.3])

# Generate internet access at home (1: Yes, 0: No, with 90% having access)
internet_access = np.random.choice([1, 0], n_students, p=[0.9, 0.1])

# Generate parent education level
# 0: Less than High School
# 1: High School
# 2: Some College
# 3: Bachelor's Degree
# 4: Graduate Degree
parent_education_levels = np.random.choice(
    [0, 1, 2, 3, 4], 
    n_students, 
    p=[0.05, 0.15, 0.25, 0.35, 0.2]
)

# Generate stress level (1-10, normally distributed around 6)
def generate_stress_levels():
    stress = np.random.normal(6, 1.8, n_students)
    return np.clip(stress, 1, 10).round().astype(int)

stress_levels = generate_stress_levels()

# Generate sleep hours per night (normally distributed around 7)
def generate_sleep_hours():
    hours = np.random.normal(7, 1.2, n_students)
    return np.clip(hours, 3, 10).round(1)

sleep_hours = generate_sleep_hours()

# Add realistic correlations

# Less sleep correlates with higher stress
for i in range(n_students):
    if sleep_hours[i] < 6:
        # Increase stress for those with less sleep
        stress_levels[i] = min(10, stress_levels[i] + random.choice([1, 2]))
    
    if study_hours[i] > 20:
        # Higher study hours can mean higher stress
        stress_levels[i] = min(10, stress_levels[i] + random.choice([0, 1, 2]))
        
    if internet_access[i] == 0:
        # No internet access slightly lowers academic scores
        assignment_avg[i] = max(40, assignment_avg[i] - random.uniform(2, 5))
        project_scores[i] = max(40, project_scores[i] - random.uniform(3, 7))

# Higher parent education tends to correlate with better academic performance
for i in range(n_students):
    if parent_education_levels[i] >= 3:  # Bachelor's or higher
        base_performance[i] = min(100, base_performance[i] + random.uniform(0, 5))
    elif parent_education_levels[i] <= 1:  # High school or less
        base_performance[i] = max(40, base_performance[i] - random.uniform(0, 3))

# Calculate total marks (assuming a specific weighting)
# Define the weights for each component
weights = {
    'Midterm': 0.25,         # 25% of total grade
    'Assignments': 0.20,     # 20% of total grade 
    'Quizzes': 0.15,         # 15% of total grade
    'Participation': 0.10,   # 10% of total grade (scaled from 0-10 to 0-100)
    'Projects': 0.30         # 30% of total grade
}

# Calculate the weighted total (out of 100)
total_marks = (midterm_scores * weights['Midterm']) + \
             (assignment_avg * weights['Assignments']) + \
             (quiz_avg * weights['Quizzes']) + \
             (participation_scores * 10 * weights['Participation']) + \
             (project_scores * weights['Projects'])

# Round to 2 decimal places
total_marks = np.round(total_marks, 2)

# Assign letter grades based on total marks
def assign_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

grades = [assign_grade(score) for score in total_marks]

# Create the DataFrame
data = {
    'Student_ID': student_ids,
    'First_Name': first_names,
    'Last_Name': last_names,
    'Email': emails,
    'Gender': genders,
    'Age': ages,
    'Department': student_departments,
    'Attendance (%)': attendance,
    'Midterm_Score': midterm_scores,
    'Assignments_Avg': assignment_avg,
    'Quizzes_Avg': quiz_avg,
    'Participation_Score': participation_scores,
    'Projects_Score': project_scores,
    'Total_Marks': total_marks,      # ADDED: Total weighted marks
    'Grade': grades,                 # ADDED: Letter grade
    'Study_Hours_per_Week': study_hours,
    'Extracurricular_Activities': extracurricular_participation,  # MODIFIED: Now binary Yes/No
    'Internet_Access_at_Home': internet_access,
    'Parent_Education_Level': parent_education_levels,
    'Stress_Level (1-10)': stress_levels,
    'Sleep_Hours_per_Night': sleep_hours
}

df = pd.DataFrame(data)

# MODIFIED: Map binary values to Yes/No for better readability
df['Extracurricular_Activities'] = df['Extracurricular_Activities'].map({1: 'Yes', 0: 'No'})
df['Internet_Access_at_Home'] = df['Internet_Access_at_Home'].map({1: 'Yes', 0: 'No'})
df['Gender'] = df['Gender'].map({1: 'Male', 0: 'Female'})

# Save the dataset to a CSV file
df.to_csv("student_dataset.csv", index=False)

# Display the first few rows
print(df.head())

# Display summary statistics
print("\nSummary Statistics:")
print(df.describe(include='all'))

# Analyze key correlations
print("\nKey Correlations (for numeric columns):")
numeric_columns = ['Attendance (%)', 'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg', 
                  'Participation_Score', 'Projects_Score', 'Total_Marks', 'Study_Hours_per_Week', 
                  'Parent_Education_Level', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night']

correlations = df[numeric_columns].corr()
print(correlations[['Total_Marks', 'Midterm_Score', 'Study_Hours_per_Week']])

print("\nDepartment Distribution:")
print(df['Department'].value_counts())

print("\nExtracurricular Activities Distribution:")
print(df['Extracurricular_Activities'].value_counts())

print("\nGrade Distribution:")
print(df['Grade'].value_counts())
print(df['Grade'].value_counts(normalize=True).round(3) * 100, '% of total')

print("\nDataset of 10,000 students successfully generated and saved to 'student_dataset_10k.csv'")