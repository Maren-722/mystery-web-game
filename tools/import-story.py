"""Import the earlier account writing pack into the captain's data schema.
Run with an explicit path to the writing pack's src/content.json.
The generated src/data files are the editable source of truth afterwards.
"""
import json
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
data=root/'src/data'
seed=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
ids={'chen':'chenguisheng','zhang':'zhangjianguo','gui':'zhangguixiang','li':'liming','wang':'wangzhiqiang','night':'chennian'}
def adapt(text):
    return text.replace('王桂英','张桂香').replace('桂英','桂香').replace('夜行者','夜归人').replace('桂英凉面','张阿姨凉面')
shops={'chen':('陈记糖粥藕','A1'),'zhang':('张记卤味','B1'),'gui':('张阿姨凉面','A2'),'li':('小李炒粉','B2'),'wang':('南桥夜市管理处',''),'night':('夜归人','')}
accounts={}
for a in seed['accounts']:
    key=ids[a['id']]
    display=adapt(a['name'])
    shop,no=shops[a['id']]
    aliases=[display,shop]+[adapt(s) for s in a['aliases'] if s not in ['王桂英','桂英','桂英凉面']]
    if a['id']=='gui': aliases+=['张阿姨','桂香']
    if a['id']=='night': aliases=['夜归人','夜行者']
    accounts[key]=dict(displayName=display,password='1010' if a['id']=='li' else a['password'],shopName=shop,stallNo=no,role='manager' if a['id']=='wang' else 'customer' if a['id']=='night' else 'merchant',aliases=list(dict.fromkeys(aliases)),intro=adapt(a['intro']))

threads=[]
for t in seed['threads']:
    threads.append(dict(id=t['id'],participants=[ids[i] for i in t['participants']],messages=[dict(id=m['id'],fromId=ids[m['sender']],at=m['at'],content=adapt(m['text']),evidenceId=m['evidence']) for m in t['messages']]))
notes=[dict(id=n['id'],accountId=ids[n['accountId']],at=n['at'],title=n['title'],content=adapt(n['body']),evidenceId=n['evidence'],kind=n['kind']) for n in seed['notes']]
for n in notes:
    if n['id']=='N-C01': n['content']=n['content'].replace('今天从医院回来，买了这个。','今天从医院回来，买了这个。报告上写着肺癌晚期。')
    if n['id']=='N-C07':
        n['title']='给念儿的'
        n['content']='念儿，这两天总能看见你在论坛问。我打了“明天别来”，又删了。你又没有做错什么。爹找了二十八年，真等你到了跟前，又不晓得怎么开口。等我能自己下楼了，再去给你煨一锅藕。'
    if n['id']=='N-W03':
        n['content']=n['content'].replace('在南桥夜市报失','在江边老摊区报失').replace('旧记录当年未在论坛公开。','江边老摊区在2008年集中挂牌为南桥夜市，这份旧档案随陈记一起迁入。旧记录当年未在论坛公开。')
    if n['id']=='N-W04': n['content']=n['content'].replace('他们到底有什么事','旧档案里的孩子我知道，可这个年轻人跟他到底有什么关系')

clues=[dict(id=c['id'],label=adapt(c['label']),sourceId=c['source']) for c in seed['clues']]
endings={
 'A':dict(title='他等到了',content='你把住院地址发给夜归人。他隔了很久才回：“谢谢。我现在过去。”\n\n陈念在病房门口站了一会儿。陈伯抬起头，先问他吃了没有。那天以后，床头多了一只保温桶。\n\n第二年春天，陈记糖粥藕的摊位又支起来了。年轻摊主用右手握着长柄勺，给新来的客人盛粥。'),
 'B':dict(title='有些话没能当面说',content='你把输入框里的地址删掉了。论坛那条询问仍留在那里，夜归人每天来看一次。\n\n几天后，王主任还是给他发去了一条消息。那张旧纸条终于有了回音，只是有些话再也没能当面问。\n\n开春以后，张记卤味旁边的灯还会亮着。有人走过，会往锁着的粥摊看一眼。')
}

