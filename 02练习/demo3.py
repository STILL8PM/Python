from pyecharts import Bar
bar = Bar("完成率", "（%)")
bar.add("2021Q4", ["唯品会-洗护","拼多多","京东POP+拼购","薄薄芯旗舰店","京东自营-纸尿裤","猫超-纸尿裤", "五羊旗舰店","业务拓展事业部","唯品会-纸尿裤","孕康专卖店"], [75,74,73,58,57,51,48,46,45,44])
bar.render("bar.html")
