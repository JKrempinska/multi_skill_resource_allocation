import pandas as pd
import random
import json
import os

def generate_nexus_enterprise():
    os.makedirs('base_data', exist_ok=True)
    random.seed(42) # Fixed seed ensures the data is the same every time you run it

    # ==========================================
    # 1. GENERATE THE 48-PERSON WORKFORCE
    # ==========================================
    departments = [
        {"dept": "Frontend", "count": 10, "core_skills": ["React", "Angular", "UIUX"]},
        {"dept": "Backend",  "count": 15, "core_skills": ["Python", "Java", "Node", "Go"]},
        {"dept": "Data",     "count": 8,  "core_skills": ["SQL", "Spark", "Python"]},
        {"dept": "DevOps",   "count": 6,  "core_skills": ["AWS", "Kubernetes", "Go"]},
        {"dept": "QA",       "count": 6,  "core_skills": ["QA", "Python"]},
        {"dept": "Design",   "count": 3,  "core_skills": ["UIUX", "React"]}
    ]

    employees = []
    emp_id_counter = 1

    for d in departments:
        for _ in range(d["count"]):
            # Determine Seniority (20% Junior, 50% Mid, 30% Senior)
            level = random.choices([1, 2, 3], weights=[0.2, 0.5, 0.3])[0]
            
            # Select skills based on department
            num_skills = random.randint(1, 3)
            skills_chosen = random.sample(d["core_skills"], min(num_skills, len(d["core_skills"])))
            
            # Format the skills string
            skill_str = "|".join([f"{s}:{level}" for s in skills_chosen])
            
            # Calculate wages
            if level == 1: base = random.randint(35, 50)
            elif level == 2: base = random.randint(65, 85)
            else: base = random.randint(100, 140)

            employees.append({
                'Employee_ID': f"E{emp_id_counter:03d}",
                'Role': f"{['Junior', 'Mid', 'Senior'][level-1]} {d['dept']}",
                'Specific_Skills': skill_str,
                'Hourly_Cost': base,
                'Max_Hours': 2080
            })
            emp_id_counter += 1

    # Add the expensive Safety Net Contractor
    all_skills = ["React:3", "Angular:3", "Python:3", "Java:3", "Node:3", "Go:3", 
                  "SQL:3", "Spark:3", "AWS:3", "Kubernetes:3", "QA:3", "UIUX:3"]
    employees.append({
        'Employee_ID': 'EXT_CONTRACTOR',
        'Role': 'Enterprise Staffing Agency',
        'Specific_Skills': "|".join(all_skills),
        'Hourly_Cost': 400, # Very expensive to force the solver to use internal staff
        'Max_Hours': 99999
    })

    df_emps = pd.DataFrame(employees)
    df_emps.to_csv('notebooks/base_data/employees_large.csv', index=False)

    # ==========================================
    # 2. GENERATE THE 24-PROJECT PORTFOLIO
    # ==========================================
    # We will use "Project Archetypes" to build realistic dependency chains
    tasks = []
    
    project_archetypes = [
        {
            "type": "SaaS Web Platform",
            "count": 8,
            "flow": [
                {"name": "Design & Prototyping", "skill": "UIUX", "hours": (80, 160)},
                {"name": "Backend Microservices", "skill": "Node", "hours": (200, 400), "pred": [0]},
                {"name": "Frontend Portal", "skill": "React", "hours": (200, 400), "pred": [0]},
                {"name": "QA Automation", "skill": "QA", "hours": (80, 120), "pred": [1, 2]},
                {"name": "K8s Deployment", "skill": "Kubernetes", "hours": (60, 100), "pred": [3]}
            ]
        },
        {
            "type": "Legacy System Migration",
            "count": 6,
            "flow": [
                {"name": "Java Audit", "skill": "Java", "hours": (120, 200)},
                {"name": "Data Lake Extraction", "skill": "SQL", "hours": (160, 300), "pred": [0]},
                {"name": "Spark Transformation", "skill": "Spark", "hours": (200, 400), "pred": [1]},
                {"name": "Cloud Infrastructure", "skill": "AWS", "hours": (100, 200), "pred": [0]}
            ]
        },
        {
            "type": "Internal AI Integration",
            "count": 10,
            "flow": [
                {"name": "Data Cleaning", "skill": "Python", "hours": (80, 120)},
                {"name": "Model Training", "skill": "Python", "hours": (160, 240), "pred": [0]},
                {"name": "API Wrapper", "skill": "Go", "hours": (80, 160), "pred": [1]},
                {"name": "Load Testing", "skill": "QA", "hours": (40, 80), "pred": [2]}
            ]
        }
    ]

    proj_counter = 1
    for arch in project_archetypes:
        for _ in range(arch["count"]):
            p_id = f"PRJ_{proj_counter:03d}"
            
            # Map relative task index to actual task IDs for predecessors
            task_id_map = {} 
            
            for index, step in enumerate(arch["flow"]):
                t_id = f"{p_id}_T{index+1}"
                task_id_map[index] = t_id
                
                # Resolve predecessors
                preds = []
                if "pred" in step:
                    preds = [task_id_map[p] for p in step["pred"]]
                
                # Assign a random required level (mostly 2s, some 3s)
                req_level = random.choices([1, 2, 3], weights=[0.2, 0.6, 0.2])[0]
                hours = random.randint(step["hours"][0], step["hours"][1])

                tasks.append({
                    'Project_ID': p_id,
                    'Task_ID': t_id,
                    'Task_Name': step["name"],
                    'Skills_Needed': f"{step['skill']}:{req_level}",
                    'Hours_Needed': hours,
                    'Predecessors': json.dumps(preds)
                })
                
            proj_counter += 1

    df_tasks = pd.DataFrame(tasks)
    df_tasks.to_csv('notebooks/base_data/tasks_large.csv', index=False)

    print(f"✅ Generated Dataset!")
    print(f"Employees: {len(df_emps)-1} Internal + 1 Contractor")
    print(f"Projects: {proj_counter-1}")
    print(f"Total Tasks: {len(df_tasks)}")
    print(f"Total Portfolio Hours: {df_tasks['Hours_Needed'].sum():,.0f}")

if __name__ == "__main__":
    generate_nexus_enterprise()