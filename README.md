# TMConfuse
##2019-08-20更新：
Forked from https://github.com/TMWu/TMConfuse .

Have below improvements:

1. Confuse.py support Python2.7;

2. Fix property regex match bug;

	```
	  Case there's blank between ";" and "//" 
	  @property(nonatomic, retain) UIView* view;  // this is a comment
	```
3. Code optimize for ConfuseBiz.scan_path;

	Better traversal judgement, reduce scan times.
   
4. Code optimize for DealUserFile; 

   Combine property and IBAction scan in parse_user_identifiers, reduce 2/3 scan times.


5. Use RunScript to  do confuse automatically before compiling.
	
	* Add a runScript for the project;
	* Use relative paths to load files and auto do confuse before hand when build the project.




## 6月6日更新：
由于上架过程中混淆词汇中存在敏感词汇，被苹果爸爸拒了一次，所以修改随机单词拼接规则，由通用的单词拼接，可以自行修改

```
def confuse_text(text):
firstArray = ['send', 'check', 'upload', 'refresh', 'has','rest', 'change', 'add', 'remove', 'is']
secondArray = ['Item', 'UserInfo', 'MediaInfo', 'Route', 'Common', 'Chat', 'Commis']
thirdArray = ['By', 'Of', 'With', 'And', 'From', 'To', 'In']
forthArray = ['Home', 'DrawMap', 'MediaID', 'Message', 'Loaction', 'Username', 'My']
fifthArray = ['Info', 'Count', 'Name', 'SystemId', 'Title', 'Topic', 'Action']
word = random.choice(firstArray) + random.choice(secondArray) + random.choice(thirdArray) + random.choice(forthArray) + random.choice(fifthArray)
return word
```
***

首先声明，此文章是综合了几位大神的精髓，再结合自身需求作的修改完善！

