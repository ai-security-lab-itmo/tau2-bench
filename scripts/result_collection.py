"""
Functions for collecting and analyzing simulation results.

This module provides utilities to load simulation files, compute metrics,
and generate comprehensive dataframes for analysis.
"""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from tau2.data_model.simulation import MultiDomainResults, Results
from tau2.metrics.agent_metrics import is_successful, pass_hat_k


def load_simulation_file(file_path: str | Path) -> Dict[str, Results]:
    """
    Load a simulation file and return a dictionary mapping domain names to Results.
    Handles both single-domain (Results) and multi-domain (MultiDomainResults) formats.

    Args:
        file_path: Path to the simulation JSON file

    Returns:
        Dictionary mapping domain names to Results objects
    """
    file_path = Path(file_path)

    # Try to load as MultiDomainResults first
    try:
        multi_domain_results = MultiDomainResults.load(file_path)
        return multi_domain_results.domains
    except Exception:
        # Fall back to single-domain Results format
        try:
            results = Results.load(file_path)
            domain_name = results.info.environment_info.domain_name
            return {domain_name: results}
        except Exception as e:
            raise ValueError(f"Failed to load simulation file {file_path}: {e}")


def load_simulations(file_paths: List[str | Path]) -> Dict[str, Results]:
    """
    Load multiple simulation files and combine them into a single dictionary.

    Args:
        file_paths: List of paths to simulation JSON files

    Returns:
        Dictionary mapping domain names to Results objects
        (if multiple files have the same domain, they will be merged)
    """
    all_domains = {}

    for file_path in file_paths:
        domains = load_simulation_file(file_path)
        for domain_name, results in domains.items():
            if domain_name in all_domains:
                # Merge simulations from the same domain
                all_domains[domain_name].simulations.extend(deepcopy(results.simulations))
                # Merge tasks (avoid duplicates)
                existing_task_ids = {task.id for task in all_domains[domain_name].tasks}
                for task in results.tasks:
                    if task.id not in existing_task_ids:
                        all_domains[domain_name].tasks.append(deepcopy(task))
            else:
                all_domains[domain_name] = deepcopy(results)

    return all_domains


def compute_task_metrics(results: Results, task_id: str) -> Dict[str, Any]:
    """
    Compute metrics for a specific task within a Results object.

    Args:
        results: Results object containing simulations
        task_id: ID of the task to compute metrics for

    Returns:
        Dictionary containing computed metrics
    """
    # Filter simulations for this task
    task_simulations = [sim for sim in results.simulations if sim.task_id == task_id]

    if not task_simulations:
        return {}

    # Compute basic metrics
    rewards = [sim.reward_info.reward if sim.reward_info else 0.0 for sim in task_simulations]
    successes = [is_successful(r) for r in rewards]
    agent_costs = [sim.agent_cost if sim.agent_cost else 0.0 for sim in task_simulations]
    user_costs = [sim.user_cost if sim.user_cost else 0.0 for sim in task_simulations]
    durations = [sim.duration for sim in task_simulations]
    num_messages = [len(sim.messages) for sim in task_simulations]

    num_trials = len(task_simulations)
    success_count = sum(successes)

    metrics = {
        "num_trials": num_trials,
        "success_count": success_count,
        "avg_reward": float(np.mean(rewards)),
        "std_reward": float(np.std(rewards)),
        "avg_agent_cost": float(np.mean(agent_costs)) if agent_costs else None,
        "avg_user_cost": float(np.mean(user_costs)) if user_costs else None,
        "avg_duration": float(np.mean(durations)),
        "avg_num_messages": float(np.mean(num_messages)),
    }

    # Compute pass^k metrics
    if num_trials > 0:
        for k in range(1, min(num_trials + 1, 5)):  # Compute pass^1 to pass^4
            if num_trials >= k:
                metrics[f"pass^{k}"] = float(pass_hat_k(num_trials, success_count, k))

    return metrics


def generate_metrics_table(simulation_files: List[str | Path]) -> pd.DataFrame:
    """
    Generate a comprehensive metrics table from simulation files.

    Args:
        simulation_files: List of paths to simulation JSON files

    Returns:
        DataFrame with columns: domain, user_model, user_model_params,
        agent_model, agent_model_params, task, and various metrics
    """
    rows = []

    # Process each file separately to preserve parameter differences
    for file_path in simulation_files:
        # Load domains from this file
        file_domains = load_simulation_file(file_path)

        for domain_name, results in file_domains.items():
            # Extract configuration info from this specific Results object
            user_model = results.info.user_info.llm
            user_model_params = (
                json.dumps(results.info.user_info.llm_args)
                if results.info.user_info.llm_args
                else "{}"
            )
            agent_model = results.info.agent_info.llm
            agent_model_params = (
                json.dumps(results.info.agent_info.llm_args)
                if results.info.agent_info.llm_args
                else "{}"
            )

            # Get unique tasks for this domain
            task_ids = set(sim.task_id for sim in results.simulations)

            for task_id in task_ids:
                # Compute metrics for this task
                task_metrics = compute_task_metrics(results, task_id)

                if not task_metrics:
                    continue

                # Create row
                row = {
                    "domain": domain_name,
                    "user_model": user_model,
                    "user_model_params": user_model_params,
                    "agent_model": agent_model,
                    "agent_model_params": agent_model_params,
                    "task": task_id,
                    **task_metrics,
                }

                rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # Reorder columns to put metrics at the end
    metric_columns = [
        col
        for col in df.columns
        if col
        not in [
            "domain",
            "user_model",
            "user_model_params",
            "agent_model",
            "agent_model_params",
            "task",
        ]
    ]
    column_order = [
        "domain",
        "user_model",
        "user_model_params",
        "agent_model",
        "agent_model_params",
        "task",
    ] + metric_columns
    df = df[column_order]

    return df


def visualize_metrics(
    simulation_files: List[str | Path],
    show_table: bool = True,
    show_summary: bool = True,
) -> pd.DataFrame:
    """
    Visualize metrics from simulation files.

    Args:
        simulation_files: List of paths to simulation JSON files
        show_table: Whether to display the full table
        show_summary: Whether to display summary statistics

    Returns:
        DataFrame with metrics
    """
    # Generate metrics table
    df = generate_metrics_table(simulation_files)

    if df.empty:
        print("No data found in simulation files.")
        return df

    if show_summary:
        print("=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)
        print(f"\nTotal unique configurations: {len(df)}")
        print(f"Domains: {df['domain'].nunique()} ({', '.join(df['domain'].unique())})")
        print(f"Tasks: {df['task'].nunique()}")
        print(f"User models: {df['user_model'].nunique()}")
        print(f"Agent models: {df['agent_model'].nunique()}")

        if "avg_reward" in df.columns:
            print(f"\nOverall average reward: {df['avg_reward'].mean():.4f}")
        if "pass^1" in df.columns:
            print(f"Overall pass^1: {df['pass^1'].mean():.4f}")
        if "avg_agent_cost" in df.columns and df["avg_agent_cost"].notna().any():
            print(f"Overall average agent cost: {df['avg_agent_cost'].mean():.4f}")

    if show_table:
        print("\n" + "=" * 80)
        print("METRICS TABLE")
        print("=" * 80)
        # Display with better formatting
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", None)
        pd.set_option("display.max_colwidth", 50)
        print(df.to_string(index=False))

    return df

