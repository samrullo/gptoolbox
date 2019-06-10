from application import app as application

if __name__ == '__main__':
    application.static_url_path = application.config['STATIC_URL'] + '/static'
    # remove old static map
    url_map = application.url_map
    try:
        for rule in url_map.iter_rules('static'):
            url_map._rules.remove(rule)
    except ValueError:
        # no static view was created yet
        pass

    # register new; the same view function is used
    application.add_url_rule(
        application.static_url_path + '/<path:filename>',
        endpoint='static', view_func=application.send_static_file)
    application.run()
