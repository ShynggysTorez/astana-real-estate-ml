import pandas as pd

# Загрузка CSV
df = pd.read_csv(r"C:\Users\cheen\PycharmProjects\krisha_parser_project\krisha_ekibastuz_detailed.csv")

# Быстрый просмотр
print(df.shape)
print(df.head(3))
print(df.info())
