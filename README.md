# 自动打包上传脚本
集成iOS项目打包、上传分发平台，发送邮件等功能，让你彻底脱离纷繁复杂的Archive，下一步，确定操作，解放你的双手，成就你的梦想~~
## 使用

### setp1：克隆项目
将你要打包的项目clone一份，放到跟uploader.py同一级目录下即可

### step2：  配置
主要就是两个文件，uploader.py和config.json，还有一个export文件，那是xcode输出ipa的配置文件。

你所有需要配置的内容都可以在config.json里找到，填上你自己的配置：

```
{
  "BaseConfig": {
    "Project_Name":"项目名",   #项目名
    "Directory_Name":"目录", #打包项目的目录
    "Configuration": "Debug",   #不解释了
    "Email_From": "mayun@taobao.com", #发件人
    "Email_Password": "wojiushiyouqian", #密码
    "Email_To": "mahuatent@qq.com", #收件人
    "Email_Smtp": "smtp.mxhichina.com"  #发件服务器
  },
  "MessageConfig": {  #短信配置
    "AppKey": "123456789",   
    "AppSecret": "123456789",
    "Mobiles": ["123456789"],
    "TemplateID" : "1278"
  },
  "Fir_Token": "123456789"   #内测分发平台token
}

```

### setp3：运行脚本
  python uploader.py
会出现四个选项任你选:

``` shell
-------Please define Build Configuration Mode:-----------
1.Debug, Upload     ##debug模式打包，上传
2.Release, Upload)    ##release模式打包，上传
3.Release, Not Upload)  ##release模式打包，不上传
4.Upload, Not Build   ##只上传，不打包
Configuration:
```

选完以后就开始打包了，如果之前选择了上传分发平台，打包完成后会让你输入change log，可以回车直接跳过。

上传完成后会给config里的发件人发一封邮件，内容包括change log和下载地址。

就酱啦~~

## 多两句废话
- 曾经想到过要加上短信功能，但考虑到短信服务商太多，各家的策略都不同，无法一一兼容，想要加入的童鞋可以参考`sendMessage(changlog)函数，里面有调阿里云sdk跟网易云信api的代码。
- 分发平台各家公司国内用的最多的就是fir跟蒲公英，用法都差不多，这个根据需要稍微改一下代码就好。
- 如果有新加入的设备请先用xcode手动打包一遍，因为用命令行打包不会更新provisioning文件，会导致新设备无法下载。
- 该脚本参考了[ipapy](https://github.com/hades0918/ipapy)