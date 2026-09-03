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

## 🤖 Machine Learning Demand Forecasting

Once the data was prepared, the next question was straightforward:

**Can we use the information from the past to estimate future product demand?**

To answer this, a **Random Forest Regressor** was used as the demand forecasting model. The model learns patterns between the prepared input features and the observed demand (`Units Sold`) from the training data.

Random Forest was selected because it can capture non-linear relationships between different factors without requiring a simple linear relationship between the inputs and demand.

The model was trained on the training portion of the dataset and then used to predict demand for the observations kept aside for testing.

### Model Evaluation

The model was evaluated using three commonly used regression metrics:

| Metric | Result |
|---|---:|
| MAE | 8.18 |
| RMSE | 10.65 |
| R² | **82.56%** |

The evaluation was performed on a **held-out test set containing 420 observations**.

An **MAE of 8.18** means that, on average, the model's predicted demand differed from the observed demand by about 8.18 units.

The **RMSE of 10.65** provides additional information about larger forecasting errors, while the **R² of 82.56%** indicates that the model explains a substantial portion of the variation in demand within the held-out test data.

### Forecasts for the Selected SKUs

After evaluating the model, it was used to generate demand forecasts for the three SKUs considered in the inventory analysis:

| SKU | Forecast Demand |
|---|---:|
| SKU_A | 105.44 |
| SKU_B | 129.68 |
| SKU_C | 85.79 |

At this point, we have an estimate of **how much demand to expect** for each SKU.

However, a forecast is still only an estimate. Actual demand can be higher or lower than the predicted value.

That raises the next important question:

**How uncertain are these forecasts?**

To answer this, the project moves from prediction to **forecast-error and uncertainty analysis**.

## 🎲 Forecast Error & Uncertainty Analysis

The demand forecasting model gives us an expected demand for each SKU, but in inventory planning, knowing the expected demand is only part of the problem.

In reality, demand does not always follow the forecast. Some days may have higher demand than expected, while others may have lower demand. If we ignore this variation, an order quantity based only on the forecast may leave too little inventory when demand unexpectedly increases.

To capture this uncertainty, the project looks at the **forecast errors** produced by the model.

A forecast error represents the difference between the actual demand and the demand predicted by the model. Instead of treating every forecasting error separately, the project summarizes their variation using the **standard deviation of the forecast errors**.

This gives us a measure of how uncertain the model's demand predictions are for each SKU.

### Forecast Uncertainty by SKU

| SKU | Forecast Demand | Forecast Error Std. |
|---|---:|---:|
| SKU_A | 105.44 | 9.36 |
| SKU_B | 129.68 | 12.40 |
| SKU_C | 85.79 | 6.63 |

The results show that the three SKUs do not have the same level of forecasting uncertainty.

For example, **SKU_B has the highest forecast-error variability**, meaning its demand predictions show greater variation around the actual demand. SKU_C, on the other hand, has lower forecast-error variability.

This difference is important for inventory planning. A SKU with more uncertain demand generally needs more protection against unexpected demand, while a more predictable SKU may require less.

Therefore, the project does not use the same uncertainty level for every SKU. Instead, the uncertainty observed from the forecasting model is carried forward into the inventory planning stage.

The next step is to understand how this uncertainty can affect inventory costs under different possible demand outcomes.

## 🎯 Monte Carlo Demand Simulation

After measuring the uncertainty in the forecasts, the next question is:

**What could actual demand look like if the forecast does not turn out exactly as expected?**

To answer this, the project uses **Monte Carlo simulation**.

Instead of assuming that future demand will always be exactly equal to the forecast, the simulation generates a large number of possible demand outcomes around the forecast using the observed forecast-error variability.

For each SKU, the forecast acts as the expected demand level, while the standard deviation of the forecast errors represents how much the actual demand can vary around that estimate.

The basic idea is:

