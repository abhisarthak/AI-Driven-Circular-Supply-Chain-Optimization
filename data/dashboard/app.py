import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI-Driven Supply Chain Decision Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    # The CSV files are in the same folder as app.py
    base_path = Path(__file__).parent

    data = {}

    files = {
        "orders": "order_level_data.csv",
        "customer_delay": "customer_delay.csv",
        "seller_delay": "seller_delay.csv",
        "month_delay": "month_delay.csv",
        "feature_importance": "feature_importance.csv",
        "intervention_results": "intervention_results.csv",
        "risk_distribution": "risk_distribution.csv",
        "risk_validation": "risk_validation.csv",
        "scenario_comparison": "scenario_comparison.csv"
    }

    for key, filename in files.items():

        file_path = base_path / filename

        if file_path.exists():

            try:
                data[key] = pd.read_csv(file_path)

                # Clean column names
                data[key].columns = (
                    data[key]
                    .columns
                    .astype(str)
                    .str.strip()
                )

            except Exception as e:
                st.warning(f"Could not load {filename}: {e}")

    return data


data = load_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_numeric_value(value, default=0):

    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def safe_column(df, column, default=0):

    if column in df.columns:
        return df[column]

    return pd.Series([default] * len(df))


def format_number(value):

    try:
        return f"{float(value):,.0f}"
    except Exception:
        return "N/A"


def format_percentage(value):

    try:
        return f"{float(value):.1f}%"
    except Exception:
        return "N/A"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚚 Supply Chain AI")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "",
    [
        "🏠 Executive Overview",
        "🚚 Late Delivery Intelligence",
        "♻️ Circular Recovery Optimization",
        "⚖️ Scenario Trade-offs",
        "🎯 Decision Recommendations"
    ]
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

