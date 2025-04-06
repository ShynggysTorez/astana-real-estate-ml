import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка очищенных данных
df = pd.read_csv("krisha_cleaned.csv")

# 📈 Корреляционная матрица
numeric_cols = ['price', 'price_per_m2', 'total_area', 'room_count',
                'floor_num', 'floor_total', 'year_built', 'ceiling_height']

plt.figure(figsize=(10, 6))
sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("📊 Корреляционная матрица")
plt.tight_layout()
plt.savefig("correlation_matrix.png")
plt.close()

# 📊 Средняя цена за м² по районам
region_stats = df.groupby("region_clean").agg({
    "price": "mean",
    "price_per_m2": "mean",
    "room_count": "count"
}).rename(columns={
    "price": "avg_price",
    "price_per_m2": "avg_price_per_m2",
    "room_count": "num_objects"
}).sort_values(by="avg_price_per_m2", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=region_stats.reset_index(), x="avg_price_per_m2", y="region_clean", palette="viridis")
plt.title("💰 Средняя цена за м² по районам Астаны")
plt.xlabel("Цена за м² (тг)")
plt.ylabel("Район")
plt.tight_layout()
plt.savefig("price_per_m2_by_region.png")
plt.close()

print("✅ EDA завершён. Графики сохранены.")