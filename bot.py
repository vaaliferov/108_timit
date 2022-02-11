import random
import soundfile
import numpy as np
import pandas as pd
import telegram.ext
from secret import *

user_last_idx = {}
df = pd.read_csv('timit/spkrinfo.csv')
df['age'] = df['age'].astype(int)
df['num'] = df.groupby('age')['age'].transform('count')
df['prob'] = 1 / len(df['age'].unique()) / df['num']

def handle_text(update, context):
    user = update.message.from_user
    
    if user['id'] in user_last_idx:
        idx = user_last_idx[user['id']]
        sex, age = df.loc[idx, ['sex','age']]
        context.bot.send_message(user['id'], f'{sex}, {int(age)}')
    
    # idx = random.randint(0, len(df) - 1)
    # idx = np.random.choice(df.index, 1, p=df['prob'])[0]
    age = random.choice(df['age'].unique())
    idx = random.choice(df[df['age'] == age].index)
    path = 'timit/' + df.loc[idx, 'audio']
    
    with open(path, 'rb') as fd:
        context.bot.send_audio(user['id'], fd)
        
    if user['id'] != TG_BOT_OWNER_ID:
        msg = f"@{user['username']} {user['id']}"
        context.bot.send_message(TG_BOT_OWNER_ID, msg)
    
    user_last_idx[user['id']] = idx

f = telegram.ext.Filters.text
h = telegram.ext.MessageHandler
u = telegram.ext.Updater(TG_BOT_TOKEN)
u.dispatcher.add_handler(h(f, handle_text))
u.start_polling(); u.idle()