from flask_assets import Bundle, Environment
from .. import app

bundles = {
    'dashboard_css': Bundle(
        'css/lib/bootstrap.css',
        'css/lib/bootstrap-theme.css',
        'css/lib/bootstrap-select.css',
        'css/lib/daterangepicker.css',
        'css/lib/dc.css',
        'css/lib/jquery-ui.css',
        'css/lib/d3-tooltips.css',
        'css/lib/bootstrap-tagsinput.css',
        'css/custom.css',
        output='gen/css.css'),

    'dashboard_js': Bundle(
        'js/lib/jquery-3.1.1.min.js',
        'js/lib/jquery-ui.js',
        'js/lib/bootstrap.js',
        'js/lib/moment.min.js',
        'js/lib/daterangepicker.js',
        'js/lib/d3.js',
        'js/lib/crossfilter.min.js',
        'js/lib/effects.js',
        'js/lib/dc.js',
        'js/lib/d3-tooltips.js',
        'js/lib/bootstrap-select.js',
        'js/lib/bootstrap-tagsinput.js',
        'js/responsive.js',
        'js/graph.js',
        'js/dashboard.js',
        output='gen/javascript.js'),
}


assets = Environment(app)
assets.register(bundles)