stalls=json.loads((data/'stalls.json').read_text(encoding='utf-8'))
key_stalls={'chenji':'chenguisheng','laozhang':'zhangjianguo','zhangayi':'zhangguixiang','xiaoli':'liming'}
review_map={
 'chenji':[
 ('老顾客','10月5日','吃了十年的味道，陈叔还是会记得我不吃太甜。'),
 ('桥下散步','10月14日','昨晚来才看见暂停营业。隔壁张老板嘴上总跟他吵，今天却帮他把门口扫了。'),
 ('小碗不加糖','10月8日','老板看见我换手拿勺子，给换了把长柄的。粥很热，坐了一会儿才走。')],
 'laozhang':[
 ('买菜回家','3月18日','三月十八撞上老板两口子结婚纪念日，老板给加了两只卤蛋。'),
 ('张记卤味','3月19日','那天没记错。我后台也用这个纪念日，四位月日，省得忘了。'),
 ('夜班司机','10月11日','陈记和张记隔着吵，吵完陈叔照样把晚饭端过来。')],
 'zhangayi':[
 ('隔壁班家长','6月12日','六月十二来扑了空，张阿姨给高三的儿子过生日去了。'),
 ('张阿姨凉面','6月13日','一年就那一天早收。我商户密码也是孩子生日，四位月日，好记。'),
 ('少加醋','10月10日','阿姨昨天上午没出摊，说陪邻居去复诊，晚上才摆出来。')],
 'xiaoli':[
 ('开业就来过','10月10日','去年十月十日开的张，今天正好一周年。还记得第一天每桌都加了蛋。'),
 ('小李炒粉','10月11日','谢谢老客。我后台密码一直就是开张那天，四位月日。'),
 ('凌晨下班','10月16日','一点多路过还看他擦陈记的桌子。小李说只是顺手，没收钱。')],
 'zhaoji':[('早到的客人','10月18日','荠菜馄饨清爽。老板说江边的风大，碗得捧紧。')],
 'zhenjie':[('晚自习之后','10月20日','水果切得新鲜，不加酸奶也好吃。')],
 'wangji':[('三人一桌','10月19日','开业折扣算清楚了，茄子记得少放蒜。')],
 'awei':[('加两个蛋','10月17日','收摊前来还能买到，酱料自己选。')],
 'liujie':[('无辣不欢','10月17日','新藕片脆。刘姐说带货的老伙计歇几天，下一批得自己去挑。')],
 'aqiang':[('路过江边','10月21日','外皮酥，阿强提醒蘸水很辣。')],
}
for s in stalls:
    s.pop('notes',None)
    if s['id'] in key_stalls: s['accountId']=key_stalls[s['id']]
    s['price']=f"{min(d['price'] for d in s['dishes'])}元起"
    s['reviews']=[dict(user=u,date=d,content=c) for u,d,c in review_map[s['id']]]
order=['chenji','laozhang','xiaoli','zhangayi']
stalls.sort(key=lambda s:order.index(s['id']) if s['id'] in order else 4)

posts=[]
def post(pid,title,author,at,content,comments,authorId=''):
    posts.append(dict(id=pid,title=title,author=author,authorId=authorId,at='2026-'+at,date=at.replace('-','月',1).split(' ')[0]+'日',preview=content[:70],content=content,comments=[dict(id=f'{pid}-c{i+1}',user=u,date=d,content=c) for i,(u,d,c) in enumerate(comments)]))
