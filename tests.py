import pymongo
import pprint

print('Работаем')
client = pymongo.MongoClient("mongodb+srv://edik:4321@main.jdg9e.mongodb.net/main?retryWrites=true&w=majority")
print('подключился')
db = client.ntk
q = []
who = 662587491
db.user.delete_many({'id':1})
for i in db.user.find({}):
    k = (i['id'], i['score'], i['name'], i['last_name'])
    q.append(k)
q.sort(key=lambda x: x[1],reverse=True)
for i in q:
    if who == i[0]:
        print(q.index(i))
        break
print(q)