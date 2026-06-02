import pandas as pd
import random
import json
import os

# ==========================================
# 1. CORE TAXONOMY
# ==========================================
TAXONOMY = {
    'Backend': ['Python', 'Java', 'Go', 'Node.js', 'C#'],
    'Frontend': ['React', 'Angular', 'Vue.js', 'TypeScript'],
    'Testing': ['PyTest', 'Selenium', 'Cypress', 'JUnit'],
    'DevOps': ['AWS', 'Docker', 'Kubernetes', 'Terraform'],
    'Data': ['SQL', 'Pandas', 'Spark', 'Tableau']
}
CATEGORIES = list(TAXONOMY.keys())

# ==========================================
# 2. PARAMETERIZED GENERATORS
# ==========================================
def generate_employees(num_employees=60, seniority_profile='balanced', random_seed=42):
    """
    Generates employee data.
    seniority_profile options: 'balanced', 'junior_heavy', 'senior_heavy'
    """
    random.seed(random_seed)
    employee_data = []
    
    for i in range(1, num_employees + 1):
        emp_id = f"E{i:03d}"
        primary_cat = random.choice(CATEGORIES)
        num_primary_skills = random.randint(1, 3)
        specific_skills = random.sample(TAXONOMY[primary_cat], k=num_primary_skills)
        
        # 35% chance of a secondary skill
        if random.random() < 0.35:
            secondary_cat = random.choice([c for c in CATEGORIES if c != primary_cat])
            specific_skills.append(random.choice(TAXONOMY[secondary_cat]))
            
        skill_strings = []
        total_seniority = 0
        
        for skill in specific_skills:
            # Apply the Seniority Profile manipulation
            if seniority_profile == 'junior_heavy':
                level = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
            elif seniority_profile == 'senior_heavy':
                level = random.choices([1, 2, 3], weights=[0.1, 0.3, 0.6])[0]
            else:
                level = random.randint(1, 3) # Balanced
                
            skill_strings.append(f"{skill}:{level}")
            total_seniority += level
            
        skills_formatted = "|".join(skill_strings)
        
        # Base hourly cost calculation
        base_cost = 30 
        hourly_cost = base_cost + (total_seniority * 15) + random.randint(-5, 5)
        
        employee_data.append({
            'Employee_ID': emp_id,
            'Specific_Skills': skills_formatted, 
            'Hourly_Cost': hourly_cost,
            'Max_Hours': 2080
        })
        
    return pd.DataFrame(employee_data)

def generate_tasks(num_projects=13, precedence_prob=0.70, random_seed=42):
    """
    Generates task data with dynamic precedence density.
    """
    random.seed(random_seed + 1) 
    task_data = []
    
    for p in range(1, num_projects + 1):
        proj_id = f"P{p:03d}"
        num_tasks = random.randint(2, 20)
        project_task_history = [] 
        
        for t in range(1, num_tasks + 1):
            task_id = f"{proj_id}_T{t}"
            task_cat = random.choice(CATEGORIES)
            num_req_skills = random.randint(1, 2)
            req_skills = random.sample(TAXONOMY[task_cat], k=num_req_skills)
            
            req_strings = []
            for skill in req_skills:
                req_strings.append(f"{skill}:{random.randint(1, 3)}")
            req_formatted = "|".join(req_strings)
            
            hours = random.randint(1, 6) * 10 
            
            # Dynamic Precedence Logic based on probability parameter
            predecessors = []
            if t > 1 and random.random() < precedence_prob:
                num_preds = random.randint(1, min(2, len(project_task_history)))
                predecessors = random.sample(project_task_history, k=num_preds)
                
            project_task_history.append(task_id)
            
            task_data.append({
                'Project_ID': proj_id,
                'Task_ID': task_id,
                'Skills_Needed': req_formatted,
                'Hours_Needed': hours,
                'Predecessors': json.dumps(predecessors)
            })
            
    return pd.DataFrame(task_data)

# ==========================================
# 3. BASELINE EXPORT UTILITY
# ==========================================
def export_baseline(output_dir='../base_data'):
    """Generates standard CSVs for initial testing."""
    os.makedirs(output_dir, exist_ok=True)
    
    df_emp = generate_employees()
    df_task = generate_tasks()
    
    df_emp.to_csv(f"{output_dir}/employees.csv", index=False)
    df_task.to_csv(f"{output_dir}/tasks.csv", index=False)
    print(f"✅ Baseline data successfully exported to {output_dir}")

if __name__ == "__main__":
    export_baseline()