post('p1','请问陈叔什么时候回来？','夜归人','10-13 18:20','我从外地来的，最近晚上总来喝粥。昨晚到的时候门已经关了，今天也没开。公告说临时休息，有人知道大概多久吗？',[('爱吃卤味','10月13日','你比老顾客还急，问问管理处吧。'),('张记卤味','10月13日','别瞎猜，老陈有事。')],'chennian')
post('p2','听说陈伯欠账跑路了？','夜猫子','10-14 20:12','有人说陈伯这半年到处借账，连着停了两天也没见人。我也是听别人说的，有没有清楚的？',[('小李炒粉','10月14日','别瞎说，陈叔不是那种人。'),('江边走走','10月15日','“听别人说”不能当真，别传了。')])
post('p3','那晚我看见老张拉了陈伯一把','路过的猫','10-15 17:36','10月12号晚上九点多，我隔着马路看见老张拉陈伯袖子，两个人说话声音很大。后来人多挡住了，我没看清。',[('张记卤味','10月15日','我们的事，没动手。'),('夜班司机','10月16日','我后来看见陈师傅自己拎包上车了。车往哪儿开没注意。')])
post('p4','小李每天半夜还在陈记门口？','凌晨一点','10-16 01:36','下班路过，陈记没开，小李却在里面擦桌子。之前不是有人说他急用钱，翻过陈叔的钱箱吗？',[('小李炒粉','10月16日','那是三年前的事，钱我记着。现在只是帮着收拾。'),('张阿姨凉面','10月16日','桌子总要有人擦，别什么都往坏处想。')])
post('p5','隔壁那篇说脸色不对的帖子怎么没了','不太辣','10-17 19:03','前几天张阿姨发过陈叔脸色不好的帖子，后来找不到了。是人没事了，还是不想大家问？',[('张阿姨凉面','10月17日','删了是不想吵架。大家好好吃饭。'),('少加醋','10月17日','那天评论越说越难听，阿姨删得对。')])
post('p6','管理处有没有陈叔的联系方式','夜归人','10-18 08:52','我不是催他开门，就是有点事想当面问。私信了管理处，还在等回复。',[('江边走走','10月18日','管理处账号叫wangzhiqiang，公开履历在首页公告里。'),('夜归人','10月18日','谢谢，已经发了。')],'chennian')
post('p7','网站又把我登出去了','小李炒粉','10-20 16:42','忙完才发现后台没登录。我就一个商户账号，liming。好在密码还是开张那四个数，不然又得跑管理处。',[('张记卤味','10月20日','我zhangjianguo也没登上，后来发现把纪念日输成年份了。'),('张阿姨凉面','10月20日','我的zhangguixiang是孩子生日的月日，不用年份。')],'liming')
post('p8','想找个人，又不知道该不该问','夜归人','10-22 00:18','一个人找了很久。真到了他面前，又觉得只问一句“认不认识我”也太重了。万一他只想安安静静做生意呢。',[('桥下散步','10月22日','先坐下喝碗粥。愿意说的时候再说。'),('夜归人','10月22日','现在粥摊也不开了。')],'chennian')
post('p9','你们都怎么记住账号密码的','加蛋不加葱','10-23 21:04','买东西能记住，密码就是记不住。手机换了以后，一个个重新登录太麻烦。',[('夜归人','10月23日','我用夜归人这个ID。密码一直用钱包里那张旧纸条背面的八位数字，换手机也没改过。'),('加蛋不加葱','10月23日','纸条收好，丢了可真找不回。')])
post('p10','求一份少辣夜宵名单','晚自习之后','10-24 20:10','室友吃不了辣，我们准备从馄饨开始，再买水果捞。还有什么可以点？',[('珍姐水果捞','10月24日','酸奶可以另装。'),('赵记馄饨','10月24日','胡椒也能不放，来时说一声。')])
post('p11','老夜市到底是从哪一年开始的','桥下散步','10-25 17:15','小时候跟家里人来江边，摊子还没有现在这么整齐。看官网写挂牌18年，怎么老照片更早？',[('南桥夜市管理处','10月25日','江边便民摊区更早就有，2008年集中挂牌叫南桥夜市。老摊主的纸档也一起迁过来了。'),('张记卤味','10月25日','陈记来的比我还早。那会儿他孩子还小。')])
post('p12','都说他有事，可没人告诉我去了哪里','夜归人','10-28 00:08','问了好几个人，都叫我等等。我已经等了半个月。是不是不该再找了？',[('夜归人','10月28日','如果有人真的知道他在哪，能不能私信我。只告诉我地址就好。'),('桥下散步','10月28日','看见了。希望你能找到他。')],'chennian')
post('p13','江边风大，别把收款牌放桌沿','阿伟烤冷面','10-26 17:42','昨晚收款牌被吹进了隔壁盆里，没坏，字糊了一半。今天重新打印，谁有塑封袋借我一个？',[('珍姐水果捞','10月26日','我有，开摊过来拿。'),('阿伟烤冷面','10月26日','谢谢，给你留份少酱的。')])
post('p14','翻出一张以前江边的合影','桥下散步','10-27 12:11','搬家找到以前的胶卷照片，摊位还支在桥边。陈师傅站在锅边，后头一排人。想洗一张送他，等他回来再说吧。',[('张记卤味','10月27日','先收好，别往网上发他家里人的照片。'),('桥下散步','10月27日','晓得，没上传。')])
post('p15','半夜还亮灯的摊位能不能收进导览','夜班司机','10-27 23:02','我们下夜班不一定赶得上营业时间。大家几点收，最好在导览里写一写，免得白跑。',[('小李炒粉','10月27日','我炒到十二点半，有时帮隔壁收桌子，会晚点走。'),('刘姐麻辣烫','10月27日','我十一点半就关火了，不要跑空。')])

manifest=[
 dict(accountId='liming',sourceType='stall',sourceId='xiaoli',rule='四位月日',password='1010'),
 dict(accountId='zhangjianguo',sourceType='stall',sourceId='laozhang',rule='四位月日',password='0318'),
 dict(accountId='zhangguixiang',sourceType='stall',sourceId='zhangayi',rule='四位月日',password='0612'),
 dict(accountId='wangzhiqiang',sourceType='notice',sourceId='management',rule='八位年月日',password='20180901'),
 dict(accountId='chenguisheng',sourceType='note',sourceId='N-W03',rule='旧档案日期',password='19980716'),
 dict(accountId='chennian',sourceType='note-and-post',sourceId='N-C04',postId='p9',rule='纸条背面八位数字',password='19980716'),
]
posts.sort(key=lambda p:p['at'])
for filename,obj in [('accounts.json',accounts),('messages.json',threads),('notes.json',notes),('clues.json',clues),('endings.json',endings),('stalls.json',stalls),('posts.json',posts),('puzzle-clues.json',manifest)]:
    (data/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Imported {len(accounts)} accounts, {len(threads)} conversations, {len(notes)} notes, {len(posts)} posts')