```text
Forecast Demand
      +
Forecast Uncertainty
      ↓
Generate Many Possible Demand Outcomes
      ↓
Calculate Inventory Cost for Each Outcome
      ↓
Estimate Expected Cost for Different Order Quantities
```

## 💰 Inventory Cost Evaluation & Optimization

Once the possible demand outcomes have been generated through simulation, the next problem is to decide:

**How much should we actually order?**

Ordering too little can lead to shortages when demand is higher than expected. Ordering too much can leave excess inventory and increase the cost of holding stock.

The project therefore evaluates different order quantities against the simulated demand scenarios.

For each candidate order quantity, the model estimates the resulting inventory cost by considering the balance between:

- **Excess inventory** when the order quantity is higher than the realized demand.
- **Shortage** when the realized demand is higher than the available quantity.

The expected cost across the simulated demand outcomes is then used to compare different order quantities.

### Finding the Optimal Order Quantity

Rather than simply using the forecast demand as the order quantity, the project searches across possible order quantities and identifies the quantity associated with the **minimum estimated expected cost**.

This creates the following decision process:

```text
Simulated Demand Scenarios
          ↓
Test Different Order Quantities
          ↓
Calculate Cost Under Each Scenario
          ↓
Average Cost Across Scenarios
          ↓
Select Quantity with Minimum Expected Cost
```

## 🛡️ Safety Stock & Reorder Point

Finding the right order quantity answers **“how much should we order?”**, but inventory management also needs to answer another question:

**“When should we place the order?”**

This is where **safety stock** and the **reorder point** come into the picture.

Because demand can vary from the forecast, some additional inventory is kept as a buffer against unexpected demand during the supplier lead time. This additional inventory is called **safety stock**.

In this project, safety stock is based on the uncertainty observed in the model's forecast errors. A **95% service level** is used as the base policy assumption, together with a **5-day lead time**.

The safety stock is therefore driven by:

- Forecast uncertainty
- Desired service level
- Lead time

The reorder point then combines the expected demand during the lead time with this safety-stock buffer.


::contentReference[oaicite:0]{index=0}


### SKU-Level Replenishment Policy

Using the forecast-error variability for each SKU gives the following inventory protection levels:

| SKU | Forecast Demand | Forecast Error Std. | Safety Stock | Reorder Point |
|---|---:|---:|---:|---:|
| SKU_A | 105.44 | 9.36 | 34.43 | 561.63 |
| SKU_B | 129.68 | 12.40 | 45.61 | 694.01 |
| SKU_C | 85.79 | 6.63 | 24.39 | 453.34 |

The differences between the SKUs are important. SKU_B has the highest forecast uncertainty among the three SKUs and consequently requires the largest safety-stock buffer.

This means the inventory policy is not the same for every product. Each SKU receives a replenishment recommendation based on its own expected demand and uncertainty.

The resulting policy can be viewed as:

```text
Expected Demand
      +
Demand Uncertainty
      +
Lead Time
      ↓
Safety Stock
      ↓
Reorder Point
      ↓
Replenishment Decision
```

## 🔬 Sensitivity Analysis

An inventory policy depends not only on the forecast, but also on the assumptions used to make the decision.

For example, a company that considers stockouts very expensive may be willing to hold more inventory. Similarly, a company targeting a higher service level will generally need a larger safety-stock buffer.

To understand how sensitive the inventory decisions are to these assumptions, the project performs **what-if and sensitivity analysis**.

Two important factors are examined:

1. **Shortage Cost**
2. **Service Level**

### 1. Shortage Cost Sensitivity

Shortage cost represents the penalty associated with not having enough inventory to meet demand.

The model was tested with different shortage-cost assumptions:

| Shortage Cost | Optimal Order Quantity |
|---:|---:|
| 5 | 123 |
| 10 | 127 |
| 20 | 131 |
| 30 | 133 |
| 50 | 135 |

The results show a clear pattern: as the cost of a shortage increases, the recommended order quantity also increases.

