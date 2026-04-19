import pandas as pd
import random
import os
import datetime
import json

# ==========================================
# 1. CONFIGURATION 
# ==========================================
CONFIG = {
    'NUM_EMPLOYEES': 100,              
    'NUM_PROJECTS': 13,               
    'MIN_TASKS_PER_PROJ': 2,          
    'MAX_TASKS_PER_PROJ': 4,          
    'SECONDARY_SKILL_PROB': 0.35,     
    'OUTPUT_DIR': f'dataset_exports/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}',  
    'RANDOM_SEED': 42                 
}

TAXONOMY = {
    'Backend': ['Python', 'Java', 'Go', 'Node.js', 'C#'],
    'Frontend': ['React', 'Angular', 'Vue.js', 'TypeScript'],
    'Testing': ['PyTest', 'Selenium', 'Cypress', 'JUnit'],
    'DevOps': ['AWS', 'Docker', 'Kubernetes', 'Terraform'],
    'Data': ['SQL', 'Pandas', 'Spark', 'Tableau']
}

CATEGORIES = list(TAXONOMY.keys())

# ==========================================
# 2. GENERATION LOGIC
# ==========================================
def generate_employees():
    random.seed(CONFIG['RANDOM_SEED'])
    employee_data = []
    
    for i in range(1, CONFIG['NUM_EMPLOYEES'] + 1):
        emp_id = f"E{i:03d}"
        
        # Determine specific skills
        primary_cat = random.choice(CATEGORIES)
        num_primary_skills = random.randint(1, 3)
        specific_skills = random.sample(TAXONOMY[primary_cat], k=num_primary_skills)
        
        if random.random() < CONFIG['SECONDARY_SKILL_PROB']:
            secondary_cat = random.choice([c for c in CATEGORIES if c != primary_cat])
            specific_skills.append(random.choice(TAXONOMY[secondary_cat]))
            
        # Assign individual seniority to each skill and calculate cost
        skills_dict = {}
        total_seniority_points = 0
        
        for skill in specific_skills:
            level = random.randint(1, 3) # 1=Junior, 2=Mid, 3=Senior
            skills_dict[skill] = level
            total_seniority_points += level
            
        # Cost scales heavily based on total accumulated seniority
        base_cost = 25 
        hourly_cost = base_cost + (total_seniority_points * 15) + random.randint(-5, 5)
        
        employee_data.append({
            'Employee_ID': emp_id,
            'Skills_Dict': json.dumps(skills_dict), # Save as JSON string for clean CSV export
            'Hourly_Cost': hourly_cost,
            'Max_Hours': 2080
        })
        
    return pd.DataFrame(employee_data)

def generate_tasks():
    random.seed(CONFIG['RANDOM_SEED'] + 1) 
    task_data = []
    
    for p in range(1, CONFIG['NUM_PROJECTS'] + 1):
        proj_id = f"P{p:03d}"
        num_tasks = random.randint(CONFIG['MIN_TASKS_PER_PROJ'], CONFIG['MAX_TASKS_PER_PROJ'])
        
        for t in range(1, num_tasks + 1):
            task_id = f"{proj_id}_T{t}"
            task_cat = random.choice(CATEGORIES)
            num_req_skills = random.randint(1, 2)
            req_skills = random.sample(TAXONOMY[task_cat], k=num_req_skills)
            
            # Assign required seniority to each task skill
            req_dict = {}
            for skill in req_skills:
                req_dict[skill] = random.randint(1, 3)
                
            hours = random.randint(2, 8) * 100 
            
            task_data.append({
                'Project_ID': proj_id,
                'Task_ID': task_id,
                'Req_Dict': json.dumps(req_dict), # Save as JSON string
                'Hours_Needed': hours
            })
            
    return pd.DataFrame(task_data)

# ==========================================
# 3. EXECUTION & EXPORT
# ==========================================
if __name__ == "__main__":
    df_employees = generate_employees()
    df_tasks = generate_tasks()
    
    if not os.path.exists(CONFIG['OUTPUT_DIR']):
        os.makedirs(CONFIG['OUTPUT_DIR'])
        
    emp_path = os.path.join(CONFIG['OUTPUT_DIR'], 'employees.csv')
    task_path = os.path.join(CONFIG['OUTPUT_DIR'], 'tasks.csv')
    df_employees.to_csv(emp_path, index=False)
    df_tasks.to_csv(task_path, index=False)
    
    print(f"✅ Data exported to: {CONFIG['OUTPUT_DIR']}")
    print("\nSample Employee Skills:", df_employees['Skills_Dict'].iloc[0])
    print("Sample Task Requirements:", df_tasks['Req_Dict'].iloc[0])