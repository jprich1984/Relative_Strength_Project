# Relative Strength Investment Project

## Project Description
This project uses Relative Strength to determine the best industries/stocks to invest in on a given day. It also builds models to predict days that should and shouldn't be 'buy days'.

## Data Sources
The project utilizes data from Yahoo Finance, accessed through the Python `yfinance` module.

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)
- see requirements.txt
### File  Descriptions

- relative_strength.py: This file calculates the relative strength of each sector and selects the top 3 industries with the most momentum. It then calculates the relative strength of stocks within these sectors, selecting the top 3 with the most momentum. 

The momentum of industries/stocks is evaluated using three methods:
	1. Slope of relative strength values for the last 20 days
	2. Pearson correlation coefficient between time (integers 1-20) and relative strength values
	3. Product of the slope and correlation coefficient
The top 3 industries/stocks are selected based on the highest metric for each method. The performance of each method is further evaluated in subsequent notebooks.

-Stock_Program_tests.py: Implements the methods in relative_strength.py

-Strategy_Evaluation.ipynb: Tests each method from the relative_strength program and evaluates which method performs the best

-Model_Invest_Days_Action_Target.ipynb: Engineers features and builds a model to predict dates/industries that should/should not be invested in.

-Performance_After_Model_20_day: Simulates investing and uses other methods to evaluate whether the model increasing the profitability of the relative_strength program.
  
### Installation

1. Clone the repository:
curl -L https://github.com/jprich1984/Relative_Strength_Project/archive/main.zip
