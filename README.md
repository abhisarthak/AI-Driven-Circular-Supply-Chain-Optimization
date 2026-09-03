# 📦 AI-Driven Inventory Optimization & Demand Forecasting

An end-to-end data science and operations research project that combines **machine learning demand forecasting, forecast uncertainty analysis, Monte Carlo simulation, and cost-based inventory optimization** to support SKU-level replenishment decisions.

The project converts demand forecasts into practical inventory decisions such as **optimal order quantity, safety stock, and reorder point**, and presents the results through an interactive **Streamlit decision dashboard**.

---

## 🎯 Project Objective

Inventory managers need to balance two competing risks:

- **Overstocking** → higher inventory holding costs
- **Understocking** → higher shortage costs and stockout risk

The objective of this project is to build a data-driven framework that:

1. Forecasts future product demand using Machine Learning.
2. Quantifies uncertainty in the forecasts.
3. Simulates possible demand outcomes.
4. Evaluates inventory costs under different order quantities.
5. Identifies cost-effective order quantities.
6. Calculates safety stock and reorder points.
7. Compares baseline and optimized inventory policies.
8. Provides an interactive dashboard for decision-making.

---

## 🔄 Project Workflow

```text
Historical Demand Data
        ↓
Data Preparation & Feature Engineering
        ↓
Machine Learning Demand Forecasting
        ↓
Forecast Error & Uncertainty Analysis
        ↓
Monte Carlo Demand Simulation
        ↓
Inventory Cost Evaluation
        ↓
Cost-Based Order Quantity Optimization
        ↓
Safety Stock & Reorder Point Calculation
        ↓
Sensitivity Analysis
        ↓
SKU-Level & Portfolio Analysis
        ↓
Streamlit Decision Dashboard
```

## 🤖 Demand Forecasting

The first stage of the project focuses on forecasting product demand using historical inventory and sales data.

A **Random Forest Regressor** was used to learn the relationship between demand and the available product, inventory, and operational features. The model was then evaluated on a **held-out test set of 420 observations**.

### Model Performance

| Metric | Result |
|---|---:|
| MAE | 8.18 |
| RMSE | 10.65 |
| R² | **82.56%** |

The model achieved an **R² of 82.56%**, meaning it explained a substantial portion of the variation in demand within the held-out test data.

### SKU-Level Forecasts

The trained model was used to generate demand forecasts for three SKUs:

| SKU | Forecast Demand | Forecast Error Std. |
|---|---:|---:|
| SKU_A | 105.44 | 9.36 |
| SKU_B | 129.68 | 12.40 |
| SKU_C | 85.79 | 6.63 |

The **forecast error standard deviation** is used as a measure of uncertainty in the demand forecast. This uncertainty is later used in the inventory optimization stage to determine appropriate safety-stock levels.

This creates the link between the predictive and optimization stages:

**Demand Forecast → Forecast Uncertainty → Inventory Decision**
