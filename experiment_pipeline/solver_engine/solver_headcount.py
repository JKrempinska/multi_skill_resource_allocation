import pandas as pd
import json
from ortools.linear_solver import pywraplp

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def parse_skill_string(skill_str):
    if pd.isna(skill_str) or not isinstance(skill_str, str):
        return {}
    skill_dict = {}
    for item in skill_str.split('|'):
        if ':' in item:
            skill, level = item.split(':')
            skill_dict[skill.strip()] = int(level.strip())
    return skill_dict

def safe_json_load(val):
    try:
        return json.loads(val)
    except (TypeError, ValueError):
        return []

def calculate_skill_rho(emp_level, task_level):
    if emp_level == 0: return 0.2  
    elif emp_level == task_level: return 1.0  
    elif emp_level > task_level: return 1.5  
    else: return 0.5  

# ==========================================
# THE FAST SOLVER ENGINE (Continuous Time)
# ==========================================
def solve_milp_model(employees_df, tasks_df, hours_per_day=8, tau_penalty=20, time_weight=500):
    """
    Executes the Continuous-Time RCPSP MILP model.
    Fast execution, respects precedence and context-switching.
    
    Returns:
        metrics (dict): High-level KPIs.
        schedule_df (DataFrame): Optimized start/finish times.
        daily_df (None): Returns None as continuous time doesn't track daily buckets.
    """
    
    # 1. DATA PREP
    if 'Specific_Skills_Dict' not in employees_df.columns:
        employees_df['Specific_Skills_Dict'] = employees_df['Specific_Skills'].apply(parse_skill_string)
    if 'Req_Dict' not in tasks_df.columns:
        tasks_df['Req_Dict'] = tasks_df['Skills_Needed'].apply(parse_skill_string)
    if 'Predecessors_List' not in tasks_df.columns:
        tasks_df['Predecessors_List'] = tasks_df['Predecessors'].apply(safe_json_load)

    # 2. VALID PAIRS & BOTTLENECK RHO
    valid_pairs = []
    rho_dict = {} 
    for _, emp in employees_df.iterrows():
        emp_skills = emp.get('Specific_Skills_Dict', {})
        for _, task in tasks_df.iterrows():
            task_reqs = task.get('Req_Dict', {})
            skill_rhos = []
            missing_skills_count = 0
            
            for skill, req_level in task_reqs.items():
                emp_level = emp_skills.get(skill, 0)
                if emp_level == 0: missing_skills_count += 1
                skill_rhos.append(calculate_skill_rho(emp_level, req_level))
            
            if missing_skills_count < len(task_reqs):
                overall_rho = min(skill_rhos)
                pair = (emp['Employee_ID'], task['Task_ID'])
                valid_pairs.append(pair)
                rho_dict[pair] = overall_rho

    # 3. INITIALIZE SOLVER
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return {'Status': 'ERROR: SCIP Not Found', 'Total_Cost': 0, 'Makespan': 0}, None, None

    M_CAP = 2080 # Big-M for capacity

    # --- DECISION VARIABLES ---
    x = {} # Integer: Clock hours assigned
    y = {} # Binary: Context Switch (assigned AT ALL)
    for (i, j) in valid_pairs:
        x[(i, j)] = solver.IntVar(0, solver.infinity(), f'x_{i}_{j}')
        y[(i, j)] = solver.BoolVar(f'y_{i}_{j}')

    S = {} # Continuous: Start Day
    F = {} # Continuous: Finish Day
    for j in tasks_df['Task_ID']:
        S[j] = solver.NumVar(0, solver.infinity(), f'Start_{j}')
        F[j] = solver.NumVar(0, solver.infinity(), f'Finish_{j}')

    C_max = solver.NumVar(0, solver.infinity(), 'Makespan') 

    # --- CONSTRAINTS ---
    # 1. Assignment Linking: x requires y
    for (i, j) in valid_pairs:
        constraint = solver.Constraint(-solver.infinity(), 0)
        constraint.SetCoefficient(x[(i, j)], 1)
        constraint.SetCoefficient(y[(i, j)], -M_CAP)

    # 2. Demand Satisfaction
    demand_dict = tasks_df.set_index('Task_ID')['Hours_Needed'].to_dict()
    for j in tasks_df['Task_ID']:
        capable_employees = [i for (i, t_id) in valid_pairs if t_id == j]
        constraint = solver.Constraint(float(demand_dict[j]), solver.infinity())
        for i in capable_employees:
            constraint.SetCoefficient(x[(i, j)], float(rho_dict[(i, j)]))

    # 3. Total Capacity Limit
    cap_dict = employees_df.set_index('Employee_ID')['Max_Hours'].to_dict()
    for i in employees_df['Employee_ID']:
        assigned_tasks = [j for (e_id, j) in valid_pairs if e_id == i]
        constraint = solver.Constraint(0, float(cap_dict[i]))
        for j in assigned_tasks:
            constraint.SetCoefficient(x[(i, j)], 1)
            constraint.SetCoefficient(y[(i, j)], tau_penalty)

    # 4. Duration Link (Finish - Start >= Work Hours / 8)
    for j in tasks_df['Task_ID']:
        capable_employees = [i for (i, t_id) in valid_pairs if t_id == j]
        constraint = solver.Constraint(0, solver.infinity())
        constraint.SetCoefficient(F[j], 1)
        constraint.SetCoefficient(S[j], -1)
        for i in capable_employees:
            constraint.SetCoefficient(x[(i, j)], - (1.0 / hours_per_day))

    # 5. Precedence Constraints
    for _, task in tasks_df.iterrows():
        j = task['Task_ID']
        predecessors = task.get('Predecessors_List', [])
        for p in predecessors:
            constraint = solver.Constraint(0, solver.infinity())
            constraint.SetCoefficient(S[j], 1)
            constraint.SetCoefficient(F[p], -1)

    # 6. Makespan Tracker
    for j in tasks_df['Task_ID']:
        constraint = solver.Constraint(0, solver.infinity())
        constraint.SetCoefficient(C_max, 1)
        constraint.SetCoefficient(F[j], -1)

    # --- OBJECTIVE FUNCTION ---
    cost_dict = employees_df.set_index('Employee_ID')['Hourly_Cost'].to_dict()
    objective = solver.Objective()

    for (i, j) in valid_pairs:
        wage = float(cost_dict[i])
        objective.SetCoefficient(x[(i, j)], wage)
        objective.SetCoefficient(y[(i, j)], wage * tau_penalty)

    objective.SetCoefficient(C_max, time_weight)
    objective.SetMinimization()

    # --- SOLVE & EXTRACT ---
    # Add a safety time limit just in case (60 seconds)
    solver.SetTimeLimit(60000)
    status = solver.Solve()

    if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        metrics = {
            'Status': 'OPTIMAL' if status == pywraplp.Solver.OPTIMAL else 'FEASIBLE',
            'Total_Cost': solver.Objective().Value(),
            'Makespan': C_max.solution_value()
        }
        
        schedule_data = []
        for j in tasks_df['Task_ID']:
            schedule_data.append({
                'Task_ID': j,
                'Start_Day': S[j].solution_value(),
                'Finish_Day': F[j].solution_value(),
                'Duration_Days': F[j].solution_value() - S[j].solution_value()
            })
        schedule_df = pd.DataFrame(schedule_data).sort_values(by='Start_Day')
        
        # We return None for the daily dataframe because continuous time doesn't generate daily buckets
        return metrics, schedule_df, None 
    
    else:
        return {'Status': 'INFEASIBLE', 'Total_Cost': 0, 'Makespan': 0}, None, None