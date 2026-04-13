NUM_STEPS = 3 

REPORT_TEMPLATE = """
Мы провели {observations} наблюдений, подбрасывая монетку: {tail_count} раз выпадал решка, а {head_count} — орёл.
Вероятности составляют {tail_percentage:.2f} % и {head_percentage:.2f} % соответственно.
По нашим прогнозам, следующие три наблюдения будут такими: {prediction}.
"""