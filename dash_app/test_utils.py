from utils import get_summary_data

data = get_summary_data()
print(data.keys())


from charts import get_top_channels_chart

summary = get_summary_data()
fig = get_top_channels_chart(summary)
fig.show()


