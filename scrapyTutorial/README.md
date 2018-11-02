### Items

* 爬取的主要目标就是从非结构性的数据源提取结构性数据, 例如网页
* Item对象始终简单的容器,保存了爬取得到的数据.其提供了类似于字典(dictionary-like)的API以及用于生命可用字段的简单语法

#### 声明Item

item使用简单的class定义语法以及Field对象来声明.

#### Item字段(Item Fields)

Field对象指明了每个字段的元数据(metadata).