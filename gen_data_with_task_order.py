import pandas as pd
import random
import os
import datetime
import json

# ==========================================
# 1. CONFIGURATION 
# ==========================================
CONFIG = {
    'NUM_EMPLOYEES': 25,              
    'NUM_PROJECTS': 4,               
    'MIN_TASKS_PER_PROJ': 2,          
    'MAX_TASKS_PER_PROJ': 4,          
    'SECONDARY_SKILL_PROB': 0.35,     
    'PRECEDENCE_PROB': 0.70,          # 70% chance a task depends on a previous one
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
        
        primary_cat = random.choice(CATEGORIES)
        num_primary_skills = random.randint(1, 3)
        specific_skills = random.sample(TAXONOMY[primary_cat], k=num_primary_skills)
        
        if random.random() < CONFIG['SECONDARY_SKILL_PROB']:
            secondary_cat = random.choice([c for c in CATEGORIES if c != primary_cat])
            specific_skills.append(random.choice(TAXONOMY[secondary_cat]))
            
        # Format as string: "Skill:Level|Skill:Level" to match your parser!
        skill_strings = []
        total_seniority = 0
        for skill in specific_skills:
            level = random.randint(1, 3)
            skill_strings.append(f"{skill}:{level}")
            total_seniority += level
            
        skills_formatted = "|".join(skill_strings)
        
        base_cost = 30 
        hourly_cost = base_cost + (total_seniority * 15) + random.randint(-5, 5)
        
        employee_data.append({
            'Employee_ID': emp_id,
            'Specific_Skills': skills_formatted, 
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
        
        # Keep track of tasks created in THIS project to use as predecessors
        project_task_history = [] 
        
        for t in range(1, num_tasks + 1):
            task_id = f"{proj_id}_T{t}"
            task_cat = random.choice(CATEGORIES)
            num_req_skills = random.randint(1, 2)
            req_skills = random.sample(TAXONOMY[task_cat], k=num_req_skills)
            
            # Format as string: "Skill:Level|Skill:Level"
            req_strings = []
            for skill in req_skills:
                req_strings.append(f"{skill}:{random.randint(1, 3)}")
            req_formatted = "|".join(req_strings)
            
            hours = random.randint(1, 6) * 100 
            
            # --- PRECEDENCE GENERATION LOGIC ---
            predecessors = []
            # Task 1 can never have a predecessor. Task 2+ can.
            if t > 1 and random.random() < CONFIG['PRECEDENCE_PROB']:
                # Pick 1 or 2 tasks that came BEFORE this one in the same project
                num_preds = random.randint(1, min(2, len(project_task_history)))
                predecessors = random.sample(project_task_history, k=num_preds)
                
            project_task_history.append(task_id)
            
            task_data.append({
                'Project_ID': proj_id,
                'Task_ID': task_id,
                'Skills_Needed': req_formatted,
                'Hours_Needed': hours,
                'Predecessors': json.dumps(predecessors) # Save list as JSON array e.g., ["P001_T1"]
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
    print("\nSample Task with Predecessors:")
    display_sample = df_tasks[df_tasks['Predecessors'] != "[]"].head(1)
    print(display_sample[['Task_ID', 'Predecessors']].to_string(index=False))