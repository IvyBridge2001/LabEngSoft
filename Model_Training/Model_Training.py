#Create single file
#import pandas as pd
#import glob

#path = r"C:\Users\danie\Desktop\gru_data\Data_filtered"
#files = glob.glob(path + "/*.csv")
#temp_dfs = []
#for filename in files:
#    temp_df = pd.read_csv(filename, index_col=None, header=0, encoding='latin')
#    temp_dfs.append(temp_df)
#df = pd.concat(temp_dfs, axis=0, ignore_index=True)
#df.to_csv(path+r'\2019.csv')
import pandas as pd
path = r"C:\Users\danie\Desktop\gru_data\2019.csv"
df = pd.read_csv(path,sep=',')
df['Delayed'] = df['Delayed'].astype(float)
print(df.dtypes)
from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(df.drop('Delayed', axis=1),df['Delayed'], test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=13)
model.fit(train_x,train_y)
import numpy as np
def predict_delay(departure_date_time, origin, destination):
    from datetime import datetime

    try:
        departure_date_time_parsed = datetime.strptime(departure_date_time, '%d/%m/%Y %H:%M:%S')
    except ValueError as e:
        return 'Error parsing date/time - {}'.format(e)

    month = departure_date_time_parsed.month
    day = departure_date_time_parsed.day
    day_of_week = departure_date_time_parsed.isoweekday()
    hour = departure_date_time_parsed.hour

    origin = origin.upper()
    destination = destination.upper()

    input = [{'Month': month,
              'Day': day,
              #'WeekDay': day_of_week,
              'Hour': hour,
              'Origin_EGLL': 1 if origin == 'EGLL' else 0,
              'Origin_SBGR': 1 if origin == 'SBGR' else 0,
              'Origin_KJFK': 1 if origin == 'KJFK' else 0,
              'Origin_SBGL': 1 if origin == 'SBGL' else 0,
              'Dest_EGLL': 1 if destination == 'EGLL' else 0,
              'Dest_SBGR': 1 if destination == 'SBGR' else 0,
              'Dest_KJFK': 1 if destination == 'KJFK' else 0,
              'Dest_SBGL': 1 if destination == 'SBGL' else 0 }]
    print(input)
    return model.predict_proba(pd.DataFrame(input))[0][0]

def main():
	try:
		
		labels = ('Oct 1', 'Oct 2', 'Oct 3', 'Oct 4', 'Oct 5', 'Oct 6', 'Oct 7')
		values = (predict_delay('1/12/2019 12:45:00', 'SBGR', 'EGLL'),
				predict_delay('2/12/2019 12:45:00', 'SBGR', 'EGLL'),
				predict_delay('3/12/2019 12:45:00', 'SBGR', 'EGLL'),
				predict_delay('4/12/2019 12:45:00', 'SBGR', 'EGLL'),
				predict_delay('5/12/2019 12:45:00', 'SBGR', 'EGLL'),
				predict_delay('6/12/2019 12:45:00', 'SBGR', 'EGLL'),
				predict_delay('7/12/2019 12:45:00', 'SBGR', 'EGLL'))
		alabels = np.arange(len(labels))
		
		# plt.bar(alabels, values, align='center', alpha=0.5)
		# plt.xticks(alabels, labels)
		# plt.ylabel('Probability of On-Time Arrival')
		# plt.ylim((0.0, 1.0))
		return values
	except Exception as e:
		print(e)
		
if __name__ == "__main__":
    main()