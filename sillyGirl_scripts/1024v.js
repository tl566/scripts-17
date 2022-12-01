/**
 * @title 1024视频
 * @create_at 2022-09-17 10:23:12
 * @rule 1024视频
 * @rule h视频
 * @description 原作者 小良 JSBOX。
 * @author onz3v
 * @public true
 * @version v1.0.1
 */

const random = (min, max) => Math.floor(Math.random() * (max - min + 1) + min);
const urlt = "https://gongdishaonv235.top";
const data = [{ "name": "国产", "id": "1" }, { "name": "无码", "id": "13" }, { "name": "欧美", "id": "6" }, { "name": "三级", "id": "4" }, { "name": "动漫", "id": "14" }]
const $ = sender
let id = data[random(0, data.length - 1)]['id'], pg = random(0, 10);
getList()
function getList() {
    let _url = urlt + "/index.php/vod/type/id/" + id + "/page/" + pg + ".html";
    let _data = []
    $.reply('加载中...')
    let resp = request(_url)
    var text = resp.body.replace(/\n|\s|\r/g, "")
    var list = text.match(/<h2class=\"f-15rows-2mt10\">(\S*?)<\/h2>/g)
    list.map(item => {
        if (item.indexOf('href=') !== -1) {
            var name = item.match(/title=\"(\S*?)\"/)[1]
            var id = item.match(/detail\/id\/(\S*?)\.html/)[1]
            _data.push({ name, id })
        }
    })
    let path = _data[random(0, _data.length - 1)]
    getVideo(path)
}

function getVideo(path) {
    let { name, id } = path;
    console.log(urlt + "/index.php/vod/play/id/" + id + "/sid/1/nid/1.html")
    let resp = request(urlt + "/index.php/vod/play/id/" + id + "/sid/1/nid/1.html")
    var text = resp.body.replace(/\n|\s|\r/g, "")
    var video = text.match(/<divclass=\"video-tips\">(\S*?)<\/script>/)[1]
    var vurl = video.match(/url\":\"(\S*?)\"/)[1]
    vurl = vurl.replace(/\\/g, "")
    console.log(vurl)
    $.reply('由于傻妞不支持安装ckplay等解析m3u8之类的插件，故你需要自己去解析一下。\nPC用potplayer\niOS用影音包、aplayer、nplayer...\n安卓自己去扒拉扒拉吧')
    sleep(100)
    $.reply(name + '\n' + vurl)

}
