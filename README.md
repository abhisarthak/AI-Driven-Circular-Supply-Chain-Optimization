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

## 🧹 Data Preparation & Feature Engineering

The historical dataset gives us the information needed for forecasting, but raw data is not immediately ready for a machine learning model.

Before building the forecasting model, the data was prepared so that the model could learn meaningful relationships between the available information and product demand.

The first step was to organize the data around the variables that can help explain changes in **Units Sold**. Product, inventory, ordering, pricing, promotional, seasonal, and other operating information were considered as potential inputs to the forecasting process.

Categorical information such as product, category, region, and other non-numeric variables needs to be represented in a form that a machine learning model can work with. Similarly, the date-related information needs to be handled appropriately so that useful time-related patterns can be captured.

The prepared dataset was then separated into:

- **Input features (X)** — information used by the model to predict demand.
- **Target variable (y)** — `Units Sold`, representing the demand that the model needs to forecast.

The data was subsequently divided into training and test portions. The training data was used to learn the relationship between the input variables and demand, while the held-out test data was kept separate to evaluate how well the model performs on observations it had not seen during training.

This separation is important because a model should not only perform well on the data it has already seen. It should also be able to make useful predictions on new observations.

Once the data was prepared and the training and test sets were created, the project moved to the forecasting stage.
