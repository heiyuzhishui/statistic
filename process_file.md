
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

根据下列的标签类别，进行合并和整理。左侧是数量，右侧是名称。标签名称意义相近的类别将合并，最终按照数量降序排列，并以HTML表格格式输出。

### 标签合并过程

- **瓷砖地板 > 地板**
- **门框, 门板 > 门**
- **床 > 床类**
- **椅子 > 家具**
- **塑料袋 > 塑料制品**
- **袜子 > 织物**
- **鞋子 > 鞋类**
- **线缆 > 电缆**
- **沙发 > 家具**
- **墙 > 墙面**
- **地毯 > 织物**
- **木质地板 > 地板**
- **茶几 > 家具**
- **液体脏污 > 脏污**
- **屏幕 > 显示设备**
- **人 > 人物**
- **沙发（ignore） > 忽略**
- **桌子 > 家具**
- **宠物便便 > 宠物相关**
- **窗帘 > 织物**
- **纸巾 > 纸品**
- **电视柜 > 家具**
- **餐桌 > 家具**
- **底座 > 家具**
- **垃圾桶 > 垃圾**
- **马桶 > 卫浴**
- **织物/纺织品 > 织物**
- **颗粒物 > 物品**
- **抽油烟机 > 家电**
- **体重秤 > 电子产品**
- **床头柜 > 家具**
- **冰箱 > 家电**
- **软质塑料袋 > 塑料制品**
- **门槛 > 门**
- **猫碗 > 宠物用品**
- **洗衣机 > 家电**
- **插线板 > 电器配件**
- **充电头 > 电器配件**
- **纸巾/纸团 > 纸品**
- **儿童玩具 > 玩具**
- **鹅卵石地板 > 地板**
- **风扇 > 家电**
- **镜子 > 家具**
- **塑料制品 > 塑料制品**
- **胶质塑料 > 塑料制品**
- **破布/毛巾 > 织物**
- **落地镜 > 家具**
- **不锈钢地板 > 地板**

### 输出格式：HTML表格

在合并后的标签种类中，每个标签会根据数量排序，输出为一个HTML表格，仅保留数量和标签名称两列。

---

## 第二部分：27个基准标签类别合并与统计

同样的操作方法，合并和整理标签种类，最终按照数量降序排列，并输出为HTML表格。

### 标签合并过程

- **塑料袋 > 塑料制品**
- **袜子 > 织物**
- **椅子 > 家具**
- **线团 > 线缆**
- **木质地板 > 地板**
- **鞋子 > 鞋类**
- **地毯 > 织物**
- **液体脏污 > 脏污**
- **人 > 人物**
- **纸巾 > 纸品**
- **桌子 > 家具**
- **屏幕/电视 > 显示设备**
- **宠物便便 > 宠物相关**
- **马桶 > 卫浴**
- **织物 > 织物**
- **颗粒物 > 物品**
- **油烟机 > 家电**
- **电视柜 > 家具**
- **冰箱 > 家电**
- **插线板 > 电器配件**
- **宠物 > 宠物用品**
- **洗衣机 > 家电**
- **鞋柜 > 家具**
- **垃圾桶 > 垃圾**
- **电风扇 > 家电**
- **钥匙 > 物品**
- **遥控器 > 电子产品**

### 输出格式：HTML表格

合并后的标签将按数量排序，并输出为HTML表格，保留数量和标签名称两列。

---

## 第三部分：基准标签的整理

整理后的标签种类将按需求合并并统计，保证数据的一致性，按最终统计结果输出HTML表格。

