

-c  把替换内容打印到控制台
-v  把替换内容复制到剪辑版
-h  帮助文档
-p  复制到剪切板再粘贴到pycahrm（需要安装第三方库 pyautogui）
-t  要用什么替换，默认用单引号替换  双引号需要转义如使用三引号替换：-t\"\"\"
-r  填 -r"$SelectedText$" -r参数 请放在最后面

例子1：-m replacess -c -r"$SelectedText$"
例子2：-m replacess -v -r"$SelectedText$"
例子3：-m replacess -v -c -r"$SelectedText$"
例子4：-m replacess -p -r"$SelectedText$"
例子5：-m replacess -p -t\" -r"$SelectedText$"  用双引号替换，并将替换的内容粘贴到pycahrm替换的位置

作者QQ：2920007919