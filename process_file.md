
```bash
# 中文标签统计
find . -type f -name "*.json" -print0 | xargs -0 cat | jq -r '.region[]? | if type == "object" then .coordinates.class elif type == "array" then .[].coordinates.class else empty end' | sort | uniq -c | sort -rn | awk '{printf "%s\t%s\n", $1, $2}'
```

```bash
# 英文标签统计
find . -type f -name "*.json" -print0 | xargs -0 cat | jq -r '.region[]?.coordinates.name' | sort | uniq -c | sort -rn | awk '{printf "%s\t%s\n", $1, $2}'
```
```bash
#统计英文标签xml
find . -type f |grep xml|xargs -i grep -hR "<name>" {} | cut -d '>' -f 2 | cut -d '<' -f 1 | sort | uniq -c | sort -nr
```

```bash
#替换xml标签
find . -type f -name "*.xml" -exec sed -i 's/<name>Slippers\/shoes<\/name>/<name>shoes<\/name>/g' {} \;

find . -type f -name "*.xml" -exec sed -i 's/<name>Cat bowl\/dog bowl<\/name>/<name>cat<\/name>/g' {} \;

find . -type f -name "*.xml" -exec sed -i 's/<name>Slippers\/shoes<\/name>/<name>shoes<\/name>/g' {} \;
```

```bash
#提取部分样本
find /media/depth/v/20241224_xml/ -type f |xargs -i grep -E -l "<name>bin|<name>pedestal|<name>socket|<name>cat |<name>dog|<name>desk_rect|<name>weighing-scale|<name>key|<name>person|<name>chair|<name>couch|<name>bed|<name>tvCabinet|<name>fridge|<name>television|<name>washingMachine|<name>electricFan|<name>remoteControl|<name>shoeCabinet" {} >all.txt

cat all.txt|xargs -i cp -r --parent {} ./
cat all.txt|sed 's|/xml|/img|g;s|.xml|.png|g;'|xargs -i cp -r --parent {} ./
```

```bash
#统计子目录所有文件总数
ls -d */ | xargs -I {} sh -c "echo -n '{} '; find {} -type f | wc -l" | sort -k2 -n
```

# 标签合并与统计

## 第一部分：49个基准标签类别合并与统计

这是一个标签表格，左面是数量，右边是名称，请把标签种类相同的进行数量合并，例如比如他有桌子1,桌子2类别。就一并合为桌子类别即可。比如他有两个类，叫做织物和其他织物，你统计的时候，就统计成一类即可。餐桌和桌子，都算桌子。最后输出一个html表格，。保持种类的丰富性，不要把小数量的种类进行合并。注意合并的适度。数量多的类别进行合并，把名称冗余的符号去除，另外，最终输出的标签种类数量要确保百分之百一样，该有的类别不能都是。按照左边的数量进行降序排列。将标签名称意思相近的或者完全相同的数量进行合并，左边是数量，右边是名称，名称一样的合并数量后，按照数量降序重新排列，生成新的表格，输出html表格，合并和整理这些标签。先分析合并的类别。同时写出所有的具体的合并类别过程，用‘变体标签、变体标签、变体标签>标签’表示

瓷砖地板 门框 门板 床 椅子 塑料袋 袜子 鞋子 线缆 沙发 墙 地毯 木质地板 茶几 液体脏污 屏幕 人 沙发（ignore） 桌子 宠物便便 窗帘 纸巾 电视柜 餐桌 底座 垃圾桶 马桶 织物/纺织品 颗粒物 抽油烟机 体重秤 床头柜 冰箱 软质塑料袋 门槛 猫碗 洗衣机 插线板 充电头 纸巾/纸团 儿童玩具 鹅卵石地板 风扇 镜子 塑料制品 胶质塑料 破布/毛巾 落地镜 不锈钢地板 这个是一个基准数据的标签，一共是49个标签类别，根据上面的数据表，这表将相同的标签类别合并，并填充到49个基准标签里面，找不到基准标签的数量用-填充，找到基准标签的合并类别并填充数量。基准标签的种类顺序不要变，输出html表格形式，html表格只保留数量和标签的类别两列，合并和整理这些标签。先分析合并的类别，同时写出全体49个具体的合并类别过程，用‘‘变体标签、变体标签、变体标签>标签’表示，比如合并的类别，将其他织物、衣服、毛巾，合并为织物

塑料袋 袜子 椅子 线团 木质地板 鞋子 地毯 液体脏污 人 纸巾 桌子 屏幕/电视 宠物便便 马桶 织物 颗粒物 油烟机 电视柜 冰箱 插线板 宠物 洗衣机 鞋柜 垃圾桶 电风扇 钥匙 遥控器 这个是一个基准数据的标签，一共是27个标签类别，根据发给数据表，这表将相同的标签类别合并，并填充到基准标签里面，找不到基准标签的数量用-填充，找到基准标签的合并类别并填充数量。合并和整理这些标签。先分析合并的类别，标签的种类顺序不要变，输出html表格形式，第一列都删除掉，只保留数量，纵向的列表格，稍等我下面发给你表格，同时写出所有的具体的27合并类别的过程，用‘变体标签、变体标签、变体标签>标签’表示，将其他织物、衣服、毛巾，合并为织物

---

## 第二部分：统计合并子数据集标签

这个是三个标签统计表格，分别对应的名称和相应的数量，都是两列的数据表格，现在把他们相同的标签名称的数量都进行合并，名称相近的合并数量，名称一样的合并数量，不要丢失任何的标签，最终生成一个全部的两列表格，按照标签的数量降序排列
