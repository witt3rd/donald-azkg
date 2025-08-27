import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# Provided data
milestones = [
    {"Year": "2024", "Quarter": "Q4", "Event": "Agentic AI Market Size", "Value": 5.2, "Type": "Market Size ($B)", "Description": "Current agentic AI market valuation"},
    {"Year": "2025", "Quarter": "Q2", "Event": "NVIDIA Research Paper Published", "Value": 1, "Type": "Research Milestone", "Description": "Small Language Models are the Future of Agentic AI"},
    {"Year": "2025", "Quarter": "Q2", "Event": "Mistral-NeMo-Minitron 8B Released", "Value": 1, "Type": "Product Release", "Description": "State-of-the-art 8B parameter model"},
    {"Year": "2025", "Quarter": "Q3", "Event": "Research Validation", "Value": 50, "Type": "Research Sources", "Description": "50+ sources confirming SLM advantages"},
    {"Year": "2025", "Quarter": "Q4", "Event": "Enterprise Adoption Begins", "Value": 25, "Type": "Adoption (%)", "Description": "Companies planning agentic AI pilots"},
    {"Year": "2026", "Quarter": "Q2", "Event": "Mainstream SLM Deployment", "Value": 1, "Type": "Deployment Milestone", "Description": "Predicted enterprise SLM adoption"},
    {"Year": "2027", "Quarter": "Q2", "Event": "Widespread Agentic AI", "Value": 50, "Type": "Adoption (%)", "Description": "Companies using agentic AI systems"},
    {"Year": "2034", "Quarter": "Q4", "Event": "Market Maturation", "Value": 200, "Type": "Market Size ($B)", "Description": "Projected agentic AI market size"}
]
df = pd.DataFrame(milestones)

def quarter_str_to_date(row):
    q = row['Quarter']
    y = int(row['Year'])
    months = {'Q1': 1, 'Q2': 4, 'Q3': 7, 'Q4': 10}
    return datetime(y, months.get(q, 1), 1)

df['Date'] = df.apply(quarter_str_to_date, axis=1)

# Market size line (y-axis >0) and 0 for milestones
market_df = df[df['Type'] == 'Market Size ($B)'].sort_values('Date')
scatter_df = df[df['Type'] != 'Market Size ($B)']

color_sequence = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C', '#964325', '#944454', '#13343B', '#DB4545']
type_to_color = {t: color_sequence[i % len(color_sequence)] for i, t in enumerate(df['Type'].unique())}
scatter_df['color'] = scatter_df['Type'].map(type_to_color)

fig = go.Figure()
# Market size progression line
fig.add_trace(go.Scatter(
    x=market_df['Date'],
    y=market_df['Value'],
    mode='lines+markers',
    name='Market Size',
    marker=dict(color=color_sequence[0], size=10),
    line=dict(color=color_sequence[0], width=3),
    hovertemplate='Market: $%{y}b<br>Date: %{x|%Y-%b}'
))
# Timeline scatter milestones
for idx, row in scatter_df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['Date']],
        y=[0],
        mode='markers+text',
        marker=dict(color=row['color'], size=14, line=dict(width=2, color='white')),
        name=row['Event'],
        hovertemplate=f"{row['Event'][:15]}<br>Date: {row['Date'].strftime('%Y-%b')}" + (f"<br>Val: {int(row['Value']) if row['Type'] in ['Research Sources', 'Adoption (%)'] else ''}"),
        text=[row['Event'][:15]],
        textposition='top center',
        showlegend=False
    ))
# Abbreviate y axis ticks
fig.update_yaxes(
    tickvals=[0,5.2,200],
    ticktext=['0', '5.2b', '200b'],
    title_text='Market /%',
    showgrid=True,
    zeroline=False
)
fig.update_xaxes(
    title_text='Year',
    tickformat='%Y',
)
fig.update_layout(
    title_text="NVIDIA SLM Agentic AI Timeline",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

fig.write_image("nvidia_ai_timeline.png")
