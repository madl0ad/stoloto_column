import json
import requests
from time import sleep
import math
def is_column(rows): 
	for i in range(5): #проверяем по столбцам
		n1 = math.floor(rows[i]/10)		#В лучших традициях индусского программирования
		n2 = math.floor(rows[i+5]/10)	#получаем число десятков
		n3 = math.floor(rows[i+10]/10)	#в номере бочонка
		if (n1 == n2 and n2 == n3): 	#если число десятков совпало, то это столбец
			return True
	return False
	
#куки, чтобы не выделяться
cookies = {"_SI_SID_1.6befd9a02400013179aba889":"5ba17d93f02a7e37c3f7e00b.1578470963029.419623","_SI_VID_1.6befd9a02400013179aba889":"4b52fccce5855f58be77271a","adspire_uid":"AS.774056202.1578470132","flocktory-uuid":"5b715254-6663-478d-ad78-b9fecc974772-5","isgua":"false","pregen_player_id":"bcfb34e6-92e5-400c-83cf-b452259f23d4"}

#это часть скрипта обновления - он может не обновлять выбранные карточки, нам эта часть неинтересна
data = {"numbersToChange":{}}
  
#Откуда грузим
API_ENDPOINT = "https://www.stoloto.ru/service/bingo/ruslotto/take"

#десять тысяч запросов по десять карточек по два полуполя ~= 200k полуполей
for i in range(10000):
	r = requests.post(url = API_ENDPOINT, cookies = cookies, data = data) #забрать данные
	jsn = r.text #забрать ответ
	arr = json.loads(jsn) #распарсить ответ
	try:
		arr = arr["combinations"] #если в ответе нет ключа "combinations", нас поймала антиддос-защита
	except:
		print (str(i) + ":" + jsn) #выведем номер и ответ для логов
		sleep(10) #и уснем на десять секунд, чтобы её не провоцировать
		continue
	for j in arr: 	#для каждой карточки
			t = j["numbers"][:15] 				#первое полуполе
			t2 = j["numbers"][15:] 				#второе полуполе
			if (is_column(t) or is_column(t2)): #если хоть в одном есть столбец
				print("YES!" + str(j["numbers"]))
	sleep(0.1) 		#не провоцируем ddos-защиту
	if (i % 100 == 0):
		print(i)	