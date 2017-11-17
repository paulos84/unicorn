from app import create_app
from app.charts import charts
from app.exp_form import create_exp


app = create_app()
app.register_blueprint(create_exp)
app.register_blueprint(charts)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, passthrough_errors=True)