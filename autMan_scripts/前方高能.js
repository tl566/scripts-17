//[rule: 前方高能]
const random = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
const urlt = "https://yj2207.com/";
const data = [{ "name": "丝袜", "id": "21" }];
// const data = [{ "name": "街拍", "id": "49" },{ "name": "写真", "id": "14" }, { "name": "自拍", "id": "15" }, { "name": "露出", "id": "16" }, { "name": "街拍", "id": "49" }, { "name": "丝袜", "id": "21" }, { "name": "欧美", "id": "114" },];
// 分页参数
const pageNum = 5
let id = data[random(0, data.length - 1)]['id'], pg = random(0, 10);
getList()
function getList() {
    let _url = urlt + "pw/thread.php?fid=" + id + "&page=" + pg;
    let _data = []
    sendText('加载中...')
    request({url:_url},function(error,resp,header,body){
       var text = resp.body.replace(/\n|\s|\r/g, "")
    if (text.indexOf('普通主题') !== -1) {
        text = text.split("普通主题")[1]
    }
    var list = text.match(/class=\"tr3t_one\">(\S*?)<\/h3>/g)
    list.map(item => {
        if (item.indexOf('href=') !== -1) {
            var id = item.match(/href=\"(\S*?)\"/)[1]
            _data.push(id)
        }
    })
    let path = _data[random(0, _data.length - 1)]
    getPic(path) 
    })
}

function getPic(path) {
  request({url:urlt + "pw/" + path},function(error,resp,header,body){
    var text = resp.body.replace(/\n|\s|\r/g, "")
    var list = text.match(/<br><imgsrc=\"(\S*?)\"/g)
    var html = ""
    list.map(item => {
        var imgs = item.replace(/<br><imgsrc=\"/, "");
        var li = "<li><img src=\"" + imgs + "\"></li>";
        html += li;
    })
    let _list = getPicInHtml(html);
    let newList = sliceIntoChunks(_list, pageNum)
    let isCancel = false;
    for (let i = 0; i < newList.length; i++) {
        if (isCancel) return sendText('已取消');
        if (i == 0) { newList[i].map(item => sendText(item)) }
        else if (i == newList.length - 1) {
            newList[i].map(item => sendText(item))
            return sendText(`已加载全部`);
        } if (i > 0 && !isCancel) {
            sendText("是否继续返回剩余图片,y/Y继续，其他取消")
            var status = input(30000)
                if (status.toLowerCase() !== 'y') {
                    isCancel = true
                    return;
                }
                newList[i].map(item => sendText(item))
            if (!status) {
                return sendText("操作超时或取消，已退出。");
            }
        }
    }   
  })
   
}

function continueReply(index, data) {
    for (let i = index; i < data.length; i++) {
        sendText(data[i])
    }
}
function getPicInHtml(html) {
    let r = /<[img]+\s+(.*?)(?<id>\w*?)[\s'"](.*?)>/g
    var _s = html.match(r)
    let list = []
    if (_s) {
        _s.forEach((item) => {
            list.push(image(item.match(/src=[\'\"]?([^\'\"]*)[\'\"]?/i)[1]))
        })
    }
    return list
}

function sliceIntoChunks(arr, chunkSize) {
    const res = [];
    for (let i = 0; i < arr.length; i += chunkSize) {
        const chunk = arr.slice(i, i + chunkSize);
        res.push(chunk);
    }
    return res;
}