def register_filters(app):
    app.jinja_env.filters['severity_class'] = serverity_class_filter

def serverity_class_filter(severity):
    if severity == 'CRITICAL':
        return "table-danger"
    elif severity == 'HIGH':
        return "table-warning"
    elif severity == 'MEDIUM':
        return "table-info"
    else:
        return "table-light"



