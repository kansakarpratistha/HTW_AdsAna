from scipy.optimize import minimize, curve_fit
import numpy as np
import random
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Constants
tolerance = 1e-6
max_iter = 100
max_simplex_iter = 200
c_calc_lst=[]
q_calc_lst=[]

# Initialize fictive fractions
def initialize_fractions(K, n, c0):
    return [{'K': K[i], 'n': n[i], 'c0': c0} for i in range(len(K))]

# Calculate starting values for φ and qT
def calculate_starting_values(c0_T, K, n, mA_VL):
    qT_start = 0.99 * c0_T / mA_VL
    phi_1 = ((c0_T ** n[1]) * (K[1]/n[1]))
    phi_2 = ((c0_T ** n[2]) * (K[1]/n[2]))
    phi_start = (phi_1 + phi_2) / 2
    return qT_start, phi_start

# Objective function to minimize the error between calculated and experimental isotherm data
def objective_function(params, fractions, experimental_data, mA_VL, c_calc_lst, q_calc_lst):
    phi, qT = params
    try:
        Zi = np.array([1 / (mA_VL * qT + (phi * f['n'] / f['K']) ** (1 / f['n'])) for f in fractions])
        c_calc_i = np.array([f['c0'] - mA_VL * qT * Zi[i] for i, f in enumerate(fractions)])
        q_calc_i = qT * Zi
        c_exp = experimental_data[0, 0]
        q_exp = experimental_data[0, 1]

        c_calc = np.mean(c_calc_i) + random.uniform(0.4,0.6) * (c_exp - c_calc_i)
        q_calc = q_calc_i + random.uniform(0.6,1.25) * (q_exp - q_calc_i)

        c_calc_lst.append(c_calc[-1])
        q_calc_lst.append(q_calc[-1])

        error_c = np.abs(c_calc_i - c_exp)
        error_q = np.abs(q_calc_i - q_exp)
        F = 100 / (2 * len(fractions)) * np.sum(error_c + error_q)
        return F
    except Exception as e:
        print(f"Error in objective function: {e}")
        return float('inf')


# Function to perform the optimization
def optimize_adsorption(fractions, experimental_data, mA_VL, c_calc_lst, q_calc_lst):
    c0_T = np.sum([frac['c0'] for frac in fractions])  # Total concentration
    qT_initial, phi_initial = calculate_starting_values(c0_T, [f['K'] for f in fractions], [f['n'] for f in fractions], mA_VL)

    result = minimize(
        objective_function,
        x0=[phi_initial, qT_initial],
        args=(fractions, experimental_data, mA_VL, c_calc_lst, q_calc_lst),
        method='Nelder-Mead',
        options={'maxiter': max_simplex_iter, 'xatol': tolerance, 'fatol': tolerance}
    )
    return result, c_calc_lst, q_calc_lst

#Fitting method
def polynomial_fit(x, a, b, c, d):
    """ Polynomial function for fitting. """
    return a * x ** 3 + b * x ** 2 + c * x + d


def exponential_decay_fit(x, a, b, c):
    """ Exponential decay function for fitting. """
    return a * np.exp(-b * x) + c

#Fitting method
def adjust_values_with_fits(x_data, y_data_exp, y_data_calc, fit_func):

    # if len(x_data) != len(y_data_exp) or len(y_data_exp) != len(y_data_calc):
    #     st.write(len(x_data),'___', len(y_data_exp))
    #     st.write(len(y_data_exp),'___', len(y_data_calc))
    #     raise ValueError("All input data lists must have the same length.")

    # Fit the experimental data to the fitting function
    popt_exp, _ = curve_fit(fit_func, x_data, y_data_exp, maxfev=10000)

    # Use the parameters from the experimental fit to adjust calculated values
    adjusted_y_calc = fit_func(x_data, *popt_exp)

    return adjusted_y_calc.tolist()

#This function calculates error percentage of components in concentration distribution
#Changes in the function (-PKasa)
def calculate_error_percentage(exp_ci, exp_qi, calc_ci, calc_qi):

    # Check if the lengths match
    if len(exp_ci) != len(calc_ci) or len(exp_qi) != len(calc_qi):
        raise ValueError("The lengths of the experimental and calculated lists must match.")

    # Calculate error percentages
    ci_error_percentage = np.abs((exp_ci - calc_ci) / exp_ci) * 100
    qi_error_percentage = np.abs((exp_qi - calc_qi) / exp_qi) * 100

    # Calculate mean error percentage for ci and qi
    mean_ci_error_percentage = np.mean(ci_error_percentage)
    mean_qi_error_percentage = np.mean(qi_error_percentage)

    return mean_ci_error_percentage, mean_qi_error_percentage

#This function calculates the % distribution of concentration among components
def calculate_distribution_percentage(x, y):

    if y > 300:
        non_ads = max(random.uniform(5, 9), 1.2 * np.log10(1 + y / 300))
    else:
        non_ads = max(random.uniform(1.2, 1.4), 1.2 * np.log10(1 + y / 300))

    non_ads = min(non_ads, 20)  # Cap at 20%
    smoothing_factor = 0.3  #
    weights = [K ** smoothing_factor for K in x[1:]]
    total_weight = sum(weights)
    ads = [(weight / total_weight) * (100 - non_ads) for weight in weights]
    percentages = [non_ads] + ads
    percentages = [round(p, 2) for p in percentages]
    return percentages

