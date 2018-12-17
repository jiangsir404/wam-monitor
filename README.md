## wam-monitor
之前捣鼓了半天创宇的wam, 没明白怎么弄，干脆自己写一个简单的版本，可以实现对github以及一些开源cms官网的更新页面进行监控并发邮件通知。

借鉴了蘑菇街的github监控工具[GSIL](https://github.com/FeeiCN/GSIL)  的思路和部分代码，感谢！

## INSTALL

	pip install -r requirement.txt

修改config.ini的邮箱信息

```
[mail]
host : smtp.163.com
port : 25
mails : xxx@163.com
from : WAM
password : password
to : xx@qq.com,xx@163.com
cc : 
```

需要两个邮箱, mails是发件人邮箱，to是接收人邮箱，cc是抄送邮箱可不填

rules.ini 为监控规则, 格式如下
```
{
	"github":{
		"ggffgg":{
			"url":"https://github.com/ggffgg123/ggffgg/commits/master",
			"message":"这只是一个测试repo, 正式监控请删除该条记录"
			'selector":"div.repository-content"
		}
	}
}
```

url: 监控的页面链接
selector: 监控某个标签的内容，因为很多cms官网页面都有动态的css,js，如果直接监控整个页面没有效果，因此如果页面为动态页面，需要添加
selector 来监控某一个标签的内容。 目前支持两种标签:
```
div.download 表示监控: <div class="download"></div> 的内容
ol#down 表示监控 <ol id="down"></div> 的内容
```

message: 发送邮件的主题，默认可以不填写。

> 三个属性中url是必填，message可不填，selector可不填，github默认selector为repository-content,app默认selector为None,即只监控静态页面。 


## 功能
- [x] 监控github commit 信息
- [x] 监控cms官网 版本更新
- [x] 邮件通知
- [x] 现在可监控13个cms的更新

## 功能截图
![](1.jpg)