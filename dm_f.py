import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
data = pd.read_csv('anew_2 (3).csv')
rd_1 = pd.read_csv("final_lead_data_with_ratios.csv")
rd_1.columns = rd_1.columns.str.strip()  # Clean column names

# Prepare funnel data
total_leads_count = data['Phone Number'].nunique()
valid_sales_calls = data[data['ConversationDuration'] > 0]
unique_phone_calls = valid_sales_calls.drop_duplicates(subset='Phone Number')
total_unique_sales_calls = len(unique_phone_calls)
phone_counts = valid_sales_calls['Phone Number'].value_counts()
repeat_follow_ups = phone_counts[phone_counts > 1]
total_follow_ups = repeat_follow_ups.count()
conversions = data[data['Delivered'] == 'Y']
total_conversions = conversions['Phone Number'].nunique()

funnel_labels = ["Leads", "Sales Call", "Follow Up", "Conversion", "Sale"]
funnel_vals = [total_leads_count, total_unique_sales_calls, total_follow_ups, total_conversions, total_conversions]
funnel_data = pd.DataFrame({"Stage": funnel_labels, "Count": funnel_vals})
funnel_fig = px.funnel(funnel_data, x='Count', y='Stage', title='Sales Funnel')

# Revenue Over Time
rd_1_filtered = rd_1[rd_1['Lead Month'] != 'Total']
revenue_fig = px.line(rd_1_filtered, x='Lead Month', y='Revenue_generated/Month', title='Revenue Over Time', markers=True)

# Lead Counts Over Time
lead_counts_fig = px.bar(rd_1_filtered, x='Lead Month', y='Lead_Count/Month', title='Lead Counts Over Time', text='Lead_Count/Month')

# Grouped Bar Chart
grouped_bar_fig = px.bar(rd_1, x='Lead Month', y=['Lead_Count/Month', 'Phone_Call_Count/Month', 'Validated_Lead_Count/Month', 'Count _of_Orders _Deliverd /Month'], title='Lead Counts / Phone Calls / Validated Leads / Count of Orders Delivered', barmode='group')

# Dual Axis Bar Chart
dual_axis_fig = go.Figure()
dual_axis_fig.add_trace(go.Bar(x=rd_1['Lead Month'], y=rd_1['Total_Cost(DM+Phone_Calls)'], name='Total Cost', marker_color='blue'))
dual_axis_fig.add_trace(go.Bar(x=rd_1['Lead Month'], y=rd_1['Revenue_generated/Month'], name='Revenue', marker_color='orange'))
dual_axis_fig.update_layout(title='Cost and Revenue by Month', barmode='group', yaxis_title='Total Cost', yaxis2=dict(title='Revenue', overlaying='y', side='right'))

# Pie Chart for Orders Delivered
pie_fig = px.pie(rd_1_filtered, names='Lead Month', values='Count _of_Orders _Deliverd /Month', title='Proportion of Orders Delivered by Month')

# Ratios Over Time
ratios = ['Cost per lead Ratio', 'Cost /confirmed_order_Month_Wise_Ratio', 'Leads to Calls Connected Ratio', 'Leads to validated Lead Ratio', 'Leads to Order Ratio', 'Roas']
ratios_figs = [px.line(rd_1_filtered, x='Lead Month', y=ratio, title=f'{ratio} Over Months', markers=True) for ratio in ratios]

