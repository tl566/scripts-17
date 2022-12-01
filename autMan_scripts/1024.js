//[rule: 1024A]
const random = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
const urlt = "https://yj2207.com/";
const data = [ { "name": "丝袜", "id": "21" }];
// const data = [{ "name": "街拍", "id": "49" },{ "name": "写真", "id": "14" }, { "name": "自拍", "id": "15" }, { "name": "露出", "id": "16" }, { "name": "街拍", "id": "49" }, { "name": "丝袜", "id": "21" }, { "name": "欧美", "id": "114" },];
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
    _list.map(item => {
        sendText(item)
    })
    })
    
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