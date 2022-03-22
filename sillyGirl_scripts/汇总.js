// [rule: 彩虹屁]
// [rule: 快手热搜榜]
// [rule: 微博热搜榜]
// [rule: 新闻热榜]
// [rule: 网易云热评]
// [rule: 历史上的今天]
// [rule: 笑话]
// [rule: 壁纸]
// [rule: 每日一图]
// [rule: 每日一言]
// [rule: 每日必看]
// [rule: 诗词]
// [rule: 线报]
// [rule: ^(.*)日记(.*)$]
// [rule: 汇总菜单]
/* 
* @author : onz3v
* updateTime : 2022-03-22
* content : 汇总一下常用脚本，根据需求自己增删
*/
if(GetContent() == "汇总菜单"){
	var n = `------------------------------\n`;
	n+="----------汇总菜单----------\n";
	var g = ['彩虹屁', '快手热搜榜', '微博热搜榜', '新闻热榜', '网易云热评', '历史上的今天', '笑话', '壁纸', '每日一图','每日一言','诗词','线报','舔狗日记'];
	g.map((item)=>{n+=item+"\n"});
	n+=`------------------------------`;
	sendText(n)
}else{
	totalClass();
}

function totalClass(){
	var input = GetContent();
	switch(input){
		case '彩虹屁':
			sendText(request('http://xiaobai.klizi.cn/API/other/chp.php'));
			break;
		case '快手热搜榜':
			sendText(request('http://xiaobai.klizi.cn/API/other/ks_rm.php'));
			break;
		case '微博热搜榜':
			sendText(request('http://xiaobai.klizi.cn/API/other/wb.php'));
			break;
		case '新闻热榜':
			sendText(request('http://xiaobai.klizi.cn/API/other/xw.php'));
			break;
		case '网易云热评':
			sendText(request('http://xiaobai.klizi.cn/API/other/wyrp.php'));
			break;
		case '历史上的今天':
			sendText(request("http://xiaobai.klizi.cn/API/other/ls.php"));
			break;
		case '笑话':
			sendText(request('http://xiaobai.klizi.cn/API/other/sjxh.php'));
			break;
		case '诗词':
			sendText(request('http://xiaobai.klizi.cn/API/other/sjsc.php'));
			break;
		case '每日一言':
			sendText(request('http://xiaobai.klizi.cn/API/other/yy.php'));
			break;
		case '每日必看':
			DAILY60S();
			break;
		case '壁纸':
			sendImage(request('http://xiaobai.klizi.cn/API/img/sjbz.php'));
			break;
		case '每日一图':
			sendImage(request('http://xiaobai.klizi.cn/API/other/bing.php'));
			break;
		case '线报':
			TIPOFF();
			break;
		default :
			sendText(request('http://xiaobai.klizi.cn/API/other/tgrj.php'));
			break;
	}
}
function DAILY60S(){
	var res = request('https://api.iyk0.com/60s');
	var data = res["imageUrl"];
	sendText(data);
}
//线报处理
function TIPOFF(){
	var info = ""
	request(`http://xiaobai.klizi.cn/API/other/xb.php`, function(err, resp, body){
		if(!err && resp.statusCode == 200){
			body = JSON.parse(body)
			var res = body["data"]
			info += "标题：" + res["title"] + "\n"+
					"类型：" + res["type"] + "\n"+
					"规则：" + res["rule"] + "\n"+
					"提示：" + res["Introduction"] + "\n"+
					"来源：" + res["manner"] + "\n"
			sendText(info);
			var imgs = res["Picture"];
			imgs.map((item)=>{
				sendImage(item);
			})
		}
	})
}