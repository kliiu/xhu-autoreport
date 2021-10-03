# xhu青柠疫服自动打卡（仅供学习）
采用**Python+Selenium**实现页面填报->调用**百度云api**实现验证码识别->**yagmail**模块实现自动邮件提醒

## To Start
1.pip install -r requirements.txt

2.在bd_img方法中填入 百度云APP_ID,API_KEY,SECRET_KEY(参考地址https://blog.csdn.net/htjy12338/article/details/108760416?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-5.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-5.no_search_link)

3.在sendMail方法中填入 配置好的发件邮箱以及授权码(参考地址https://blog.csdn.net/heye13/article/details/83861983)

4.run lime.py 学号 姓名 密码 邮箱  (example:run lime.py 3120190000000 张三 ***** zs@mail.com)

注：邮箱用于接收提醒
