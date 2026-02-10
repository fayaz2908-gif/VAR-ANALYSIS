import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from datetime import datetime

class MarketRiskAnalyzer:
    """
    A class to analyze market risk using Value at Risk (VaR) models.
    Designed to compare Historical vs. Parametric methodologies.
    """
    
    def __init__(self, file_path, confidence_level=0.95):
        """
        Initialize the analyzer with data and parameters.
        
        Args:
            file_path (str): Path to the Excel file containing historical data.
            confidence_level (float): The confidence interval (default 0.95).
        """
        self.file_path = file_path
        self.confidence_level = confidence_level
        self.data = None
        self.results = {}
        
        # Load data upon initialization
        self.load_data()

    def load_data(self):
        """
        Loads data from Excel, calculates daily returns, and cleans missing values.
        """
        try:
            print(f"Loading data from {self.file_path}...")
            self.data = pd.read_excel(self.file_path)
            
            # Ensure proper datetime formatting
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            self.data = self.data.sort_values(by='Date')
            
            # Calculate Daily Log Returns
            # Log returns are preferred in risk management for their additive properties
            self.data['Returns'] = np.log(self.data['Close'] / self.data['Close'].shift(1))
            
            # Drop NaN values created by the shift operation
            self.data = self.data.dropna()
            
            print(f"Data loaded successfully. Total trading days analyzed: {len(self.data)}")
            
        except Exception as e:
            print(f"Error loading data: {e}")

    def calculate_historical_var(self):
        """
        Calculates VaR using the Historical Simulation method.
        This method sorts past returns and finds the cutoff at the specific percentile.
        """
        if self.data is None:
            return None
        
        # Calculate the percentile index
        var_percentile = 1 - self.confidence_level
        
        # Calculate VaR based on the empirical distribution
        var_value = self.data['Returns'].quantile(var_percentile)
        
        self.results['Historical VaR'] = var_value
        return var_value

    def calculate_parametric_var(self):
        """
        Calculates VaR using the Variance-Covariance (Parametric) method.
        Assumes returns follow a Normal (Gaussian) Distribution.
        """
        if self.data is None:
            return None
        
        # Calculate statistical properties
        mu = np.mean(self.data['Returns'])
        sigma = np.std(self.data['Returns'])
        
        # Get the Z-score for the confidence level (e.g., -1.645 for 95%)
        z_score = stats.norm.ppf(1 - self.confidence_level)
        
        # Formula: Mean + (Z-score * Std Dev)
        var_value = mu + (z_score * sigma)
        
        self.results['Parametric VaR'] = var_value
        return var_value

    def generate_risk_report(self):
        """
        Prints a professional summary of the risk metrics.
        """
        print("\n" + "="*40)
        print(f"   MARKET RISK ANALYSIS REPORT")
        print("="*40)
        print(f"Confidence Level: {self.confidence_level * 100}%")
        print(f"Volatility (Daily): {self.data['Returns'].std():.4f}")
        print("-" * 40)
        print(f"1. Historical VaR:   {self.results.get('Historical VaR', 0):.4%}")
        print(f"2. Parametric VaR:   {self.results.get('Parametric VaR', 0):.4%}")
        print("="*40)
        
        # Interpretation for the user/recruiter
        print("\nInterpretation:")
        print(f"With {self.confidence_level*100}% confidence, the maximum expected daily loss")
        print(f"will not exceed {-1 * self.results.get('Parametric VaR', 0):.2%} (Parametric model).")

    def visualize_risk(self):
        """
        Generates a histogram of returns and plots the VaR thresholds.
        """
        plt.figure(figsize=(10, 6))
        
        # Plot histogram of returns
        plt.hist(self.data['Returns'], bins=50, alpha=0.6, color='skyblue', label='Daily Returns')
        
        # Add vertical lines for VaR
        plt.axvline(self.results['Historical VaR'], color='red', linestyle='--', linewidth=2, label=f'Historical VaR ({self.results["Historical VaR"]:.2%})')
        plt.axvline(self.results['Parametric VaR'], color='green', linestyle='-', linewidth=2, label=f'Parametric VaR ({self.results["Parametric VaR"]:.2%})')
        
        plt.title('Portfolio Return Distribution & VaR Thresholds')
        plt.xlabel('Daily Log Returns')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

# --- Main Execution Block ---
if __name__ == "__main__":
    # Settings
    INPUT_FILE = 'market_data.xlsx'
    CONFIDENCE = 0.97 # 97% Confidence Level
    
    # Initialize the engine
    risk_engine = MarketRiskAnalyzer(INPUT_FILE, CONFIDENCE)
    
    # Run Calculations
    risk_engine.calculate_historical_var()
    risk_engine.calculate_parametric_var()
    
    # Output Results
    risk_engine.generate_risk_report()
    
    # Visualize
    risk_engine.visualize_risk()