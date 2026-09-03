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

## 📊 Historical Demand Data

Every inventory decision starts with understanding what has happened in the past.

The project begins with historical retail data containing information about product sales, inventory levels, orders, pricing, promotions, seasonality, and other operating conditions. The main demand measure used in the project is **Units Sold**, which represents the observed demand for a product.

The dataset contains information at the product and store level, allowing demand to be studied in the context of different products, locations, and operating conditions.

Some of the important variables available in the dataset include:

| Category | Variables |
|---|---|
| Demand | Units Sold |
| Inventory | Inventory Level |
| Orders | Units Ordered |
| Product | Product ID, Category |
| Location | Store ID, Region |
| Pricing | Price, Discount, Competitor Pricing |
| External Conditions | Weather Condition, Holiday/Promotion |
| Time & Seasonality | Date, Seasonality |

Rather than looking at demand as an isolated number, the project uses these surrounding factors to understand the conditions under which demand changes.

For the final inventory decision analysis, the project focuses on three representative SKUs:

- `SKU_A`
- `SKU_B`
- `SKU_C`

The historical data is therefore the starting point of the entire analysis. However, raw historical data cannot be directly given to a forecasting model. It first needs to be cleaned, organized, and converted into useful model features.

This leads to the next stage of the project:

**Historical Data → Data Preparation & Feature Engineering → Demand Forecasting**