# Stacked Bar Chart for Leads and Orders
stacked_fig = go.Figure()
stacked_fig.add_trace(go.Bar(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Lead_Count/Month'], name='Lead Count', marker_color='blue', text=rd_1_filtered['Lead_Count/Month'], textposition='auto'))
stacked_fig.add_trace(go.Bar(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Phone_Call_Count/Month'], name='Phone Call Count', marker_color='orange', text=rd_1_filtered['Phone_Call_Count/Month'], textposition='auto'))
stacked_fig.add_trace(go.Bar(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Validated_Lead_Count/Month'], name='Validated Lead Count', marker_color='green', text=rd_1_filtered['Validated_Lead_Count/Month'], textposition='auto'))
stacked_fig.add_trace(go.Bar(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Count _of_Orders _Deliverd /Month'], name='Orders Delivered', marker_color='purple', text=rd_1_filtered['Count _of_Orders _Deliverd /Month'], textposition='auto'))

# Trendlines for the stacked bar chart
stacked_fig.add_trace(go.Scatter(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Lead_Count/Month'].cumsum(), mode='lines+markers', name='Lead Count Trend', line=dict(color='blue', width=2, dash='dash')))
stacked_fig.add_trace(go.Scatter(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Phone_Call_Count/Month'].cumsum(), mode='lines+markers', name='Phone Call Count Trend', line=dict(color='orange', width=2, dash='dash')))
stacked_fig.add_trace(go.Scatter(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Validated_Lead_Count/Month'].cumsum(), mode='lines+markers', name='Validated Lead Count Trend', line=dict(color='green', width=2, dash='dash')))
stacked_fig.add_trace(go.Scatter(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Count _of_Orders _Deliverd /Month'].cumsum(), mode='lines+markers', name='Orders Delivered Trend', line=dict(color='purple', width=2, dash='dash')))

stacked_fig.update_layout(title='Monthly Metrics Overview: Leads and Orders', barmode='stack', xaxis_title='Lead Month', yaxis_title='Count', legend_title='Metrics')

# Revenue vs Total Cost
revenue_cost_fig = go.Figure()
revenue_cost_fig.add_trace(go.Bar(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Revenue_generated/Month'], name='Revenue Generated', marker_color='lightblue'))
revenue_cost_fig.add_trace(go.Bar(x=rd_1_filtered['Lead Month'], y=rd_1_filtered['Total_Cost(DM+Phone_Calls)'], name='Total Cost', marker_color='lightcoral'))
revenue_cost_fig.update_layout(title='Revenue Generated vs. Total Cost', barmode='group', xaxis_title='Lead Month', yaxis_title='Amount', legend_title='Metrics')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Digital Marketing Dashboard From April to September 2024", style={'textAlign': 'center'}),
    
    # Sales Funnel
    dcc.Graph(figure=funnel_fig, id='funnel-graph'),
    html.Div("**1. Sales Funnel:** This funnel chart illustrates the sales process from leads to conversions."),
    html.P("Funnel: Leads -> Calls -> Follow-ups -> Conversions."),
    html.Hr(),  # Horizontal line

    # Revenue Over Time
    dcc.Graph(figure=revenue_fig, id='revenue-graph'),
    html.Div("**2. Revenue Over Time:** This plot shows the total revenue generated each month."),
    html.Hr(),  # Horizontal line

    # Lead Counts Over Time
    dcc.Graph(figure=lead_counts_fig, id='lead-counts-graph'),
    html.Div("**3. Lead Counts Over Time:** This bar chart represents the number of leads generated each month."),
    html.Hr(),  # Horizontal line

    # Cost and Revenue by Month
    dcc.Graph(figure=grouped_bar_fig, id='grouped-bar-graph'),
    html.Div("**4. Cost and Revenue by Month:** This chart compares total costs with revenue for each month."),
    html.Div("**Note:** Validated lead data is not available for April month."),
    html.Div("Validated data means when our telecaller team calls a lead and the lead expresses interest or requests more information."),
    html.Hr(),  # Horizontal line

    # Dual Axis Bar Chart
    dcc.Graph(figure=dual_axis_fig, id='dual-axis-graph'),
    html.Hr(),  # Horizontal line

    # Pie Chart for Orders Delivered
    dcc.Graph(figure=pie_fig, id='pie-graph'),
    html.Div("**5. Proportion of Orders Delivered:** This pie chart shows the proportion of orders delivered for each month."),
    html.Hr(),  # Horizontal line

    # Display each ratio figure with notes
    html.Div([  
        dcc.Graph(figure=ratios_figs[0], id='cost-per-lead-graph'),
        html.Div("**6. Cost per Lead Ratio:** This plot shows the cost incurred for each lead over time. **Cost per Lead = Total Costs / Leads**"),
        html.Hr(),  # Horizontal line

        dcc.Graph(figure=ratios_figs[1], id='cost-per-confirmed-order-graph'),
        html.Div("**7. Cost per Confirmed Order Ratio:** This plot shows the cost incurred for each confirmed order over time. **Cost per Confirmed Order = Total revenue generated in a particular month / Confirmed Orders**"),
        html.Hr(),  # Horizontal line

        dcc.Graph(figure=ratios_figs[2], id='leads-to-calls-graph'),
        html.Div("**8. Leads to Calls Connected Ratio:** This plot shows the ratio of leads that resulted in connected calls. **Leads to Calls Ratio = Connected Calls / Total Leads**"),
        html.Hr(),  # Horizontal line

        dcc.Graph(figure=ratios_figs[3], id='leads-to-validated-graph'),
        html.Div("**9. Leads to Validated Lead Ratio:** This plot shows the ratio of leads that were validated. **Leads to Validated Leads Ratio = Validated Leads / Total Leads**"),
        html.Hr(),  # Horizontal line

        dcc.Graph(figure=ratios_figs[4], id='leads-to-order-graph'),
        html.Div("**10. Leads to Order Ratio:** This plot shows the ratio of leads that resulted in confirmed orders. **Leads to Order Ratio = Total Order Count / Total Leads**"),
        html.Hr(),  # Horizontal line

        dcc.Graph(figure=ratios_figs[5], id='roas-graph'),
        html.Div("**11. Return on Advertising Spend (ROAS):** This plot shows the return on advertising spend over time. **ROAS = Revenue / Advertising Spend (Total Costs, where total cost is equal to the call cost of all leads plus digital marketing costs per month).**"),
        html.Hr(),  # Horizontal line
    ]),

    # Stacked Bar Chart for Leads and Orders
    dcc.Graph(figure=stacked_fig, id='stacked-graph'),
    html.Div("**12. Monthly Metrics Overview:** This stacked bar chart provides insights into leads and orders for each month."),
    html.Hr(),  # Horizontal line

    # Revenue vs Total Cost
    dcc.Graph(figure=revenue_cost_fig, id='revenue-cost-graph'),
    html.Div("**13. Revenue Generated vs. Total Cost:** This chart compares revenue generated with total costs for each month."),
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
