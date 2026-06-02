import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import your custom modules
from dataset_engine.data_generator import generate_employees, generate_tasks
from solver_engine.solver_skills import solve_milp_model

def run_skill_gap_experiment():
    # 1. Setup Directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"experiments/{timestamp}_Skill_Gap_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    print(f"🚀 Starting Skill Gap Analysis. Saving to: {output_dir}\n")

    # 2. Generate a "Junior-Heavy" workforce to force bottlenecks
    print("Generating Junior-Heavy workforce to expose skill bottlenecks...")
    base_employees = generate_employees(num_employees=50, seniority_profile='junior_heavy', random_seed=42)
    base_tasks = generate_tasks(num_projects=12, precedence_prob=0.5, random_seed=42)
    
    # Inject the Contractor Safety Net
    all_reqs = set()
    for req_str in base_tasks['Skills_Needed']:
        for item in req_str.split('|'):
            if ':' in item: all_reqs.add(item.split(':')[0])
    
    contractor_skills = "|".join([f"{skill}:5" for skill in all_reqs])
    contractor_df = pd.DataFrame([{
        'Employee_ID': 'EXT_CONTRACTOR', 'Specific_Skills': contractor_skills,
        'Hourly_Cost': 5000, 'Max_Hours': 999999
    }])
    test_employees = pd.concat([base_employees, contractor_df], ignore_index=True)

    # 3. Run the Solver
    print("Running Solver...")
    metrics, schedule_df, assignments_df = solve_milp_model(
        employees_df=test_employees, tasks_df=base_tasks, 
        hours_per_day=8, tau_penalty=20, time_weight=500
    )

    if metrics['Status'] != 'OPTIMAL' and metrics['Status'] != 'FEASIBLE':
        print("❌ Solver failed to find a solution.")
        return

    # 4. Analyze the Assignments to find Skill Gaps
    print("Analyzing assignment efficiency by technology stack...")
    skill_records = []
    
    # Build a quick lookup dictionary for task requirements
    task_reqs_lookup = {}
    for _, task in base_tasks.iterrows():
        reqs = [item.split(':')[0] for item in task['Skills_Needed'].split('|') if ':' in item]
        task_reqs_lookup[task['Task_ID']] = reqs

    for _, assign in assignments_df.iterrows():
        emp_id = assign['Employee_ID']
        task_id = assign['Task_ID']
        hours = assign['Work_Hours']
        rho = assign['Rho']
        
        # What skills was this task demanding?
        required_skills = task_reqs_lookup.get(task_id, [])
        
        for skill in required_skills:
            # We divide hours by len(required_skills) to prevent double-counting massive tasks
            allocated_hours = hours / len(required_skills) 
            
            status = "Optimal/Expert"
            if emp_id == 'EXT_CONTRACTOR':
                status = "Outsourced (Missing Skill)"
            elif rho < 1.0:
                status = "Under-Qualified Penalty"
                
            skill_records.append({
                'Skill': skill,
                'Status': status,
                'Hours': allocated_hours
            })

    df_skills = pd.DataFrame(skill_records)
    
    # Group by Skill and Status to sum the hours
    heatmap_df = df_skills.groupby(['Skill', 'Status'])['Hours'].sum().unstack(fill_value=0)
    
    # Ensure all columns exist for consistent plotting
    for col in ['Optimal/Expert', 'Under-Qualified Penalty', 'Outsourced (Missing Skill)']:
        if col not in heatmap_df.columns:
            heatmap_df[col] = 0
            
    # Sort by total hours of pain (Outsourced + Penalty)
    heatmap_df['Total_Pain'] = heatmap_df['Outsourced (Missing Skill)'] + heatmap_df['Under-Qualified Penalty']
    heatmap_df = heatmap_df.sort_values(by='Total_Pain', ascending=True)
    heatmap_df = heatmap_df.drop(columns=['Total_Pain'])

    # Save data
    heatmap_df.to_csv(f"{output_dir}/skill_gap_data.csv")

    # 5. Visualize the Capability Gap
    sns.set_theme(style="whitegrid")
    
    # Define custom colors
    color_map = {
        'Optimal/Expert': 'mediumseagreen',
        'Under-Qualified Penalty': 'gold',
        'Outsourced (Missing Skill)': 'firebrick'
    }

    # Plot a horizontal stacked bar chart
    ax = heatmap_df.plot(kind='barh', stacked=True, figsize=(12, 8), 
                         color=[color_map.get(x, '#333333') for x in heatmap_df.columns])

    plt.title('The Capability Gap: Workforce Efficiency by Technology Stack', fontsize=16, fontweight='bold')
    plt.xlabel('Total Billed Hours', fontsize=12)
    plt.ylabel('Required Skill / Technology', fontsize=12)
    
    # Clean up legend
    plt.legend(title="Assignment Quality", loc='lower right', framealpha=0.9)
    plt.tight_layout()
    
    plot_path = f"{output_dir}/capability_gap_chart.png"
    plt.savefig(plot_path, dpi=300)
    print(f"📊 Saved Capability Gap plot to: {plot_path}")
    plt.show()

if __name__ == "__main__":
    run_skill_gap_experiment()