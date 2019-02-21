## Intro

I'd like to make a gtd soft with multi functions, including task management, sync to calendar, time consume statistics, etc.

This soft runs at Google Cloud Platform. The Json communication func will be added to meet the requirement of mobile apps.

## Installation
In order to run this app locally, you neet to install google-cloud-sdk first.

Once installed, you can run by command:

`[path to google-cloud-sdk]/bin/dev_appserver [path to gtdcomplete]/.`

## LICENSE
Released under the MIT License

## Progressing
1. Task magagement almost done. 2017-09-13
2. Synced with Google calendar. 2017-10-17

## TODO
1. [x] 更改流程：Inbox -> 计划 -> 执行
2. [x] 添加Today选项，默认显示当天的所有计划安排和执行情况
3. [x] Today页面按照时间先后排序
4. [] 去掉默认的inbox project
5. [] 去掉New Event页面，相应的添加plan calendar的功能是否需要去掉？
6. [] 时间选择页面，是否需要改成手动输入？
7. [] collection和schedule页面需要增加删除和修改功能
8. [] bug: projects和timeCategory页面修改布局以后，查询指定范围内的已完成事件会引起accessControl页面的bug