def executive_overview(data):

    st.title("AI-Driven Supply Chain Decision Intelligence")

    st.markdown(
        """
        **An integrated analytics framework for proactive delivery-risk management
        and circular recovery optimization.**
        """
    )

    st.divider()

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_orders = 0
    late_rate = 0

    if "orders" in data:

        orders = data["orders"]

        total_orders = len(orders)

        if "is_late_delivery" in orders.columns:

            late_rate = (
                orders["is_late_delivery"]
                .mean()
                * 100
            )

    # Circular recovery KPI
    optimized_recovery = 0
    recommended_circularity = 0

    if "scenario_comparison" in data:

        scenario_df = data["scenario_comparison"].copy()

        if "circular_recovery_rate" in scenario_df.columns:

            recommended_circularity = (
                scenario_df["circular_recovery_rate"]
                .max()
            )

            if recommended_circularity <= 1:
                recommended_circularity *= 100

        if "objective_value" in scenario_df.columns:

            optimized_recovery = (
                scenario_df["objective_value"]
                .max()
            )

    # --------------------------------------------------------
    # KPI DISPLAY
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Orders",
            format_number(total_orders)
        )

    with col2:
        st.metric(
            "Late Delivery Rate",
            f"{late_rate:.2f}%"
        )

    with col3:
        st.metric(
            "Optimized Recovery Value",
            format_number(optimized_recovery)
        )

    with col4:
        st.metric(
            "Recommended Circularity",
            f"{recommended_circularity:.1f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # DECISION INTELLIGENCE FRAMEWORK
    # --------------------------------------------------------

    st.header("Decision Intelligence Framework")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🚚 Forward Logistics")

        st.markdown(
            """
            - Predict late-delivery risk
            - Segment orders into risk categories
            - Prioritize operational interventions
            - Reduce unnecessary monitoring workload
            """
        )

        if "intervention_results" in data:

            intervention_df = data["intervention_results"]

            if "Strategy" in intervention_df.columns:

                recommended = intervention_df.iloc[
                    (
                        intervention_df["Capture Rate (%)"]
                        / intervention_df["Workload (%)"].replace(0, np.nan)
                    ).idxmax()
                ]

                st.info(
                    f"""
                    Monitoring **{recommended['Workload (%)']:.1f}% of orders**
                    can capture approximately
                    **{recommended['Capture Rate (%)']:.1f}% of late deliveries**.
                    """
                )

    with col2:

        st.subheader("♻️ Reverse Logistics")

        st.markdown(
            """
            - Evaluate recovery pathways
            - Compare economic vs circular outcomes
            - Optimize product recovery allocation
            - Minimize disposal dependency
            """
        )

        if "scenario_comparison" in data:

            scenario_df = data["scenario_comparison"]

            if (
                "circular_recovery_rate" in scenario_df.columns
                and "economic_cost_pct" in scenario_df.columns
            ):

                best_circular = scenario_df.loc[
                    scenario_df["economic_cost_pct"].idxmin()
                ]

                recovery = get_numeric_value(
                    best_circular["circular_recovery_rate"]
                )

                if recovery <= 1:
                    recovery *= 100

                cost = get_numeric_value(
                    best_circular["economic_cost_pct"]
                )

                st.success(
                    f"""
                    The **{best_circular['scenario']}** policy achieves
                    approximately **{recovery:.1f}% circular recovery**
                    with a **{cost:.2f}% economic trade-off**
                    versus the best economic scenario.
                    """
                )


# ============================================================
# LATE DELIVERY INTELLIGENCE
# ============================================================

def late_delivery_intelligence(data):

    st.title("🚚 Late Delivery Intelligence")

    st.markdown(
        """
        Analyze delivery-risk patterns and identify where targeted
        intervention provides the highest operational value.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # MONTHLY DELIVERY PERFORMANCE
    # --------------------------------------------------------

    if "month_delay" in data:

        month_df = data["month_delay"].copy()

        st.header("📅 Monthly Late Delivery Pattern")

        if (
            "purchase_month" in month_df.columns
            and "Late_Delivery_Rate (%)" in month_df.columns
        ):

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.plot(
                month_df["purchase_month"],
                month_df["Late_Delivery_Rate (%)"],
                marker="o"
            )

            ax.set_xlabel("Purchase Month")
            ax.set_ylabel("Late Delivery Rate (%)")
            ax.set_title("Monthly Late Delivery Rate")

            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

    # --------------------------------------------------------
    # CUSTOMER STATE RISK
    # --------------------------------------------------------

    if "customer_delay" in data:

        customer_df = data["customer_delay"].copy()

        st.header("📍 Customer Location Risk")

        if (
            "customer_state" in customer_df.columns
            and "Late_Delivery_Rate (%)" in customer_df.columns
        ):

            top_customer = (
                customer_df
                .sort_values(
                    "Late_Delivery_Rate (%)",
                    ascending=False
                )
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.bar(
                top_customer["customer_state"],
                top_customer["Late_Delivery_Rate (%)"]
            )

            ax.set_xlabel("Customer State")
            ax.set_ylabel("Late Delivery Rate (%)")
            ax.set_title("Top Customer States by Late Delivery Risk")

            plt.xticks(rotation=45)

            st.pyplot(fig)

    # --------------------------------------------------------
    # SELLER STATE RISK
    # --------------------------------------------------------

    if "seller_delay" in data:

        seller_df = data["seller_delay"].copy()

        st.header("🏭 Seller Location Risk")

        if (
            "seller_state" in seller_df.columns
            and "Late_Delivery_Rate (%)" in seller_df.columns
        ):

            top_seller = (
                seller_df
                .sort_values(
                    "Late_Delivery_Rate (%)",
                    ascending=False
                )
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.bar(
                top_seller["seller_state"],
                top_seller["Late_Delivery_Rate (%)"]
            )

            ax.set_xlabel("Seller State")
            ax.set_ylabel("Late Delivery Rate (%)")
            ax.set_title("Top Seller States by Late Delivery Risk")

            plt.xticks(rotation=45)

            st.pyplot(fig)

    # --------------------------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------------------------

    if "feature_importance" in data:

        feature_df = data["feature_importance"].copy()

        st.header("🧠 Key Risk Drivers")

        if (
            "Feature_Group" in feature_df.columns
            and "Importance (%)" in feature_df.columns
        ):

            feature_df = feature_df.sort_values(
                "Importance (%)",
                ascending=True
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.barh(
                feature_df["Feature_Group"],
                feature_df["Importance (%)"]
            )

            ax.set_xlabel("Importance (%)")
            ax.set_ylabel("Feature Group")
            ax.set_title("Feature Importance in Late Delivery Prediction")

            st.pyplot(fig)

    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    if "risk_distribution" in data:

        risk_df = data["risk_distribution"].copy()

        st.header("⚠️ Distribution of Orders Across Risk Categories")

        # Handle different CSV formats safely
        if len(risk_df.columns) >= 2:

            category_col = risk_df.columns[0]
            value_col = risk_df.columns[1]

            fig, ax = plt.subplots(figsize=(10, 5))

            bars = ax.bar(
                risk_df[category_col].astype(str),
                risk_df[value_col]
            )

            ax.set_xlabel("Risk Category")
            ax.set_ylabel("Number of Orders")
            ax.set_title(
                "Distribution of Orders Across Late-Delivery Risk Categories"
            )

            for bar in bars:

                height = bar.get_height()

                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{height:,.0f}",
                    ha="center",
                    va="bottom"
                )

            st.pyplot(fig)

    # --------------------------------------------------------
    # INTERVENTION STRATEGY
    # --------------------------------------------------------

    if "intervention_results" in data:

        intervention_df = data["intervention_results"].copy()

        st.header("🎯 Risk-Based Monitoring Strategy")

        if (
            "Strategy" in intervention_df.columns
            and "Workload (%)" in intervention_df.columns
            and "Capture Rate (%)" in intervention_df.columns
        ):

            fig, ax = plt.subplots(figsize=(10, 6))

            ax.scatter(
                intervention_df["Workload (%)"],
                intervention_df["Capture Rate (%)"],
                s=120
            )

            # Random baseline
            max_value = max(
                intervention_df["Workload (%)"].max(),
                intervention_df["Capture Rate (%)"].max()
            )

            ax.plot(
                [0, max_value],
                [0, max_value],
                linestyle="--",
                label="Random Monitoring Baseline"
            )

            for _, row in intervention_df.iterrows():

                ax.annotate(
                    row["Strategy"],
                    (
                        row["Workload (%)"],
                        row["Capture Rate (%)"]
                    ),
                    xytext=(8, 5),
                    textcoords="offset points"
                )

            ax.set_xlabel("Operational Workload (%)")
            ax.set_ylabel("Late Deliveries Captured (%)")

            ax.set_title(
                "Risk-Based Monitoring: Workload vs Late-Delivery Capture"
            )

            ax.legend()
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)


# ============================================================
# CIRCULAR RECOVERY OPTIMIZATION
# ============================================================

def circular_recovery_optimization(data):

    st.title("♻️ Circular Recovery Optimization")

    st.markdown(
        """
        Optimize product recovery pathways to balance economic value,
        circularity, and disposal reduction.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # DATA CHECK
    # --------------------------------------------------------

    if "scenario_comparison" not in data:

        st.warning("Scenario comparison data is not available.")

        return

    scenario_df = data["scenario_comparison"].copy()

    # Clean column names again for safety
    scenario_df.columns = (
        scenario_df.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # KPI SECTION
    # --------------------------------------------------------

    st.header("📊 Circular Recovery Performance")

    best_economic = None
    best_circular = None

    if "objective_value" in scenario_df.columns:

        best_economic = scenario_df.loc[
            scenario_df["objective_value"].idxmax()
        ]

    if "circular_recovery_rate" in scenario_df.columns:

        best_circular = scenario_df.loc[
            scenario_df["circular_recovery_rate"].idxmax()
        ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if best_economic is not None:

            st.metric(
                "Best Economic Scenario",
                str(best_economic["scenario"])
            )

    with col2:

        if best_economic is not None:

            st.metric(
                "Maximum Objective Value",
                format_number(
                    best_economic["objective_value"]
                )
            )

    with col3:

        if best_circular is not None:

            recovery = get_numeric_value(
                best_circular["circular_recovery_rate"]
            )

            if recovery <= 1:
                recovery *= 100

            st.metric(
                "Maximum Circular Recovery",
                f"{recovery:.1f}%"
            )

    with col4:

        if (
            best_circular is not None
            and "economic_cost_pct" in scenario_df.columns
        ):

            cost = get_numeric_value(
                best_circular["economic_cost_pct"]
            )

            st.metric(
                "Economic Trade-off",
                f"{cost:.2f}%"
            )

    st.divider()

    # --------------------------------------------------------
    # SCENARIO COMPARISON TABLE
    # --------------------------------------------------------

    st.header("📋 Scenario Comparison")

    display_columns = [
        col for col in [
            "scenario",
            "objective_value",
            "circular_recovery_rate",
            "economic_cost_pct",
            "max_disposal_pct"
        ]
        if col in scenario_df.columns
    ]

    st.dataframe(
        scenario_df[display_columns],
        use_container_width=True
    )

    # --------------------------------------------------------
    # ECONOMIC VS CIRCULARITY
    # --------------------------------------------------------

    if (
        "economic_cost_pct" in scenario_df.columns
        and "circular_recovery_rate" in scenario_df.columns
        and "scenario" in scenario_df.columns
    ):

        st.header("⚖️ Economic vs Circular Recovery Trade-off")

        fig, ax = plt.subplots(figsize=(10, 6))

        x = scenario_df["economic_cost_pct"]

        y = scenario_df["circular_recovery_rate"].copy()

        # Convert to percentage if stored as decimal
        if y.max() <= 1:
            y = y * 100

        ax.scatter(
            x,
            y,
            s=180
        )

        for _, row in scenario_df.iterrows():

            recovery = get_numeric_value(
                row["circular_recovery_rate"]
            )

            if recovery <= 1:
                recovery *= 100

            ax.annotate(
                str(row["scenario"]),
                (
                    get_numeric_value(row["economic_cost_pct"]),
                    recovery
                ),
                xytext=(8, 5),
                textcoords="offset points"
            )

        ax.set_xlabel("Economic Cost vs Best Scenario (%)")
        ax.set_ylabel("Circular Recovery Rate (%)")

        ax.set_title(
            "Economic Cost vs Circular Recovery Trade-off"
        )

        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

    # --------------------------------------------------------
    # RECOVERY PATHWAY ALLOCATION
    # --------------------------------------------------------

    pathway_columns = [
        "resell",
        "repair",
        "refurbishment",
        "recycling"
    ]

    available_pathways = [
        col for col in pathway_columns
        if col in scenario_df.columns
    ]

    if available_pathways:

        st.header("♻️ Recovery Pathway Allocation")

        fig, ax = plt.subplots(figsize=(11, 6))

        scenario_df.set_index("scenario")[
            available_pathways
        ].plot(
            kind="bar",
            stacked=True,
            ax=ax
        )

        ax.set_xlabel("Scenario")
        ax.set_ylabel("Allocation")
        ax.set_title("Recovery Pathway Allocation by Scenario")

        plt.xticks(rotation=0)

        st.pyplot(fig)

    # --------------------------------------------------------
    # DISPOSAL ANALYSIS
    # --------------------------------------------------------

    if (
        "max_disposal_pct" in scenario_df.columns
        and "scenario" in scenario_df.columns
    ):

        st.header("🗑️ Disposal Reduction Constraint")

        disposal_values = scenario_df[
            "max_disposal_pct"
        ].copy()

        if disposal_values.max() <= 1:
            disposal_values = disposal_values * 100

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            scenario_df["scenario"],
            disposal_values
        )

        ax.set_xlabel("Scenario")
        ax.set_ylabel("Maximum Disposal (%)")

        ax.set_title(
            "Maximum Disposal Allowed Across Scenarios"
        )

        plt.xticks(rotation=0)

        st.pyplot(fig)


# ============================================================
# SCENARIO TRADE-OFFS
# ============================================================

def scenario_tradeoffs(data):

    st.title("⚖️ Scenario Trade-offs")

    st.markdown(
        """
        Compare economic performance, circular recovery, and disposal
        constraints across alternative supply chain policies.
        """
    )

    st.divider()

    if "scenario_comparison" not in data:

        st.warning("Scenario comparison data is not available.")

        return

    scenario_df = data["scenario_comparison"].copy()

    scenario_df.columns = (
        scenario_df.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # OBJECTIVE VALUE
    # --------------------------------------------------------

    if (
        "scenario" in scenario_df.columns
        and "objective_value" in scenario_df.columns
    ):

        st.header("💰 Economic Performance")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            scenario_df["scenario"],
            scenario_df["objective_value"]
        )

        ax.set_xlabel("Scenario")
        ax.set_ylabel("Objective Value")

        ax.set_title("Economic Performance Across Scenarios")

        st.pyplot(fig)

    # --------------------------------------------------------
    # CIRCULAR RECOVERY
    # --------------------------------------------------------

    if (
        "scenario" in scenario_df.columns
        and "circular_recovery_rate" in scenario_df.columns
    ):

        st.header("♻️ Circular Recovery Performance")

        recovery = scenario_df[
            "circular_recovery_rate"
        ].copy()

        if recovery.max() <= 1:
            recovery = recovery * 100

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            scenario_df["scenario"],
            recovery
        )

        ax.set_xlabel("Scenario")
        ax.set_ylabel("Circular Recovery Rate (%)")

        ax.set_title(
            "Circular Recovery Across Scenarios"
        )

        st.pyplot(fig)

    # --------------------------------------------------------
    # ECONOMIC TRADE-OFF
    # --------------------------------------------------------

    if (
        "scenario" in scenario_df.columns
        and "economic_cost_pct" in scenario_df.columns
    ):

        st.header("📉 Economic Cost of Circularity")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            scenario_df["scenario"],
            scenario_df["economic_cost_pct"]
        )

        ax.set_xlabel("Scenario")
        ax.set_ylabel("Economic Cost vs Best Scenario (%)")

        ax.set_title(
            "Economic Trade-off Across Circular Policies"
        )

        st.pyplot(fig)

    # --------------------------------------------------------
    # KEY INSIGHT
    # --------------------------------------------------------

    if (
        "circular_recovery_rate" in scenario_df.columns
        and "economic_cost_pct" in scenario_df.columns
    ):

        st.divider()

        st.header("💡 Decision Insight")

        tradeoff_score = (
            scenario_df["circular_recovery_rate"]
            /
            (
                scenario_df["economic_cost_pct"]
                .abs()
                + 0.01
            )
        )

        recommended = scenario_df.loc[
            tradeoff_score.idxmax()
        ]

        recovery = get_numeric_value(
            recommended["circular_recovery_rate"]
        )

        if recovery <= 1:
            recovery *= 100

        cost = get_numeric_value(
            recommended["economic_cost_pct"]
        )

        st.success(
            f"""
### Recommended Balanced Policy: {recommended["scenario"]}

This scenario provides a strong balance between circular recovery
and economic performance.

- **Circular Recovery:** {recovery:.1f}%
- **Economic Trade-off:** {cost:.2f}%
            """
        )


# ============================================================
# DECISION RECOMMENDATIONS
# ============================================================

def decision_recommendations(data):

    st.title("🎯 Decision Recommendations")

    st.markdown(
        """
        Integrated recommendations combining predictive delivery-risk
        analytics and circular recovery optimization.
        """
    )

    st.divider()

    # ========================================================
    # FORWARD LOGISTICS
    # ========================================================

    st.header("🚚 Forward Logistics Recommendation")

    if "intervention_results" in data:

        intervention_df = data[
            "intervention_results"
        ].copy()

        intervention_df.columns = (
            intervention_df.columns
            .astype(str)
            .str.strip()
        )

        required_columns = [
            "Strategy",
            "Orders Monitored",
            "Workload (%)",
            "Capture Rate (%)"
        ]

        if all(
            col in intervention_df.columns
            for col in required_columns
        ):

            # Practical efficiency:
            # maximize late-delivery capture relative to workload
            intervention_df["efficiency_score"] = (
                intervention_df["Capture Rate (%)"]
                /
                intervention_df["Workload (%)"].replace(0, np.nan)
            )

            recommended_strategy = intervention_df.loc[
                intervention_df["efficiency_score"].idxmax()
            ]

            strategy = str(
                recommended_strategy["Strategy"]
            )

            orders_monitored = get_numeric_value(
                recommended_strategy["Orders Monitored"]
            )

            workload = get_numeric_value(
                recommended_strategy["Workload (%)"]
            )

            capture_rate = get_numeric_value(
                recommended_strategy["Capture Rate (%)"]
            )

            st.success(
                f"""
### Recommended Strategy: {strategy}

- **Orders monitored:** {orders_monitored:,.0f}
- **Operational workload:** {workload:.1f}%
- **Late deliveries captured:** {capture_rate:.1f}%

This strategy provides the strongest practical balance between
intervention workload and late-delivery detection.
                """
            )

        else:

            st.warning(
                "Required intervention strategy columns are missing."
            )

    else:

        st.warning(
            "Intervention results are not available."
        )

    st.divider()

    # ========================================================
    # REVERSE LOGISTICS
    # ========================================================

    st.header("♻️ Reverse Logistics Recommendation")

    if "scenario_comparison" in data:

        scenario_df = data[
            "scenario_comparison"
        ].copy()

        scenario_df.columns = (
            scenario_df.columns
            .astype(str)
            .str.strip()
        )

        required_columns = [
            "scenario",
            "circular_recovery_rate",
            "economic_cost_pct"
        ]

        if all(
            col in scenario_df.columns
            for col in required_columns
        ):

            # Balance circularity and economic cost
            scenario_df["balance_score"] = (
                scenario_df["circular_recovery_rate"]
                /
                (
                    scenario_df["economic_cost_pct"]
                    .abs()
                    + 0.01
                )
            )

            recommended_circular = scenario_df.loc[
                scenario_df["balance_score"].idxmax()
            ]

            scenario_name = str(
                recommended_circular["scenario"]
            )

            circular_rate = get_numeric_value(
                recommended_circular[
                    "circular_recovery_rate"
                ]
            )

            # Convert decimal to percentage if necessary
            if circular_rate <= 1:
                circular_rate = circular_rate * 100

            economic_cost = get_numeric_value(
                recommended_circular[
                    "economic_cost_pct"
                ]
            )

            st.info(
                f"""
### Recommended Circular Policy: {scenario_name}

- **Circular Recovery Rate:** {circular_rate:.1f}%
- **Economic Cost vs Best Scenario:** {economic_cost:.2f}%

This policy provides the strongest balance between circular recovery
and economic performance while reducing dependency on disposal.
                """
            )

        else:

            st.warning(
                "Required circular recovery columns are missing."
            )

    else:

        st.warning(
            "Scenario comparison data is not available."
        )

    # ========================================================
    # INTEGRATED DECISION
    # ========================================================

    st.divider()

    st.header("🧠 Integrated Supply Chain Decision")

    st.markdown(
        """
### Recommended Operating Framework

**1. Predict and Prioritize**
- Use delivery-risk segmentation to identify high-risk orders.
- Focus monitoring resources where late-delivery probability is highest.

**2. Optimize Intervention Workload**
- Avoid monitoring every order.
- Use targeted risk categories to maximize late-delivery capture.

**3. Recover Product Value**
- Allocate returned products across resell, repair, refurbishment,
  and recycling pathways.

**4. Balance Profit and Circularity**
- Select policies based on both economic performance and circular
  recovery outcomes.

**5. Support Decision Intelligence**
- Combine predictive analytics with optimization to move from
  reactive supply chain management toward proactive decision-making.
        """
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "🏠 Executive Overview":

    executive_overview(data)


elif page == "🚚 Late Delivery Intelligence":

    late_delivery_intelligence(data)


elif page == "♻️ Circular Recovery Optimization":

    circular_recovery_optimization(data)


elif page == "⚖️ Scenario Trade-offs":

    scenario_tradeoffs(data)


elif page == "🎯 Decision Recommendations":

    decision_recommendations(data)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Driven Circular Supply Chain Decision Intelligence | "
    "Predictive Analytics + Risk Segmentation + Circular Optimization"
)