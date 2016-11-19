import os
import webbrowser


def pytest_unconfigure(config):
    htmlcov_path = os.path.join('htmlcov', 'index.html')
    if (hasattr(config.option, 'cov_report') and
            'html' in config.option.cov_report and
            os.path.isfile(htmlcov_path)):
        try:
            webbrowser.open_new_tab(htmlcov_path)
        except webbrowser.Error:
            pass
