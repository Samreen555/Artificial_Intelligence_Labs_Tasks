"""
Crop Recommendation Dataset Generator
Generates a realistic agricultural dataset matching the Kaggle Crop Recommendation Dataset structure.
Source reference: Atharva Ingle, Kaggle Crop Recommendation Dataset (2020)
"""
import numpy as np
import pandas as pd

np.random.seed(42)

CROP_PARAMS = {
    'rice':        dict(N=(79,6),  P=(47,4),  K=(40,4),  temp=(23,1.5),hum=(82,3), ph=(6.4,0.4), rain=(236,20), yield_base=38),
    'maize':       dict(N=(78,5),  P=(48,5),  K=(20,3),  temp=(22,2),  hum=(65,5), ph=(6.0,0.5), rain=(85,12),  yield_base=55),
    'chickpea':    dict(N=(40,4),  P=(67,5),  K=(79,6),  temp=(18,2),  hum=(16,4), ph=(7.3,0.4), rain=(73,10),  yield_base=18),
    'kidneybeans': dict(N=(20,3),  P=(67,5),  K=(20,3),  temp=(20,2),  hum=(21,4), ph=(5.7,0.4), rain=(105,12), yield_base=22),
    'pigeonpeas':  dict(N=(20,3),  P=(67,5),  K=(20,3),  temp=(27,2),  hum=(49,5), ph=(5.8,0.4), rain=(149,15), yield_base=15),
    'mothbeans':   dict(N=(21,3),  P=(48,4),  K=(20,3),  temp=(28,2),  hum=(53,5), ph=(6.9,0.4), rain=(51,8),   yield_base=12),
    'mungbean':    dict(N=(20,3),  P=(47,4),  K=(20,3),  temp=(28,2),  hum=(85,5), ph=(6.7,0.4), rain=(49,8),   yield_base=14),
    'blackgram':   dict(N=(40,4),  P=(67,5),  K=(19,3),  temp=(29,2),  hum=(65,5), ph=(7.1,0.4), rain=(68,10),  yield_base=13),
    'lentil':      dict(N=(18,3),  P=(68,5),  K=(19,3),  temp=(24,2),  hum=(65,5), ph=(6.9,0.4), rain=(46,7),   yield_base=16),
    'pomegranate': dict(N=(18,3),  P=(18,3),  K=(40,4),  temp=(21,2),  hum=(90,4), ph=(6.5,0.4), rain=(107,12), yield_base=20),
    'banana':      dict(N=(100,8), P=(82,6),  K=(50,5),  temp=(27,2),  hum=(80,4), ph=(5.9,0.4), rain=(105,12), yield_base=180),
    'mango':       dict(N=(20,3),  P=(27,3),  K=(30,3),  temp=(31,2),  hum=(50,5), ph=(5.8,0.4), rain=(95,12),  yield_base=60),
    'grapes':      dict(N=(23,3),  P=(132,8), K=(200,10),temp=(23,2),  hum=(81,4), ph=(5.9,0.4), rain=(69,10),  yield_base=85),
    'watermelon':  dict(N=(100,8), P=(57,5),  K=(50,5),  temp=(25,2),  hum=(85,4), ph=(6.5,0.4), rain=(51,8),   yield_base=110),
    'muskmelon':   dict(N=(100,8), P=(17,3),  K=(50,5),  temp=(28,2),  hum=(92,3), ph=(6.4,0.4), rain=(25,5),   yield_base=90),
    'apple':       dict(N=(20,3),  P=(134,8), K=(200,10),temp=(21,2),  hum=(92,3), ph=(5.9,0.4), rain=(113,12), yield_base=45),
    'orange':      dict(N=(20,3),  P=(16,3),  K=(10,2),  temp=(22,2),  hum=(92,3), ph=(7.0,0.4), rain=(111,12), yield_base=55),
    'papaya':      dict(N=(49,5),  P=(59,5),  K=(50,5),  temp=(33,2),  hum=(92,3), ph=(6.7,0.4), rain=(139,15), yield_base=120),
    'coconut':     dict(N=(21,3),  P=(16,3),  K=(30,3),  temp=(27,2),  hum=(94,3), ph=(5.9,0.4), rain=(175,18), yield_base=70),
    'cotton':      dict(N=(117,8), P=(46,5),  K=(19,3),  temp=(23,2),  hum=(79,5), ph=(6.9,0.4), rain=(80,12),  yield_base=25),
    'jute':        dict(N=(78,5),  P=(46,5),  K=(39,4),  temp=(24,2),  hum=(80,5), ph=(6.7,0.4), rain=(175,18), yield_base=32),
    'coffee':      dict(N=(101,8), P=(29,3),  K=(30,3),  temp=(25,2),  hum=(58,5), ph=(6.8,0.4), rain=(159,18), yield_base=8),
}

SAMPLES_PER_CROP = 100
rows = []

for crop, p in CROP_PARAMS.items():
    N    = np.random.normal(p['N'][0],    p['N'][1],    SAMPLES_PER_CROP).clip(0, 140)
    P    = np.random.normal(p['P'][0],    p['P'][1],    SAMPLES_PER_CROP).clip(5, 145)
    K    = np.random.normal(p['K'][0],    p['K'][1],    SAMPLES_PER_CROP).clip(5, 205)
    temp = np.random.normal(p['temp'][0], p['temp'][1], SAMPLES_PER_CROP).clip(8, 44)
    hum  = np.random.normal(p['hum'][0],  p['hum'][1],  SAMPLES_PER_CROP).clip(14, 100)
    ph   = np.random.normal(p['ph'][0],   p['ph'][1],   SAMPLES_PER_CROP).clip(3.5, 9.9)
    rain = np.random.normal(p['rain'][0], p['rain'][1], SAMPLES_PER_CROP).clip(20, 300)
    # Synthetic yield: agronomically weighted formula + per-crop baseline
    noise  = np.random.normal(0, p['yield_base'] * 0.08, SAMPLES_PER_CROP)
    yield_ = (p['yield_base']
              + 0.05*N + 0.04*P + 0.03*K
              + 0.20*temp + 0.02*hum
              - 1.5*(ph - p['ph'][0])**2
              + 0.01*rain + noise).clip(1, 350)

    for i in range(SAMPLES_PER_CROP):
        rows.append([round(N[i],2), round(P[i],2), round(K[i],2),
                     round(temp[i],2), round(hum[i],2), round(ph[i],2),
                     round(rain[i],2), crop, round(yield_[i],2)])

df = pd.DataFrame(rows, columns=['N','P','K','temperature','humidity','ph','rainfall','label','yield'])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv('Crop_recommendation.csv', index=False)
print(f"Dataset generated: {df.shape[0]} rows × {df.shape[1]} columns")
print(df.head())
