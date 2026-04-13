#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt

# Данные
years = [1987, 1990, 1993, 1996]
length_thousand_km = [33.4, 37.3, 38.0, 38.8]        # тыс. км
percent_of_total = [39.3, 42.8, 43.6, 44.8]          # %

# DataFrame
df = pd.DataFrame({
    "Year": years,
    "Length_thousand_km": length_thousand_km,
    "Percent_of_total": percent_of_total
}).set_index("Year")

output_dir = os.path.abspath(".")
bar_path = os.path.join(output_dir, "bar_chart.png")
pie_path = os.path.join(output_dir, "pie_charts.png")

# --- a) Ленточная диаграмма (bar) ---
fig, ax = plt.subplots(figsize=(9, 5))
bar_width = 0.35
x = list(range(len(df.index)))

ax.bar([i - bar_width/2 for i in x], df["Length_thousand_km"], width=bar_width, label="Протяжённость, тыс км", color="#4C72B0")
ax.bar([i + bar_width/2 for i in x], df["Percent_of_total"], width=bar_width, label="В % к общей длине", color="#55A868")

ax.set_xticks(x)
ax.set_xticklabels(df.index)
ax.set_xlabel("Год")
ax.set_ylabel("Значение")
ax.set_title("Протяжённость электрифицированных линий — ленточная диаграмма")
ax.legend()
ax.grid(axis='y', linestyle=':', alpha=0.6)

# Подписи значений над столбцами
for i in x:
    ax.text(i - bar_width/2, df["Length_thousand_km"].iloc[i] + 0.4, f"{df['Length_thousand_km'].iloc[i]:.1f}", ha='center', fontsize=9)
    ax.text(i + bar_width/2, df["Percent_of_total"].iloc[i] + 0.6, f"{df['Percent_of_total'].iloc[i]:.1f}%", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(bar_path, dpi=300)
plt.close(fig)

# --- б) Структурные диаграммы (pie) ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie 1: доля каждого года от суммарной электрифицированной протяжённости за все годы
axes[0].pie(df["Length_thousand_km"], labels=df.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired(range(len(df))))
axes[0].set_title("Доля протяжённости по годам (тыс. км)")

# Pie 2: сравнение процентов (нормируем к сумме для наглядности)
axes[1].pie(df["Percent_of_total"], labels=df.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired(range(len(df))))
axes[1].set_title("Сравнение % электрификации по годам (от суммы % для наглядности)")

plt.tight_layout()
plt.savefig(pie_path, dpi=300)
plt.close(fig)

print(f"Saved: {bar_path}")
print(f"Saved: {pie_path}")
