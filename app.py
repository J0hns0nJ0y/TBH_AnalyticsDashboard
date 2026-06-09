import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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
            (df["Month"].isin(selected_months)) &
            (df["Company"].isin(selected_companies)) &
            (df["Channel"].isin(selected_channels))
        ]

        # ---------------- SUCCESS MESSAGE ---------------- #

        st.success("Data Processed Successfully!")

        # ---------------- TABS ---------------- #

        monthly_tab, ytd_tab = st.tabs([
            "Monthly Analytics",
            "YTD Analytics"
        ])

        with monthly_tab:
            # ---------------- KPI CALCULATIONS ---------------- #

            total_spend = filtered_df["Amount Spent"].sum()

            total_revenue = filtered_df["Revenue Amount"].sum()

            total_contracts = filtered_df["Contracts"].sum()

            overall_roas = (
                total_revenue / total_spend
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
                "Best Channel",
                best_channel
            )

            col6.metric(
                "Best Company (by Revenue)",
                best_company
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

            st.subheader("Advanced Channel Performance Analysis")

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