[原文：kaich/codeobscure](https://github.com/LennonChin/Code-Confuse-Plugin)

[iOS安全攻防（二十三）：Objective-C代码混淆](https://blog.csdn.net/yiyaaixuexi/article/details/29201699)

使用之前，需要先了解[class-dump](https://cnbin.github.io/blog/2015/05/21/objective-c-class-dump-an-zhuang-he-shi-yong-fang-fa/)的使用和安装，在此就不作过多介绍了。

由于iOS系统的封闭性，相对于安卓来说，iOS开发过程中代码混淆可能就显得并不是得非有不可了。但是在安全性(可通过[class-dump](https://cnbin.github.io/blog/2015/05/21/objective-c-class-dump-an-zhuang-he-shi-yong-fang-fa/)反编译暴露出类的方法名)和特殊需求上(例如马甲包的混淆过审)还是有一定需求的！
此脚本借鉴于[kaich/codeobscure](https://github.com/LennonChin/Code-Confuse-Plugin)。在使用原作者脚本的过程中，发现了一些BUG和不足，比如正则表达式的判断不准确，生成过多无用的替换宏，需要花费过多时间去人工排错...
由于本人对python并不是很熟，所以只是在原作者的基础上作了一些完善修改。
#### 优化内容：
- 修改正则表达式，更精准地找出关键词。
- 替换规则更改：随机字符串==>随机生成2个单词拼接。防止苹果审核过程被误认加入混淆乱码。
- 增加-k选项，通过ignoreKey.txt文件添加需要过滤的关键词，可避免每次生成都要手动删除部分关键词的麻烦。
- 增加property关键词、懒加载方法名过滤，减少无用宏的生成。
- 增加IBAction方法关键词的二次过滤（原脚本存在自定义方法跟IBAction方法重名，无法排除的情况）。

***
### 以下内容大部分来源于[kaich/codeobscure](https://github.com/LennonChin/Code-Confuse-Plugin)

## 实现原理

其实插件的实现方式十分简单，提取用户编写的文件中的方法名，使用宏定义将其更换为任意的无规则字符串。但这种方式有一些需要注意的点：

1. 对于系统库产生的方法名，不可替换；对于系统使用到的关键字，也不可以替换；否则会报错；
2. Swift混编的项目，Swift中的代码不可替换；同时Swift调用Objective-C的特定方法名也不可以轻易替换；
3. 第三方库暴露的头文件的方法名，不可替换；

根据上面的规则（可能有遗漏），该脚本采用了相对简单的方法来避免：

1. 只扫描.h和.m文件，只扫描方法名。（对于属性名，尝试过扫描，但由于属性的访问方式多样，并不建议做混淆，会产生额外的工作量）；
2. 对于系统库，让用户手动指定，这个是可以提取的，直接拿到系统库的头文件即可，脚本会自动扫描到所有的系统关键字，直接做排除处理。（以iOS11的SDK为例，系统关键字约6万个）；
3. 对于Swift代码，可以直接排除在扫描目录外；
4. 对于第三方库，用户可以手动指定目录，脚本会自动扫描提取关键字，在混淆时避免这些关键字。

依据上述原理，基本可以避免多数情况下产生的混淆错误；当然，由于各种项目的复杂性，有一些复杂的混淆错误无法避免，需要后续手动调整代码。

## 使用方式

1. clone本仓库；
2. 你需要安装python3的运行环境，这个可以使用brew进行安装，这里不再赘述。
3. 你首先需要确定以下几项：

- 提取一份你当前项目编译环境的SDK库头文件目录；（Demo中提取了iOS11的SDK头文件目录）
- 你需要混淆的代码的目录；
- 你不需要混淆的代码的目录；
- 你需要提取关键字做排除混淆的目录；（例如Pod仓库、第三方头文件）
- Swift代码目录；（理论上不会扫描替换，可以用于排除桥接文件）
- 输出文件目录；脚本运行后会产生多个log文件，以及最终需要使用到的混淆头文件；

> 注：建议目录使用绝对路径，相对路径容易出问题。

4. 确定以上几项后，找到仓库根目录的Confuse.py文件，使用以下命令行模板运行：

```shell
python3 Confuse.py \
-i 你需要混淆的代码的目录，可以是多个目录，以`,`分隔 \
-s 当前项目编译环境的SDK库头文件目录，可以是多个目录，以`,`分隔 \
-e 你不需要混淆的代码的目录，Swift代码目录，可以是多个目录，以`,`分隔 \
-c 你需要提取关键字做排除混淆的目录，可以是多个目录，以`,`分隔 \
-k 可选，用于存放需要过滤的key(增加内容)
-o 输出文件目录
```

> 注：各参数的意义如下：

- `-i`（input_dirs）：必须，项目需要处理的主要文件所在的目录
- `-s`（system_dirs）：可选，配置系统Framework文件的目录，一般用于做排除字典，避免替换系统关键字
- `-e`（exclusive_dirs）：可选，用于存放不扫描处理的文件的目录，比如Swift文件目录
- `-c`（clean_dirs）：可选，用于存放排除关键字的文件的目录，例如Pods下的目录，或者静态库（头文件修改后会出错）
- `-k`（ignore_key_dir）：可选，用于存放需要过滤的key(增加内容)
- `-o`（output_dir）：必须，输出文件的目录，用于输出关键字、日志以及最后生成的混淆头文件的目录

5. 运行后会在你指定的输出目录下产生一份Confuse.h文件，内容一般如下：

```c
#ifndef NEED_CONFUSE_h
#define NEED_CONFUSE_h
// 生成时间： 2018-04-03 17:20:51
#define Function1 linotypistStonecrop
#define function1 exactingnessMimologist
#define function2 sheepmanSupersublimated
#define functionWithTitle kensititeCratinean
#define subTitle icelandicUntell
#endif
```

这份文件包含了一堆的宏定义，将需要替换的方法名都替换为了一些随机的字符串，因为宏定义是全局替换，我们只需要将该文件引入到自己的项目中，并在PCH文件中进行引入即可。

引入该文件后，Command+B测试编译，如果无法避免而产生编译错误则需要手动调整；由于将所有的替换归集到了头文件中了，所以遇到有错误的地方尝试删除对应宏定义替换信息重新编辑即可。

另外附上一个系统系统库路径：
>/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks



