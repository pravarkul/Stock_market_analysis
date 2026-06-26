# Stock Market Analytics Dashboard

## Overview

An end to end Stock Market Analytics Platform built using Python, MySQL, and Power BI. The project automates the collection, transformation, storage, and visualization of stock market data from Yahoo Finance and provides interactive dashboards for stock performance analysis, technical analysis, risk assessment, and sector level insights.

The system uses an incremental update pipeline to efficiently process new market data while preventing duplicate records through database level constraints.

---

## Objectives

The primary objective of this project is to:

* Automate stock market data collection
* Store and manage historical market data in a relational database
* Calculate technical indicators for analysis
* Build interactive dashboards for decision making
* Compare stocks and sectors using risk and return metrics
* Demonstrate an end to end Data Analytics workflow

---

## Technology Stack

### Data Collection

* Python
* Yahoo Finance (yfinance)

### Data Processing

* Pandas
* NumPy

### Database

* MySQL
* SQLAlchemy
* PyMySQL

### Visualization

* Power BI

---

## Architecture

Yahoo Finance

↓

Python ETL Pipeline

↓

Data Transformation & Feature Engineering

↓

MySQL Database

↓

Incremental Update Engine

↓

Power BI Dashboard

---

## Key Features

### Automated Data Pipeline

* Automated stock market data extraction from Yahoo Finance
* Historical and incremental data loading
* Efficient daily update process

### Feature Engineering

Calculated the following technical indicators:

* Daily Return
* Price Change
* MA20 (20 Day Moving Average)
* MA50 (50 Day Moving Average)
* RSI (Relative Strength Index)
* Rolling Volatility

### Database Management

* MySQL integration for centralized storage
* Incremental update mechanism
* Duplicate prevention using unique constraints on ticker and date

### Interactive Dashboards

#### Page 1: Executive Overview

* Best Performing Stock
* Highest Return %
* Most Volatile Stock
* Risk vs Return Analysis
* Volume Analysis
* Stock Ranking

<img width="1281" height="719" alt="Page 1" src="https://github.com/user-attachments/assets/d7691a37-5ef1-4d41-a54c-8b23cf04350f" />


#### Page 2: Technical Analysis

* Candlestick Chart
* MA20 and MA50 Trend Analysis
* RSI Analysis
* Volume Trend
* Daily Return Trend
* Bullish/Bearish Signals

<img width="1280" height="722" alt="Page 2" src="https://github.com/user-attachments/assets/2c4d2dc7-9e9f-4d56-821c-90a0e418babb" />


#### Page 3: Market Comparison

* Stock Ranking
* Risk vs Return Comparison
* Heatmaps
* Performance Comparison Across Stocks

<img width="1276" height="721" alt="Page 3" src="https://github.com/user-attachments/assets/84bed3f9-d7a9-4f79-af8d-91c25e2baefb" />


#### Page 4: Sector Analysis

* Sector Performance Ranking
* Sector Risk Analysis
* Sector Return Comparison
* Sector Contribution Analysis

<img width="1281" height="719" alt="Page 4" src="https://github.com/user-attachments/assets/2ee1f6de-ecec-4640-8c98-5066c63b5f80" />



---

## Technical Challenges Solved

### Incremental Data Loading

Initially the system downloaded and processed the entire historical dataset during every execution.

The pipeline was optimized by:

* Reading the latest available date from MySQL
* Downloading only recent data
* Recalculating indicators using a rolling historical window
* Appending only new records

This significantly reduced processing time and database operations.

### Duplicate Record Prevention

Implemented a database level unique constraint using:

(ticker, date)

This prevents duplicate stock entries even if the update script is executed multiple times.

### Dynamic Power BI Measures

Developed dynamic DAX measures that correctly respond to date filters and slicers for:

* Total Return %
* Stock Ranking
* Risk Adjusted Return
* Sector Analysis

---

## Sample Insights

* Telecom sector generated the highest long term returns within the selected stock universe.
* Infrastructure sector exhibited higher volatility compared to most sectors.
* Banking stocks demonstrated strong risk adjusted performance.
* Technical indicators helped identify trend reversals and momentum shifts.

---

## Future Improvements

* Portfolio Optimization Dashboard
* Sector Rotation Analysis
* Machine Learning Based Price Forecasting
* Real Time Market Data Integration

---

## Skills Demonstrated

* Data Analytics
* Data Engineering
* ETL Development
* SQL
* Power BI
* Data Visualization
* Financial Analytics
* Feature Engineering
* Database Design
* Automation

---

## Author

Pravar Kulshrestha
