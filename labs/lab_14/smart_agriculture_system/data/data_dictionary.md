# Data Dictionary — Crop Recommendation Dataset

| Column | Type | Unit | Range | Description |
|--------|------|------|-------|-------------|
| N | float | kg/ha | 0–140 | Nitrogen content in soil |
| P | float | kg/ha | 5–145 | Phosphorous content in soil |
| K | float | kg/ha | 5–205 | Potassium content in soil |
| temperature | float | °C | 8–44 | Ambient temperature |
| humidity | float | % | 14–100 | Relative humidity |
| ph | float | — | 3.5–9.9 | Soil pH value |
| rainfall | float | mm | 20–300 | Annual rainfall |
| label | string | — | 22 classes | Target crop recommendation |
| yield | float | q/ha | 1–350 | Estimated crop yield (derived) |

## Preprocessing Steps
1. Structural validation
2. Median imputation for missing values
3. IQR-fence outlier clipping
4. StandardScaler normalisation
5. LabelEncoder for crop names
6. 80/20 stratified train-test split
