from dash import Dash, dcc, html, Input, Output

import datetime
import os

from flask_caching import cache

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
cache = cache(app.server, config={
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
})
app.config.suppress_callback_exceptions = True

timeout = 20
app.layout = html.Div([
    html.Div(id='flask-cache-memoized-children'),
    dcc.RadioItems(
        [f"Option {i}" for i in range(1, 4)],
        'Option 1',
        id='flask-cache-memoized-dropdown'
    ),
    html.Div(f'Results are cached for {timeout} seconds')
])


@app.callback(
    Output('flask-cache-memoized-children', 'children'),
    Input('flask-cache-memoized-dropdown', 'value'))
@cache.memoize(timeout=timeout)  # in seconds
def render(value):
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    return f'Selected "{value}" at "{current_time}"'


if __name__ == '__main__':
    app.run_server(debug=True)