#### SQL布尔注入脚本

#### 依赖库
- re
- urllib
- requests

#### 实现思路
获取url，进行各种payload构造访问，判断返回值差异

#### 未改进
- 打算使用sleep休眠注入进行布尔判断[ - ]
- 闭合方式暂未自动化判断
- 没有写各种绕waf方式
- 没有使用线程，可能爆破时间缓慢，未测试
- 没有使用代理池，可能有流量检测风险
- 没有使用二分法
- 使用redis存储信息，结构清晰

#### 改进
- Check()方法未写好[ok]
- 增加布尔判断方法，暂时为页面区分和延迟区分，目前默认延迟区分[ok]
- 修改关系对象[ok]
- 后期增加选择判断方式[ok]
- 增加爬虫异步机制防堵塞[ok]
- 超时重连[ok]