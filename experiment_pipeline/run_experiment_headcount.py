import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Import your custom modules
from dataset_engine.data_generator import generate_employees, generate_tasks
from solver_engine.solver_headcount import solve_milp_model

def run_headcount_experiment():
    # 1. Setup the Experiment Directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"experiments/{timestamp}_Headcount_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    print(f"🚀 Starting Headcount Experiment. Results will be saved to: {output_dir}\n")

    # 2. Generate a single Baseline Dataset
    # We use a fixed baseline so we are stripping away from the exact same pool of people.
    base_employees = generate_employees(num_employees=40, seniority_profile='balanced', random_seed=42)
    base_tasks = generate_tasks(num_projects=20, precedence_prob=0.5, random_seed=42)
    
    # Ensure the external contractor is available as a safety net
    all_required_skills = set()
    for req_str in base_tasks['Skills_Needed']:
        for item in req_str.split('|'):
            if ':' in item:
                all_required_skills.add(item.split(':')[0])
                
    contractor_skills = "|".join([f"{skill}:5" for skill in all_required_skills])
    contractor_df = pd.DataFrame([{
        'Employee_ID': 'EXT_CONTRACTOR',
        'Specific_Skills': contractor_skills,
        'Hourly_Cost': 5000,
        'Max_Hours': 999999
    }])

    results = []
    # Test from 100% workforce down to 40% in 10% increments
    fractions_to_test = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]

    for frac in fractions_to_test:
        current_headcount = int(len(base_employees) * frac)
        print(f"--- Testing at {frac*100:.0f}% Capacity ({current_headcount} Internal Employees) ---")
        
        # Randomly sample the workforce (simulating layoffs/attrition)
        sampled_staff = base_employees.sample(n=current_headcount, random_state=42)
        
        # Add the contractor back into the test pool
        test_employees = pd.concat([sampled_staff, contractor_df], ignore_index=True)
        
        # 3. Call the Solver Engine!
        metrics, schedule_df, daily_df = solve_milp_model(
            employees_df=test_employees, 
            tasks_df=base_tasks, 
            hours_per_day=8, 
            tau_penalty=20, 
            time_weight=500
        )
        
        if metrics['Status'] == 'OPTIMAL':
            # Check how much the contractor was used
            contractor_hours = 0
            if daily_df is not None:
                contractor_work = daily_df[daily_df['Employee_ID'] == 'EXT_CONTRACTOR']
                contractor_hours = len(contractor_work) * 8 # 8 hours per day active
                
            results.append({
                'Retained_Pct': frac * 100,
                'Headcount': current_headcount,
                'Total_Cost': metrics['Total_Cost'],
                'Makespan_Days': metrics['Makespan'],
                'Contractor_Hours': contractor_hours
            })
            print(f"✅ OPTIMAL: Cost = ${metrics['Total_Cost']:,.0f} | Makespan = {metrics['Makespan']:.0f} days | Contractor Hours = {contractor_hours}\n")
        else:
            print("❌ INFEASIBLE: Even with the contractor, the project cannot be completed within the Time Horizon.\n")

    # 4. Generate the Visualization (The Efficient Frontier)
# 4. Generate the Visualizations
    if results:
        df_results = pd.DataFrame(results)
        
        # Calculate Internal vs External Costs
        # (Contractor rate is fixed at $5000/hr in our generator)
        df_results['Contractor_Cost'] = df_results['Contractor_Hours'] * 5000
        df_results['Internal_Cost'] = df_results['Total_Cost'] - df_results['Contractor_Cost']
        
        # Calculate Project Delay (Compared to Baseline)
        baseline_makespan = df_results.iloc[0]['Makespan_Days']
        df_results['Days_Delayed'] = df_results['Makespan_Days'] - baseline_makespan

        df_results.to_csv(f"{output_dir}/experiment_metrics.csv", index=False)
        
        sns.set_theme(style="whitegrid")
        
        # --- PLOT 1: The Efficient Frontier (Original) ---
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df_results, x='Retained_Pct', y='Total_Cost', color='steelblue', alpha=0.8, ax=ax1)
        ax1.set_xlabel('Workforce Retained (%)', fontsize=12)
        ax1.set_ylabel('Total Project Cost ($)', fontsize=12, color='steelblue')
        ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        
        ax2 = ax1.twinx()
        sns.lineplot(data=df_results, x=range(len(df_results)), y='Makespan_Days', 
                     color='darkorange', marker='o', linewidth=3, markersize=10, ax=ax2)
        ax2.set_ylabel('Project Makespan (Days)', fontsize=12, color='darkorange')
        
        plt.title('The Efficient Frontier: Cost vs. Makespan', fontsize=16, fontweight='bold')
        plt.tight_layout()
        fig1.savefig(f"{output_dir}/01_efficient_frontier.png", dpi=300)
        plt.show()

if __name__ == "__main__":
    run_headcount_experiment()