import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

# ---------------- SAFE DIVISION FUNCTION ---------------- #

def safe_divide(a, b):

    # HANDLE SINGLE NUMBER DIVISION
    if isinstance(
        b,
        (int, float, np.int64, np.float64)
    ):

        if b == 0:
            return 0

        return a / b

    # HANDLE SERIES DIVISION
    return a.div(
        b.where(b != 0, pd.NA)
    ).fillna(0)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Marketing Analytics Dashboard -TheBuziHub",
    page_icon="thebuzihub.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.image("tbhsidebar.png", width=120)

st.title("Marketing Analytics Dashboard - ᴛʜᴇʙᴜᴢɪʜᴜʙ")

st.info(
    "📘 First time using the dashboard? "
    "Review the Excel template structure and user guide before uploading your file."
)

st.link_button(
    "Open User Guide",
    "https://docs.google.com/document/d/1UpCMJNBtDmD3B0rOBUrQDmCdZEAIrXmYFvf6-PTUNnY/edit?usp=sharing"
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

# ---------------- PROCESS FILE ---------------- #

if uploaded_file is not None:

    try:

        # READ SHEET
        df = pd.read_excel(
            uploaded_file,
            sheet_name="Month_Python"
        )

        # READ YTD SHEET
        ytd_df = pd.read_excel(
            uploaded_file,
            sheet_name="YTD_Python"
        )

        # ---------------- REQUIRED COLUMNS ---------------- #

        required_columns = [
            "Month",
            "Company",
            "Channel",
            "Amount Spent",
            "Prospects",
            "Leads",
            "Contracts",
            "Revenue Amount",
            "Target ROAS"
        ]

        required_ytd_columns = [
            "Company",
            "Channel",
            "Amount Spent",
            "Prospects",
            "Leads",
            "Contracts",
            "Revenue Amount",
            "Target ROAS"
        ]

        # ---------------- VALIDATE MONTH SHEET ---------------- #

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:

            st.error(
                f"""
                Month_Python sheet is missing columns:

                {missing_columns}
                """
            )

            st.stop()

        # ---------------- VALIDATE YTD SHEET ---------------- #

        missing_ytd_columns = [
            col for col in required_ytd_columns
            if col not in ytd_df.columns
        ]

        if missing_ytd_columns:

            st.error(
                f"""
                YTD_Python sheet is missing columns:

                {missing_ytd_columns}
                """
            )

            st.stop()

        # ---------------- CLEAN CURRENCY COLUMNS ---------------- #

        currency_columns = [
            "Amount Spent",
            "Revenue Amount"
        ]

        for col in currency_columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace("AED", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        # ---------------- CLEAN OTHER NUMERIC COLUMNS ---------------- #

        numeric_columns = [
            "Prospects",
            "Leads",
            "Contracts",
            "Target ROAS"
        ]

        for col in numeric_columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        # ---------------- CLEAN YTD CURRENCY COLUMNS ---------------- #

        for col in currency_columns:

            ytd_df[col] = (
                ytd_df[col]
                .astype(str)
                .str.replace("AED", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            ytd_df[col] = pd.to_numeric(
                ytd_df[col],
                errors="coerce"
            )

        # ---------------- CLEAN YTD NUMERIC COLUMNS ---------------- #

        for col in numeric_columns:

            ytd_df[col] = pd.to_numeric(
                ytd_df[col],
                errors="coerce"
            )

        # ---------------- KPI CALCULATIONS ---------------- #

        # CPP
        df["CPP"] = safe_divide(
            df["Amount Spent"],
            df["Prospects"]
        )

        # PRS TO LEAD %
        df["PRS to Lead %"] = (
            safe_divide(
                df["Leads"],
                df["Prospects"]
            ) * 100
        )

        # CPL
        df["CPL"] = safe_divide(
            df["Amount Spent"],
            df["Leads"]
        )

        # COST PER CONTRACT
        df["Cost Per Contract"] = safe_divide(
            df["Amount Spent"],
            df["Contracts"]
        )

        # REVENUE PER ORDER
        df["Revenue Per Order"] = safe_divide(
            df["Revenue Amount"],
            df["Contracts"]
        )

        # CONVERSION RATE %
        df["Conversion Rate %"] = (
            safe_divide(
                df["Contracts"],
                df["Leads"]
            ) * 100
        )

        # LEAD QUALITY %
        df["Lead Quality %"] = (
            safe_divide(
                df["Leads"],
                df["Prospects"]
            ) * 100
        )

        # CLOSE RATE %
        df["Close Rate %"] = (
            safe_divide(
                df["Contracts"],
                df["Leads"]
            ) * 100
        )

        # ROAS %
        df["ROAS %"] = (
            safe_divide(
                df["Revenue Amount"],
                df["Amount Spent"]
            ) * 100
        )

        # ROAS AED
        df["ROAS AED"] = safe_divide(
            df["Revenue Amount"],
            df["Amount Spent"]
        )

        # DIFF ROAS
        df["DIFF ROAS"] = (
            df["ROAS AED"] - df["Target ROAS"]
        )

        # ---------------- YTD KPI CALCULATIONS ---------------- #

        # CPP
        ytd_df["CPP"] = safe_divide(
            ytd_df["Amount Spent"],
            ytd_df["Prospects"]
        )

        # PRS TO LEAD %
        ytd_df["PRS to Lead %"] = (
            safe_divide(
                ytd_df["Leads"],
                ytd_df["Prospects"]
            ) * 100
        )

        # CPL
        ytd_df["CPL"] = safe_divide(
            ytd_df["Amount Spent"],
            ytd_df["Leads"]
        )

        # COST PER CONTRACT
        ytd_df["Cost Per Contract"] = safe_divide(
            ytd_df["Amount Spent"],
            ytd_df["Contracts"]
        )

        # REVENUE PER ORDER
        ytd_df["Revenue Per Order"] = safe_divide(
            ytd_df["Revenue Amount"],
            ytd_df["Contracts"]
        )

        # CONVERSION RATE %
        ytd_df["Conversion Rate %"] = (
            safe_divide(
                ytd_df["Contracts"],
                ytd_df["Leads"]
            ) * 100
        )

        # LEAD QUALITY %
        ytd_df["Lead Quality %"] = (
            safe_divide(
                ytd_df["Leads"],
                ytd_df["Prospects"]
            ) * 100
        )

        # CLOSE RATE %
        ytd_df["Close Rate %"] = (
            safe_divide(
                ytd_df["Contracts"],
                ytd_df["Leads"]
            ) * 100
        )

        # ROAS %
        ytd_df["ROAS %"] = (
            safe_divide(
                ytd_df["Revenue Amount"],
                ytd_df["Amount Spent"]
            ) * 100
        )

        # ROAS AED
        ytd_df["ROAS AED"] = safe_divide(
            ytd_df["Revenue Amount"],
            ytd_df["Amount Spent"]
        )

        # DIFF ROAS
        ytd_df["DIFF ROAS"] = (
            ytd_df["ROAS AED"] - ytd_df["Target ROAS"]
        )

        # ---------------- SIDEBAR FILTERS ---------------- #

        st.sidebar.header("Filters")

        # YEAR FILTER
        selected_years = st.sidebar.multiselect(
            "Select Year",
            options=sorted(df["Year"].unique()),
            default=sorted(df["Year"].unique())
        )

        # MONTH FILTER
        selected_months = st.sidebar.multiselect(
            "Select Month",
            options=df["Month"].unique(),
            default=df["Month"].unique()
        )

        # COMPANY FILTER
        selected_companies = st.sidebar.multiselect(
            "Select Company",
            options=df["Company"].unique(),
            default=df["Company"].unique()
        )

        # CHANNEL FILTER
        selected_channels = st.sidebar.multiselect(
            "Select Channel",
            options=df["Channel"].unique(),
            default=df["Channel"].unique()
        )

        # ---------------- FILTERED DATAFRAME ---------------- #

        filtered_df = df[
            (df["Year"].isin(selected_years)) &
            (df["Month"].isin(selected_months)) &
            (df["Company"].isin(selected_companies)) &
            (df["Channel"].isin(selected_channels))
        ]

        # ---------------- SUCCESS MESSAGE ---------------- #

        st.success("Data Processed Successfully!")

        # ---------------- TABS ---------------- #

        monthly_tab, budget_tab, forecast_tab, ytd_tab = st.tabs([
            "Monthly Analytics",
            "Budget & Planning",
            "Forecast & Projections",
            "YTD Analytics"
        ])

        with monthly_tab:
            # ---------------- KPI CALCULATIONS ---------------- #

            total_spend = filtered_df["Amount Spent"].sum()

            total_revenue = filtered_df["Revenue Amount"].sum()

            total_contracts = filtered_df["Contracts"].sum()

            overall_roas = safe_divide(
                total_revenue,
                total_spend
            )

            # NEW KPI
            total_leads = filtered_df["Leads"].sum()

            avg_cpl = safe_divide(
                total_spend,
                total_leads
            )

            avg_cpa = safe_divide(
                total_spend,
                total_contracts
            )

            # BEST CHANNEL
            channel_performance = (
                filtered_df.groupby("Channel")["Revenue Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            best_channel = (
                channel_performance.index[0]
                if not channel_performance.empty
                else "N/A"
            )

            # BEST COMPANY
            company_performance = (
                filtered_df.groupby("Company")["Revenue Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            best_company = (
                company_performance.index[0]
                if not company_performance.empty
                else "N/A"
            )

            # ---------------- KPI DISPLAY ---------------- #

            st.subheader("Dashboard Overview")

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            col1.metric(
                "Total Spend (AED)",
                f"{total_spend:,.0f}"
            )

            col2.metric(
                "Total Revenue (AED)",
                f"{total_revenue:,.0f}"
            )

            col3.metric(
                "Contracts",
                f"{int(total_contracts)}"
            )

            col4.metric(
                "Overall ROAS",
                f"{overall_roas:.2f}x"
            )

            col5.metric(
                "Average CPL (AED)",
                f"{avg_cpl:,.0f}"
            )

            col6.metric(
                "Average CPA (AED)",
                f"{avg_cpa:,.0f}"
            )

            # =====================================================
            # EXECUTIVE PERFORMANCE ANALYTICS
            # =====================================================

            st.markdown("---")

            st.header("Executive Performance Analytics")

            # =====================================================
            # ROAS TARGET GAUGE
            # =====================================================

            st.subheader("🇷🇴🇦🇸 🇹🇦🇷🇬🇪🇹 🇦🇨🇭🇮🇪🇻🇪🇲🇪🇳🇹 🇧🇾 🇨🇭🇦🇳🇳🇪🇱")

            gauge_channels = (
                filtered_df.groupby("Channel")
                .agg({
                    "Revenue Amount": "sum",
                    "Amount Spent": "sum",
                    "Target ROAS": "mean"
                })
                .reset_index()
            )

            gauge_channels["ROAS AED"] = safe_divide(
                gauge_channels["Revenue Amount"],
                gauge_channels["Amount Spent"]
            )

            # 3 COLUMN LAYOUT
            cols = st.columns(3)

            for idx, (_, row) in enumerate(gauge_channels.iterrows()):

                max_scale = max(
                    row["Target ROAS"] * 2,
                    row["ROAS AED"] * 1.5,
                    5
                )

                fig_gauge = go.Figure(
                    go.Indicator(
                        mode="gauge+number",

                        value=row["ROAS AED"],

                        title={
                            "text":
                            f"<b>{row['Channel']}</b><br>Target: {row['Target ROAS']:.1f}"
                        },

                        gauge={
                            "axis": {
                                "range": [0, max_scale]
                            },

                            "threshold": {
                                "line": {
                                    "color": "red",
                                    "width": 4
                                },

                                "value": row["Target ROAS"]
                            }
                        }
                    )
                )

                fig_gauge.update_layout(
                    height=320,
                    margin=dict(
                        l=10,
                        r=10,
                        t=50,
                        b=10
                    )
                )

                with cols[idx % 3]:

                    st.plotly_chart(
                        fig_gauge,
                        use_container_width=True
                    )


            # ---------------- SHOW DATA ---------------- #

            st.subheader("Processed Marketing Data")

            st.dataframe(filtered_df)

            # ---------------- CHARTS SECTION ---------------- #

            st.subheader("Marketing Analytics Visuals")

            # =====================================================
            # CHART 1 — SPEND VS REVENUE
            # =====================================================

            spend_revenue = (
                filtered_df.groupby("Company")[[
                    "Amount Spent",
                    "Revenue Amount"
                ]]
                .sum()
                .reset_index()
            )

            fig1 = px.bar(
                spend_revenue,
                x="Company",
                y=["Amount Spent", "Revenue Amount"],
                barmode="group",
                title="Spend vs Revenue by Company"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            # =====================================================
            # CHART 2 — CHANNEL PERFORMANCE
            # =====================================================

            channel_roas = (
                filtered_df.groupby("Channel")["ROAS AED"]
                .mean()
                .reset_index()
            )

            fig2 = px.bar(
                channel_roas,
                x="Channel",
                y="ROAS AED",
                title="Average ROAS by Channel",
                text_auto=True
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            # =====================================================
            # CHART 3 — COMPANY PERFORMANCE
            # =====================================================

            company_revenue = (
                filtered_df.groupby("Company")["Revenue Amount"]
                .sum()
                .reset_index()
            )

            fig3 = px.pie(
                company_revenue,
                names="Company",
                values="Revenue Amount",
                title="Revenue Contribution by Company"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

            # =====================================================
            # CHART 4 — MONTHLY REVENUE TREND
            # =====================================================

            monthly_trend = (
                filtered_df.groupby("Month")["Revenue Amount"]
                .sum()
                .reset_index()
            )

            fig4 = px.line(
                monthly_trend,
                x="Month",
                y="Revenue Amount",
                markers=True,
                title="Monthly Revenue Trend"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

            # =====================================================
            # MONTH ORDER
            # =====================================================

            month_order = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ]

            # =====================================================
            # MOM ROAS TREND BY CHANNEL
            # =====================================================

            st.subheader("ROAS Trend by Channel")

            roas_trend = (
                filtered_df.groupby(
                    ["Month", "Channel"]
                )
                .agg({
                    "Revenue Amount":"sum",
                    "Amount Spent":"sum"
                })
                .reset_index()
            )

            roas_trend["ROAS AED"] = safe_divide(
                roas_trend["Revenue Amount"],
                roas_trend["Amount Spent"]
            )

            roas_trend["Month"] = pd.Categorical(
                roas_trend["Month"],
                categories=month_order,
                ordered=True
            )

            roas_trend = roas_trend.sort_values("Month")

            fig_roas_trend = px.line(
                roas_trend,
                x="Month",
                y="ROAS AED",
                color="Channel",
                markers=True,
                title="Month-over-Month ROAS by Channel"
            )

            st.plotly_chart(
                fig_roas_trend,
                use_container_width=True
            )

            # =====================================================
            # MOM SPEND TREND BY CHANNEL
            # =====================================================

            st.subheader("Spend Trend by Channel")

            spend_trend = (
                filtered_df.groupby(
                    ["Month", "Channel"]
                )["Amount Spent"]
                .sum()
                .reset_index()
            )

            spend_trend["Month"] = pd.Categorical(
                spend_trend["Month"],
                categories=month_order,
                ordered=True
            )

            spend_trend = spend_trend.sort_values("Month")

            fig_spend_trend = px.line(
                spend_trend,
                x="Month",
                y="Amount Spent",
                color="Channel",
                markers=True,
                title="Month-over-Month Spend by Channel"
            )

            st.plotly_chart(
                fig_spend_trend,
                use_container_width=True
            )


            # =====================================================
            # LEAD QUALITY ANALYSIS
            # =====================================================

            st.header("Lead Quality Analytics")

            # =====================================================
            # LEAD QUALITY VS CLOSE RATE
            # =====================================================

            lead_quality_chart = (
                filtered_df.groupby("Channel")
                .agg({
                    "Lead Quality %":"mean",
                    "Close Rate %":"mean",
                    "Revenue Amount":"sum"
                })
                .reset_index()
            )

            fig_lead_quality = px.scatter(
                lead_quality_chart,

                x="Lead Quality %",
                y="Close Rate %",

                size="Revenue Amount",

                color="Channel",

                text="Channel",

                title="Lead Quality vs Close Rate by Channel"
            )

            fig_lead_quality.update_traces(
                textposition="top center"
            )

            st.plotly_chart(
                fig_lead_quality,
                use_container_width=True
            )

            st.info("""
            Scatter Plot Interpretation:

            • Top Right = Excellent Channels

            • Bottom Right = Good Leads but Poor Sales Conversion

            • Top Left = Poor Lead Quality but Strong Sales Team

            • Bottom Left = Underperforming Channels
            """)

            # =====================================================
            # LEAD QUALITY RANKING
            # =====================================================

            lead_quality_rank = (
                filtered_df.groupby("Channel")
                ["Lead Quality %"]
                .mean()
                .reset_index()
            )

            lead_quality_rank = (
                lead_quality_rank
                .sort_values(
                    "Lead Quality %",
                    ascending=False
                )
            )

            fig_quality_rank = px.bar(
                lead_quality_rank,

                x="Channel",

                y="Lead Quality %",

                color="Lead Quality %",

                text_auto=".1f",

                title="Average Lead Quality by Channel"
            )

            st.plotly_chart(
                fig_quality_rank,
                use_container_width=True
            )

            # =====================================================
            # CLOSE RATE RANKING
            # =====================================================

            close_rate_rank = (
                filtered_df.groupby("Channel")
                ["Close Rate %"]
                .mean()
                .reset_index()
            )

            close_rate_rank = (
                close_rate_rank
                .sort_values(
                    "Close Rate %",
                    ascending=False
                )
            )

            fig_close_rank = px.bar(
                close_rate_rank,

                x="Channel",

                y="Close Rate %",

                color="Close Rate %",

                text_auto=".1f",

                title="Average Close Rate by Channel"
            )

            st.plotly_chart(
                fig_close_rank,
                use_container_width=True
            )

            # =====================================================
            # SPEND EFFICIENCY HEATMAPS
            # =====================================================

            st.header("Spend Efficiency Analytics")

            # =====================================================
            # ROAS HEATMAP
            # =====================================================

            st.subheader("ROAS Performance Heatmap")

            roas_heatmap = (
                filtered_df.groupby(
                    ["Month", "Channel"]
                )
                .agg({
                    "Revenue Amount":"sum",
                    "Amount Spent":"sum"
                })
                .reset_index()
            )

            roas_heatmap["ROAS AED"] = safe_divide(
                roas_heatmap["Revenue Amount"],
                roas_heatmap["Amount Spent"]
            )

            roas_pivot = roas_heatmap.pivot(
                index="Month",
                columns="Channel",
                values="ROAS AED"
            )

            roas_pivot = roas_pivot.reindex(
                month_order
            )

            fig_roas_heatmap = px.imshow(
                roas_pivot,

                text_auto=".1f",

                aspect="auto",

                title="ROAS by Month and Channel"
            )

            st.plotly_chart(
                fig_roas_heatmap,
                use_container_width=True
            )

            st.info("""
            ROAS Heatmap:
            Shows which channels generated the highest return on spend during each month.
            """)

            # =====================================================
            # CLOSE RATE HEATMAP
            # =====================================================

            st.subheader("Conversion Efficiency Heatmap")

            conversion_heatmap = (
                filtered_df.groupby(
                    ["Month", "Channel"]
                )
                .agg({
                    "Leads":"sum",
                    "Contracts":"sum"
                })
                .reset_index()
            )

            conversion_heatmap["Close Rate %"] = (
                conversion_heatmap["Contracts"]
                /
                conversion_heatmap["Leads"]
            ) * 100

            conversion_pivot = conversion_heatmap.pivot(
                index="Month",
                columns="Channel",
                values="Close Rate %"
            )

            conversion_pivot = conversion_pivot.reindex(
                month_order
            )

            fig_conversion_heatmap = px.imshow(
                conversion_pivot,

                text_auto=".1f",

                aspect="auto",

                title="Close Rate % by Month and Channel"
            )

            st.plotly_chart(
                fig_conversion_heatmap,
                use_container_width=True
            )

            st.info("""
            Conversion Heatmap:
            Shows which channels converted leads into contracts most effectively.
            """)

            # =====================================================
            # CHANNEL COMPARISON RADAR CHART
            # =====================================================

            st.header("Channel Comparison Dashboard")

            radar_df = (
                filtered_df.groupby("Channel")
                .agg({
                    "Amount Spent":"sum",
                    "Revenue Amount":"sum",
                    "Leads":"sum",
                    "Contracts":"sum"
                })
                .reset_index()
            )

            total_spend_all = radar_df["Amount Spent"].sum()
            total_revenue_all = radar_df["Revenue Amount"].sum()

            radar_df["ROAS"] = (
                radar_df["Revenue Amount"]
                /
                radar_df["Amount Spent"]
            )

            radar_df["Spend %"] = (
                radar_df["Amount Spent"]
                /
                total_spend_all
            ) * 100

            radar_df["Revenue %"] = (
                radar_df["Revenue Amount"]
                /
                total_revenue_all
            ) * 100

            radar_df["Close Rate %"] = (
                radar_df["Contracts"]
                /
                radar_df["Leads"]
            ) * 100

            lead_quality_lookup = (
                filtered_df.groupby("Channel")
                ["Lead Quality %"]
                .mean()
                .reset_index()
            )

            radar_df = radar_df.merge(
                lead_quality_lookup,
                on="Channel",
                how="left"
            )

            max_roas = radar_df["ROAS"].max()

            if max_roas > 0:
                radar_df["ROAS Normalized"] = (
                    radar_df["ROAS"]
                    /
                    max_roas
                ) * 100
            else:
                radar_df["ROAS Normalized"] = 0

            selected_radar_channels = st.multiselect(
                "Select Channels for Radar Comparison",
                options=radar_df["Channel"].unique(),
                default=list(radar_df["Channel"].unique())[:5]
            )

            radar_filtered = radar_df[
                radar_df["Channel"].isin(
                    selected_radar_channels
                )
            ]

            fig_radar = go.Figure()

            for _, row in radar_filtered.iterrows():

                fig_radar.add_trace(
                    go.Scatterpolar(
                        r=[
                            row["ROAS Normalized"],
                            row["Spend %"],
                            row["Revenue %"],
                            row["Lead Quality %"],
                            row["Close Rate %"]
                        ],

                        theta=[
                            "ROAS",
                            "Spend %",
                            "Revenue %",
                            "Lead Quality %",
                            "Close Rate %"
                        ],

                        fill="toself",

                        name=row["Channel"]
                    )
                )

            fig_radar.update_layout(

                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0,100]
                    )
                ),

                title="Multi-Metric Channel Comparison",

                showlegend=True,

                height=700
            )

            st.plotly_chart(
                fig_radar,
                use_container_width=True
            )

            st.info("""
            Larger coverage indicates stronger overall performance.
            """)

            # ---------------- ADVANCED BUSINESS INSIGHTS ---------------- #

            st.subheader("Business Insights & Performance Analysis")

            # =====================================================
            # BEST & WORST CHANNEL
            # =====================================================

            channel_analysis = (
                filtered_df.groupby("Channel")
                .agg({
                    "Revenue Amount": "sum",
                    "Amount Spent": "sum",
                    "ROAS AED": "mean",
                    "Conversion Rate %": "mean",
                    "Lead Quality %": "mean",
                    "Close Rate %": "mean"
                })
                .reset_index()
            )

            # % OF TOTAL SPEND
            channel_analysis["Spend %"] = (
                safe_divide(
                    channel_analysis["Amount Spent"],
                    channel_analysis["Amount Spent"].sum()
                ) * 100
            )

            # % OF TOTAL REVENUE
            channel_analysis["Revenue %"] = (
                safe_divide(
                    channel_analysis["Revenue Amount"],
                    channel_analysis["Revenue Amount"].sum()
                ) * 100
            )

            # ROAS RANKING
            channel_analysis["ROAS Rank"] = (
                channel_analysis["ROAS AED"]
                .rank(
                    ascending=False,
                    method="dense"
                )
                .astype(int)
            )

            # BUDGET CHANGE %

            def budget_change(roas):

                if roas >= 5:
                    return "+30%"

                elif roas >= 3:
                    return "+15%"

                elif roas >= 2:
                    return "Hold"

                elif roas >= 1:
                    return "-15%"

                else:
                    return "-40% / Pause"

            channel_analysis["Budget Change"] = (
                channel_analysis["ROAS AED"]
                .apply(budget_change)
            )

            # RECOMMENDATIONS

            def recommendation(roas):

                if roas >= 5:
                    return "Scale aggressively. Excellent profitability."

                elif roas >= 3:
                    return "Increase budget gradually."

                elif roas >= 2:
                    return "Stable performance. Maintain budget."

                elif roas >= 1:
                    return "Needs optimization before scaling."

                else:
                    return "Poor profitability. Reduce spend or pause."

            channel_analysis["Recommendation"] = (
                channel_analysis["ROAS AED"]
                .apply(recommendation)
            )

            # ---------------- ADVANCED ANALYSIS TABLE ---------------- #

            st.subheader("🇦🇩🇻🇦🇳🇨🇪🇩 🇨🇭🇦🇳🇳🇪🇱 🇵🇪🇷🇫🇴🇷🇲🇦🇳🇨🇪 🇦🇳🇦🇱🇾🇸🇮🇸")

            st.dataframe(

                channel_analysis[
                    [
                        "Channel",
                        "ROAS AED",
                        "ROAS Rank",
                        "Spend %",
                        "Revenue %",
                        "Lead Quality %",
                        "Close Rate %",
                        "Budget Change",
                        "Recommendation"
                    ]
                ]

            )

            # BEST CHANNEL
            best_channel_row = channel_analysis.loc[
                channel_analysis["ROAS AED"].idxmax()
            ]

            # WORST CHANNEL
            worst_channel_row = channel_analysis.loc[
                channel_analysis["ROAS AED"].idxmin()
            ]

            # =====================================================
            # BEST COMPANY
            # =====================================================

            company_analysis = (
                filtered_df.groupby("Company")
                .agg({
                    "Revenue Amount": "sum",
                    "Amount Spent": "sum",
                    "ROAS AED": "mean",
                    "Conversion Rate %": "mean"
                })
                .reset_index()
            )

            best_company_row = company_analysis.loc[
                company_analysis["ROAS AED"].idxmax()
            ]

            # =====================================================
            # DISPLAY INSIGHTS
            # =====================================================

            insight_col1, insight_col2 = st.columns(2)

            with insight_col1:

                st.success(
                    f"""
                    BEST CHANNEL: {best_channel_row['Channel']}

                    • Average ROAS: {best_channel_row['ROAS AED']:.2f}x

                    • Revenue Generated: AED {best_channel_row['Revenue Amount']:,.0f}

                    • Conversion Rate: {best_channel_row['Conversion Rate %']:.2f}%
                    """
                )

                st.info(
                    f"""
                    BEST COMPANY (with highest ROAS): {best_company_row['Company']}

                    • Average ROAS: {best_company_row['ROAS AED']:.2f}x

                    • Revenue Generated: AED {best_company_row['Revenue Amount']:,.0f}

                    • Conversion Rate: {best_company_row['Conversion Rate %']:.2f}%
                    """
                )

            with insight_col2:

                st.warning(
                    f"""
                    WORST CHANNEL: {worst_channel_row['Channel']}

                    • Average ROAS: {worst_channel_row['ROAS AED']:.2f}x

                    • Revenue Generated: AED {worst_channel_row['Revenue Amount']:,.0f}

                    • Conversion Rate: {worst_channel_row['Conversion Rate %']:.2f}%
                    """
                )

            # =====================================================
            # OVERALL PROFITABILITY STATUS
            # =====================================================

            avg_diff_roas = filtered_df["DIFF ROAS"].mean()

            if avg_diff_roas > 0:

                st.success(
                    f"""
                    OVERALL PERFORMANCE STATUS

                    Campaigns are performing ABOVE target ROAS.

                    Average DIFF ROAS: {avg_diff_roas:.2f}
                    """
                )

            else:

                st.error(
                    f"""
                    OVERALL PERFORMANCE STATUS

                    Campaigns are performing BELOW target ROAS.

                    Average DIFF ROAS: {avg_diff_roas:.2f}
                    """
                )

            # ---------------- FUNNEL ANALYTICS ---------------- #

            st.subheader("Marketing Funnel Analysis")

            # TOTALS
            total_prospects = filtered_df["Prospects"].sum()

            total_leads = filtered_df["Leads"].sum()

            total_contracts = filtered_df["Contracts"].sum()

            # FUNNEL DATA
            funnel_values = [
                total_prospects,
                total_leads,
                total_contracts
            ]

            funnel_labels = [
                "Prospects",
                "Leads",
                "Contracts"
            ]

            # CREATE FUNNEL CHART
            fig_funnel = go.Figure(go.Funnel(
                y=funnel_labels,
                x=funnel_values,
                textinfo="value+percent initial"
            ))

            fig_funnel.update_layout(
                title="Marketing Conversion Funnel"
            )

            st.plotly_chart(
                fig_funnel,
                use_container_width=True
            )

            # ---------------- FUNNEL INSIGHTS ---------------- #

            lead_conversion = (
                (total_leads / total_prospects) * 100
                if total_prospects > 0 else 0
            )

            contract_conversion = (
                (total_contracts / total_leads) * 100
                if total_leads > 0 else 0
            )

            overall_conversion = (
                (total_contracts / total_prospects) * 100
                if total_prospects > 0 else 0
            )

            st.info(
                f"""
                FUNNEL PERFORMANCE SUMMARY

                • Prospect to Lead Conversion: {lead_conversion:.2f}%

                • Lead to Contract Conversion: {contract_conversion:.2f}%

                • Overall Funnel Conversion: {overall_conversion:.2f}%
                """
            )

            # =====================================================
            # CHANNEL CONVERSION JOURNEY
            # =====================================================

            st.subheader("Prospect-to-Contract Journey by Channel")

            channel_funnel = (
                filtered_df.groupby("Channel")
                .agg({
                    "Prospects":"sum",
                    "Leads":"sum",
                    "Contracts":"sum"
                })
                .reset_index()
            )

            channel_funnel_melted = channel_funnel.melt(
                id_vars="Channel",

                value_vars=[
                    "Prospects",
                    "Leads",
                    "Contracts"
                ],

                var_name="Stage",

                value_name="Count"
            )

            fig_channel_funnel = px.bar(
                channel_funnel_melted,

                x="Channel",

                y="Count",

                color="Stage",

                barmode="group",

                title="Prospects → Leads → Contracts by Channel"
            )

            st.plotly_chart(
                fig_channel_funnel,
                use_container_width=True
            )

            st.subheader("Channel Leakage Analysis")
            leakage_df = channel_funnel.copy()

            leakage_df["Prospect-to-Lead Loss %"] = (
                (
                    leakage_df["Prospects"]
                    -
                    leakage_df["Leads"]
                )
                /
                leakage_df["Prospects"]
            ) * 100

            leakage_df["Lead-to-Contract Loss %"] = (
                (
                    leakage_df["Leads"]
                    -
                    leakage_df["Contracts"]
                )
                /
                leakage_df["Leads"]
            ) * 100

            leakage_melted = leakage_df.melt(
                id_vars="Channel",

                value_vars=[
                    "Prospect-to-Lead Loss %",
                    "Lead-to-Contract Loss %"
                ],

                var_name="Loss Stage",

                value_name="Loss %"
            )

            fig_leakage = px.bar(
                leakage_melted,

                x="Channel",

                y="Loss %",

                color="Loss Stage",

                barmode="group",

                title="Conversion Leakage by Channel"
            )

            st.plotly_chart(
                fig_leakage,
                use_container_width=True
            )

            conversion_summary = channel_funnel.copy()

            conversion_summary["Overall Conversion %"] = (
                conversion_summary["Contracts"]
                /
                conversion_summary["Prospects"]
            ) * 100

            best_conversion = (
                conversion_summary.loc[
                    conversion_summary[
                        "Overall Conversion %"
                    ].idxmax(),
                    "Channel"
                ]
            )

            worst_conversion = (
                conversion_summary.loc[
                    conversion_summary[
                        "Overall Conversion %"
                    ].idxmin(),
                    "Channel"
                ]
            )
            col_a, col_b = st.columns(2)

            with col_a:

                st.success(
                    f"🏆 Best Conversion Channel: {best_conversion}"
                )

            with col_b:

                st.error(
                    f"⚠️ Lowest Conversion Channel: {worst_conversion}"
                )
            st.info("""
            Channel Funnel Interpretation

            • High Prospect-to-Lead Loss = Poor lead generation quality.

            • High Lead-to-Contract Loss = Sales conversion issue.

            • Low loss percentages indicate an efficient channel.

            • Compare channels to identify where prospects are dropping out of the journey.
            """)


            # ---------------- SMART RECOMMENDATIONS ---------------- #

            st.subheader("AI-Based Marketing Recommendations")

            recommendations = []

            # =====================================================
            # BEST CHANNEL RECOMMENDATION
            # =====================================================

            best_roas_channel = channel_analysis.loc[
                channel_analysis["ROAS AED"].idxmax()
            ]

            recommendations.append(
                f"""
                Increase investment in {best_roas_channel['Channel']}
                campaigns because it has the highest ROAS
                of {best_roas_channel['ROAS AED']:.2f}x.
                """
            )

            # =====================================================
            # WORST CHANNEL RECOMMENDATION
            # =====================================================

            worst_roas_channel = channel_analysis.loc[
                channel_analysis["ROAS AED"].idxmin()
            ]

            recommendations.append(
                f"""
                Optimize or reduce spending on
                {worst_roas_channel['Channel']}
                campaigns due to lower ROAS performance.
                """
            )

            # =====================================================
            # LOW CONVERSION ALERT
            # =====================================================

            avg_conversion = filtered_df["Conversion Rate %"].mean()

            if avg_conversion < 10:

                recommendations.append(
                    """
                    Overall conversion rate is below 10%.
                    Review lead quality and sales conversion process.
                    """
                )

            # =====================================================
            # HIGH CPL ALERT
            # =====================================================

            avg_cpl = filtered_df["CPL"].mean()

            if avg_cpl > 1000:

                recommendations.append(
                    f"""
                    Average CPL is high at AED {avg_cpl:,.0f}.
                    Consider improving targeting strategy.
                    """
                )

            # =====================================================
            # DISPLAY RECOMMENDATIONS
            # =====================================================

            for rec in recommendations:
                st.info(rec)

        # =====================================================
        # BUDGET & ANALYTICS ANALYTICS TAB
        # =====================================================
        with budget_tab:
            st.header("Budget Allocation & Planning")

            # =====================================================
            # BUDGET KPIs
            # =====================================================

            total_budget = filtered_df["Budget Allocation"].sum()

            actual_spend = filtered_df["Amount Spent"].sum()

            budget_variance = (
                (
                    actual_spend - total_budget
                )
                /
                total_budget
            ) * 100 if total_budget > 0 else 0

            budget_utilization = (
                actual_spend
                /
                total_budget
            ) * 100 if total_budget > 0 else 0

            b1, b2, b3, b4 = st.columns(4)

            with b1:
                st.metric(
                    "Budget Allocated",
                    f"AED {total_budget:,.0f}"
                )

            with b2:
                st.metric(
                    "Actual Spend",
                    f"AED {actual_spend:,.0f}"
                )

            with b3:
                st.metric(
                    "Budget Variance %",
                    f"{budget_variance:.1f}%"
                )

            with b4:
                st.metric(
                    "Budget Utilization %",
                    f"{budget_utilization:.1f}%"
                )

            st.subheader("Budget vs Actual Spend by Channel")

            budget_channel = (
                filtered_df.groupby("Channel")
                .agg({
                    "Budget Allocation":"sum",
                    "Amount Spent":"sum"
                })
                .reset_index()
            )

            budget_melt = budget_channel.melt(
                id_vars="Channel",
                value_vars=[
                    "Budget Allocation",
                    "Amount Spent"
                ],
                var_name="Metric",
                value_name="Amount"
            )

            fig_budget_actual = px.bar(
                budget_melt,
                x="Channel",
                y="Amount",
                color="Metric",
                barmode="group",
                title="Budget vs Actual Spend"
            )

            st.plotly_chart(
                fig_budget_actual,
                use_container_width=True
            )

            st.subheader("Budget Variance by Channel")

            variance_df = budget_channel.copy()

            variance_df["Variance %"] = (
                (
                    variance_df["Amount Spent"]
                    -
                    variance_df["Budget Allocation"]
                )
                /
                variance_df["Budget Allocation"]
            ) * 100

            fig_variance = px.bar(
                variance_df,
                x="Channel",
                y="Variance %",
                color="Variance %",
                title="Budget Variance (%)"
            )

            st.plotly_chart(
                fig_variance,
                use_container_width=True
            )

            st.subheader("Budget Utilization by Channel")

            utilization_df = budget_channel.copy()

            utilization_df["Utilization %"] = (
                utilization_df["Amount Spent"]
                /
                utilization_df["Budget Allocation"]
            ) * 100

            fig_utilization = px.bar(
                utilization_df,
                x="Channel",
                y="Utilization %",
                color="Utilization %",
                title="Budget Utilization (%)"
            )

            st.plotly_chart(
                fig_utilization,
                use_container_width=True
            )

            st.subheader("Monthly Budget Tracking")
            budget_monthly = (
                filtered_df.groupby(
                    ["Year","Month"]
                )
                .agg({
                    "Budget Allocation":"sum",
                    "Amount Spent":"sum"
                })
                .reset_index()
            )

            budget_monthly["Period"] = (
                budget_monthly["Month"]
                +
                " "
                +
                budget_monthly["Year"].astype(str)
            )

            budget_monthly_melt = budget_monthly.melt(
                id_vars="Period",
                value_vars=[
                    "Budget Allocation",
                    "Amount Spent"
                ],
                var_name="Metric",
                value_name="Amount"
            )

            fig_monthly_budget = px.line(
                budget_monthly_melt,
                x="Period",
                y="Amount",
                color="Metric",
                markers=True,
                title="Monthly Budget Tracking"
            )

            st.plotly_chart(
                fig_monthly_budget,
                use_container_width=True
            )

            st.subheader("Budget Recommendations")

            recommendation_df = (
                filtered_df.groupby("Channel")
                .agg({
                    "Revenue Amount":"sum",
                    "Amount Spent":"sum",
                    "Target ROAS":"mean"
                })
                .reset_index()
            )

            recommendation_df["ROAS"] = (
                recommendation_df["Revenue Amount"]
                /
                recommendation_df["Amount Spent"]
            )

            def recommend_budget(row):

                if row["ROAS"] >= row["Target ROAS"] * 1.2:
                    return "Increase Budget"

                elif row["ROAS"] >= row["Target ROAS"]:
                    return "Maintain Budget"

                else:
                    return "Reduce Budget"

            recommendation_df["Recommendation"] = (
                recommendation_df.apply(
                    recommend_budget,
                    axis=1
                )
            )

            st.dataframe(
                recommendation_df[
                    [
                        "Channel",
                        "ROAS",
                        "Target ROAS",
                        "Recommendation"
                    ]
                ],
                use_container_width=True
            )

        # =====================================================
        # FORECAST & PROJECTION ANALYTICS TAB
        # =====================================================

        with forecast_tab:
            st.header("Revenue Forecast & Projections")

            forecast_df = (
                df.groupby(
                    ["Year", "Month"]
                )["Revenue Amount"]
                .sum()
                .reset_index()
            )

            month_map = {
                "January":1,
                "February":2,
                "March":3,
                "April":4,
                "May":5,
                "June":6,
                "July":7,
                "August":8,
                "September":9,
                "October":10,
                "November":11,
                "December":12
            }
            forecast_df["Month_Number"] = (
                forecast_df["Month"]
                .map(month_map)
            )

            forecast_df = (
                forecast_df
                .sort_values(
                    ["Year","Month_Number"]
                )
                .reset_index(drop=True)
            )

            latest_year = int(forecast_df.iloc[-1]["Year"])
            latest_month_num = int(forecast_df.iloc[-1]["Month_Number"])

            forecast_df["Time_Index"] = (
                range(len(forecast_df))
            )

            X = forecast_df[["Time_Index"]]

            y = forecast_df["Revenue Amount"]

            model = LinearRegression()

            model.fit(X, y)

            forecast_months = st.slider(
                "Forecast Horizon (Months)",
                min_value=1,
                max_value=24,
                value=6
            )

            future_periods = forecast_months

            future_index = np.arange(
                len(forecast_df),
                len(forecast_df) + future_periods
            ).reshape(-1,1)

            future_predictions = model.predict(
                future_index
            )

            future_months = []

            current_year = latest_year
            current_month = latest_month_num

            for _ in range(future_periods):

                current_month += 1

                if current_month > 12:
                    current_month = 1
                    current_year += 1

                future_months.append(
                    datetime(
                        current_year,
                        current_month,
                        1
                    ).strftime("%B %Y")
                )
            st.write("Months:", len(future_months))
            st.write("Predictions:", len(future_predictions))

            forecast_table = pd.DataFrame({
                "Forecast Period": future_months,
                "Projected Revenue": future_predictions
            })

            st.subheader("Forecast Summary")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Next Month Revenue",
                    f"AED {future_predictions[0]:,.0f}"
                )

            with c2:
                st.metric(
                    "Future Month Projection",
                    f"AED {future_predictions.sum():,.0f}"
                )

            growth_rate = (
                (
                    future_predictions[0]
                    -
                    forecast_df["Revenue Amount"].iloc[-1]
                )
                /
                forecast_df["Revenue Amount"].iloc[-1]
            ) * 100

            with c3:
                st.metric(
                    "Expected Growth %",
                    f"{growth_rate:.1f}%"
                )

            # =====================================================
            # FORECAST CHART
            # =====================================================

            historical_chart = forecast_df.copy()

            historical_chart["Type"] = "Historical"

            future_chart = pd.DataFrame({
                "Time_Index": future_index.flatten(),
                "Revenue Amount": future_predictions,
                "Type": "Forecast"
            })

            combined_chart = pd.concat([
                historical_chart[
                    [
                        "Time_Index",
                        "Revenue Amount",
                        "Type"
                    ]
                ],
                future_chart
            ])

            fig_forecast = px.line(
                combined_chart,
                x="Time_Index",
                y="Revenue Amount",
                color="Type",
                markers=True,
                title="Historical Revenue vs Forecast Revenue"
            )

            st.plotly_chart(
                fig_forecast,
                use_container_width=True
            )

            # =====================================================
            # FORECAST TABLE
            # =====================================================

            st.subheader("Projected Revenue Forecast")

            st.dataframe(
                forecast_table,
                use_container_width=True
            )

            # =====================================================
            # FORECAST INSIGHT
            # =====================================================

            if growth_rate > 0:

                st.success(
                    f"Forecast indicates approximately "
                    f"{growth_rate:.1f}% growth "
                    f"next period."
                )

            else:

                st.warning(
                    f"Forecast indicates approximately "
                    f"{abs(growth_rate):.1f}% decline "
                    f"next period."
                )         
        # =====================================================
        # YTD ANALYTICS TAB
        # =====================================================

        with ytd_tab:

            st.header("YTD Marketing Analytics")

            # ---------------- YTD OVERVIEW ---------------- #

            total_ytd_spend = ytd_df["Amount Spent"].sum()

            total_ytd_revenue = ytd_df["Revenue Amount"].sum()

            total_ytd_contracts = ytd_df["Contracts"].sum()

            overall_ytd_roas = (
                total_ytd_revenue / total_ytd_spend
            )

            # ---------------- KPI DISPLAY ---------------- #

            st.subheader("YTD Dashboard Overview")

            ytd_col1, ytd_col2, ytd_col3, ytd_col4 = st.columns(4)

            ytd_col1.metric(
                "YTD Spend (AED)",
                f"{total_ytd_spend:,.0f}"
            )

            ytd_col2.metric(
                "YTD Revenue (AED)",
                f"{total_ytd_revenue:,.0f}"
            )

            ytd_col3.metric(
                "YTD Contracts",
                f"{int(total_ytd_contracts)}"
            )

            ytd_col4.metric(
                "YTD ROAS",
                f"{overall_ytd_roas:.2f}x"
            )

            # ---------------- YTD CHARTS ---------------- #

            st.subheader("YTD Visual Analytics")

            # =====================================================
            # YTD COMPANY REVENUE
            # =====================================================

            ytd_company_chart = (
                ytd_df.groupby("Company")["Revenue Amount"]
                .sum()
                .reset_index()
            )

            fig_ytd_company = px.bar(
                ytd_company_chart,
                x="Company",
                y="Revenue Amount",
                color="Company",
                title="YTD Revenue by Company"
            )

            st.plotly_chart(
                fig_ytd_company,
                use_container_width=True
            )

            # =====================================================
            # YTD CHANNEL ROAS
            # =====================================================

            ytd_channel_chart = (
                ytd_df.groupby("Channel")["ROAS AED"]
                .mean()
                .reset_index()
            )

            fig_ytd_channel = px.bar(
                ytd_channel_chart,
                x="Channel",
                y="ROAS AED",
                color="Channel",
                title="YTD ROAS by Channel",
                text_auto=True
            )

            st.plotly_chart(
                fig_ytd_channel,
                use_container_width=True
            )

            # =====================================================
            # YTD COMPANY CONTRIBUTION
            # =====================================================

            ytd_company_pie = (
                ytd_df.groupby("Company")["Revenue Amount"]
                .sum()
                .reset_index()
            )

            fig_ytd_pie = px.pie(
                ytd_company_pie,
                names="Company",
                values="Revenue Amount",
                title="YTD Revenue Contribution"
            )

            st.plotly_chart(
                fig_ytd_pie,
                use_container_width=True
            )

            # =====================================================
            # YTD ADVANCED CHANNEL ANALYSIS
            # =====================================================

            ytd_channel_analysis = (

                ytd_df.groupby("Channel")
                .agg({
                    "Revenue Amount": "sum",
                    "Amount Spent": "sum",
                    "ROAS AED": "mean",
                    "Lead Quality %": "mean",
                    "Close Rate %": "mean"
                })

                .reset_index()
            )

            # ---------------- SPEND % ---------------- #

            ytd_channel_analysis["Spend %"] = (

                safe_divide(
                    ytd_channel_analysis["Amount Spent"],
                    ytd_channel_analysis["Amount Spent"].sum()
                ) * 100
            )

            # ---------------- REVENUE % ---------------- #

            ytd_channel_analysis["Revenue %"] = (

                safe_divide(
                    ytd_channel_analysis["Revenue Amount"],
                    ytd_channel_analysis["Revenue Amount"].sum()
                ) * 100
            )

            # ---------------- ROAS RANK ---------------- #

            ytd_channel_analysis["ROAS Rank"] = (

                ytd_channel_analysis["ROAS AED"]
                .rank(
                    ascending=False,
                    method="dense"
                )
                .astype(int)
            )

            # ---------------- BUDGET CHANGE ---------------- #

            ytd_channel_analysis["Budget Change"] = (

                ytd_channel_analysis["ROAS AED"]
                .apply(budget_change)
            )

            # ---------------- RECOMMENDATION ---------------- #

            ytd_channel_analysis["Recommendation"] = (

                ytd_channel_analysis["ROAS AED"]
                .apply(recommendation)
            )

            # ---------------- YTD ADVANCED TABLE ---------------- #

            st.subheader("YTD Advanced Channel Analysis")

            st.dataframe(

                ytd_channel_analysis[
                    [
                        "Channel",
                        "ROAS AED",
                        "ROAS Rank",
                        "Spend %",
                        "Revenue %",
                        "Lead Quality %",
                        "Close Rate %",
                        "Budget Change",
                        "Recommendation"
                    ]
                ]

            )

            # ---------------- YTD INSIGHTS ---------------- #

            st.subheader("YTD Business Insights")

            best_ytd_company = (
                ytd_df.groupby("Company")["ROAS AED"]
                .mean()
                .idxmax()
            )

            best_ytd_channel = (
                ytd_df.groupby("Channel")["ROAS AED"]
                .mean()
                .idxmax()
            )

            worst_ytd_channel = (
                ytd_df.groupby("Channel")["ROAS AED"]
                .mean()
                .idxmin()
            )

            st.success(
                f"""
                BEST YTD COMPANY (Highest ROAS): {best_ytd_company}
                """
            )

            st.info(
                f"""
                BEST YTD CHANNEL: {best_ytd_channel}
                """
            )

            st.warning(
                f"""
                WORST YTD CHANNEL: {worst_ytd_channel}
                """
            )

            # ---------------- YTD RECOMMENDATIONS ---------------- #

            st.subheader("YTD Strategic Recommendations")

            ytd_recommendations = []

            ytd_recommendations.append(
                f"""
                Increase budget allocation toward
                {best_ytd_channel} campaigns due to
                strongest YTD ROAS performance.
                """
            )

            ytd_recommendations.append(
                f"""
                Review optimization strategy for
                {worst_ytd_channel} campaigns to
                improve efficiency.
                """
            )

            for rec in ytd_recommendations:
                st.info(rec)

            # ---------------- YTD DATAFRAME ---------------- #

            st.subheader("Processed YTD Data")

            st.dataframe(ytd_df)

    # ---------------- WATERMARK ---------------- #

        st.markdown(
            """
            <hr>
            <div style='text-align: center; color: gray; font-size: 14px;'>
                Developed by Johnson Joy | © 2026 Marketing Analytics Dashboard | TheBuziHub
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        st.error(f"Error: {e}")
