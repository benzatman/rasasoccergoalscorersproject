from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import gspread


scope = ['https://www.googlapis.com/feeds','https://www.googlapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

gc = gspread.service_account(filename="primordial-veld-328114-15112a3eb6b2.json")
sheet = gc.open("2020/21 pl goalscorers").sheet1

data = sheet.get_all_records()
df=pd.DataFrame(data)



class ActionNumGoals(Action):

    def name(self) -> Text:
         return "action_num_goals"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        def getPlayer():
            player = tracker.get_slot("player")
            if player[0].isupper():
                return player
            else:
                player = player.split(" ")
                for i in range(len(player)):
                    player[i] = player[i][0].upper() + player[i][1:]
                player = (" ").join(player)
                return player


        def scoredx():
            for a in range(len(df)):
                if getPlayer() == df.loc[a]["Player"]:
                    goals = df.loc[a]["Goals (Penalty)"]
                    return goals
            return False
        if scoredx()== False:
            msg= f"{getPlayer()} was not a player in the PL last season or you misspelled his name"
            dispatcher.utter_message(text=msg)
        else:
            msg= f"{getPlayer()} scored {scoredx()} goals in the 2020/21 pl season"
            dispatcher.utter_message(text=msg)
        return []

