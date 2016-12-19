# -*- coding: utf-8 -*-

#######################################
##contact: https://vk.com/id27919760 ##
#######################################

import vk_api
import time
import pickle
import sys
import traceback
from antigate import AntiGate
import urllib

import settings

def chunks(lst, chunk_size):
	return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def usemethod(api,method,values,gate):
	if True:
		if True:
			try:
				api.method(method,values)
			except vk_api.Captcha as error:
				print u'//oh shit,captcha'
				if settings.detour:
					print u'//timer unlock'
					time.sleep(60)
					try:
						api.method(method,values)
					except vk_api.Captcha as error:
						if settings.use_antigate:
							urllib.urlretrieve(error.get_url(), "captcha.jpg")
						print u'//надо вводить в ручную'
						print u'//разгадка капчи:\n//ссылка на картинку: ' + error.get_url()
						if settings.use_antigate:
							captcha_code = gate.get(gate.send('captcha.jpg'))
							print u'//response: ' + captcha_code
						else:
							captcha_code = raw_input('//response: ')
						try:
							error.try_again(captcha_code)
						except:
							print u'//ты ее наверно не так ввел,пропускаем пользователя'
							pass
					except:
						print u'//автор криворукий мудила,неизвестная ошибка'
						traceback.print_exc()
						pass
				else:
					try:
						api.method(method,values)
					except vk_api.Captcha as error:
						if settings.use_antigate:
							urllib.urlretrieve(error.get_url(), "captcha.jpg")
						print u'//надо вводить в ручную'
						print u'//разгадка капчи:\n//ссылка на картинку: ' + error.get_url()
						if settings.use_antigate:
							captcha_code = gate.get(gate.send('captcha.jpg'))
							print u'//response: ' + captcha_code
						else:
							captcha_code = raw_input('//response: ')
						try:
							error.try_again(captcha_code)
						except:
							print u'//ты ее наверно не так ввел,пропускаем пользователя'
							pass
					except:
						print u'//автор криворукий мудила,неизвестная ошибка'
						traceback.print_exc()
						pass
			except:
				print u'//автор криворукий мудила,неизвестная ошибка'
				traceback.print_exc()
				pass

def main(login,password):
	api = vk_api.VkApi(login,password)
	api.authorization()
#######################################
	if settings.use_antigate:
		gate = AntiGate(settings.key_antigate)
		try:
			print gate.balance()
		except ValueError:
			print u'ag ключ не валидный'
			return
	else:
		gate = None
#######################################
	response = api.method('groups.getById',{'group_ids':settings.good_group.split('/')[3]})
	banan_allow = True
	if response[0]['is_admin'] == 0:
		print u'ты не владеешь привелегиями в своей группе'
		banan_allow = False
		while raw_input('//exit?? (y/n) ').lower() == 'y':
			return
		
	settings.good_group = response[0]['id']
	settings.bad_group = api.method('groups.getById',{'group_ids':settings.bad_group.split('/')[3]})[0]['id']
#######################################
	members = []
	
	response = api.method('groups.getMembers',{'group_id':settings.good_group,'count':1})
	print u'Получено пользователей твоей группы:'
	while len(members) < response['count'] and not settings.use_dump:
		members += api.method('groups.getMembers',{'group_id':settings.good_group,'offset':len(members)})['items']
		print len(members)
	
	if settings.use_dump:
		members = pickle.load(open(settings.dump_file,'r'))
	else:
		pizda = open(settings.dump_file,'w')
		pickle.dump(members,pizda)
		pizda.close()
	print u'все пользователи получены'
#######################################
	if not banan_allow:
		print u'режим бана всех,переменуй базы'
		return
	bad_members = []
	print u'\n\nполучение подписчиков которые подписались на плохой пабос'

	if not settings.use_dump_bad:
		members_chunks = chunks(members,500)
		if not settings.ggf:
			for memblist in members_chunks:
				user_ids = str(memblist)[1:]
				response = api.method('groups.isMember',{'group_id':settings.bad_group,'user_ids':user_ids})
				print u'wait......'
				for user in response:
					if user['member'] == 1:
						bad_members.append(user['user_id'])
		else:
			code = u'var members = [];\n'
			response = []
			i = 0
			j = 0
			while i < len(members_chunks):
				code += 'members = members + API.groups.isMember({"group_id":' + str(settings.bad_group) +',"user_ids":"' + str(members_chunks[i])[1:] +'"});\n'
				i += 1
				j += 1
				if j == 10:
					code += u'return members;'
					print u'wait......'
					response += api.method('execute',{'code':code})
					code = u'var members = [];\n'
					j = 0
			code += u'return members;'
			#print code
			print u'wait......'
			response += api.method('execute',{'code':code})
			for user in response:
				if user['member'] == 1:
					bad_members.append(user['user_id'])
			
	if settings.use_dump_bad:
		bad_members = pickle.load(open(settings.dump_bad_file,'r'))
	else:
		pizda = open(settings.dump_bad_file,'w')
		pickle.dump(bad_members,pizda)
		pizda.close()
	print u'все пользователи получены'
	print str(len(bad_members))+'/'+str(len(members)) + '     Это ' + str(round(len(bad_members)*100/len(members))) + '% из общего числа'
#######################################
	print u'\n\nбан пользователей'
	banned_users = []
	if not settings.more_bans:
		i = 0
		for user_id in bad_members:
			values = {
				'group_id':settings.good_group,
				'user_id':user_id,
				'reason':0,
				'comment':settings.comment,
				'comment_visible':settings.comment_visible
				}
			if not settings.forever:
				values.update({'end_date':settings.end_date})
			usemethod(api,'groups.banUser',values,gate)
			banned_users.append(user_id)
			print user_id
			i += 1
			print u'забанено ' + str(i) + u'/' + str(len(bad_members))
	else:
		code = u''
		i = 0
		j = 0
		while i < len(bad_members):
			print bad_members[i]
			values = u'"group_id":' + str(settings.good_group)+u',"user_id":'+str(bad_members[i])+u',"reason":0,"comment":"'+str(settings.comment)+u'","comment_visible":'+str(settings.comment_visible)
			if not settings.forever:
				values += u',"end_date":' + str(settings.end_date)
			code += u'API.groups.banUser({'+ values +'});\n'
			i += 1
			j += 1
			if j == 15:
				code += u'return [1];'
				usemethod(api,'execute',{'code':code},gate)
				j = 0
				code = u''
			print u'забанено ' + str(i) + u'/' + str(len(bad_members))
		code += u'return [1];'
		usemethod(api,'execute',{'code':code},gate)
	print u'end......'
						

if __name__ == '__main__':
	settings.good_group = sys.argv[3]
	settings.bad_group = sys.argv[4]
	settings.comment_visible = 1
	timeparm = int(sys.argv[5])
	if timeparm == 0:
		settings.forever = True
	else:
		settings.forever = False
		settings.mesyacev = timeparm
	main(sys.argv[1],sys.argv[2])