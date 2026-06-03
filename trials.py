import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr"],
    "Sales": [100, 150, 130, 200]
})

fig = px.line(df, x="Month", y="Sales", title="Monthly Sales")
fig.show()