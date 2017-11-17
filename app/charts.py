from flask import render_template, Blueprint


charts = Blueprint('charts', __name__)

@charts.route('/unicorn/plot')
def plot(chart_id='chart_ID', chart_type='line', chart_height=550, chart_width=800):
    #exp = Experiment.query.filter_by(id=exp_id).first()
    chart = {"renderTo": chart_id, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": 'GOS', "data": [3,2,3,4]}, {"name": 'dp3+', "data": [2,6,5,7]}]
    title = {"text": 'Experiment_id: {}. Conditions:...'.format('foo')}
    xaxis = {"categories": [1,2,3,4]}
    yaxis = {"title": {"text": '%'}}
    return render_template('chart.html', chartID=chart_id, chart=chart, series=series, title=title, xAxis=xaxis,
                           yAxis=yaxis)