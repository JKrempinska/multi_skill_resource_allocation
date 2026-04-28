import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from dataset_engine.data_generator import generate_employees, generate_tasks
from solver_engine.solver_skills import solve_milp_model

def run_seniority_experiment():
    # 1. Setup Directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"experiments/{timestamp}_Seniority_Distribution"
    os.makedirs(output_dir, exist_ok=True)
    print(f"🚀 Starting Seniority Distribution Experiment. Saving to: {output_dir}\n")

    # 2. Generate a Fixed Project Portfolio
    # We must use the same tasks for every test so the comparison is fair!
    base_tasks = generate_tasks(num_projects=10, precedence_prob=0.5, random_seed=42)
    
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

    # 3. Define the Scenarios
    scenarios = ['junior_heavy', 'balanced', 'senior_heavy']
    results = []

    for profile in scenarios:
        print(f"--- Testing Scenario: {profile.upper()} ---")
        
        # Generate exactly 50 employees, but change their skill levels
        test_employees = generate_employees(num_employees=50, seniority_profile=profile, random_seed=42)
        test_employees = pd.concat([test_employees, contractor_df], ignore_index=True)
        
        # Calculate Average Hourly Rate to prove the junior team is "cheaper" on paper
        avg_wage = test_employees[test_employees['Employee_ID'] != 'EXT_CONTRACTOR']['Hourly_Cost'].mean()
        
        # Run Solver
        metrics, schedule_df, assignments_df = solve_milp_model(
            employees_df=test_employees, tasks_df=base_tasks, 
            hours_per_day=8, tau_penalty=20, time_weight=500
        )
        
        if metrics['Status'] in ['OPTIMAL', 'FEASIBLE']:
            results.append({
                'Profile': profile.replace('_', ' ').title(),
                'Avg_Hourly_Rate': avg_wage,
                'Total_Cost': metrics['Total_Cost'],
                'Makespan_Days': metrics['Makespan']
            })
            print(f"✅ Result: Avg Wage = ${avg_wage:.2f}/hr | Total Cost = ${metrics['Total_Cost']:,.0f} | Makespan = {metrics['Makespan']:.0f} days\n")
        else:
            print(f"❌ Result: INFEASIBLE. The {profile} team could not complete the project.\n")

    # 4. Visualization: The Cheap Labor Trap
    if results:
        df_results = pd.DataFrame(results)
        df_results.to_csv(f"{output_dir}/seniority_metrics.csv", index=False)
        
        sns.set_theme(style="whitegrid")
        fig, axes = plt.subplots(1, 3, figsize=(15, 6))
        
        # Plot 1: Average Hourly Rate (The Illusion)
        sns.barplot(data=df_results, x='Profile', y='Avg_Hourly_Rate', ax=axes[0], palette='Blues')
        axes[0].set_title('Average Hourly Wage\n(The Illusion of Savings)', fontweight='bold')
        axes[0].set_ylabel('Wage ($/hr)')
        axes[0].yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        
        # Plot 2: Total Project Cost (The Reality)
        sns.barplot(data=df_results, x='Profile', y='Total_Cost', ax=axes[1], palette='Reds')
        axes[1].set_title('Total Billed Cost\n(The Reality of Bottlenecks)', fontweight='bold')
        axes[1].set_ylabel('Total Cost ($)')
        axes[1].yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        
        # Plot 3: Project Makespan (The Time Cost)
        sns.barplot(data=df_results, x='Profile', y='Makespan_Days', ax=axes[2], palette='Oranges')
        axes[2].set_title('Project Completion Time\n(The Delivery Stretch)', fontweight='bold')
        axes[2].set_ylabel('Makespan (Days)')
        
        plt.tight_layout()
        plot_path = f"{output_dir}/seniority_trap_plot.png"
        plt.savefig(plot_path, dpi=300)
        print(f"📊 Saved Seniority Plot to: {plot_path}")
        plt.show()

if __name__ == "__main__":
    run_seniority_experiment()