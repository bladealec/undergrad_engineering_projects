import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Generate a larger sample dataset
np.random.seed(42)

# Example: 3 different groups with continuous data
group_a = np.random.normal(50, 10, 100)  # Mean=50, Std Dev=10
group_b = np.random.normal(55, 12, 100)  # Mean=55, Std Dev=12
group_c = np.random.normal(60, 15, 100)  # Mean=60, Std Dev=15

# Creating a DataFrame with 3 groups
df = pd.DataFrame({
    'Group': ['A']*100 + ['B']*100 + ['C']*100,
    'Value': np.concatenate([group_a, group_b, group_c])
})

# 1. ANOVA (Analysis of Variance) - Testing if there are significant differences between the groups
f_stat, p_value_anova = stats.f_oneway(group_a, group_b, group_c)
print(f"ANOVA Test: F-statistic = {f_stat}, p-value = {p_value_anova}")

# 2. Multiple Linear Regression - Predicting a dependent variable based on several independent variables
# Create another feature (predictor)
df['X1'] = np.random.normal(30, 5, 300)  # Feature 1
df['X2'] = np.random.normal(45, 7, 300)  # Feature 2

# Fit the multiple regression model
X = df[['X1', 'X2']]
X = sm.add_constant(X)  # Adds a constant (intercept)
y = df['Value']

model = sm.OLS(y, X).fit()  # Ordinary Least Squares regression
print("\nMultiple Linear Regression Results:")
print(model.summary())

# 3. Hypothesis Testing - T-test to compare two independent samples (e.g., Group A vs. Group B)
t_stat, p_value_ttest = stats.ttest_ind(group_a, group_b)
print(f"\nT-test between Group A and Group B: t-statistic = {t_stat}, p-value = {p_value_ttest}")

# 4. Correlation Matrix and Heatmap (for multiple variables)
# Create more features
df['X3'] = np.random.normal(25, 3, 300)
df['X4'] = np.random.normal(70, 10, 300)

# Calculate correlation matrix
correlation_matrix = df[['X1', 'X2', 'X3', 'X4']].corr()

# Plot the heatmap of the correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=1)
plt.title("Correlation Matrix Heatmap")
plt.show()

# 5. Logistic Regression - Predicting binary outcomes
# Create a binary target variable
df['Target'] = np.random.choice([0, 1], size=300)

# Fit the logistic regression model
log_model = sm.Logit(df['Target'], X[['const', 'X1', 'X2']]).fit()
print("\nLogistic Regression Results:")
print(log_model.summary())

# 6. Residuals Plot for Linear Regression (to check for homoscedasticity)
plt.figure(figsize=(8, 6))
plt.scatter(model.fittedvalues, model.resid)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted Values')
plt.show()

# 7. Checking Normality using Q-Q plot for Group A data
plt.figure(figsize=(6, 6))
stats.probplot(group_a, dist="norm", plot=plt)
plt.title('Q-Q Plot for Group A')
plt.show()
