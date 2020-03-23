import pandas as pd
import glob

path = r"C:\Users\danie\Desktop\all\processed"
files = glob.glob(path + "/*.csv")
temp_dfs = []
for filename in files:
    temp_df = pd.read_csv(filename, index_col=None, header=0, encoding='latin')
    print(temp_df.shape)
    temp_dfs.append(temp_df)
df = pd.concat(temp_dfs, axis=0, ignore_index=True)
#print(df.shape)

from sklearn.model_selection import train_test_split
train_x, text_x, train_y, test_y = train_test_split(df.drop('Delayed', axis=1),df['Delayed'], test_size=0.2, random_state=42)
print(train_x.shape,train_y.shape)