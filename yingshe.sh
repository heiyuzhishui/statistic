#!/bin/bash

# 遍历当前目录及其子目录中的所有XML文件
for file in $(find . -name "*.xml"); do
    # 使用sed进行批量替换
    sed -i '
        s|<name>Slippers / shoes</name>|<name>鞋子</name>|g
        s|<name>trash can</name>|<name>垃圾桶</name>|g
        s|<name>Fan base</name>|<name>底座</name>|g
        s|<name>wire</name>|<name>线团</name>|g
        s|<name>Cat bowl / dog bowl</name>|<name>猫碗</name>|g
        s|<name>table</name>|<name>桌子</name>|g
        s|<name>Weighing scale</name>|<name>体重称</name>|g
        s|<name>chair</name>|<name>椅子</name>|g
        s|<name>sofa</name>|<name>沙发</name>|g
        s|<name>Bed</name>|<name>床</name>|g
        s|<name>TV cabinet</name>|<name>电视柜</name>|g
        s|<name>Refrigerator</name>|<name>冰箱</name>|g
        s|<name>Television</name>|<name>电视</name>|g
        s|<name>Washing machine</name>|<name>洗衣机</name>|g
        s|<name>Socks</name>|<name>袜子</name>|g
        s|<name>tea table</name>|<name>茶几</name>|g
        s|<name>Pet feces</name>|<name>宠物便便</name>|g
        s|<name>closestool</name>|<name>马桶</name>|g
        s|<name>clothes</name>|<name>纺织物</name>|g
        s|<name>carpet</name>|<name>地毯</name>|g
        s|<name>door</name>|<name>门</name>|g
    ' "$file"
done

echo "所有XML文件的标签已更新完成。"