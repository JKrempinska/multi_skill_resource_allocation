import pandas as pd
import json
import os

def generate_agile_portfolio():
    os.makedirs('base_data', exist_ok=True)
    
    # 1. TechNova Employees (Same team)
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
        {'Employee_ID': 'EXT_CONTRACTOR', 'Role': 'Emergency Agency', 'Specific_Skills': 'Python:3|React:3|AWS:3|QA:3|Node:3|SQL:3|UIUX:3', 'Hourly_Cost': 300, 'Max_Hours': 9999}
    ]
    pd.DataFrame(employees).to_csv('notebooks/base_data/technova_employees_agile.csv', index=False)
    
    # 2. Agile Tickets (Max 120 hours per ticket)
    tasks = [
        # --- PROJECT A: E-Commerce Web App (Sprints 1-3) ---
        # Sprint 1: Foundation
        {'Project_ID': 'P_A', 'Task_ID': 'PA_01', 'Task_Name': 'Wireframe Auth Flow', 'Skills_Needed': 'UIUX:2', 'Hours_Needed': 24, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_02', 'Task_Name': 'Wireframe Product Grid', 'Skills_Needed': 'UIUX:2', 'Hours_Needed': 40, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_03', 'Task_Name': 'DB Schema - Users', 'Skills_Needed': 'SQL:2', 'Hours_Needed': 16, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_04', 'Task_Name': 'DB Schema - Products', 'Skills_Needed': 'SQL:2', 'Hours_Needed': 32, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_05', 'Task_Name': 'AWS VPC Setup', 'Skills_Needed': 'AWS:2', 'Hours_Needed': 24, 'Predecessors': json.dumps([])},
        
        # Sprint 2: Core Development
        {'Project_ID': 'P_A', 'Task_ID': 'PA_06', 'Task_Name': 'API: User Auth', 'Skills_Needed': 'Python:2', 'Hours_Needed': 60, 'Predecessors': json.dumps(['PA_03'])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_07', 'Task_Name': 'API: Catalog CRUD', 'Skills_Needed': 'Python:2', 'Hours_Needed': 80, 'Predecessors': json.dumps(['PA_04'])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_08', 'Task_Name': 'UI: Login/Register', 'Skills_Needed': 'React:2', 'Hours_Needed': 50, 'Predecessors': json.dumps(['PA_01', 'PA_06'])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_09', 'Task_Name': 'UI: Product Grid', 'Skills_Needed': 'React:2', 'Hours_Needed': 90, 'Predecessors': json.dumps(['PA_02', 'PA_07'])},
        
        # Sprint 3: Integration & QA
        {'Project_ID': 'P_A', 'Task_ID': 'PA_10', 'Task_Name': 'API: Payment Gateway', 'Skills_Needed': 'Python:3', 'Hours_Needed': 80, 'Predecessors': json.dumps(['PA_06', 'PA_07'])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_11', 'Task_Name': 'UI: Checkout Cart', 'Skills_Needed': 'React:3', 'Hours_Needed': 100, 'Predecessors': json.dumps(['PA_09', 'PA_10'])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_12', 'Task_Name': 'QA Automated Test Suite', 'Skills_Needed': 'QA:2', 'Hours_Needed': 60, 'Predecessors': json.dumps(['PA_08', 'PA_11'])},
        {'Project_ID': 'P_A', 'Task_ID': 'PA_13', 'Task_Name': 'Production CI/CD', 'Skills_Needed': 'AWS:3', 'Hours_Needed': 40, 'Predecessors': json.dumps(['PA_05', 'PA_12'])},

        # --- PROJECT B: Legacy API Modernization ---
        {'Project_ID': 'P_B', 'Task_ID': 'PB_01', 'Task_Name': 'Audit Legacy Codebase', 'Skills_Needed': 'Node:3', 'Hours_Needed': 40, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_B', 'Task_ID': 'PB_02', 'Task_Name': 'Data Extraction Script', 'Skills_Needed': 'SQL:2', 'Hours_Needed': 60, 'Predecessors': json.dumps(['PB_01'])},
        {'Project_ID': 'P_B', 'Task_ID': 'PB_03', 'Task_Name': 'Node API - Users', 'Skills_Needed': 'Node:2', 'Hours_Needed': 80, 'Predecessors': json.dumps(['PB_01'])},
        {'Project_ID': 'P_B', 'Task_ID': 'PB_04', 'Task_Name': 'Node API - Orders', 'Skills_Needed': 'Node:2', 'Hours_Needed': 120, 'Predecessors': json.dumps(['PB_01', 'PB_02'])},
        {'Project_ID': 'P_B', 'Task_ID': 'PB_05', 'Task_Name': 'Regression Testing', 'Skills_Needed': 'QA:3', 'Hours_Needed': 80, 'Predecessors': json.dumps(['PB_03', 'PB_04'])},

        # --- PROJECT C: Internal Admin Dashboard ---
        {'Project_ID': 'P_C', 'Task_ID': 'PC_01', 'Task_Name': 'Figma Mockups', 'Skills_Needed': 'UIUX:1', 'Hours_Needed': 20, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_C', 'Task_ID': 'PC_02', 'Task_Name': 'Python Data Scraper', 'Skills_Needed': 'Python:1', 'Hours_Needed': 40, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_C', 'Task_ID': 'PC_03', 'Task_Name': 'React Admin Table', 'Skills_Needed': 'React:1', 'Hours_Needed': 60, 'Predecessors': json.dumps(['PC_01', 'PC_02'])},
        {'Project_ID': 'P_C', 'Task_ID': 'PC_04', 'Task_Name': 'Manual QA', 'Skills_Needed': 'QA:1', 'Hours_Needed': 16, 'Predecessors': json.dumps(['PC_03'])},
    ]
    pd.DataFrame(tasks).to_csv('notebooks/base_data/technova_tasks_agile.csv', index=False)
    print(f"✅ Generated Agile Portfolio: {len(tasks)} detailed tickets.")

if __name__ == "__main__":
    generate_agile_portfolio()