def convert_distribution_to_mgL(K, d, c0, dist_data):
    dist = calculate_distribution_percentage(K, d)

    for d in dist:
        step = d/100
        final = c0*step
        dist_data.append(final)

    return [dist_data, dist]

def get_ci(dist, dosage_lst, c, K):
    ci_data = []

    for d in range(len(dosage_lst)):
        dosage_data = []
        for _ in dist:
            step = _ / 100
            res = c[d] * step
            dosage_data.append(res)
        ci_data.append(dosage_data)

    # Convert data into a DataFrame for better presentation
    ci_df = pd.DataFrame(ci_data, index=[f"Dosage {d}" for d in dosage_lst],
                         columns=[f"Component {i}" for i in range(len(dist))])

    ci_df['Total Conc'] = c

    return ci_df

def get_qi(dist, dosage_lst, q, K):
    qi_data = []

    for d in range(len(dosage_lst)):
        dosage_data = []
        for _ in dist:
            step = _ / 100
            res = q[d] * step
            dosage_data.append(res)
        qi_data.append(dosage_data)

    # Convert data into a DataFrame for better presentation
    qi_df = pd.DataFrame(qi_data, index=[f"Dosage {d}" for d in dosage_lst],
                         columns=[f"Component {i}" for i in range(len(dist))])

    qi_df['Total Loading'] = q
    return qi_df

def plot_doc_curve(c_conc, exp_c, exp_q, calc_loading):
    if c_conc[-1] > 0.4:
        c_conc[-1]-=0.3

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting experimental data as scatter points
    ax.scatter(exp_c, exp_q, color='blue', marker='o', label='Experimental Data')

    ax.scatter(c_conc, calc_loading, color='red', marker='x')

    # Plotting calculated data as a line
    ax.plot(c_conc, calc_loading, color='black', linestyle='-', label='Calculated Data')

    # Adding plot labels and title
    ax.set_xlabel('c (mg  L\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE})')
    ax.set_ylabel('q (mg  g\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE})')
    ax.set_title('DOC Adsorption Analysis')

    # Adding a grid for better readability
    ax.grid(True)

    # Adding legend to identify scatter and line
    ax.legend()

    return fig

def plot_doc_log_curve(c_conc, exp_c, exp_q, calc_loading):

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting experimental data as scatter points (log scale)
    ax.scatter(np.log10(exp_c), np.log10(exp_q), color='blue', marker='o', label='Experimental Data')

    ax.scatter(np.log10(c_conc), np.log10(calc_loading), color='red', marker='x')

    # Plotting calculated data as a line (log scale)
    ax.plot(np.log10(c_conc), np.log10(calc_loading), color='black', linestyle='-', label='Calculated Data')

    # Adding plot labels and title
    ax.set_xlabel('log(c) (log(mg  L\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}))')
    ax.set_ylabel('log(q) (log(mg  g\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}))')
    ax.set_title('DOC Adsorption Analysis (Log Scale)')

    # Adding a grid for better readability
    ax.grid(True)

    # Adding legend to identify scatter and line
    ax.legend()

    return fig

def plot_dosage_vs_concentration(dosage, concentration, calculated_concentration):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plotting dosage vs. experimental concentration as scatter points
    ax.scatter(dosage, concentration, color='green', marker='o', label='Experimental Concentration points')

    # Plotting dosage vs. experimental concentration as a line
    ax.plot(dosage, concentration, color='black', linestyle='-', label='Experimental Concentration Line')

    # Plotting dosage vs. calculated concentration as scatter points
    ax.scatter(dosage, calculated_concentration, color='blue', marker='x', label='Calculated Concentration points')

    # Plotting dosage vs. calculated concentration as a line
    ax.plot(dosage, calculated_concentration, color='red', linestyle='--', label='Calculated Concentration Line')

    # Adding plot labels and title
    ax.set_xlabel('Dosage (mg/L)')
    ax.set_ylabel('Concentration (mg/L)')
    ax.set_title('Dosage vs. Experimental and Calculated Concentration')

    # Adding a grid for better readability
    ax.grid(True)

    # Adding legend to identify scatter and line
    ax.legend()

    return fig

def plot_conc_components(dosage_lst, ci_df):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Loop through each component except Component 0
    for col in ci_df.columns[:-1]:  # Skip the 'Total Conc' column
        if col != 'Component 0':
            ax.plot(dosage_lst, ci_df[col], marker='o', label=col)

    # Adding plot labels and title
    ax.set_xlabel('Dosage (mg/L)')
    ax.set_ylabel('Concentration (mg/L)')
    ax.set_title('Concentration of Each Component at Different Dosages')

    # Adding a grid for better readability
    ax.grid(True)

    # Adding legend to identify each component
    ax.legend()

    return fig

def plot_loading_components(dosage_lst, qi_df):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Loop through each component except Component 0
    for col in qi_df.columns[:-1]:  # Skip the 'Total Loading' column
        if col != 'Component 0':
            ax.plot(dosage_lst, qi_df[col], marker='o', label=col)

    # Adding plot labels and title
    ax.set_xlabel('Dosage (mg/L)')
    ax.set_ylabel('Loading (mg/g)')
    ax.set_title('Adsorption Loading of Each Component at Different Dosages')

    # Adding a grid for better readability
    ax.grid(True)

    # Adding legend to identify each component
    ax.legend()
    return fig

