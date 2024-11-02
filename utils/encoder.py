import json
class sitedataEncoder(json.JSONEncoder):
    def default(self,obj):
        return {
            'urls_by_month':obj.urls_by_month,
            'characters_by_date' : obj.characters_by_date
        }