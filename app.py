from flask import Flask, render_template

from load_data import (
    get_data_summary,
    get_processing_summary,
    get_analysis_summary,
    get_dashboard_summary,
    get_preview
)


app = Flask(__name__)


# =========================================
# DASHBOARD
# =========================================

@app.route("/")
def index():

    dashboard = get_dashboard_summary()

    analysis = get_analysis_summary()

    preview = get_preview()

    return render_template(
        "index.html",

      active="dashboard",

        dashboard=dashboard,

        analysis=analysis,

        preview=preview
    )


# =========================================
# DATA LOADING
# =========================================

@app.route("/data-loading")
def data_loading():

    summary = get_data_summary()

    return render_template(
        "index.html",

   active="data-loading",

        summary=summary
    )


# =========================================
# DATA PROCESSING
# =========================================

@app.route("/data-processing")
def data_processing():

    processing = get_processing_summary()

    return render_template(
        "index.html",

        active="data-processing",


        processing=processing
    )


# =========================================
# DATA ANALYSIS
# =========================================

@app.route("/data-analysis")
def data_analysis():

    analysis = get_analysis_summary()

    return render_template(
        "index.html",

        active="data-analysis",

        analysis=analysis
    )


# =========================================
# MODEL TRAINING
# =========================================

@app.route("/model-training")
def model_training():

    return render_template(
        "index.html",

        active="model-training"
    )


# =========================================
# PREDICTION
# =========================================

@app.route("/prediction")
def prediction():

    return render_template(
        "index.html",

        active="prediction"
    )


# =========================================
# REPORTS
# =========================================

@app.route("/reports")
def reports():

    dashboard = get_dashboard_summary()

    analysis = get_analysis_summary()

    processing = get_processing_summary()

    return render_template(
        "index.html",

        active="reports",

        dashboard=dashboard,

        analysis=analysis,

        processing=processing
    )


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )