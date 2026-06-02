import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dataset_engine.data_generator import generate_employees, generate_tasks
from solver_engine.solver_skills import solve_milp_model

def run_bottleneck_experiment():
    # 1. Setup
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"experiments/{timestamp}_Project_Bottlenecks"
    os.makedirs(output_dir, exist_ok=True)
    print(f"🚀 Starting Project Bottleneck Analysis. Saving to: {output_dir}\n")

    # 2. Generate Data
    base_employees = generate_employees(num_employees=40, seniority_profile='balanced', random_seed=42)
    base_tasks = generate_tasks(num_projects=10, precedence_prob=0.6, random_seed=42)
    
    # Contractor Safety Net
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

    # 3. Baseline Solve (Full Portfolio)
    print("Running Baseline (Full Portfolio)...")
    full_metrics, _, _ = solve_milp_model(test_employees, base_tasks)
    baseline_makespan = full_metrics['Makespan']
    print(f"Full Portfolio Makespan: {baseline_makespan:.1f} days\n")

    results = []
    project_ids = base_tasks['Project_ID'].unique()

    # 4. Leave-One-Out Loop
    for pid in project_ids:
        print(f"--- Analyzing Marginal Impact of {pid} ---")
        
        # Create a subset of tasks EXCLUDING this project
        reduced_tasks = base_tasks[base_tasks['Project_ID'] != pid].copy()
        
        # We must re-index/clean predecessors that might have been broken (though our generator stays within projects)
        metrics, _, _ = solve_milp_model(test_employees, reduced_tasks)
        
        if metrics['Status'] in ['OPTIMAL', 'FEASIBLE']:
            # The "Marginal Impact" is how many days the timeline SHRINKS when this project is removed
            impact = baseline_makespan - metrics['Makespan']
            results.append({
                'Project_ID': pid,
                'Marginal_Impact_Days': impact,
                'Project_Workload_Hours': base_tasks[base_tasks['Project_ID'] == pid]['Hours_Needed'].sum()
            })
            print(f"Impact: Timeline shrinks by {impact:.1f} days if {pid} is removed.")

    # 5. Visualization: The Project Tornado Chart
    if results:
        df_res = pd.DataFrame(results).sort_values(by='Marginal_Impact_Days', ascending=True)
        df_res.to_csv(f"{output_dir}/bottleneck_data.csv", index=False)
        
        plt.figure(figsize=(10, 7))
        sns.set_theme(style="whitegrid")
        
        # Color code: Highlight projects that cause more than 5 days of delay
        colors = ['firebrick' if x > 5 else 'steelblue' for x in df_res['Marginal_Impact_Days']]
        
        ax = sns.barplot(data=df_res, x='Marginal_Impact_Days', y='Project_ID', palette=colors)
        
        plt.title('Portfolio Bottleneck Analysis: Marginal Impact on Timeline', fontsize=16, fontweight='bold')
        plt.xlabel('Days Added to Total Portfolio Makespan', fontsize=12)
        plt.ylabel('Project ID', fontsize=12)
        
        # Add labels to show the workload size for comparison
        for i, row in df_res.iterrows():
            ax.text(row['Marginal_Impact_Days'] + 0.2, i, f"({row['Project_Workload_Hours']} hrs)", 
                    va='center', fontsize=9, color='gray')

        plt.tight_layout()
        plt.savefig(f"{output_dir}/portfolio_bottlenecks.png", dpi=300)
        plt.show()

if __name__ == "__main__":
    run_bottleneck_experiment()