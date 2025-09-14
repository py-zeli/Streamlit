import streamlit
import pandas as pd

df = pd.read_csv('01 Spotify.csv')

df.loc[df['Stream'] >= (10**9)]
print('Olá, Senhor!')