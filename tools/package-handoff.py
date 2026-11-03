"""Create review artifacts without Git metadata, dependencies, or test runtime data."""
import json
from pathlib import Path
from html import escape
from zipfile import ZipFile, ZIP_DEFLATED

root=Path(__file__).resolve().parents[1]
out=root.parent/'完善交付'
out.mkdir(exist_ok=True)
report=(root/'完善说明.txt').read_text(encoding='utf-8')
parts=[]
for line in report.splitlines():
    if not line.strip():continue
    tag='h1' if line=='南桥夜市网站检查与完善说明' else 'h2' if line[0] in '一二三四五六' and ' ' in line and len(line)<30 else 'p'
    parts.append(f'<{tag}>{escape(line)}</{tag}>')
(out/'完善清单与合并说明.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>南桥夜市网站完善清单</title><style>body{max-width:900px;margin:48px auto;padding:0 24px;font:16px/1.9 "Microsoft YaHei",sans-serif;color:#30251d;background:#faf7f2}h1{font-size:29px}h2{font-size:23px;margin-top:40px}p{margin:12px 0;overflow-wrap:anywhere}@media print{body{background:white;margin:0;font-size:11pt}h2{break-after:avoid}}</style>'+''.join(parts)+'</html>',encoding='utf-8')

accounts=json.loads((root/'src/data/accounts.json').read_text(encoding='utf-8'))
clues=json.loads((root/'src/data/puzzle-clues.json').read_text(encoding='utf-8'))
walk=['开发验收与密码表 含剧透','建议先盲测，再使用本表核对。所有账号均为游戏虚构。','']
for id,a in accounts.items():
    c=next(c for c in clues if c['accountId']==id)
    walk.append(f"{a['displayName']}  ID {id}  密码 {a['password']}  前置 {c['sourceId']}")
walk+=['','完整推荐路线','1 浏览首页公告、商户评价和论坛。先用李明1010、张建国0318、张桂香0612读取普通摊主私信和手记，解释传闻。','2 从管理处公开资料得知ID与2018年9月1日到岗日期，按八位年月日登录王志强20180901。','3 阅读临时停业登记获得EV_HOSPITAL，阅读陈记旧档案获得EV_LOST_DATE，并推导陈桂生19980716。','4 登录陈桂生，阅读7篇手记，尤其纸条、认出手指和给念儿的，发现父亲已经认出年轻人。','5 结合论坛p9的纸条密码习惯，用夜归人19980716登录，阅读没有发出的私信获得EV_IDENTITY。','6 三条关键证据齐全，在夜归人手记页选择A或B。回看手记可以重选，重新开始会清除本机调查和发帖评论。','','构建包说明','南桥夜市构建文件.zip中包含nanqiao-night-market目录，该目录应挂载在HTTP服务的/nanqiao-night-market/路径。双击index.html不会加载hash路由应用的模块资源。当前GitHub Actions会自行生成dist，不需要手工把构建包提交进源码。']
(out/'开发验收与密码表.txt').write_text('\n'.join(walk),encoding='utf-8-sig')

source=out/'南桥夜市完善源码.zip'
files=[]
with ZipFile(source,'w',ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(root)
        if any(part in {'.git','node_modules','dist','__pycache__'} for part in rel.parts):continue
        if p.suffix in {'.log','.jpg','.png'}:continue
        z.write(p,Path('nanqiao-night-market')/rel)
        files.append(str(rel))
with ZipFile(out/'南桥夜市构建文件.zip','w',ZIP_DEFLATED) as z:
    for p in sorted((root/'dist').rglob('*')):
        if p.is_file():z.write(p,Path('nanqiao-night-market')/p.relative_to(root/'dist'))
with ZipFile(source) as z:
    assert z.testzip() is None
    assert any(n.endswith('src/game/state.js') for n in z.namelist())
    assert any(n.endswith('.github/workflows/deploy.yml') for n in z.namelist())
    assert not any('/node_modules/' in n or '/.git/' in n for n in z.namelist())
print(f'Packaged {len(files)} source files and verified ZIP integrity')