This makes intuitive sense. When running out of stock becomes more expensive, the optimization model places greater value on protecting against high-demand outcomes.

In other words:

**Higher Shortage Cost → Greater Protection Against Shortage → Higher Optimal Order Quantity**

---

### 2. Service-Level Sensitivity

The project also examines how the required service level affects safety stock.

| Service Level | Z-value | Safety Stock |
|---:|---:|---:|
| 90% | 1.28 | 30.12 |
| 95% | 1.65 | 38.82 |
| 97% | 1.88 | 44.23 |
| 99% | 2.33 | 54.82 |

As the target service level increases, more safety stock is required.

This illustrates an important inventory trade-off:

**Higher Service Level → More Safety Stock → Greater Inventory Protection**

However, greater protection also means holding more inventory. Therefore, the appropriate service level depends on how the business balances inventory cost against the risk of shortages.

---

### What-If Analysis

The same idea is incorporated into the interactive dashboard, where users can change demand and uncertainty assumptions and observe how the resulting **safety stock and reorder point** change.

This allows the model to answer practical questions such as:

> *“What happens to our inventory requirement if expected demand increases?”*

or

> *“What happens if demand becomes more uncertain?”*

The purpose of this analysis is not to identify one universally correct inventory policy. Instead, it shows how inventory decisions respond to changes in the assumptions behind them.

This makes the framework more useful for decision-making because users can understand not only **what the recommended decision is**, but also **why that decision changes when the business situation changes**.

## 📦 SKU-Level & Portfolio Analysis

So far, the analysis has looked at the inventory decision for each SKU separately.

However, an inventory manager is usually not responsible for only one product. The more useful question is:

**What happens when these individual SKU decisions are considered together?**

The project therefore compares the three SKUs side by side and evaluates how their demand, uncertainty, inventory requirements, and costs differ.

### Comparing the SKUs

Each SKU has a different demand profile and therefore receives a different inventory recommendation.

| SKU | Forecast Demand | Optimal Q | Safety Stock | Reorder Point | Estimated Cost Reduction |
|---|---:|---:|---:|---:|---:|
| SKU_A | 105.44 | 115 | 34.43 | 561.63 | 18.28% |
| SKU_B | 129.68 | 142 | 45.61 | 694.01 | 19.63% |
| SKU_C | 85.79 | 92 | 24.39 | 453.34 | 14.64% |

The comparison highlights an important point: **the same inventory policy does not need to be applied to every SKU.**

For example, SKU_B has both the highest forecast demand and the highest forecast-error variability among the three SKUs. As a result, it receives the highest order quantity, safety stock, and reorder point.

SKU_C has lower expected demand and lower forecast uncertainty, resulting in lower inventory requirements.

### Portfolio-Level Impact

The individual SKU decisions are then combined to understand their overall impact.

| Measure | Portfolio Result |
|---|---:|
| Baseline Expected Cost | 289.23 |
| Optimized Expected Cost | 237.83 |
| Estimated Savings | 51.39 |
| Estimated Cost Reduction | **17.77%** |

The optimized policy reduces the estimated portfolio cost from **289.23 to 237.83**, giving an estimated saving of **51.39**, or **17.77%** under the modeled assumptions.

The portfolio analysis therefore shows that the value of optimization does not come from applying one fixed rule to all products. Instead, it comes from using the demand and uncertainty characteristics of each SKU to make more appropriate inventory decisions.

### From Analysis to Decision

At this point, the project has produced several outputs:

- A demand forecast for each SKU
- A measure of forecast uncertainty
- Simulated demand scenarios
- An optimized order quantity
- Safety-stock requirements
- Reorder points
- Estimated cost impact
- SKU-level priorities

The next challenge is making all of these results easy to understand and use.

Rather than requiring a user to go through notebooks and calculations, the project brings these outputs together into an interactive decision-support dashboard.
