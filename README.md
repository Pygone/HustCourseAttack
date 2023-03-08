# HustCourseAttack
Hust 抢课小助手
# HustCourseAttack

## StartUp

​		Python env requirements

```sh
pip install -r requirements.txt
```

## Start

```shell
python.exe HustCourseAttack.py [Your StuId] [Your Course File] [Your Cookie File] [Time]
```

**time-format: month/day/hour/minute**

### Example

Your StuId:U2021XXXXX  
Your Course File: course.txt  
Your Cookie File: Cookie.txt  
The time of course selection: 02/14/10/00  
You should type the command as follow:  

```
python.exe HustCourseAttack.py U2021XXXXX course.txt Cookie.txt 02/14/10/00
```

Your course.txt should contain:  
**Verilog语言:xxx**  
**CourseName:teacher**  

Your Cookie.txt should contain the Cookie from the website:[本科生专业选课 (hust.edu.cn)](http://wsxk.hust.edu.cn/zyxxk/index)  
below i will show my way to get the cookie, if you have some awesome ideas…..  

Your time-format should follow as month/day/hour/minute  
for an example now is 22:04  2023/3/8, so you should make it like **03/08/22/04**  

### How to Get Cookie 

#### Login

Login the course selection website  
![Step1](https://github.com/Pygone/HustCourseAttack/blob/master/Pic/Pic1.png)

#### enter in Dev zone

My broswer is Edge, so i press F12 to enter in Dev zone, you can search for your way to enter in Dev zone  

#### Copy Cookie
Get in the Network zone, if there is no content, you can refresh the page to get response. And select the one with name of “getIndexInfo”,  selsct the headers column and slide down, find the row with name of “Cookie”, now you can copy the value of it. 
![Step2](https://github.com/Pygone/HustCourseAttack/blob/master/Pic/Pic2.png)
