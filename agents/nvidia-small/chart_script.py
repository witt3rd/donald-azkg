import pandas as pd
import plotly.graph_objects as go

# Data from the provided json
models = [
    {
        "Model": "Microsoft Phi-2",
        "Parameters": "2.7B",
        "Comparison_Model_Size": "30B",
        "Performance": "Matches",
        "Efficiency_Advantage": "15x lower latency",
        "Parameter_Ratio": 11.1
    },
    {
        "Model": "NVIDIA Nemotron-H",
        "Parameters": "2-9B",
        "Comparison_Model_Size": "30B",
        "Performance": "Matches",
        "Efficiency_Advantage": "90% fewer FLOPs",
        "Parameter_Ratio": 6.7
    },
    {
        "Model": "Hugging Face SmolLM2",
        "Parameters": "0.125-1.7B",
        "Comparison_Model_Size": "14B",
        "Performance": "Competes",
        "Efficiency_Advantage": "Similar accuracy",
        "Parameter_Ratio": 11.8
    },
    {
        "Model": "NVIDIA Hymba-1.5B",
        "Parameters": "1.5B",
        "Comparison_Model_Size": "13B",
        "Performance": "Outperforms",
        "Efficiency_Advantage": "3.5x higher throughput",
        "Parameter_Ratio": 8.7
    },
    {
        "Model": "Salesforce xLAM-2",
        "Parameters": "8B",
        "Comparison_Model_Size": "GPT-4o/Claude 3.5",
        "Performance": "Outperforms",
        "Efficiency_Advantage": "Superior tool calling",
        "Parameter_Ratio": 20
    },
    {
        "Model": "DeepMind RETRO",
        "Parameters": "7.5B",
        "Comparison_Model_Size": "175B (GPT-3)",
        "Performance": "Matches",
        "Efficiency_Advantage": "25x fewer parameters",
        "Parameter_Ratio": 23.3
    },
]

# prepare dataframe
brand_colors = ["#1FB8CD", "#DB4545", "#2E8B57", "#5D878F", "#D2BA4C", "#B4413C"]

df = pd.DataFrame(models)

# Axis labels limited to 15 chars
xaxis_title = "Model"
yaxis_title = "Perf/Param x"

# Plotting Parameter Efficiency Advantage as bars
data = [
    go.Bar(
        x=df["Model"],
        y=df["Parameter_Ratio"],
        marker=dict(color=brand_colors[:len(df)]),
        text=df["Efficiency_Advantage"],
        hovertemplate="Model: %{x}<br>Param: %{customdata[0]}<br>Vs: %{customdata[1]}<br>Eff: %{text}<br>Perf: %{customdata[2]}<br>Ratio: %{y}x<extra></extra>",
        customdata=df[["Parameters", "Comparison_Model_Size", "Performance"]].values,
        showlegend=False
    )
]

fig = go.Figure(data=data)

fig.update_layout(
    title="SLMs vs LLMs: Param & Cost Edge",
    xaxis_title=xaxis_title,
    yaxis_title=yaxis_title,
)

fig.update_xaxes()
fig.update_yaxes()

fig.write_image("slm_vs_llm_param_cost.png")
