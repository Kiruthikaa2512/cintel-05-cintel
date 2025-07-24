# --------------------------------------------
# Imports at the top - PyShiny EXPRESS VERSION
# --------------------------------------------

from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats
from faicons import icon_svg
import plotly.graph_objs as go

# --------------------------------------------
# Constants and reactive data setup
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 15
DEQUE_SIZE: int = 20
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# --------------------------------------------
# Reactive calc that generates temp + humidity
# --------------------------------------------

@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Generate random data
    temperature = round(random.uniform(-18, -16), 1)
    humidity = round(random.uniform(60, 100), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_dictionary_entry = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp,
    }

    reactive_value_wrapper.get().append(new_dictionary_entry)
    deque_snapshot = reactive_value_wrapper.get()
    df = pd.DataFrame(deque_snapshot)

    return deque_snapshot, df, new_dictionary_entry

# --------------------------------------------
# Page layout & sidebar
# --------------------------------------------

ui.page_opts(title="Global Climate Monitor by Kiruthikaa", fillable=True)

with ui.sidebar(open="open"):
    ui.h2("Climate Stream Center", class_="text-center")
    ui.p("Live environmental metrics updating in real-time using PyShiny.", class_="text-center")
    ui.hr()
    ui.h6("Links:")
    ui.a("PyShiny Docs", href="https://shiny.posit.co/py/", target="_blank")

# --------------------------------------------
# Value Boxes Section
# --------------------------------------------

with ui.layout_columns():
    with ui.value_box(showcase=icon_svg("sun"), theme="bg-gradient-orange-red"):
        "Temperature"
        @render.text
        def show_temp():
            _, _, latest = reactive_calc_combined()
            return f"{latest['temperature']} °C"
        "Live Antarctic Temperature"

    with ui.value_box(showcase=icon_svg("droplet"), theme="bg-gradient-cyan-blue"):
        "Humidity"
        @render.text
        def show_humidity():
            _, _, latest = reactive_calc_combined()
            return f"{latest['humidity']} %"
        "Live Antarctic Humidity"

    with ui.value_box(showcase=icon_svg("clock"), theme="bg-gradient-purple-indigo"):
        "Timestamp"
        @render.text
        def show_time():
            _, _, latest = reactive_calc_combined()
            return latest["timestamp"]
        "Last Updated"

# --------------------------------------------
# Data Grid Section
# --------------------------------------------

with ui.card(full_screen=True):
    ui.card_header("Recent Readings Snapshot")
    @render.data_frame
    def display_grid():
        _, df, _ = reactive_calc_combined()
        return render.DataGrid(df, width="100%")

# --------------------------------------------
# Temperature Trend Chart
# --------------------------------------------

with ui.card():
    ui.card_header("Temperature Trend")

    @render_plotly
    def temp_chart():
        _, df, _ = reactive_calc_combined()
        if df.empty:
            return go.Figure()

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["temperature"],
            mode="lines+markers",
            name="Temp",
            line=dict(color="#FF5733"),
        ))

        if len(df) >= 2:
            x_vals = list(range(len(df)))
            slope, intercept, *_ = stats.linregress(x_vals, df["temperature"])
            trend = [slope * x + intercept for x in x_vals]

            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=trend,
                mode="lines",
                name="Trend",
                line=dict(color="#900C3F", dash="dash"),
            ))

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            plot_bgcolor="#FDFEFE",
            paper_bgcolor="#FBFCFC",
            font=dict(color="#1B2631"),
            title="Live Temperature Chart"
        )

        return fig

# --------------------------------------------
# Humidity Trend Chart (Enhanced Feature)
# --------------------------------------------

with ui.card():
    ui.card_header("Humidity Trend")

    @render_plotly
    def humidity_chart():
        _, df, _ = reactive_calc_combined()
        if df.empty:
            return go.Figure()

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["timestamp"],
            y=df["humidity"],
            mode="lines+markers",
            name="Humidity",
            line=dict(color="#3498DB"),
        ))

        if len(df) >= 2:
            x_vals = list(range(len(df)))
            slope, intercept, *_ = stats.linregress(x_vals, df["humidity"])
            trend = [slope * x + intercept for x in x_vals]

            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=trend,
                mode="lines",
                name="Humidity Trend",
                line=dict(color="#1F618D", dash="dash"),
            ))

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Humidity (%)",
            plot_bgcolor="#EBF5FB",
            paper_bgcolor="#F7F9F9",
            font=dict(color="#154360"),
            title="Live Humidity Chart"
        )

        return fig