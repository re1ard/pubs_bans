# -*- coding: utf-8 -*-
import time

##################################################
#antigate
use_antigate = False
key_antigate = u''
##################################################
#линки на группу
good_group = u'https://vk.com/good'
bad_group = u'https://vk.com/bad'
##################################################
#забанить пользователя навсегда? True - да False - нет
forever = True
#если не на всегда то на сколько месяцев
mesyacev = 1
end_date = time.time() + mesyacev * 2629743
##################################################
#причина бана
comment = u'retard'
##################################################
#обход капчи ожиданием(не всегда работает)
detour = True
##################################################
#использовать execute метод при получении подписоты
ggf = True
##################################################
#использовать execute метод для бана
more_bans = True
##################################################
if not len(comment) == 0:
	comment_visible = 1
else:
	comment_visible = 0
##################################################
use_dump = False
dump_file = 'members.list'
##################################################
use_dump_bad = False
dump_bad_file = 'bad_members.list'