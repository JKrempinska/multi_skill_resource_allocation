import pandas as pd
import json
import os

def generate_annual_portfolio():
    os.makedirs('base_data', exist_ok=True)
    
    # 1. TechNova Employees (Same as before)
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
    pd.DataFrame(employees).to_csv('base_data/technova_employees_annual.csv', index=False)
    
    # 2. The 15,500-Hour Annual Project Portfolio
    tasks = [
        # Project 01: Enterprise E-Commerce Platform (3,000 hrs)
        {'Project_ID': 'P_01', 'Task_ID': 'P01_T1', 'Task_Name': 'UX/UI Design', 'Skills_Needed': 'UIUX:3', 'Hours_Needed': 400, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_01', 'Task_ID': 'P01_T2', 'Task_Name': 'DB Architecture', 'Skills_Needed': 'SQL:3', 'Hours_Needed': 400, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_01', 'Task_ID': 'P01_T3', 'Task_Name': 'Backend APIs', 'Skills_Needed': 'Python:3', 'Hours_Needed': 1000, 'Predecessors': json.dumps(['P01_T2'])},
        {'Project_ID': 'P_01', 'Task_ID': 'P01_T4', 'Task_Name': 'React Storefront', 'Skills_Needed': 'React:2', 'Hours_Needed': 1000, 'Predecessors': json.dumps(['P01_T1', 'P01_T3'])},
        {'Project_ID': 'P_01', 'Task_ID': 'P01_T5', 'Task_Name': 'AWS Production', 'Skills_Needed': 'AWS:3', 'Hours_Needed': 200, 'Predecessors': json.dumps(['P01_T4'])},

        # Project 02: Legacy Migration to Cloud (3,500 hrs)
        {'Project_ID': 'P_02', 'Task_ID': 'P02_T1', 'Task_Name': 'Cloud Infrastructure', 'Skills_Needed': 'AWS:3', 'Hours_Needed': 800, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_02', 'Task_ID': 'P02_T2', 'Task_Name': 'Data Migration', 'Skills_Needed': 'SQL:3', 'Hours_Needed': 1000, 'Predecessors': json.dumps(['P02_T1'])},
        {'Project_ID': 'P_02', 'Task_ID': 'P02_T3', 'Task_Name': 'Node.js Rewrite', 'Skills_Needed': 'Node:3', 'Hours_Needed': 1500, 'Predecessors': json.dumps(['P02_T1'])},
        {'Project_ID': 'P_02', 'Task_ID': 'P02_T4', 'Task_Name': 'QA Regression', 'Skills_Needed': 'QA:3', 'Hours_Needed': 200, 'Predecessors': json.dumps(['P02_T2', 'P02_T3'])},

        # Project 03: Internal Tooling Suite (1,500 hrs)
        {'Project_ID': 'P_03', 'Task_ID': 'P03_T1', 'Task_Name': 'Internal Dashboards', 'Skills_Needed': 'React:1', 'Hours_Needed': 600, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_03', 'Task_ID': 'P03_T2', 'Task_Name': 'Reporting Scripts', 'Skills_Needed': 'Python:1', 'Hours_Needed': 600, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_03', 'Task_ID': 'P03_T3', 'Task_Name': 'Basic Testing', 'Skills_Needed': 'QA:1', 'Hours_Needed': 300, 'Predecessors': json.dumps(['P03_T1', 'P03_T2'])},

        # Project 04: Mobile App MVP (2,500 hrs)
        {'Project_ID': 'P_04', 'Task_ID': 'P04_T1', 'Task_Name': 'App Design', 'Skills_Needed': 'UIUX:2', 'Hours_Needed': 500, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_04', 'Task_ID': 'P04_T2', 'Task_Name': 'React Native Build', 'Skills_Needed': 'React:3', 'Hours_Needed': 1000, 'Predecessors': json.dumps(['P04_T1'])},
        {'Project_ID': 'P_04', 'Task_ID': 'P04_T3', 'Task_Name': 'Mobile API Gateway', 'Skills_Needed': 'Node:2', 'Hours_Needed': 500, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_04', 'Task_ID': 'P04_T4', 'Task_Name': 'Device QA', 'Skills_Needed': 'QA:2', 'Hours_Needed': 500, 'Predecessors': json.dumps(['P04_T2', 'P04_T3'])},

        # Project 05: Data Analytics Pipeline (1,800 hrs)
        {'Project_ID': 'P_05', 'Task_ID': 'P05_T1', 'Task_Name': 'Data Lake Setup', 'Skills_Needed': 'AWS:2', 'Hours_Needed': 200, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_05', 'Task_ID': 'P05_T2', 'Task_Name': 'ETL Pipelines', 'Skills_Needed': 'Python:2', 'Hours_Needed': 800, 'Predecessors': json.dumps(['P05_T1'])},
        {'Project_ID': 'P_05', 'Task_ID': 'P05_T3', 'Task_Name': 'SQL Transformations', 'Skills_Needed': 'SQL:2', 'Hours_Needed': 800, 'Predecessors': json.dumps(['P05_T2'])},

        # Project 06: Holiday Traffic Scaling (1,200 hrs)
        {'Project_ID': 'P_06', 'Task_ID': 'P06_T1', 'Task_Name': 'Load Balancing', 'Skills_Needed': 'AWS:3', 'Hours_Needed': 600, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_06', 'Task_ID': 'P06_T2', 'Task_Name': 'Service Optimization', 'Skills_Needed': 'Node:2', 'Hours_Needed': 200, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_06', 'Task_ID': 'P06_T3', 'Task_Name': 'Stress Testing', 'Skills_Needed': 'QA:3', 'Hours_Needed': 400, 'Predecessors': json.dumps(['P06_T1', 'P06_T2'])},

        # Project 07: Client B2B Portal (2,000 hrs)
        {'Project_ID': 'P_07', 'Task_ID': 'P07_T1', 'Task_Name': 'Portal Design', 'Skills_Needed': 'UIUX:2', 'Hours_Needed': 300, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_07', 'Task_ID': 'P07_T2', 'Task_Name': 'Auth & Backend', 'Skills_Needed': 'Python:2', 'Hours_Needed': 800, 'Predecessors': json.dumps([])},
        {'Project_ID': 'P_07', 'Task_ID': 'P07_T3', 'Task_Name': 'Client Frontend', 'Skills_Needed': 'React:2', 'Hours_Needed': 700, 'Predecessors': json.dumps(['P07_T1', 'P07_T2'])},
        {'Project_ID': 'P_07', 'Task_ID': 'P07_T4', 'Task_Name': 'Database Tuning', 'Skills_Needed': 'SQL:2', 'Hours_Needed': 200, 'Predecessors': json.dumps(['P07_T2'])},
    ]
    pd.DataFrame(tasks).to_csv('base_data/technova_tasks_annual.csv', index=False)
    print(f"✅ Generated Annual Portfolio: {sum(t['Hours_Needed'] for t in tasks):,.0f} Total Hours across 7 Projects.")

if __name__ == "__main__":
    generate_annual_portfolio()