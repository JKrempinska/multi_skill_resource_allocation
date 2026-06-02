import pandas as pd
import json
import os

def generate_technova_dataset():
    """Generates the deterministic real-world scenario for the final presentation."""
    
    os.makedirs('base_data', exist_ok=True)
    
    # 1. Employee Dataset (TechNova Solutions)
    employees = [
        {'Employee_ID': 'E001', 'Role': 'Tech Lead', 'Specific_Skills': 'Python:3|Node:3|AWS:2|SQL:3', 'Hourly_Cost': 120, 'Max_Hours': 2080},
        {'Employee_ID': 'E002', 'Role': 'Senior Backend', 'Specific_Skills': 'Python:3|SQL:2', 'Hourly_Cost': 90, 'Max_Hours': 2080},
        {'Employee_ID': 'E003', 'Role': 'Mid Backend', 'Specific_Skills': 'Node:2|Python:1|SQL:2', 'Hourly_Cost': 65, 'Max_Hours': 2080},
        {'Employee_ID': 'E004', 'Role': 'Senior Frontend', 'Specific_Skills': 'React:3|UIUX:1', 'Hourly_Cost': 90, 'Max_Hours': 2080},
        {'Employee_ID': 'E005', 'Role': 'Junior Frontend', 'Specific_Skills': 'React:1', 'Hourly_Cost': 40, 'Max_Hours': 2080},
        {'Employee_ID': 'E006', 'Role': 'Mid Fullstack', 'Specific_Skills': 'React:2|Python:2|SQL:1', 'Hourly_Cost': 75, 'Max_Hours': 2080},
        {'Employee_ID': 'E007', 'Role': 'Junior Fullstack', 'Specific_Skills': 'React:1|Node:1', 'Hourly_Cost': 45, 'Max_Hours': 2080},
        {'Employee_ID': 'E008', 'Role': 'DevOps Engineer', 'Specific_Skills': 'AWS:3|Python:1', 'Hourly_Cost': 100, 'Max_Hours': 2080},
        {'Employee_ID': 'E009', 'Role': 'QA Automation', 'Specific_Skills': 'QA:3|Python:1', 'Hourly_Cost': 70, 'Max_Hours': 2080},
        {'Employee_ID': 'E010', 'Role': 'UI/UX Designer', 'Specific_Skills': 'UIUX:3|React:1', 'Hourly_Cost': 75, 'Max_Hours': 2080},
        
        # The ultimate safety net - expensive but can do everything
        {'Employee_ID': 'EXT_CONTRACTOR', 'Role': 'Emergency Agency', 'Specific_Skills': 'Python:3|React:3|AWS:3|QA:3|Node:3|SQL:3|UIUX:3', 'Hourly_Cost': 300, 'Max_Hours': 9999}
    ]
    
    df_employees = pd.DataFrame(employees)
    df_employees.to_csv('base_data/technova_employees.csv', index=False)
    
    # 2. Project Portfolio Dataset
    tasks = [
        # Project A: E-Commerce MVP
        {'Project_ID': 'P_A', 'Task_ID': 'P_A_T1', 'Task_Name': 'Wireframing & UI', 'Skills_Needed': 'UIUX:2', 'Hours_Needed': 80, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_A', 'Task_ID': 'P_A_T2', 'Task_Name': 'Database Schema', 'Skills_Needed': 'SQL:2', 'Hours_Needed': 40, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_A', 'Task_ID': 'P_A_T3', 'Task_Name': 'Core Backend Logic', 'Skills_Needed': 'Python:2', 'Hours_Needed': 120, 'Predecessors': json.dumps(['P_A_T2'])},
        {'Project_ID': 'P_A', 'Task_ID': 'P_A_T4', 'Task_Name': 'Frontend Dev', 'Skills_Needed': 'React:2', 'Hours_Needed': 160, 'Predecessors': json.dumps(['P_A_T1', 'P_A_T3'])},
        {'Project_ID': 'P_A', 'Task_ID': 'P_A_T5', 'Task_Name': 'Cloud Deployment', 'Skills_Needed': 'AWS:3', 'Hours_Needed': 40, 'Predecessors': json.dumps(['P_A_T4'])},
        
        # Project B: Legacy API Migration
        {'Project_ID': 'P_B', 'Task_ID': 'P_B_T1', 'Task_Name': 'Architecture Audit', 'Skills_Needed': 'Node:3|AWS:1', 'Hours_Needed': 60, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_B', 'Task_ID': 'P_B_T2', 'Task_Name': 'Data Migration', 'Skills_Needed': 'SQL:3', 'Hours_Needed': 80, 'Predecessors': json.dumps(['P_B_T1'])},
        {'Project_ID': 'P_B', 'Task_ID': 'P_B_T3', 'Task_Name': 'API Rewrites', 'Skills_Needed': 'Node:2', 'Hours_Needed': 200, 'Predecessors': json.dumps(['P_B_T1'])},
        {'Project_ID': 'P_B', 'Task_ID': 'P_B_T4', 'Task_Name': 'QA Load Testing', 'Skills_Needed': 'QA:2', 'Hours_Needed': 60, 'Predecessors': json.dumps(['P_B_T2', 'P_B_T3'])},
        
        # Project C: Internal Admin Dashboard
        {'Project_ID': 'P_C', 'Task_ID': 'P_C_T1', 'Task_Name': 'Frontend Scaffold', 'Skills_Needed': 'React:1', 'Hours_Needed': 80, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_C', 'Task_ID': 'P_C_T2', 'Task_Name': 'Python Endpoints', 'Skills_Needed': 'Python:1', 'Hours_Needed': 60, 'Predecessors': json.dumps(['P_C_T1'])},
        {'Project_ID': 'P_C', 'Task_ID': 'P_C_T3', 'Task_Name': 'User Acceptance', 'Skills_Needed': 'QA:1', 'Hours_Needed': 40, 'Predecessors': json.dumps(['P_C_T2'])},
    ]
    
    df_tasks = pd.DataFrame(tasks)
    df_tasks.to_csv('base_data/technova_tasks.csv', index=False)
    
    print("✅ TechNova Solutions dataset generated successfully in /base_data!")
    print(f"Total Employees: {len(df_employees) - 1} (Plus 1 Contractor)")
    print(f"Total Portfolio Hours: {df_tasks['Hours_Needed'].sum()}")

if __name__ == "__main__":
    generate_technova_dataset()