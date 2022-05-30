def number_style(value):
    if value < 0:
        style = 'red'
    else:
        style = 'green'
    return f'<span style="color:{style};">{value}</span>'
