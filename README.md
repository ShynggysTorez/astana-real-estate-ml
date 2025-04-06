# 🏙️ Astana Real Estate Price Prediction 🇿🇿

This project showcases a complete machine learning pipeline to predict apartment prices in **Astana, Kazakhstan**, based on real listings collected from the popular real estate platform [Krisha.kz](https://krisha.kz).

The work was done fully from scratch by me, including:
- Writing a custom web scraper
- Cleaning and transforming raw text data
- Performing exploratory data analysis (EDA)
- Training and evaluating machine learning models
- Deploying an interactive prediction tool using Streamlit

---

## 🔍 Data Collection & Parsing

I built a scraper using `requests` and `BeautifulSoup` to extract:
- Title, price, address, region, link
- Technical info: building type, floor, year built, ceiling height, area
- Apartment condition and complex name (if available)
- Raw description text for optional NLP analysis

All listings were collected from over **200 pages** for Astana.

---

## 🪜 Data Cleaning & Feature Engineering

Since Krisha data is semi-structured, I manually cleaned fields such as:
- Extracted floor and total floors from "4 из 9"
- Converted ceiling height "2.7 м" to float
- Parsed area like "69.5 м²" and extracted numeric value
- Standardized categories like building type and condition
- Corrected district names by cleaning address strings

I saved the cleaned data as `krisha_cleaned.csv`, which served as the foundation for modeling.

---

## 📊 Exploratory Data Analysis (EDA)

Using Seaborn and Matplotlib, I visualized:
- Average price per m² across districts
- Distribution of room count, floor, year built
- Correlation heatmaps for numeric features
- Feature importance after training the model

This helped guide feature selection and understand patterns in the market.

---

## 📊 Model Training

I used the powerful `XGBoostRegressor` wrapped in a pipeline with:
- StandardScaler for numeric values
- OneHotEncoder for categorical features

**Target variable:** apartment price (in KZT)

**Features used:**
- total_area, room_count
- floor_num, floor_total
- year_built, ceiling_height
- region_clean, house_type, condition, complex

---

## 🔢 Model Results

The final model performed well:

- 📊 **MAE:** 5,023,638 ₸
- 📉 **RMSE:** 9,043,667 ₸
- 🎯 **R² Score:** 0.90

Model was saved as `model_xgboost.pkl`

---

## 🔍 Streamlit Web App

I also created a simple prediction interface with **Streamlit**, allowing users to:
- Select district and building type
- Enter floor, area, year, ceiling height
- See instant price predictions based on trained ML model

> Screenshot of local app is available below:

![App Screenshot](./screenshot.png)

---

## 📂 Files in this Repository

```
krisha_astana_detailed.csv    # Raw listings from Krisha.kz
krisha_cleaned.csv            # Cleaned dataset for ML
eda_analysis.py               # Exploratory data analysis code
ml_model.py                   # XGBoost model training
app.py                        # Streamlit prediction UI
model_xgboost.pkl             # Trained model
screenshot.png                # Optional app interface preview
```

---

## 🚀 Next Steps

- Add more cities like Ekibastuz, Almaty, Shymkent
- Add real-time scraping and auto-update feature
- Deploy the app on my personal website or Render/Heroku

---

## 📧 Contact

**Author:** Shynggys Torez  
**Email:** cheengis01@gmail.com  
**GitHub:** [ShynggysTorez](https://github.com/ShynggysTorez)

Feel free to reach out if you'd like a custom project, price prediction model, or data dashboard!

