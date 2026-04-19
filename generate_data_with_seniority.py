import pandas as pd
import random
import os
import datetime

# 1. CONFIGURATION 
CONFIG = {
    'NUM_EMPLOYEES': 90,
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

SKILL_LEVELS = {
    1: "Novice",
    2: "Intermediate",
    3: "Advanced",
    4: "Expert",
    5: "Master"
}

def generate_employees(seniority=False):
    random.seed(CONFIG['RANDOM_SEED'])
    employee_data = []
    
    for i in range(1, CONFIG['NUM_EMPLOYEES'] + 1):
        emp_id = f"E{i:03d}" # e.g., E001, E015

        primary_cat = random.choice(CATEGORIES)
        if seniority:
            profile_level = random.choices([1, 2, 3, 4, 5], weights=[20, 30, 25, 15, 10])[0]
            
            num_primary_skills = random.randint(1, 3)
            selected_skills = random.sample(TAXONOMY[primary_cat], k=num_primary_skills)
            
            skills_with_levels = []
            total_skill_points = 0
            
            for s in selected_skills:
                # Poziom skilla oscyluje wokół profilu pracownika (+/- 1)
                level = max(1, min(5, profile_level + random.randint(-1, 1)))
                skills_with_levels.append(f"{s}:{level}")
                total_skill_points += level

            # T-Shape: Dodatkowy skill z innej kategorii (zazwyczaj na niższym poziomie)
            if random.random() < CONFIG['SECONDARY_SKILL_PROB']:
                sec_cat = random.choice([c for c in CATEGORIES if c != primary_cat])
                sec_skill = random.choice(TAXONOMY[sec_cat])
                sec_level = max(1, profile_level - random.randint(1, 2))
                skills_with_levels.append(f"{sec_skill}:{sec_level}")
                total_skill_points += sec_level
                
            # Koszt zależy od sumy poziomów skilli (im więcej umiesz i na wyższym poziomie, tym droższy jesteś)
            hourly_cost = 50 + (total_skill_points * 8) + random.randint(-5, 5)
            
            employee_data.append({
                'Employee_ID': emp_id,
                'Profile_Level': profile_level,
                'Primary_Category': primary_cat,
                'Specific_Skills': '|'.join(skills_with_levels),
                'Hourly_Cost': hourly_cost,
                'Max_Hours': 2080
            })

        else:    
            # 1. Assign Primary Category & Skills
            num_primary_skills = random.randint(1, 3)
            specific_skills = random.sample(TAXONOMY[primary_cat], k=num_primary_skills)
            emp_categories = [primary_cat]
            
            # 2. Assign Secondary Category (The "T-Shaped" Developer)
            if random.random() < CONFIG['SECONDARY_SKILL_PROB']:
                # Pick a category that isn't their primary
                secondary_cat = random.choice([c for c in CATEGORIES if c != primary_cat])
                emp_categories.append(secondary_cat)
                # Give them exactly 1 skill from this secondary category
                specific_skills.append(random.choice(TAXONOMY[secondary_cat]))
                
            # 3. Calculate Cost (More skills = higher hourly cost)
            base_cost = 40
            cost_per_skill = 15
            hourly_cost = base_cost + (len(specific_skills) * cost_per_skill) + random.randint(-5, 10)
            
            employee_data.append({
                'Employee_ID': emp_id,
                # We join lists with a pipe '|' to avoid breaking the CSV format
                'Categories': '|'.join(emp_categories),     
                'Specific_Skills': '|'.join(specific_skills),
                'Hourly_Cost': hourly_cost,
                'Max_Hours': 2080
            })
        
    return pd.DataFrame(employee_data)


def generate_tasks(seniority=False):
    random.seed(CONFIG['RANDOM_SEED'] + 1) # Slight offset for independent generation
    task_data = []
    
    for p in range(1, CONFIG['NUM_PROJECTS'] + 1):
        proj_id = f"P{p:03d}"
        num_tasks = random.randint(CONFIG['MIN_TASKS_PER_PROJ'], CONFIG['MAX_TASKS_PER_PROJ'])
        
        for t in range(1, num_tasks + 1):
            task_id = f"{proj_id}_T{t}"
            
            # Tasks usually sit firmly within one category
            task_cat = random.choice(CATEGORIES)

            if seniority:
                # Zadanie wymaga 1-2 skilli, każdy na określonym poziomie
                num_req_skills = random.randint(1, 2)
                req_skills = random.sample(TAXONOMY[task_cat], k=num_req_skills)
                
                req_with_levels = []
                max_req_level = 0
                for rs in req_skills:
                    # Losujemy wymagany poziom (1-5)
                    r_level = random.choices([1, 2, 3, 4, 5], weights=[30, 40, 15, 10, 5])[0]
                    req_with_levels.append(f"{rs}:{r_level}")
                    max_req_level = max(max_req_level, r_level)
                
                # Czas zadania zależy od jego trudności (max_req_level)
                hours = random.randint(2, 6) * 20 * max_req_level
                
                task_data.append({
                    'Project_ID': proj_id,
                    'Task_ID': task_id,
                    'Category': task_cat,
                    'Skills_Needed': '|'.join(req_with_levels),
                    'Complexity_Level': max_req_level,
                    'Hours_Needed': hours
                })


            else:
                # Task requires 1 to 2 specific skills from that category
                num_req_skills = random.randint(1, 2)
                req_skills = random.sample(TAXONOMY[task_cat], k=num_req_skills)
                
                # Hours needed to complete the task
                hours = random.randint(2, 8) * 100 
                
                task_data.append({
                    'Project_ID': proj_id,
                    'Task_ID': task_id,
                    'Category_Needed': task_cat,
                    'Skills_Needed': '|'.join(req_skills),
                    'Hours_Needed': hours
                })
            
    return pd.DataFrame(task_data)

# 3. EXECUTION & EXPORT
if __name__ == "__main__":
    # Generate the dataframes
    df_employees = generate_employees(seniority=True)
    df_tasks = generate_tasks(seniority=True)
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(CONFIG['OUTPUT_DIR']):
        os.makedirs(CONFIG['OUTPUT_DIR'])
        
    # Save to CSV
    emp_path = os.path.join(CONFIG['OUTPUT_DIR'], 'employees.csv')
    task_path = os.path.join(CONFIG['OUTPUT_DIR'], 'tasks.csv')
    
    df_employees.to_csv(emp_path, index=False)
    df_tasks.to_csv(task_path, index=False)
    
    print(f"✅ Successfully generated {len(df_employees)} employees and {len(df_tasks)} tasks.")
    print(f"📁 Saved to: '{CONFIG['OUTPUT_DIR']}' directory.")
    
    print("\n--- Sample Employee ---")
    print(df_employees.iloc[0])
    print("\n--- Sample Task ---")
    print(df_tasks.iloc[0])


