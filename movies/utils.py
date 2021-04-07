def case_of_entries(x):
    decade = x % 100
    one = x % 10
    if decade in range(11, 20):
        return f'{x} записей были обновлены'
    elif one == 1:
        return f'{x} запись была обновлена'
    elif 1 < one < 5:
        return f'{x} записи были обновлены'
    else:
        return f'{x} записей были обновлены'
