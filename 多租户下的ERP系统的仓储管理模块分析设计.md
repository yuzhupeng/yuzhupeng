# [多租户下的ERP系统的仓储管理模块分析设计](https://www.cnblogs.com/wuhuacong/p/19763242 "发布于 2026-03-24 12:40")

前面介绍了《多租户下的系统基础表设计》, 介绍了一个多租户系统底层所需要的用户、角色、机构、权限、日志等相关的内容，这个是构建一个多租户的业务系统的基础设施层，随着我们对接多种不同的业务系统类型，如下面会介绍到的ERP系统，其中可能会涉及很多不同的模块，如生产制造管理、库存/仓储管理、采购模块、销售模块、财务模块、人力资源模块、客户关系模块、项目管理模块、质量管理、集成平台 / 开放接口等等，都需要一些基础设施层模块的支持。 我们以仓储模块为例进行一些基础数据模块和库存管理等进行分析设计。

前面介绍了[《多租户下的系统基础表设计》](https://www.cnblogs.com/wuhuacong/p/19724431),介绍了一个多租户系统底层所需要的用户、角色、机构、权限、日志等相关的内容，这个是构建一个多租户的业务系统的基础设施层，随着我们对接多种不同的业务系统类型，如下面会介绍到的ERP系统，其中可能会涉及很多不同的模块，如生产制造管理、库存/仓储管理、采购模块、销售模块、财务模块、人力资源模块、客户关系模块、项目管理模块、质量管理、集成平台 / 开放接口等等，都需要一些基础设施层模块的支持。

我们以仓储模块为例进行一些基础数据模块和库存管理等进行分析设计。

# 1、基础数据模块

这些是进销存基础数据。

## 商品分类（product\_category）

```sql
tb_product_category
----------------
id bigint primary key
tenant_id bigint

category_code -- 分类编码
category_name -- 分类名称
pinyin_code -- 拼音码
pid -- 父级分类ID
path -- 分类路径
sort -- 排序
status -- 状态, 1 启用, 0 停用

```

## 品牌表（product\_brand）

在进销存 / ERP 的 商品模块里，品牌（Brand） 是一个非常标准的 基础数据表，主要用于：

-   商品分类维度
-   商品筛选
-   统计分析
-   商品展示（电商 / 门店）

```sql
tb_product_brand
-------------
id
tenant_id

brand_code -- 品牌编码
brand_name -- 品牌名称
brand_en_name -- 品牌英文名称
pinyin_code -- 拼音码

logo_url -- 品牌logo
website -- 品牌官网

description   -- 品牌描述
sort          -- 排序
status -- 状态, 1 启用, 0 停用

created_at -- 创建时间
updated_at -- 更新时间
created_by -- 创建人
updated_by -- 更新人
```

## SPU 商品表（product\_spu）

SPU = 商品主体，即商品本身。  
SPU 是商品层面，无法精确管理库存。

```sql
tb_product_spu
-------
id
tenant_id

product_code -- 商品编码
product_name       -- 商品名称
product_en_name   -- 商品英文名称
pinyin_code       -- 拼音码
category_id       -- 商品分类
brand_id         -- 商品品牌

base_uom_id -- 基本单位
enable_batch -- 是否启用批次
enable_serial -- 是否启用序列号
enable_expire   -- 是否启用过期管理
expire_days     -- 过期天数
description     -- 商品描述

status -- 商品状态, 1 启用, 0 停用
created_at -- 创建时间
updated_at -- 更新时间
created_by -- 创建人
updated_by -- 更新人

```

## SKU商品规格（product\_sku）

SKU = Stock Keeping Unit，库存单位，本质是 可管理库存的最小单位。  
SKU = 商品的不同属性组合。  
在进销存和仓库管理中，如果没有 SKU，会出现很多问题  
例如：商品：T恤, 如果没有 SKU，库存只按 SPU 管理：

-   红色M和蓝色M混在一起
-   库存统计不准确
-   销售和采购无法精确匹配

SKU 例子：

| SKU | 颜色 | 尺寸 |
| --- | --- | --- |
| T恤-红-L | 红色 | L |
| T恤-红-M | 红色 | M |
| T恤-蓝-L | 蓝色 | L |

tb\_product\_sku 表：

```sql
tb_product_sku
-----------
id
tenant_id

spu_id -- SPU商品ID

sku_code -- SKU编码
sku_name -- SKU名称
sku_en_name -- SKU英文名称
pinyin_code -- 拼音码

spec_json -- SKU规格属性
barcode -- 条码
base_uom_id -- 基本单位

sale_price decimal(10,2)   -- 销售价格
cost_price decimal(10,2)   -- 成本价格

weight decimal(10,2) -- 重量
volume decimal(10,2) -- 体积

status -- 状态, 1 启用, 0 停用
created_at -- 创建时间
updated_at -- 更新时间
created_by -- 创建人
updated_by -- 更新人
```

spec\_json 是一个 JSON 字符串，用于保存 SKU 的规格属性。

```json
{
 "color": "红色",
 "size": "L"
}
```

批次（Batch）和序列号（Serial）都是SKU级别管理的。

ERP 商品模块完整关系图：

```text
tb_product_category
        │
        ▼
     tb_product_spu
        │
        ▼
     tb_product_sku
        │
 ┌──────┼─────────┐
 ▼      ▼         ▼
tb_unit  tb_product_unit  tb_product_barcode

        │
        ▼
       BOM
        │
        ▼
     bom_item
```

库存：

```text

tb_product_sku
     │
     ▼
 tb_inventory
     │
     ├── tb_inventory_batch
     └── tb_inventory_serial

```

ERP 商品模块核心原则：

-   商品和库存分离
-   库存只用基本单位
-   SKU 才参与库存, SPU 不参与库存
-   条码绑定 SKU + 单位,扫码可以识别：SKU + 单位

## 商品条码（product\_barcode）

一个 SKU 可以有多个条码, 例如：

-   箱条码
-   瓶条码

```sql
tb_product_barcode
---------------
id
tenant_id

sku_id -- SKU ID
barcode -- 条码
unit_id -- 单位 ID

created_at -- 创建时间
created_by -- 创建人
updated_at -- 更新时间
updated_by -- 更新人
```

示例：

| barcode | 单位 |
| --- | --- |
| 69000001 | 瓶 |
| 69000002 | 箱 |

扫码：

> 扫码 → SKU + 单位

仓库收货/出货都是按条码操作。

-   条码必须对应 SKU（+ 单位）
-   扫描条码 → 系统识别库存、批次、序列号

如果没有 SKU：

-   条码只能绑定 SPU
-   库存扣减不精确

## 计量单位（unit）

```sql
tb_unit
-----
id
tenant_id

unit_code -- 计量单位编码
unit_name -- 计量单位名称
pinyin_code -- 拼音码
status -- 状态, 1 启用, 0 停用

```

示例数据：

| id | unit\_name |
| --- | --- |
| 1 | 瓶 |
| 2 | 箱 |
| 3 | 托盘 |

## 商品单位（product\_unit）

```sql
tb_product_unit
------------
id
tenant_id

sku_id -- SKU ID
unit_id  -- 计量单位 ID
is_base_unit -- 是否是基础单位
conversion_rate -- 换算率
```

conversion\_rate = 基本单位数量

例：

1箱 = 24个  
base\_unit = 个

示例数据：

| unit | conversion\_rate |
| --- | --- |
| 瓶 | 1 |
| 箱 | 24 |
| 托盘 | 960 |

库存全部统一为基本单位，例如：库存全部存 个, 销售：2箱, 系统自动转换：  
2 \* 24 = 48 个

## 仓库表（warehouse）

仓库是用于储存货物的建筑物，库区是指把仓库分成不同的区域用于储存不同的货物，而库位是指具体放置货物的位置。

```sql
tb_warehouse
---------
id
tenant_id

warehouse_code -- 仓库编码
warehouse_name -- 仓库名称
pinyin_code  -- 拼音码
warehouse_type -- 仓库类型
address -- 地址
org_id -- 组织

manager_id -- 负责人
status -- 状态, 1 启用, 0 停用
created_at -- 创建时间
updated_at -- 更新时间
created_by -- 创建人
updated_by -- 更新人

```

仓库一般 归属于某个组织。

| 仓库 | 所属机构 |
| --- | --- |
| 上海仓 | 上海门店 |
| 杭州仓 | 杭州门店 |
| 深圳仓 | 深圳门店 |

仓库类型 warehouse\_type：

| type | 说明 |
| --- | --- |
| STORE | 门店仓 |
| REGIONAL | 区域仓 |
| CENTRAL | 中心仓 |

索引：

```sql
index(tenant_id, org_id)
```

## 库区表（warehouse\_area）

库区是指把一大幢仓库分成不同的区域，用于储存不同的货物的区域，这种把仓库划分为不同的区域，称为库区。  
在进行仓库管理时，分库区管理是非常重要的环节。合理的分库区管理可以提高仓库的工作效率，减少错误发货率，更好地利用仓储空间。

```sql
tb_warehouse_area
---------
id
tenant_id

warehouse_id -- 仓库
area_code  -- 库区编码
area_name -- 库区名称
pinyin_code -- 拼音码
area_type   -- 库区类型

status -- 状态, 1 启用, 0 停用
created_at -- 创建时间
updated_at -- 更新时间
created_by -- 创建人
updated_by -- 更新人
```

库区示例：

```text
A仓
 ├─ 收货区
 ├─ 存储区
 ├─ 拣货区
 └─ 发货区
B仓
 ├─ 收货区
 ├─ 存储区
 ├─ 拣货区
 └─ 发货区
```

库区类型 area\_type：

| type | 说明 |
| --- | --- |
| RECEIVING | 收货区 |
| STOCK | 存储区 |
| PICKING | 拣货区 |
| SENDING | 发货区 |

## 库位表（warehouse\_location）

大型仓库需要 库位。  
库位是指放置货物的具体位置，如，采用多层货架储存货物，通常对货架及货架储存货物的位置进行编号，以利于人们识别存放货物的位置，具体如，编号为：A12031，即指的是A区12号货架第31号库位。

库位：指货物存放的位置，在库房管理上为了便于查找货物，对货物存放都采用“四号定位”管理，即：库、架、层、位。库—指货物存放在几号库。架—指货物存放在几号库几号架。层—指货物存放在几号架几层。位—指货物存放在几号架几层几号位

```sql
tb_warehouse_location
------------------
id
tenant_id

warehouse_id -- 仓库
area_id -- 库区

location_code -- 库位编码
location_name -- 库位名称
location_type   -- 库位类型
pinyin_code -- 拼音码

status -- 状态, 1 启用, 0 停用
```

库位示例：

```text
A01-01-01
A01-01-02
A01-02-01
```

库存：

> product + warehouse + location

## 容器（warehouse\_container）

容器是一种物理容器，用于装载货物。  
它用于描述 “库存被装在什么容器里”，例如：

-   托盘（Pallet）
-   周转箱（Bin / Tote）
-   料箱
-   包裹
-   物流箱
-   小推车

如果只有库位：

```text
A01-01-01
  ├─ 商品A 50
  ├─ 商品B 20
```

但真实仓库：

```text
A01-01-01
  ├─ 托盘P001
  │     ├─ 商品A 30
  │     └─ 商品B 20
  │
  └─ 托盘P002
        └─ 商品A 20
```

如果没有容器：

-   无法整托盘移动
-   无法箱拣
-   无法托盘出库
-   无法物流打包

```sql
tb_warehouse_container
------------------
id
tenant_id

warehouse_id -- 仓库
area_id -- 库区
location_id -- 库位
pid -- 父容器

container_code -- 容器编码
container_name -- 容器名称
pinyin_code -- 拼音码

container_type -- 容器类型
weight -- 重量
volume -- 体积
status -- 状态, 1 启用, 0 停用

created_at
created_by

```

容器编号 container\_code:

```text
PLT0001   托盘
BIN0012   料箱
BOX1234   纸箱
PKG9001   包裹
```

容器类型 container\_typ:

| type | 说明 |
| --- | --- |
| PALLE | 托盘 |
| BIN | 周转箱 |
| TOTE | 周转箱 |
| BOX | 料箱 |
| PACK | 包裹 |
| TRUCK | 物流箱 |
| SHELF | 小推车 |

parent\_container\_id 支持 容器嵌套,例如：

```text
托盘P001
   ├─ 箱BOX01
   ├─ 箱BOX02
```

## 供应商（supplier）

```sql
tb_supplier
--------
id
tenant_id
org_id -- 机构ID

supplier_code -- 供应商编码
supplier_name -- 供应商名称
supplier_type -- 供应商类型
pinyin_code -- 拼音码
address -- 地址

contact_name -- 联系人
contact_phone -- 联系电话
contact_email -- 联系邮箱

```

## 客户（customer）

```sql
tb_customer
--------
id 
tenant_id 
org_id -- 组织

customer_code -- 客户编码
customer_name -- 客户名称
customer_type -- 客户类型
pinyin_code -- 拼音码
address -- 地址

contact_name -- 联系人
contact_phone -- 联系电话
contact_email -- 联系邮箱
```

# 2、库存模块

库存是进销存核心。真正的ERP设计，包括：

-   多仓库库存锁定设计
-   库存并发扣减
-   商品多单位
-   批次库存
-   序列号库存
-   库存预占（订单锁库存）
-   可追溯库存流水

## 库存表（inventory）：

```sql
tb_inventory
---------
id                      bigint pk

-- 多租户 / 组织
tenant_id               bigint not null            -- 租户
org_id                  bigint not null            -- 组织/法人
owner_id                bigint null                -- 货主（建议保留）

-- 仓储维度
warehouse_id            bigint not null            -- 仓库
area_id                 bigint null                -- 库区,冗余字段，便于查询
location_id             bigint null                -- 库位
container_id            bigint null                -- 容器/托盘/箱

-- 商品维度
sku_id                  bigint not null            -- SKU
base_uom_id                  bigint not null            -- 库存单位（基本单位）

-- 批次 / 序列
batch_no                varchar(64) null           -- 批次号

-- 状态维度（强烈建议）
quality_status          varchar(32) not null       -- 质量状态：GOOD / HOLD / BAD / QC
inventory_status        varchar(32) not null       -- 库存状态：AVAILABLE / FROZEN / LOCKED / QUARANTINE

-- 数量字段（核心）
on_hand_qty            int not null default 0   -- 现存量（物理在库）
reserved_qty           int not null default 0   -- 预占量
frozen_qty             int not null default 0   -- 冻结量（质检/盘点/异常）
in_transit_qty         int not null default 0   -- 在途量（可选）
available_qty          int not null default 0   -- 可用量（冗余字段）

-- 成本（你未来要做库存金额，先预留）
unit_cost               decimal(18,2) null -- 单位成本（可选）
amount                  decimal(18,2) null -- 库存金额（可选）

-- 并发控制
version_no              bigint not null default 0          -- 乐观锁版本号

-- 时间
last_txn_time           timestamp null                     -- 最近库存变动时间

-- 审计
created_at              timestamp not null
created_by              bigint null
updated_at              timestamp not null
updated_by              bigint null
```

说明：

库存表统一用基本单位：  
同一个 SKU 在同一库位，可能因为状态不同而不能合并：

库存状态不同，例如：冻结、不良品、待检、不良、隔离、锁定，因此不能合并，所以加：

-   quality\_status（质量状态）
-   inventory\_status（库存状态 / 业务状态

on\_hand\_qty： 物理在库量 / 现存量

-   仓库里真实存在的数量
-   入库增加
-   出库减少
-   预占时不变

reserved\_qty：已被业务预占的数量

-   销售订单占用
-   生产领料占用
-   调拨出库占用
-   预占时增加
-   释放时减少
-   转正式出库时减少

frozen\_qty: 不可用但未出库的冻结量, 比如：

-   质检冻结
-   盘点冻结
-   异常锁定
-   财务冻结
-   法务冻结（极少数场景）

in\_transit\_qty: 在途量, 表示：

-   调拨途中
-   采购已发货未收货
-   委外发出未回厂
-   跨仓移动途中

available\_qty: 当前可用量, 推荐公式：

> available\_qty = on\_hand\_qty - reserved\_qty - frozen\_qty

库存计算关系：

```sql
available_qty = on_hand_qty - reserved_qty
```

一般 不要把 in\_transit\_qty 算进 available  
因为在途不在当前仓实际可发。

在途库存 = 已发出但未入库的库存, 在途库存 不算可用库存。

上海仓 → 北京仓 调拨 100 件：

| 阶段 | 库存 |
| --- | --- |
| 上海仓 | 减少100 |
| 在途库存 | +100 |
| 北京仓 | 0 |

当北京仓收货：

| 阶段 | 库存 |
| --- | --- |
| 在途库存 | \-100 |
| 北京仓 | +100 |

推荐唯一键（推荐版）：

```text
tenant_id
org_id
owner_id
warehouse_id
location_id
container_id
sku_id
base_uom_id
batch_no
serial_no
quality_status
inventory_status
```

建议加 3 个“约束规则”:

1 数量不能为负（如果你不允许负库存）

```sql
check (on_hand_qty >= 0)
check (reserved_qty >= 0)
check (frozen_qty >= 0)
check (in_transit_qty >= 0)
check (available_qty >= 0)
```

2 预占不能超过现存（通常建议）

```sql
check (reserved_qty <= on_hand_qty)
```

如果你支持“超卖 / 负可用 / 虚拟预占”，这个约束要谨慎。

3 可用量公式一致性（如果你要强约束）

```sql
check (available_qty = on_hand_qty - reserved_qty - frozen_qty)
```

库存扣减必须 原子操作。

```sql
UPDATE tb_inventory
SET
  on_hand_qty = on_hand_qty - :qty
WHERE
  id = :id
AND
  on_hand_qty >= :qty
```

判断：影响行数 == 1  
否则：库存不足

## 库存流水

库存流水记录库存变动。库存问题排查 全部依赖库存流水。  
每次对 tb\_inventory 的数量变更，都必须插入一条 tb\_inventory\_log。

```sql
tb_inventory_log
-------------
id

-- 多租户 / 组织
tenant_id                   bigint not null
org_id                      bigint not null            -- 建议补上
owner_type                  varchar(32) null          -- 货主类型 / 所有者类型（VMI等）
owner_id                    bigint null               -- 货主ID

-- 关联库存快照（建议保留）
inventory_id                bigint null               -- 对应 tb_inventory.id（建议有）

-- 仓储维度
warehouse_id                bigint not null           -- 仓库
area_id                     bigint null               -- 库区 建议补上（便于查询）
from_location_id            bigint null               -- 原库位
to_location_id              bigint null               -- 目标库位
from_container_id           bigint null               -- 原容器
to_container_id             bigint null               -- 目标容器

-- 商品维度
sku_id                      bigint not null          -- SKU
uom_id                      bigint not null          -- 业务单位（例如 2箱），仅追溯
base_uom_id                 bigint not null          -- 基本单位（例如 个）

-- 批次 / 序列
batch_no                    varchar(64) null         -- 批次号

-- 状态维度（强烈建议）
quality_status              varchar(32) not null      -- GOOD / HOLD / BAD / QC
inventory_status            varchar(32) not null      -- AVAILABLE / FROZEN / LOCKED / QUARA

-- 业务来源
biz_type                    varchar(32) not null      -- 业务类型
biz_id                      bigint not null           -- 业务单ID
biz_no                      varchar(64) null          -- 业务单号（建议加）
biz_line_id                 bigint null               -- 业务明细ID（建议加）

-- 变更动作分类（非常重要）
action_type  varchar(32) not null    -- IN / OUT / MOVE / RESERVE / RELEASE / CONSUME / FREEZE / UNFREEZE / ADJUST
change_type  varchar(32) not null -- ON_HAND / RESERVED / FROZEN / IN_TRANSIT / AVAILABLE / COMPOS

-- 预占关联（强烈建议）
reservation_id              bigint null               -- 对应 tb_inventory_reservation.id

-- 数量变化（核心）
uom_qty                     int not null default 0    -- 数量（业务单位），仅追溯
change_qty                  int not null default 0    -- 主变化量（基本单位变化量（例如 48个））

delta_on_hand_qty           int not null default 0    -- 变化量（物理在库）
delta_reserved_qty          int not null default 0    -- 变化量（预占）
delta_frozen_qty            int not null default 0    -- 变化量（冻结）
delta_in_transit_qty        int not null default 0    -- 变化量（在途）
delta_available_qty         int not null default 0    -- 变化量（可用）

-- 变更前快照
before_on_hand_qty          int not null default 0 
before_reserved_qty         int not null default 0
before_frozen_qty           int not null default 0
before_in_transit_qty       int not null default 0
before_available_qty        int not null default 0

-- 变更后快照
after_on_hand_qty           int not null default 0 
after_reserved_qty          int not null default 0
after_frozen_qty            int not null default 0
after_in_transit_qty        int not null default 0
after_available_qty         int not null default 0

-- 原因 / 备注 / 审计
reason_code
remark

created_at
created_by
```

库存日志为什么需要关联inventory\_id?

-   方便查询：可以直接查询库存快照，而不是去关联库存表。
-   快速定位“当时操作的是哪一行库存快照”
-   tb\_inventory\_log 不是必须强依赖 inventory\_id，  
    但在大多数 ERP / WMS / 多租户 + 高并发库存快照模型 里，  
    建议保留 inventory\_id，作为“快照关联指针”，但不要把它当成唯一可信关系。

业务类型biz\_type示例：

```text
PURCHASE_IN     -- 采购入库
SALE_OUT        -- 销售出库
TRANSFER_OUT    -- 调拨出库
TRANSFER_IN     -- 调拨入库
ADJUST          -- 调整
INVENTORY_CHECK -- 盘点
RETURN_IN       -- 退货入库
RETURN_OUT      -- 退货出库
MOVE_OUT        -- 移库出库
MOVE_IN         -- 移库入库
FREEZE            -- 冻结
UNFREEZE          -- 解冻
QC_HOLD           -- 质检冻结
QC_RELEASE        -- 质检解冻
INIT              -- 初始化库存
```

action\_type 示例：

```text
IN             -- 入库
OUT            -- 出库
MOVE           -- 移库
RESERVE        -- 预占
RELEASE        -- 释放
CONSUME        -- 转出
FREEZE         -- 冻结
UNFREEZE       -- 解冻
ADJUST         -- 调整
```

这样：

-   biz\_type = SALE\_OUT
-   action\_type = OUT

或者：

-   biz\_type = SALE\_RESERVE
-   action\_type = RESERVE

这会让统计、审计、权限规则都更清晰。

移库/调拨尽量拆成“双边流水”.

所有者类型 owner\_type:

```text
SELF        自有库存
SUPPLIER    供应商库存（VMI）
CUSTOMER    客户库存
```

VMI 相关：

```text
VMI_REPLENISH
VMI_CONSUME
VMI_TRANSFER
```

库存表和库存流水引入 container\_id 的原因：

```text
1️⃣ 整托盘移动
2️⃣ 箱拣 / 料箱管理
3️⃣ 物流包裹管理
4️⃣ 自动化仓库支持
5️⃣ 减少库存操作数量
6️⃣ 支持容器嵌套
7️⃣ 支持库位容量控制
8️⃣ 库存追溯更精确
```

现代 WMS 几乎一定会有 container 模型。

真正的 ERP 库存一般包含 4 张核心表：

```text
tb_inventory              当前库存
tb_inventory_log          库存流水
tb_inventory_reservation  库存预占
tb_inventory_batch        批次库存
```

如果有序列号：tb\_inventory\_serial

## 库存预占（锁库存）

库存预占是一种特殊的库存变动，用于防止库存超卖。  
预占本质是“未来可能出库/消耗”的承诺，不一定立刻减少物理库存。

这是 高并发订单系统的关键设计。  
例如：

> 库存 100  
> 订单A锁定 30  
> 订单B锁定 20

库存：

> on\_hand\_qty = 100  
> reserved\_qty = 50  
> available = 50

预占表：

```sql
tb_inventory_reservation
---------------------
id bigint 
tenant_id bigint  -- 租户
org_id bigint  -- 组织

reservation_no varchar(50) -- 预占单号
reservation_type varchar(50) -- 预占类型：SALE / PICK / TRANSFER / PROD / MANUAL / RETURN 等

warehouse_id bigint -- 仓库
area_id bigint null -- 库区 建议补上（便于查询）
location_id bigint -- 库位
container_id bigint -- 容器

sku_id bigint -- 商品SKU ID
uom_id bigint-- 业务单位
base_uom_id bigint -- 基本单位

batch_no varchar(50) -- 批次

biz_type varchar(50) -- 业务类型
biz_id bigint-- 业务单据ID
biz_no varchar(50) -- 业务单号
biz_item_id bigint     -- 业务明细ID

quality_status varchar(50)    -- 质量状态（GOOD / HOLD / DEFECT）
inventory_status varchar(50)  -- 库存状态（AVAILABLE / FROZEN / QC / DAMAGED）

inventory_id           -- 对应快照行ID（建议保留，逻辑关联 tb_inventory.id，可空）
source_inventory_id    -- 可选：来源库存ID（某些拆分场景可用，一般可不加）

reserved_qty int -- 预占数量
consumed_qty int -- 已执行数量
released_qty int -- 已释放数量
effective_qty int   -- 有效数量

reserve_time           -- 预占生效时间
expire_time            -- 过期时间（可空，超时自动释放）
released_time          -- 全部释放时间（可空）
consumed_time          -- 全部转执行时间（可空）

is_locked              -- 是否硬锁定（可选）
lock_version           -- 乐观锁版本号（建议有）

remark                 -- 备注

reservation_status     -- 状态：ACTIVE / PARTIAL_RELEASED / RELEASED / CONSUMED / CANCELLED
created_at
created_by
updated_at
updated_by
```

预占状态reservation\_status, 推荐枚举：

```text
LOCKED      已锁定
PARTIAL_RELEASED   部分释放
CONSUMED    已全部执行（已转实际出库）
RELEASED    已全部释放
CANCELLED   已取消
EXPIRED     已过期
```

biz\_type + biz\_id + biz\_item\_id

这是整张表最关键的业务定位字段。

建议固定设计：

-   biz\_type：业务单据类型
-   biz\_id：业务主单ID
-   biz\_item\_id：业务明细ID（强烈建议必须有）

例如：

| biz\_type | biz\_id | biz\_item\_id | 说明 |
| --- | --- | --- | --- |
| SALES\_ORDER | 1001 | 10011 | 销售订单明细锁库存 |
| STOCK\_TRANSFER | 2001 | 20012 | 调拨单明细锁库存 |
| PROD\_PICK | 3001 | 30015 | 生产领料锁库存 |
| WAVE\_PICK | 4001 | 40018 | 波次拣货锁库存 |

为什么 biz\_item\_id 很重要？

因为一张单多个相同 SKU 的明细行很常见。  
只靠 biz\_id + sku\_id 可能不够唯一。

数量字段设计:  
建议至少 4 个：

```text
reserve_qty    本次总锁定量
consumed_qty   已执行量
released_qty   已释放量
effective_qty  当前有效锁定量
```

公式：

```text
effective_qty = reserve_qty - consumed_qty - released_qty
```

这样支持：

-   部分发货
-   部分取消
-   部分调拨执行
-   多次释放

为什么不能只存一个 reserved\_qty? 因为真实业务是这样的：

销售单锁 100：

-   reserve\_qty = 100

第一次发货 30：

-   consumed\_qty = 30
-   effective\_qty = 70

客户取消 20：

-   released\_qty = 20
-   effective\_qty = 50

第二次发货 50：

-   consumed\_qty = 80
-   effective\_qty = 0
-   status = CONSUMED

如果只有一个字段，你后期对账会非常痛苦。

**流程：**

***订单创建***

-   检查库存: inventory.available\_qty >= order.total\_amount
-   库存锁定:写入库存预占 inventory\_reservation
-   并更新：inventory.reserved\_qty

***订单发货***

```sql
on_hand_qty -= qty
reserved_qty -= qty
```

***订单取消***

-   释放 reserved\_qty

```sql
reserved_qty -= qty
```

预占表和 tb\_inventory 的关系:

1）tb\_inventory.reserved\_qty 是汇总值

表示当前快照上被占用了多少。

2）tb\_inventory\_reservation 是明细值

表示到底是谁占的、怎么占的。

预占表和库存流水表的关系:

-   预占动作要写库存流水
-   释放动作要写库存流水
-   预占转实扣动作也要写库存流水

## 批次库存

很多商品必须支持：

```text
生产批次
有效期
生产日期
```

批次表：

```sql
tb_inventory_batch
---------------
id
tenant_id
org_id

owner_type              -- 所有者类型（自有 / VMI / 寄售）
owner_id                -- 所有者ID

sku_id -- SKU ID

batch_source_type       -- 批次来源类型：PURCHASE / PROD / TRANSFER / RETURN / MANUAL / INIT
batch_source_id         -- 批次来源单据ID
batch_source_no         -- 批次来源单号（冗余便于查询）
batch_source_line_id    -- 来源明细行ID（建议）

supplier_id             -- 供应商ID（采购/VMI场景建议）
supplier_batch_no       -- 供应商批号（非常建议）
manufacturer_id         -- 生产商ID（可选）
manufacturer_batch_no   -- 生产批号 / 厂家批号（建议）
production_lot_no       -- 生产批号（如与 batch_no 区分时使用，可选）

production_date -- 生产日期
expire_date -- 有失效日期 / 到期日期
shelf_life_days         -- 有效期天数（可选，冗余）

quality_status          -- 批次默认质量状态（GOOD / HOLD / QC / DEFECT）
batch_status            -- 批次状态（ACTIVE / HOLD / FROZEN / BLOCKED / EXPIRED / CLOSED）

country_of_origin       -- 原产地（可选）
inspection_status       -- 检验状态：PENDING / PASS / FAIL / PARTIAL（建议）
inspection_no           -- 质检单号（可选）
inspection_result       -- 检验结果备注（可选）

remark                  -- 备注
ext_json                -- 扩展属性JSON（如批次自定义属性）

created_at
created_by
updated_at
updated_by
```

批次状态建议枚举, batch\_status 推荐值：

-   ACTIVE：正常可用
-   HOLD：暂扣
-   FROZEN：冻结
-   BLOCKED：禁止出库
-   EXPIRED：已过期
-   CLOSED：批次关闭（库存已清零且不再使用）
-   CANCELLED：作废批次（初始化错误等）

库存表引用：batch\_no

## 序列号库存（高端 ERP）

当商品启用序列号时使用。  
例如：

```text
手机
电脑
医疗设备
```

必须逐个追踪。  
序列号表：

```sql
tb_inventory_serial
----------------
id
tenant_id
org_id

owner_type              -- 所有者类型（自有 / VMI / 寄售）
owner_id                -- 所有者ID

sku_id  --SKU ID
serial_no -- 序列号

warehouse_id -- 仓库
area_id                     -- 当前库区
location_id                 -- 当前库位
container_id                -- 当前容器

serial_status               -- 序列号状态,IN_STOCK / RESERVED / PICKING / SHIPPED / SOLD / SCRAPPED
quality_status              -- 质量状态,  GOOD / QC / HOLD / DEFECT / SCRAP
inventory_status            -- 库存状态（可选）,NORMAL / LOCKED / FROZEN / DAMAGED（可选）

customer_id                 -- 客户ID（若已售出/寄售可选）
supplier_id                 -- 供应商ID（可选）

is_reserved               -- 是否已预占
reservation_id            -- 当前有效预占ID（可空）
is_locked                 -- 是否锁定
is_in_transit             -- 是否在途

source_type                 -- 来源类型：PURCHASE / PROD / RETURN / INIT / TRANSFER_IN
source_id                   -- 来源单据ID
source_no                   -- 来源单号
source_line_id              -- 来源明细ID

uom_id                      -- 业务单位（可选）
base_uom_id                 -- 基本单位（建议）
qty                         -- 数量，固定=1（建议保留）
base_qty                    -- 基本数量，固定=1（建议保留）

remark                  -- 备注
ext_json                -- 扩展属性JSON（如批次自定义属性）
version_no

created_at
created_by
updated_at
updated_by
```

serial\_status 状态：

```text
IN_STOCK        -- 在库
RESERVED        -- 已预占
PICKING         -- 拣货中
PACKED          -- 已打包
SHIPPED         -- 已发货
IN_TRANSIT      -- 在途
SOLD            -- 已销售/已出库
RETURNED        -- 已退回
SCRAPPED        -- 已报废
LOCKED          -- 已锁定
QC_HOLD         -- 质检冻结
LOST            -- 丢失
```

# 3、采购模块

### 采购订单

```sql
tb_purchase_order
--------------
id
tenant_id
org_id -- 组织

order_no -- 订单编号）
supplier_id              -- 供应商ID
supplier_code            -- 供应商编码（冗余）
supplier_name            -- 供应商名称（冗余）

warehouse_id             -- 仓库
buyer_id                 -- 采购员/采购负责人
department_id            -- 采购部门（可选）

source_type              -- 来源类型：MANUAL/PR/MRP/CONTRACT
source_id                -- 来源单ID（可选，如采购申请单/合同）

biz_type                 -- 业务类型：NORMAL/VMI/CONSIGNMENT/OUTSOURCING/URGENT
order_type               -- 订单类型：STANDARD/DIRECT/FRAMEWORK

currency_code            -- 币种：CNY/USD...
exchange_rate            -- 汇率（相对本位币）

price_tax_included       -- 单价是否含税
tax_mode                 -- 税模式：EXCLUSIVE/INCLUSIVE

order_date               -- 下单日期
expected_arrival_date    -- 整单期望到货日期
delivery_address_id      -- 收货地址ID（可选）
delivery_contact         -- 收货联系人
delivery_phone           -- 收货电话

total_qty                -- 总订购数量（业务单位汇总）
total_base_qty           -- 总基本数量汇总（可选但强烈建议）
total_amount             -- 未税金额合计
total_tax_amount         -- 税额合计
total_amount_with_tax    -- 含税金额合计

discount_amount          -- 整单优惠金额（可选）
other_fee_amount         -- 其他费用（运费/杂费，可选）

remark                   -- 备注
extra_data               -- 扩展JSON（可选）

version_no               -- 乐观锁版本号

created_at
created_by
updated_at
updated_by

approved_at
approved_by
closed_at
closed_by
```

业务状态：

```text
DRAFT           -- 草稿
PENDING_APPROVAL-- 待审批
APPROVED        -- 已审批/待执行
PART_RECEIVED   -- 部分收货
RECEIVED        -- 全部收货
PART_CLOSED     -- 部分关闭
CLOSED          -- 已关闭
CANCELLED       -- 已取消
```

approval\_status审批状态，例如：

-   PENDING
-   APPROVED
-   REJECTED

close\_status 关闭状态，例如：

-   OPEN
-   PARTIAL
-   CLOSED

为什么要冗余 supplier\_code / supplier\_name? 因为主数据会变：

-   供应商改名
-   编码调整
-   但历史单据必须保留“下单时快照”。

### 采购订单明细

```sql
tb_purchase_order_item
-------------------
id
tenant_id
org_id

order_id -- 订单ID
order_no -- 订单编号
line_no -- 行号

sku_id  -- SKU ID
sku_code                 -- SKU编码（冗余）
sku_name                 -- SKU名称（冗余）
sku_spec                 -- 规格型号（冗余）

enable_batch -- 是否启用批次
enable_serial -- 是否启用序列号

source_type              -- 来源类型（可选）
source_id                -- 来源单ID（可选）
source_item_id           -- 来源明细ID（可选）

warehouse_id             -- 收货仓库（可覆盖头表）
area_id                  -- 默认库区（可选）
location_id              -- 默认库位（可选，通常不建议采购阶段强制）
owner_type               -- 库存所有者类型（支持VMI/寄售）
owner_id                 -- 库存所有者ID

uom_id                   -- 采购单位ID（业务单位）
uom_code                 -- 采购单位编码（冗余）
uom_name                 -- 采购单位名称（冗余）

base_unit_id             -- 基本单位ID
base_unit_code           -- 基本单位编码（冗余）
base_unit_name           -- 基本单位名称（冗余）

uom_numerator            -- 换算分子
uom_denominator          -- 换算分母
uom_rate                 -- 换算率（冗余，便于直接计算，可选）

order_qty                -- 订购数量（业务单位）
order_base_qty           -- 订购基本数量

received_qty             -- 已收货数量（业务单位）
received_base_qty        -- 已收货基本数量

returned_qty             -- 已退货数量（业务单位）
returned_base_qty        -- 已退货基本数量

pending_receive_qty      -- 待收货数量（业务单位，可冗余）
pending_receive_base_qty -- 待收货基本数量（可冗余）

unit_price               -- 未税单价（业务单位）
tax_rate                 -- 税率（如13.00）
tax_amount               -- 税额
amount                   -- 未税金额
amount_with_tax          -- 含税金额
tax_included_price       -- 含税单价（可选冗余）

expected_arrival_date    -- 行期望到货日期

item_status              -- 行状态：OPEN/PART_RECEIVED/RECEIVED/CLOSED/CANCELLED
close_reason             -- 关闭原因（可选）

remark                   -- 行备注
extra_data               -- 扩展JSON（可选）

version_no

created_at
created_by
updated_at
updated_by
```

| 字段 | 值 |
| --- | --- |
| uom\_id | 箱 |
| order\_qty | 2 |
| order\_base\_qty | 48 |

价格通常使用 业务单位。如果需要成本计算，系统会换算成 基本单位：

采购明细表为什么要冗余这么多字段?

采购明细必须保存“下单快照”

因为 SKU 主数据可能变化：

-   名称变了
-   规格变了
-   单位换了
-   换算率调整了
-   税率策略变了
-   如果不冗余，历史单据会失真。

所以建议冗余：SKU编码、名称、规格型号、单位、换算率、税率策略、等信息：

-   sku\_code
-   sku\_name
-   sku\_spec
-   uom\_code/uom\_name
-   base\_unit\_code/base\_unit\_name
-   uom\_numerator/uom\_denominator
-   tax\_rate
-   price

为什么采购明细必须有单位字段？

因为采购经常出现：

-   按箱采购，库存按个管理
-   按卷采购，库存按米管理
-   按托采购，库存按箱/个管理

例如：

-   采购单位：箱
-   基本单位：个
-   1箱 = 24个

所以：

-   order\_qty = 10 箱
-   order\_base\_qty = 240 个

推荐单位换算设计:  
例如：

```text
uom_numerator = 24
uom_denominator = 1
```

表示：1 箱 = 24 个

计算：

```text
order_base_qty = order_qty * uom_numerator / uom_denominator
```

为什么不用只存 uom\_rate ?

可以存，但建议：

```text
uom_numerator
uom_denominator
（可选）uom_rate
```

因为：

-   分数更精确
-   更适合复杂单位
-   避免浮点误差

明细状态 item\_status：

```text
OPEN
PART_RECEIVED
RECEIVED
CLOSED
CANCELLED
```

采购订单 不直接改库存。正确关系是：tb\_purchase\_order\_item 记录：

-   订了多少
-   已收到多少
-   待收多少

真正入库时，后续生成：

-   tb\_purchase\_receipt
-   tb\_purchase\_receipt\_item

然后收货过账时：

-   写 tb\_inventory\_log
-   更新 tb\_inventory

如果批次管理：

-   更新 tb\_inventory\_batch

如果 SN 管理：

-   更新 tb\_inventory\_serial

### 采购收货单（到货确认）

表示：货到了，我收到了。  
它负责：

-   记录供应商送货事实
-   记录实收数量
-   记录短交 / 多交 / 拒收
-   记录到货批次 / 序列号
-   可进入“待检 / 待上架 / 暂存区”

如果收货单和入库单分开：

> 正式库存（tb\_inventory）建议只在“采购入库单过账”时更新

也就是：

-   收货单创建/审核：通常 不直接增加正式库存
-   入库单过账：才真正增加 tb\_inventory

这是最标准、最干净的做法。

```sql
tb_purchase_receipt
---
id                  BIGINT PRIMARY KEY,                 -- 主键ID

tenant_id           BIGINT NOT NULL,                   -- 租户ID
org_id              BIGINT NOT NULL,                   -- 组织ID（收货所属组织）

receipt_no          VARCHAR(64) NOT NULL,              -- 收货单号（业务唯一）
order_id -- 订单ID
order_no -- 订单编号

receipt_type               -- 收货类型：PO/NON_PO/RETURN_BACK/VMI
biz_type                   -- 业务类型：NORMAL/VMI/CONSIGNMENT/OUTSOURCING

source_type         VARCHAR(32),                       -- 来源类型：PURCHASE_ORDER / ASN / NONE
source_id           BIGINT,                            -- 来源单据ID（如PO头ID）
source_no           VARCHAR(64),                       -- 来源单号（如PO单号）

supplier_id         BIGINT NOT NULL,                   -- 供应商ID
supplier_code       VARCHAR(64),                       -- 供应商编码（冗余）
supplier_name       VARCHAR(200),                      -- 供应商名称（冗余）

warehouse_id        BIGINT NOT NULL,                   -- 收货仓库ID（到货仓）
receiving_area_id   BIGINT,                            -- 收货库区ID（收货区/待检区）
receiving_location_id BIGINT,                          -- 收货库位ID（暂存库位/待检库位）
receiving_container_id BIGINT,                         -- 收货容器ID（可选）

owner_type          VARCHAR(32) DEFAULT 'SELF',        -- 货权类型：SELF=自有，SUPPLIER=供应商（VMI可用）
owner_id            BIGINT,                            -- 货权所有者ID（VMI场景可为供应商ID
receipt_date        TIMESTAMP NOT NULL,                -- 收货日期（业务日期）
expected_arrival_date TIMESTAMP,                       -- 预计到货日期（可选，来自PO/ASN）
posting_date        TIMESTAMP,                         -- 收货确认日期（确认时间）

receipt_status      VARCHAR(32) NOT NULL,              -- 单据状态：DRAFT/CONFIRMED/PART_INBOUND/COMPLETED/CANCELLED
approval_status     VARCHAR(32),                       -- 审批状态（如启用审批流，可选）

total_received_qty      DECIMAL(20,6) DEFAULT 0,       -- 合计实收数量（业务单位汇总）
total_received_base_qty DECIMAL(20,6) DEFAULT 0,       -- 合计实收数量（基本单位汇总）

total_accepted_qty      DECIMAL(20,6) DEFAULT 0,       -- 合计合格数量（业务单位汇总）
total_accepted_base_qty DECIMAL(20,6) DEFAULT 0,       -- 合计合格数量（基本单位汇总）

total_rejected_qty      DECIMAL(20,6) DEFAULT 0,       -- 合计拒收数量（业务单位汇总）
total_rejected_base_qty DECIMAL(20,6) DEFAULT 0,       -- 合计拒收数量（基本单位汇总）

total_inbound_qty       DECIMAL(20,6) DEFAULT 0,       -- 合计已入库数量（业务单位汇总，累计）
total_inbound_base_qty  DECIMAL(20,6) DEFAULT 0,       -- 合计已入库数量（基本单位汇总，累计）

total_pending_inbound_qty      DECIMAL(20,6) DEFAULT 0,-- 合计待入库数量（业务单位汇总）
total_pending_inbound_base_qty DECIMAL(20,6) DEFAULT 0,-- 合计待入库数量（基本单位汇总）

remark              VARCHAR(500),                      -- 备注

ext1                VARCHAR(200),                      -- 扩展字段1（预留）
ext2                VARCHAR(200),                      -- 扩展字段2（预留）
ext3                VARCHAR(200),                      -- 扩展字段3（预留）

version_no          BIGINT DEFAULT 0 NOT NULL,         -- 乐观锁版本号

created_at          TIMESTAMP NOT NULL,                -- 创建时间
created_by          BIGINT,                            -- 创建人ID
updated_at          TIMESTAMP NOT NULL,                -- 更新时间
updated_by          BIGINT,                            -- 更新人ID

confirmed_at        TIMESTAMP,                         -- 确认时间（收货确认）
confirmed_by        BIGINT,                            -- 确认人ID

cancelled_at        TIMESTAMP,                         -- 作废时间
cancelled_by        BIGINT                             -- 作废人ID
```

收货单头状态 receipt\_status:

```text
DRAFT        -- 草稿
CONFIRMED    -- 已确认（已完成收货确认）
PART_INBOUND -- 部分入库
COMPLETED    -- 全部入库完成
CANCELLED    -- 已作废
```

receipt\_type 建议枚举：

-   PO：采购订单
-   NON\_PO：非采购订单

### 收货单明细

```sql
tb_purchase_receipt_item
---
id                  BIGINT PRIMARY KEY,                 -- 主键ID

tenant_id           BIGINT NOT NULL,                   -- 租户ID
org_id              BIGINT NOT NULL,                   -- 组织ID（收货所属组织）

receipt_id -- 收货单ID
receipt_no -- 收货单号
line_no -- 行号

sku_id -- SKU ID
sku_code -- SKU编码（冗余）
sku_name -- SKU名称（冗余）
sku_spec -- 规格型号（冗余）

enable_batch -- 是否启用批次
enable_serial -- 是否启用序列号

batch_no            VARCHAR(64),                       -- 批次号（简单模式下可直接放明细；复杂场景建议拆批次子表）
serial_no           VARCHAR(128),                      -- 序列号（仅单SN场景；一般SN管理建议拆子表）

source_type -- 来源类型（可选）
source_id -- 来源单ID（可选）
source_item_id -- 来源明细ID（可选）

warehouse_id        BIGINT NOT NULL,                   -- 收货仓库ID
receiving_area_id   BIGINT,                            -- 收货库区ID
receiving_location_id BIGINT,                          -- 收货库位ID
receiving_container_id BIGINT,                         -- 收货容器ID

owner_type -- 库存所有者类型（支持VMI/寄售）
owner_id -- 库存所有者ID

uom_id -- 业务单位ID
uom_code -- 业务单位编码（冗余）
uom_name -- 业务单位名称（冗余）

base_unit_id -- 基本单位ID
base_unit_code -- 基本单位编码（冗余）
base_unit_name -- 基本单位名称（冗余）

uom_numerator       DECIMAL(20,6) NOT NULL,           -- 换算分子（业务单位）
uom_denominator     DECIMAL(20,6) NOT NULL,           -- 换算分母（基本单位）
-- base_qty = qty * uom_denominator / uom_numerator
-- 示例：1箱=12个，则业务单位=箱，基本单位=个，建议 numerator=1, denominator=12

ordered_qty         DECIMAL(20,6) DEFAULT 0,          -- 订单数量（业务单位，冗余）
ordered_base_qty    DECIMAL(20,6) DEFAULT 0,          -- 订单数量（基本单位，冗余）

received_qty        DECIMAL(20,6) NOT NULL,           -- 本次实收数量（业务单位）
received_base_qty   DECIMAL(20,6) NOT NULL,           -- 本次实收数量（基本单位）

accepted_qty        DECIMAL(20,6) NOT NULL,           -- 本次合格数量（业务单位）
accepted_base_qty   DECIMAL(20,6) NOT NULL,           -- 本次合格数量（基本单位）

rejected_qty        DECIMAL(20,6) DEFAULT 0,          -- 本次拒收数量（业务单位）
rejected_base_qty   DECIMAL(20,6) DEFAULT 0,          -- 本次拒收数量（基本单位）

inbound_qty         DECIMAL(20,6) DEFAULT 0,          -- 已入库数量（业务单位，累计）
inbound_base_qty    DECIMAL(20,6) DEFAULT 0,          -- 已入库数量（基本单位，累计）

pending_inbound_qty      DECIMAL(20,6) DEFAULT 0,     -- 待入库数量（业务单位）= accepted_qty - inbound_qty
pending_inbound_base_qty DECIMAL(20,6) DEFAULT 0,     -- 待入库数量（基本单位）

unit_price          DECIMAL(20,6),                    -- 含税/未税单价（按你采购口径决定，建议与PO一致）
tax_rate            DECIMAL(10,4),                    -- 税率（如13.0000）
amount              DECIMAL(20,6),                    -- 金额（未税或按你系统口径）
tax_amount          DECIMAL(20,6),                    -- 税额
amount_with_tax     DECIMAL(20,6),                    -- 含税金额

item_status         VARCHAR(32) NOT NULL,             -- 行状态：OPEN/PART_INBOUND/COMPLETED/CANCELLED

remark              VARCHAR(500),                     -- 行备注

ext1                VARCHAR(200),                     -- 扩展字段1
ext2                VARCHAR(200),                     -- 扩展字段2
ext3                VARCHAR(200),                     -- 扩展字段3

version_no          BIGINT DEFAULT 0 NOT NULL,        -- 乐观锁版本号

created_at          TIMESTAMP NOT NULL,               -- 创建时间
created_by          BIGINT,                           -- 创建人ID
updated_at          TIMESTAMP NOT NULL,               -- 更新时间
updated_by          BIGINT                            -- 更新人ID
```

收货行基础公式

```text
accepted_qty = received_qty - rejected_qty
accepted_base_qty = received_base_qty - rejected_base_qty
```

待入库数量

```text
pending_inbound_qty = accepted_qty - inbound_qty
pending_inbound_base_qty = accepted_base_qty - inbound_base_qty
```

# 4、销售模块

### 销售订单

```sql
tb_sales_order
-----------
id
tenant_id

order_no -- 订单编号

customer_id -- 客户
warehouse_id -- 仓库
org_id      -- 组织

order_type -- 订单类型
order_source -- 订单来源

total_amount -- 总金额
discount_amount -- 折扣金额

status -- 状态
remark -- 备注

created_by
created_at
updated_at

```

头表 order\_status 状态：

```text
DRAFT
CONFIRMED
PART_RESERVED
PART_SHIPPED
COMPLETED
CANCELLED
CLOSED
```

### 销售订单明细

```sql
tb_sales_order_item
-
id
tenant_id

order_id -- 订单ID
sku_id  -- SKU ID
product_name -- 商品名称

unit_id -- 单位

quantity  -- 销售数量，业务单位
price -- 销售单价，业务单位
amount -- 销售金额，业务单位

warehouse_id -- 仓库
remark -- 备注

```

## 5、出入库模块

### 采购入库单

采购入库单的职责必须是：

-   引用收货单 / 收货明细
-   确认最终入库仓位（仓 / 库区 / 库位 / 容器）
-   确认最终库存状态（通常 AVAILABLE）
-   确认批次 / 序列号
-   正式更新库存
-   写库存流水
-   回写收货单已入库数量
-   更新批次库存 / 序列号库存

```sql
CREATE TABLE tb_purchase_inbound (
    id                  BIGINT PRIMARY KEY,                 -- 主键ID

    tenant_id           BIGINT NOT NULL,                   -- 租户ID
    org_id              BIGINT NOT NULL,                   -- 组织ID（入库所属组织）

    inbound_no          VARCHAR(64) NOT NULL,              -- 入库单号（业务唯一）

    inbound_type        VARCHAR(32) NOT NULL,              -- 入库类型：FROM_RECEIPT=来源收货单，DIRECT=直接入库，RETURN_BACK=退货回库等
    biz_type            VARCHAR(32) DEFAULT 'NORMAL',      -- 业务类型：NORMAL=普通采购，VMI=VMI，CONSIGNMENT=寄售等

    source_type         VARCHAR(32),                       -- 来源类型：PURCHASE_RECEIPT / NONE
    source_id           BIGINT,                            -- 来源单据ID（如收货单ID）
    source_no           VARCHAR(64),                       -- 来源单号（如收货单号）

    receipt_id          BIGINT,                            -- 收货单ID
    receipt_no          VARCHAR(64),                       -- 收货单号（冗余）

    order_id               BIGINT,                            -- 采购订单ID（冗余）
    order_no               VARCHAR(64),                       -- 采购订单号（冗余）

    supplier_id         BIGINT NOT NULL,                   -- 供应商ID
    supplier_code       VARCHAR(64),                       -- 供应商编码（冗余）
    supplier_name       VARCHAR(200),                      -- 供应商名称（冗余）

    warehouse_id        BIGINT NOT NULL,                   -- 默认目标仓库ID
    area_id             BIGINT,                            -- 默认目标库区ID
    location_id         BIGINT,                            -- 默认目标库位ID
    container_id        BIGINT,                            -- 默认目标容器ID

    owner_type          VARCHAR(32) DEFAULT 'SELF',        -- 货权类型：SELF/SUPPLIER
    owner_id            BIGINT,                            -- 货权所有者ID（VMI可为供应商ID）

    inbound_date        TIMESTAMP NOT NULL,                -- 入库业务日期
    posting_date        TIMESTAMP,                         -- 过账日期（正式入账日期）

    inbound_status      VARCHAR(32) NOT NULL,              -- 单据状态：DRAFT/CONFIRMED/POSTED/CANCELLED
    approval_status     VARCHAR(32),                       -- 审批状态（可选）
    post_status         VARCHAR(32) DEFAULT 'UNPOSTED',    -- 过账状态：UNPOSTED/POSTED

    total_inbound_qty       DECIMAL(20,6) DEFAULT 0,       -- 合计入库数量（业务单位）
    total_inbound_base_qty  DECIMAL(20,6) DEFAULT 0,       -- 合计入库数量（基本单位）

    total_amount            DECIMAL(20,6) DEFAULT 0,       -- 合计金额
    total_tax_amount        DECIMAL(20,6) DEFAULT 0,       -- 合计税额
    total_amount_with_tax   DECIMAL(20,6) DEFAULT 0,       -- 合计含税金额

    remark              VARCHAR(500),                      -- 备注

    ext1                VARCHAR(200),                      -- 扩展字段1
    ext2                VARCHAR(200),                      -- 扩展字段2
    ext3                VARCHAR(200),                      -- 扩展字段3

    version_no          BIGINT DEFAULT 0 NOT NULL,         -- 乐观锁版本号

    created_at          TIMESTAMP NOT NULL,                -- 创建时间
    created_by          BIGINT,                            -- 创建人ID
    updated_at          TIMESTAMP NOT NULL,                -- 更新时间
    updated_by          BIGINT,                            -- 更新人ID

    confirmed_at        TIMESTAMP,                         -- 确认时间（可选）
    confirmed_by        BIGINT,                            -- 确认人ID（可选）

    posted_at           TIMESTAMP,                         -- 过账时间（正式库存生效时间）
    posted_by           BIGINT,                            -- 过账人ID

    cancelled_at        TIMESTAMP,                         -- 作废时间
    cancelled_by        BIGINT                             -- 作废人ID
);
```

入库单头状态 inbound\_status：

```text
DRAFT       -- 草稿
CONFIRMED   -- 已确认（可选，如果你有确认动作）
POSTED      -- 已过账（正式入库存）
CANCELLED   -- 已作废
```

inbound\_type 建议枚举：

```text
FROM_RECEIPT   -- 来源收货单（推荐主路径）
DIRECT         -- 直接采购入库（不经过收货）
RETURN_BACK    -- 采购退货撤回回库（可选）
ADJUST_IN      -- 特殊调整入库（可选）
```

source\_type / source\_id:  
当前主路径建议：

```text
source_type = PURCHASE_RECEIPT
source_id   = receipt_id
```

这样以后也能兼容：

-   ASN 入库
-   委外入库
-   调拨回库

为什么头表也保留 warehouse\_id / location\_id ?

因为很多业务里：

-   整张单默认入同一仓位
-   明细可覆盖头表默认值

> 头表做默认值，明细做最终落地值  
> 这是 ERP/WMS 非常常见的做法。

### 采购入库明细

```sql
CREATE TABLE tb_purchase_inbound_item (
    id                  BIGINT PRIMARY KEY,                 -- 主键ID

    tenant_id           BIGINT NOT NULL,                   -- 租户ID
    org_id              BIGINT NOT NULL,                   -- 组织ID

    inbound_id          BIGINT NOT NULL,                   -- 入库单头ID
    inbound_no          VARCHAR(64) NOT NULL,              -- 入库单号（冗余）
    line_no             INT NOT NULL,                      -- 行号（单内唯一）

    source_type         VARCHAR(32),                       -- 来源类型：PURCHASE_RECEIPT_ITEM / NONE
    source_id           BIGINT,                            -- 来源头ID（可选）
    source_item_id      BIGINT,                            -- 来源明细ID（通常=receipt_item_id）

    receipt_id          BIGINT,                            -- 收货单ID
    receipt_item_id     BIGINT,                            -- 收货明细ID
    receipt_no          VARCHAR(64),                       -- 收货单号（冗余）
    receipt_line_no     INT,                               -- 收货单行号（冗余）

    order_id               BIGINT,                            -- 采购订单ID
    order_item_id          BIGINT,                            -- 采购订单明细ID
    order_no               VARCHAR(64),                       -- 采购订单号（冗余）
    order_line_no          INT,                               -- 采购订单行号（冗余）

    warehouse_id        BIGINT NOT NULL,                   -- 目标仓库ID
    area_id             BIGINT,                            -- 目标库区ID
    location_id         BIGINT,                            -- 目标库位ID
    container_id        BIGINT,                            -- 目标容器ID

    owner_type          VARCHAR(32) DEFAULT 'SELF',        -- 货权类型：SELF/SUPPLIER
    owner_id            BIGINT,                            -- 货权所有者ID

    sku_id              BIGINT NOT NULL,                   -- SKU ID
    sku_code            VARCHAR(64),                       -- SKU编码（冗余）
    sku_name            VARCHAR(200),                      -- SKU名称（冗余）
    sku_spec            VARCHAR(200),                      -- SKU规格（冗余）

    is_batch_managed    BOOLEAN DEFAULT FALSE,             -- 是否批次管理
    is_serial_managed   BOOLEAN DEFAULT FALSE,             -- 是否序列号管理

    batch_no            VARCHAR(64),                       -- 批次号（简单模式）
    serial_no           VARCHAR(128),                      -- 序列号（简单模式）

    mfg_date            DATE,                              -- 生产日期
    expiry_date         DATE,                              -- 失效日期/有效期至

    quality_status      VARCHAR(32),                       -- 最终质量状态：GOOD/HOLD/REJECT
    inventory_status    VARCHAR(32) NOT NULL,             -- 最终库存状态：AVAILABLE/INSPECTION/HOLD/BLOCKED

    uom_id              BIGINT NOT NULL,                   -- 业务单位ID
    uom_code            VARCHAR(32),                       -- 业务单位编码（冗余）
    uom_name            VARCHAR(64),                       -- 业务单位名称（冗余）

    base_unit_id        BIGINT NOT NULL,                   -- 基本单位ID
    base_unit_code      VARCHAR(32),                       -- 基本单位编码（冗余）
    base_unit_name      VARCHAR(64),                       -- 基本单位名称（冗余）

    uom_numerator       DECIMAL(20,6) NOT NULL,           -- 换算分子
    uom_denominator     DECIMAL(20,6) NOT NULL,           -- 换算分母

    receipt_qty         DECIMAL(20,6) DEFAULT 0,          -- 来源收货数量（业务单位，冗余）
    receipt_base_qty    DECIMAL(20,6) DEFAULT 0,          -- 来源收货数量（基本单位，冗余）

    inbound_qty         DECIMAL(20,6) NOT NULL,           -- 本次入库数量（业务单位）
    inbound_base_qty    DECIMAL(20,6) NOT NULL,           -- 本次入库数量（基本单位）

    unit_price          DECIMAL(20,6),                    -- 单价（与PO/收货保持一致）
    tax_rate            DECIMAL(10,4),                    -- 税率
    amount              DECIMAL(20,6),                    -- 金额
    tax_amount          DECIMAL(20,6),                    -- 税额
    amount_with_tax     DECIMAL(20,6),                    -- 含税金额

    item_status         VARCHAR(32) NOT NULL,             -- 行状态：OPEN/POSTED/CANCELLED

    inventory_log_id    BIGINT,                           -- 主库存流水ID（可选，指向本次入库主流水）
    inventory_id        BIGINT,                           -- 目标库存ID（可选，过账后回填）
    batch_id            BIGINT,                           -- 目标批次库存ID（可选，过账后回填）
    serial_id           BIGINT,                           -- 目标序列号库存ID（可选，过账后回填，单SN场景）

    remark              VARCHAR(500),                     -- 备注

    ext1                VARCHAR(200),                     -- 扩展字段1
    ext2                VARCHAR(200),                     -- 扩展字段2
    ext3                VARCHAR(200),                     -- 扩展字段3

    version_no          BIGINT DEFAULT 0 NOT NULL,        -- 乐观锁版本号

    created_at          TIMESTAMP NOT NULL,               -- 创建时间
    created_by          BIGINT,                           -- 创建人ID
    updated_at          TIMESTAMP NOT NULL,               -- 更新时间
    updated_by          BIGINT                            -- 更新人ID
);
```

一条收货明细可以拆成多次入库， 这是标准场景：

-   收到 100
-   先入库 60
-   后入库 40

所以关系是：

```text
tb_purchase_receipt_item (1)
    ↓
tb_purchase_inbound_item (N)
```

入库过账总体流程:

```text
采购入库单 POST
    ↓
逐行处理 tb_purchase_inbound_item
    ↓
1. 更新 tb_inventory
2. 写 tb_inventory_log
3. 更新 tb_inventory_batch（如批次管理）
4. 更新 tb_inventory_serial（如序列号管理）
5. 回写 tb_purchase_receipt_item
6. 汇总回写 tb_purchase_receipt
7. 更新本单状态为 POSTED
```

步骤5：回写 tb\_purchase\_receipt\_item

这是分离模式最关键的回写。

对来源收货明细：

```text
inbound_qty      += 本次 inbound_qty
inbound_base_qty += 本次 inbound_base_qty

pending_inbound_qty      = accepted_qty - inbound_qty
pending_inbound_base_qty = accepted_base_qty - inbound_base_qty
```

明细状态更新：

```text
if inbound_qty = 0:
    OPEN

if 0 < inbound_qty < accepted_qty:
    PART_INBOUND

if inbound_qty = accepted_qty:
    COMPLETED
```

步骤6：回写 tb\_purchase\_receipt 头表

汇总所有明细：

```text
total_inbound_qty
total_inbound_base_qty
total_pending_inbound_qty
total_pending_inbound_base_qty
```

头表状态更新：

```text
如果全部明细 COMPLETED:
    receipt_status = COMPLETED

如果存在 PART_INBOUND:
    receipt_status = PART_INBOUND

如果都还未入库:
    receipt_status = CONFIRMED
```

### 出库单

```sql
CREATE TABLE tb_inventory_outbound (
    id BIGINT PRIMARY KEY COMMENT '主键ID',

    tenant_id BIGINT NOT NULL COMMENT '租户ID',
    org_id BIGINT NOT NULL COMMENT '组织ID/库存组织',

    outbound_no VARCHAR(64) NOT NULL COMMENT '出库单号',

    outbound_type VARCHAR(32) NOT NULL COMMENT '出库类型：NORMAL/RETURN/TRANSFER/ADJUST',
    biz_type VARCHAR(32) NOT NULL COMMENT '业务类型：SALES_SHIP/PROD_PICK/TRANSFER_OUT/PURCHASE_RETURN/SCRAP_OUT/ADJUST_OUT等',

    source_type VARCHAR(32) NULL COMMENT '来源单据类型：SO_DELIVERY/PROD_PICK_REQ/TRANSFER_ORDER/PURCHASE_RETURN_REQ等',
    source_id BIGINT NULL COMMENT '来源单据ID',
    source_no VARCHAR(64) NULL COMMENT '来源单号',

    warehouse_id BIGINT NOT NULL COMMENT '出库仓库ID',

    owner_type VARCHAR(32) NULL COMMENT '货权类型：SELF/VMI/CONSIGNMENT',
    owner_id BIGINT NULL COMMENT '货权方ID（如供应商/客户/本公司）',

    customer_id BIGINT NULL COMMENT '客户ID（销售发货场景）',
    customer_code VARCHAR(64) NULL COMMENT '客户编码',
    customer_name VARCHAR(128) NULL COMMENT '客户名称',

    supplier_id BIGINT NULL COMMENT '供应商ID（采购退货/VMI退回场景）',
    supplier_code VARCHAR(64) NULL COMMENT '供应商编码',
    supplier_name VARCHAR(128) NULL COMMENT '供应商名称',

    department_id BIGINT NULL COMMENT '领用部门ID（生产领料/办公领用等）',
    department_code VARCHAR(64) NULL COMMENT '领用部门编码',
    department_name VARCHAR(128) NULL COMMENT '领用部门名称',

    out_date DATETIME NOT NULL COMMENT '出库业务日期',
    posting_date DATETIME NULL COMMENT '过账日期（正式扣库存时间）',

    outbound_status VARCHAR(32) NOT NULL DEFAULT 'DRAFT' COMMENT '单据状态：DRAFT/CONFIRMED/POSTED/CANCELLED',
    post_status VARCHAR(32) NOT NULL DEFAULT 'UNPOSTED' COMMENT '过账状态：UNPOSTED/POSTED',

    total_out_qty DECIMAL(20,6) NOT NULL DEFAULT 0 COMMENT '出库总数量（业务单位合计）',
    total_out_base_qty DECIMAL(20,6) NOT NULL DEFAULT 0 COMMENT '出库总数量（基本单位合计）',

    remark VARCHAR(500) NULL COMMENT '备注',

    version_no INT NOT NULL DEFAULT 0 COMMENT '乐观锁版本号',

    created_at DATETIME NOT NULL COMMENT '创建时间',
    created_by BIGINT NOT_
```

出库单的业务类型biz\_type:

```text
SALES_SHIP        -- 销售发货
PROD_PICK         -- 生产领料
TRANSFER_OUT      -- 调拨出库
PURCHASE_RETURN   -- 采购退货（退供应商）
SCRAP_OUT         -- 报废出库
ADJUST_OUT        -- 库存调整出库
BORROW_OUT        -- 借出
SAMPLE_OUT        -- 样品出库
OTHER_OUT         -- 其他出库
```

outbound\_type 建议枚举：

```text
NORMAL        -- 普通出库
RETURN        -- 退货出库
TRANSFER      -- 调拨出库
ADJUST        -- 调整出库
```

头表状态 outbound\_status:

```text
DRAFT        -- 草稿
CONFIRMED    -- 已确认/已审核
POSTED       -- 已过账（正式扣库存）
CANCELLED    -- 已作废
```

明细状态 item\_status:

```text
OPEN         -- 未过账
POSTED       -- 已过账
CANCELLED    -- 已取消
```

### 出库明细

```sql
CREATE TABLE tb_inventory_outbound_item (
    id BIGINT PRIMARY KEY COMMENT '主键ID',

    tenant_id BIGINT NOT NULL COMMENT '租户ID',
    org_id BIGINT NOT NULL COMMENT '组织ID/库存组织',

    outbound_id BIGINT NOT NULL COMMENT '出库单ID',
    outbound_no VARCHAR(64) NOT NULL COMMENT '出库单号（冗余）',
    line_no INT NOT NULL COMMENT '行号',

    source_type VARCHAR(32) NULL COMMENT '来源单据类型',
    source_id BIGINT NULL COMMENT '来源单据ID',
    source_item_id BIGINT NULL COMMENT '来源单据明细ID',
    source_no VARCHAR(64) NULL COMMENT '来源单号',
    source_line_no INT NULL COMMENT '来源行号',

    warehouse_id BIGINT NOT NULL COMMENT '出库仓库ID',
    area_id BIGINT NULL COMMENT '出库库区ID',
    location_id BIGINT NULL COMMENT '出库库位ID',
    container_id BIGINT NULL COMMENT '出库容器ID',

    owner_type VARCHAR(32) NULL COMMENT '货权类型：SELF/VMI/CONSIGNMENT',
    owner_id BIGINT NULL COMMENT '货权方ID',

    sku_id BIGINT NOT NULL COMMENT '商品SKU ID',
    sku_code VARCHAR(64) NOT NULL COMMENT '商品SKU编码',
    sku_name VARCHAR(128) NOT NULL COMMENT '商品名称',
    sku_spec VARCHAR(256) NULL COMMENT '规格型号',

    is_batch_managed TINYINT NOT NULL DEFAULT 0 COMMENT '是否批次管理：0否1是',
    is_serial_managed TINYINT NOT NULL DEFAULT 0 COMMENT '是否序列号管理：0否1是',

    batch_no VARCHAR(64) NULL COMMENT '批次号（第一阶段可直接放明细行；多批次建议拆子表）',
    serial_no VARCHAR(128) NULL COMMENT '序列号（单SN场景可直接放明细行；多SN建议拆子表）',

    mfg_date DATE NULL COMMENT '生产日期',
    expiry_date DATE NULL COMMENT '失效日期/有效期至',

    quality_status VARCHAR(32) NULL COMMENT '质量状态：GOOD/HOLD/REJECT等',
    inventory_status VARCHAR(32) NULL COMMENT '库存状态：AVAILABLE/INSPECTION/LOCKED/DAMAGED等',

    reservation_id BIGINT NULL COMMENT '关联预占记录ID（若由预占释放后出库）',

    uom_id BIGINT NOT NULL COMMENT '业务单位ID',
    uom_code VARCHAR(32) NOT NULL COMMENT '业务单位编码',
    uom_name VARCHAR(32) NOT NULL COMMENT '业务单位名称',

    base_unit_id BIGINT NOT NULL COMMENT '基本单位ID',
    base_unit_code VARCHAR(32) NOT NULL COMMENT '基本单位编码',
    base_unit_name VARCHAR(32) NOT NULL COMMENT '基本单位名称',

    uom_numerator DECIMAL(20,8) NOT NULL DEFAULT 1 COMMENT '换算分子（业务单位→基本单位）',
    uom_denominator DECIMAL(20,8) NOT NULL DEFAULT 1 COMMENT '换算分母（业务单位→基本单位）',

    request_qty DECIMAL(20,6) NOT NULL DEFAULT 0 COMMENT '需求数量/来源需求数量（业务单位）',
    request_base_qty DECIMAL(20,6) NOT NULL DEFAULT 0 COMMENT '需求数量（基本单位）',

    out_qty DECIMAL(20,6) NOT NULL DEFAULT 0 COMMENT '本次出库数量（业务单位）',
    out_base_qty DECIMAL(20,6) NOT NULL DEFAULT 0 COMMENT '本次出库数量（基本单位）',

    unit_cost DECIMAL(20,6) NULL COMMENT '单位成本（按基本单位或业务单位，需统一口径）',
    total_cost DECIMAL(20,6) NULL COMMENT '出库成本金额',

    item_status VARCHAR(32) NOT NULL DEFAULT 'OPEN' COMMENT '行状态：OPEN/POSTED/CANCELLED',

    inventory_log_id BIGINT NULL COMMENT '正式过账后对应的主库存流水ID（可选）',

    remark VARCHAR(500) NULL COMMENT '备注',

    version_no INT NOT NULL DEFAULT 0 COMMENT '乐观锁版本号',

    created_at DATETIME NOT NULL COMMENT '创建时间',
    created_by BIGINT NOT NULL COMMENT '创建人ID',
    updated_at DATETIME NOT NULL COMMENT '更新时间',
    updated_by BIGINT NOT NULL COMMENT '更新人ID'
) COMMENT='库存出库单明细';
```

为什么要保留 request\_qty ? 因为很多业务场景：

-   申请领料 100
-   实际拣货 98
-   实际出库 96

所以推荐保留：

-   request\_qty —— 来源需求
-   out\_qty —— 实际出库

出库单和库存表的关系:  
**过账前**

-   tb\_inventory\_outbound / item 只是业务单
-   不改库存

**过账后**  
正式执行：

1）扣减 tb\_inventory

按库存维度扣减：

-   quantity -= out\_base\_qty
    
-   available\_qty -= out\_base\_qty（通常）
    
-   若先有预占：
    
    -   reserved\_qty -= out\_base\_qty
    -   quantity -= out\_base\_qty
    -   available\_qty 可能不再额外减（取决于你的可用库存维护策略）

### 调拨单（tb\_stock\_transfer）

库存调拨单用于：

-   仓库间调拨：库存从仓库A → 仓库B
-   组织间调拨：跨部门、跨分公司调拨
-   库存在途管理：调拨过程中库存状态不同于可用库存

特点：

-   主表：记录调拨单信息（单号、源仓、目标仓、状态）
-   明细表：记录每个 SKU 的调拨数量、单位、批次等信息

主表：tb\_stock\_transfer

```sql
tb_stock_transfer
---------------
CREATE TABLE tb_stock_transfer (
    id                  BIGINT PRIMARY KEY,
    
    -- 多租户
    tenant_id           BIGINT NOT NULL,
    
    -- 单据基础
    transfer_no         VARCHAR(50) NOT NULL,              -- 调拨单号
    transfer_type       VARCHAR(20) NOT NULL,              -- 调拨类型：warehouse / location / org / virtual
    biz_type            VARCHAR(30) DEFAULT 'normal',      -- 业务类型：normal / return / replenish / allocate
    
    -- 组织维度（如果你的ERP是流程中心，建议保留）
    org_id              BIGINT NULL,                       -- 所属组织
    dept_id             BIGINT NULL,                       -- 所属部门
    
    -- 来源 / 目标 仓
    from_warehouse_id   BIGINT NOT NULL,                  -- 源仓库
    to_warehouse_id     BIGINT NOT NULL,                  -- 目标仓库
    
    -- 如果支持仓内库位调拨，可选
    from_owner_id       BIGINT NULL,                       -- 源货主（可选，第三方仓储/寄售场景）
    to_owner_id         BIGINT NULL,                       -- 目标货主（可选）
    
    -- 单据状态
    bill_status         VARCHAR(20) NOT NULL DEFAULT 'draft', 
    -- draft 草稿
    -- submitted 已提交
    -- approved 已审核
    -- executing 执行中
    -- completed 已完成
    -- cancelled 已作废
    -- closed 已关闭
    
    -- 执行状态（建议和单据状态拆开）
    execute_status      VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending 未执行
    -- partial 部分执行
    -- done 已完成
    -- reversed 已冲销
    
    -- 日期
    biz_date            TIMESTAMP NOT NULL,               -- 业务日期
    expected_date       TIMESTAMP NULL,                   -- 期望调拨日期
    approved_at         TIMESTAMP NULL,                   -- 审核时间
    completed_at        TIMESTAMP NULL,                   -- 完成时间
    
    -- 汇总字段（方便列表展示/统计）
    total_qty           DECIMAL(18,6) NOT NULL DEFAULT 0, -- 总数量（基本单位或交易单位，建议统一定义）
    total_amount        DECIMAL(18,6) NOT NULL DEFAULT 0, -- 总金额（可选）
    item_count          INT NOT NULL DEFAULT 0,           -- 明细行数
    
    -- 关联单据
    source_bill_type    VARCHAR(30) NULL,                 -- 来源单据类型
    source_bill_id      BIGINT NULL,                      -- 来源单据ID
    source_bill_no      VARCHAR(50) NULL,                 -- 来源单据号
    
    -- 备注
    remark              VARCHAR(500) NULL,
    
    -- 乐观锁（推荐）
    version             INT NOT NULL DEFAULT 0,
    
    -- 审计字段
    created_by          BIGINT NULL,
    created_name        VARCHAR(50) NULL,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    updated_by          BIGINT NULL,
    updated_name        VARCHAR(50) NULL,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    approved_by         BIGINT NULL,
    approved_name       VARCHAR(50) NULL,
    
    is_deleted          SMALLINT NOT NULL DEFAULT 0
);
```

bill\_status 设计：

```text
draft：草稿
submitted：已提交
approved：已审核
executing：执行中
completed：已完成
cancelled：已作废
closed：已关闭
```

execute\_status 设计：

```text
pending：未执行
partial：部分执行
done：已完成
reversed：已冲销
```

为什么要拆两个状态？因为：

-   审核状态 ≠ 库存执行状态

例如：

-   单据已审核，但仓库还没开始调拨
-   已审核，部分明细先调拨
-   已审核，后续撤销一部分

所以建议：

-   bill\_status：流程控制
-   execute\_status：库存控制

### 调拨单明细表：tb\_stock\_transfer\_item

```sql
tb_stock_transfer_item
------------------
CREATE TABLE tb_stock_transfer_item (
    id                      BIGINT PRIMARY KEY,
    
    -- 多租户
    tenant_id               BIGINT NOT NULL,
    
    -- 主表关联
    transfer_id             BIGINT NOT NULL,
    line_no                 INT NOT NULL,                       -- 行号
    
    -- 物料信息
    sku_id                  BIGINT NOT NULL,                    -- SKU/物料ID
    sku_code                VARCHAR(50) NOT NULL,
    sku_name                VARCHAR(200) NOT NULL,
    spec                    VARCHAR(200) NULL,
    model                   VARCHAR(100) NULL,
    
    -- 单位
    unit_id                 BIGINT NULL,                        -- 交易单位
    unit_name               VARCHAR(50) NULL,
    base_unit_id            BIGINT NULL,                        -- 基本单位
    base_unit_name          VARCHAR(50) NULL,
    unit_rate               DECIMAL(18,6) NOT NULL DEFAULT 1,   -- 单位换算率
    
    -- 数量（建议同时保留交易单位与基本单位）
    qty                     DECIMAL(18,6) NOT NULL,             -- 调拨数量（交易单位）
    base_qty                DECIMAL(18,6) NOT NULL,             -- 调拨数量（基本单位）
    
    -- 已执行数量（支持部分执行）
    executed_qty            DECIMAL(18,6) NOT NULL DEFAULT 0,   -- 已执行数量（交易单位）
    executed_base_qty       DECIMAL(18,6) NOT NULL DEFAULT 0,   -- 已执行数量（基本单位）
    
    -- 单价金额（可选）
    unit_price              DECIMAL(18,6) NOT NULL DEFAULT 0,   -- 成本单价/参考单价
    amount                  DECIMAL(18,6) NOT NULL DEFAULT 0,   -- 金额
    
    -- 库位信息（支持仓内/跨仓更精细调拨）
    from_location_id        BIGINT NULL,                        -- 源库位
    to_location_id          BIGINT NULL,                        -- 目标库位
    
    -- 库存属性（如需精细库存）
    lot_no                  VARCHAR(100) NULL,                  -- 批次号
    production_date         DATE NULL,                          -- 生产日期
    expire_date             DATE NULL,                          -- 失效日期
    
    -- 序列号模式（高值物料）
    sn_required             SMALLINT NOT NULL DEFAULT 0,        -- 是否启用序列号
    
    -- 货主 / 库存维度（可选）
    from_owner_id           BIGINT NULL,
    to_owner_id             BIGINT NULL,
    
    -- 行状态
    line_status             VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending / partial / done / cancelled
    
    -- 来源明细（方便追溯）
    source_item_id          BIGINT NULL,
    source_bill_type        VARCHAR(30) NULL,
    source_bill_id          BIGINT NULL,
    
    -- 备注
    remark                  VARCHAR(500) NULL,
    
    -- 审计
    created_by              BIGINT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by              BIGINT NULL,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    is_deleted              SMALLINT NOT NULL DEFAULT 0
);
```

业务逻辑流程:

1 创建调拨单（draft）

-   录入源仓库、目标仓库、SKU及数量
-   状态：draft

2 提交调拨单（submitted）

-   检查源仓库存是否足够
-   可以冻结源仓库存（预占）

3 审核调拨单（approved）

-   更新库存状态：
-   源仓：扣减可用库存（可用库存 - 调拨数量）
-   目标仓：增加在途库存（在途库存 + 调拨数量）

4 入库确认（optional）

-   目标仓确认收货
-   在途库存 → 可用库存
-   写库存流水 inventory\_log

调拨中库存通常有三种状态：

| 状态 | 说明 |
| --- | --- |
| 可用库存 | 可以销售/出库 |
| 锁定/预占库存 | 调拨、销售占用 |
| 在途库存 | 调拨未到目标仓库，暂不算可用库存 |

调拨单执行时：

```text
源仓：
可用库存 -= base_quantity
锁定库存 += base_quantity（可选）

目标仓：
在途库存 += base_quantity
```

调拨单据状态设计：

```text
DRAFT      -- 草稿
SUBMITTED  -- 提交
APPROVED   -- 审核
SHIPPED    -- 出库
RECEIVED   -- 收货
CANCELED   -- 取消
```

调拨类型(transfer\_type)设计:

| 值 | 说明 |
| --- | --- |
| INTERNAL | 同组织调拨 |
| CROSS\_ORG | 跨组织调拨 |
| TEMP | 临时借用/返还 |

典型 ERP 调拨流程示意:

```text
stock_transfer (调拨单)
      │
      ▼
stock_transfer_item (明细)
      │
      ▼
冻结源仓库存 / 增加在途库存
      │
      ▼
目标仓确认收货
      │
      ▼
在途库存 → 可用库存
      │
      ▼
写 inventory_log（流水）
```

调拨业务如何处理,在途库存。  
例如：上海仓库存 100， 调拨 30 到 北京仓。

***调出仓库***：  
on\_hand\_qty -= 30  
上海仓：库存 = 70

***调入仓库***：  
in\_transit\_qty += 30  
北京仓：在途库存 = 30

***到货确认***：  
北京仓收货：

```sql
in_transit_qty -= 30
on_hand_qty += 30
```

北京仓：  
库存 = 30  
在途库存 = 0

***库存流水记录***：

| 仓库 | 变化 | 类型 |
| --- | --- | --- |
| 上海仓 | \-30 | TRANSFER\_OUT |
| 北京仓 | +30 | TRANSFER\_IN |

### 盘点单（tb\_stock\_check）

用于 库存盘点：系统库存 vs 实际库存  
库存盘点单用于：

-   定期盘点：按计划对仓库、库位或商品进行盘点
-   差异调整：发现库存差异后，生成 stock\_adjust 调整单
-   库存核对：确保账面库存与实际库存一致

特点：

-   主表：记录盘点单信息（盘点时间、仓库、状态）
-   明细表：记录每个 SKU 的盘点结果（实际库存、系统库存、差异）

主表：tb\_stock\_check

```sql
tb_stock_check
------------
CREATE TABLE tb_stock_check (
    id                      BIGINT PRIMARY KEY,

    -- 多租户
    tenant_id               BIGINT NOT NULL,

    -- 单据基础
    check_no                VARCHAR(50) NOT NULL,                -- 盘点单号
    check_type              VARCHAR(20) NOT NULL DEFAULT 'full', -- full全盘 / cycle循环 / random抽盘 / spot动态盘
    biz_type                VARCHAR(30) NOT NULL DEFAULT 'normal',

    -- 组织维度（建议保留）
    org_id                  BIGINT NULL,
    dept_id                 BIGINT NULL,

    -- 盘点范围
    warehouse_id            BIGINT NOT NULL,                     -- 盘点仓库
    owner_id                BIGINT NULL,                         -- 货主（第三方仓/寄售）
    area_id                 BIGINT NULL,                         -- 库区（可选）
    location_id             BIGINT NULL,                         -- 指定库位（可选，单库位盘点）

    -- 盘点模式
    scope_type              VARCHAR(20) NOT NULL DEFAULT 'warehouse',
    -- warehouse 按仓
    -- area 按库区
    -- location 按库位
    -- sku 按SKU
    -- category 按品类
    -- custom 自定义范围

    check_mode              VARCHAR(20) NOT NULL DEFAULT 'blind',
    -- blind 盲盘（不显示账面）
    -- visible 明盘（显示账面）
    -- recount 复盘

    -- 是否冻结库存
    freeze_mode             VARCHAR(20) NOT NULL DEFAULT 'none',
    -- none 不冻结
    -- soft 软冻结（禁止出入库业务）
    -- hard 硬冻结（严格锁库存）

    -- 单据状态
    bill_status             VARCHAR(20) NOT NULL DEFAULT 'draft',
    -- draft 草稿
    -- submitted 已提交
    -- counting 盘点中
    -- counted 已盘点
    -- approved 已审核
    -- completed 已完成
    -- cancelled 已作废
    -- closed 已关闭

    execute_status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending 未处理
    -- partial 部分处理
    -- done 已完成
    -- reversed 已冲销

    -- 日期
    biz_date                TIMESTAMP NOT NULL,                  -- 业务日期
    start_time              TIMESTAMP NULL,                      -- 开始盘点时间
    end_time                TIMESTAMP NULL,                      -- 结束盘点时间
    approved_at             TIMESTAMP NULL,
    completed_at            TIMESTAMP NULL,

    -- 汇总（非常有用）
    item_count              INTEGER NOT NULL DEFAULT 0,          -- 明细行数
    counted_item_count      INTEGER NOT NULL DEFAULT 0,          -- 已录入实盘行数
    profit_item_count       INTEGER NOT NULL DEFAULT 0,          -- 盘盈行数
    loss_item_count         INTEGER NOT NULL DEFAULT 0,          -- 盘亏行数

    total_book_qty          NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 账面总数
    total_actual_qty        NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 实盘总数
    total_diff_qty          NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 差异总数（实盘-账面）

    total_profit_qty        NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 盘盈总数
    total_loss_qty          NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 盘亏总数

    total_profit_amount     NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 盘盈金额
    total_loss_amount       NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 盘亏金额

    -- 来源（可选）
    source_bill_type        VARCHAR(30) NULL,
    source_bill_id          BIGINT NULL,
    source_bill_no          VARCHAR(50) NULL,

    -- 盘点说明
    remark                  VARCHAR(500) NULL,

    -- 乐观锁
    version                 INTEGER NOT NULL DEFAULT 0,

    -- 审计
    created_by              BIGINT NULL,
    created_name            VARCHAR(50) NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_by              BIGINT NULL,
    updated_name            VARCHAR(50) NULL,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    approved_by             BIGINT NULL,
    approved_name           VARCHAR(50) NULL,

    is_deleted              SMALLINT NOT NULL DEFAULT 0
);
```

盘点类型check\_type：FULL（全盘）、PART（抽盘）、SKU（指定商品）  
主表状态 bill\_status :

```text
draft：草稿
submitted：已提交
counting：盘点中
counted：已盘点（全部录完）
approved：已审核
completed：已完成（已生成调整）
cancelled：已作废
closed：已关闭
```

明细表：tb\_stock\_check\_item

盘点明细表的本质是：

> “盘点时刻的库存快照 + 实盘结果 + 差异结果”

所以明细表里一定要有：

-   账面数量（快照）
-   实盘数量
-   差异数量
-   差异方向（盈/亏/平）

```sql
tb_stock_check_item
----------------
CREATE TABLE tb_stock_check_item (
    id                          BIGINT PRIMARY KEY,

    -- 多租户
    tenant_id                   BIGINT NOT NULL,

    -- 主表关联
    check_id                    BIGINT NOT NULL,
    line_no                     INTEGER NOT NULL,

    -- 库存维度（非常关键）
    warehouse_id                BIGINT NOT NULL,
    owner_id                    BIGINT NULL,
    area_id                     BIGINT NULL,
    location_id                 BIGINT NULL,

    -- 物料
    sku_id                      BIGINT NOT NULL,
    sku_code                    VARCHAR(50) NOT NULL,
    sku_name                    VARCHAR(200) NOT NULL,
    spec                        VARCHAR(200) NULL,
    model                       VARCHAR(100) NULL,

    -- 单位
    unit_id                     BIGINT NULL,                        -- 交易单位/展示单位
    unit_name                   VARCHAR(50) NULL,
    base_unit_id                BIGINT NULL,
    base_unit_name              VARCHAR(50) NULL,
    unit_rate                   NUMERIC(18,6) NOT NULL DEFAULT 1,

    -- 批次/库存属性
    lot_no                      VARCHAR(100) NULL,
    production_date             DATE NULL,
    expire_date                 DATE NULL,

    -- 库存快照（账面）
    book_qty                    NUMERIC(18,6) NOT NULL DEFAULT 0,   -- 账面数量（交易单位）
    book_base_qty               NUMERIC(18,6) NOT NULL DEFAULT 0,   -- 账面数量（基本单位）

    -- 实盘
    actual_qty                  NUMERIC(18,6) NULL,                 -- 实盘数量（交易单位）
    actual_base_qty             NUMERIC(18,6) NULL,                 -- 实盘数量（基本单位）

    -- 差异（实盘 - 账面）
    diff_qty                    NUMERIC(18,6) NOT NULL DEFAULT 0,
    diff_base_qty               NUMERIC(18,6) NOT NULL DEFAULT 0,

    -- 差异分类
    diff_type                   VARCHAR(20) NOT NULL DEFAULT 'equal',
    -- equal 一致
    -- profit 盘盈
    -- loss 盘亏

    -- 成本 / 金额（建议保留）
    unit_cost                   NUMERIC(18,6) NOT NULL DEFAULT 0,   -- 成本单价（快照时）
    diff_amount                 NUMERIC(18,6) NOT NULL DEFAULT 0,   -- 差异金额

    -- 盘点状态
    line_status                 VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending 未盘
    -- counted 已录入
    -- confirmed 已确认
    -- adjusted 已调整
    -- cancelled 已取消

    -- 是否需要复盘
    recount_flag                SMALLINT NOT NULL DEFAULT 0,
    recount_qty                 NUMERIC(18,6) NULL,
    recount_base_qty            NUMERIC(18,6) NULL,

    -- 复盘后最终值（可选，但很实用）
    final_qty                   NUMERIC(18,6) NULL,
    final_base_qty              NUMERIC(18,6) NULL,

    -- 是否盲盘时隐藏账面
    is_blind_visible            SMALLINT NOT NULL DEFAULT 0,

    -- 序列号控制
    sn_required                 SMALLINT NOT NULL DEFAULT 0,

    -- 来源库存记录（强烈建议保留）
    stock_balance_id            BIGINT NULL,                         -- 来源库存余额记录ID（如果有）
    
    -- 盘点人信息（行级，支持多人盘点）
    checked_by                  BIGINT NULL,
    checked_name                VARCHAR(50) NULL,
    checked_at                  TIMESTAMP NULL,

    confirmed_by                BIGINT NULL,
    confirmed_name              VARCHAR(50) NULL,
    confirmed_at                TIMESTAMP NULL,

    -- 备注
    remark                      VARCHAR(500) NULL,

    -- 审计
    created_by                  BIGINT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by                  BIGINT NULL,
    updated_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    is_deleted                  SMALLINT NOT NULL DEFAULT 0
);
```

明细状态 line\_status:

```text
pending：未盘
counted：已录入
confirmed：已确认
adjusted：已调整
cancelled：已取消
```

1）创建盘点单

-   指定仓库 / 库区 / 库位 / SKU范围
    
-   生成盘点明细（从 tb\_stock\_balance 快照）
    
-   填充：
    
    -   book\_qty
    -   book\_base\_qty
    -   unit\_cost

盘点录入:

-   仓库人员录入 actual\_qty
    
-   系统自动计算：
    
    -   actual\_base\_qty
    -   diff\_qty = actual\_qty - book\_qty
    -   diff\_base\_qty = actual\_base\_qty - book\_base\_qty
    -   diff\_type

**业务逻辑流程**:

1 创建盘点单

-   按仓库/库位/商品生成盘点任务
-   状态：draft
-   可以录入盘点明细（sku、系统数量、实盘数量）

2 提交盘点单

-   状态变为 submitted
-   不能修改明细

3 审核盘点单

-   状态变为 approved
-   系统生成 stock\_adjust 调整单处理差异

4 更新库存

-   审核后，差异数量通过 stock\_adjust 调整库存
-   写入 inventory\_log

盘点类型设计:

| 类型 | 说明 |
| --- | --- |
| FULL | 全仓库盘点，全部商品逐一盘点 |
| PART | 抽盘，仅盘点部分 SKU |
| SKU | 指定 SKU 盘点 |

### 库存调整单（tb\_stock\_adjust）

库存调整单（tb\_stock\_adjust）用于处理 非正常库存变动，例如：

-   盘点差异调整
-   手工库存修正
-   损耗 / 报废
-   初始化库存

主表：tb\_stock\_adjust

```sql
tb_stock_adjust
------------

CREATE TABLE tb_stock_adjust (
    id                      BIGINT PRIMARY KEY,

    -- 多租户
    tenant_id               BIGINT NOT NULL,

    -- 单据基础
    adjust_no               VARCHAR(50) NOT NULL,                    -- 调整单号
    adjust_type             VARCHAR(20) NOT NULL DEFAULT 'qty',      -- qty数量调整 / attr属性调整 / mixed混合
    biz_type                VARCHAR(30) NOT NULL DEFAULT 'normal',   -- normal / check_diff / import_fix / manual_fix / system_fix

    -- 组织维度
    org_id                  BIGINT NULL,
    dept_id                 BIGINT NULL,

    -- 调整范围（主表建议至少保留仓库）
    warehouse_id            BIGINT NOT NULL,                         -- 默认调整仓库（明细可覆盖）
    owner_id                BIGINT NULL,                             -- 默认货主（明细可覆盖）

    -- 调整模式
    adjust_mode             VARCHAR(20) NOT NULL DEFAULT 'delta',
    -- delta  差量调整（直接给差值）
    -- target 定量调整（给调整后数量）
    -- mixed  混合模式（按行决定）

    -- 单据状态
    bill_status             VARCHAR(20) NOT NULL DEFAULT 'draft',
    -- draft 草稿
    -- submitted 已提交
    -- approved 已审核
    -- executing 执行中
    -- completed 已完成
    -- cancelled 已作废
    -- closed 已关闭

    execute_status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending / partial / done / reversed

    -- 日期
    biz_date                TIMESTAMP NOT NULL,
    approved_at             TIMESTAMP NULL,
    completed_at            TIMESTAMP NULL,

    -- 汇总字段
    item_count              INTEGER NOT NULL DEFAULT 0,
    inc_item_count          INTEGER NOT NULL DEFAULT 0,              -- 增加行数
    dec_item_count          INTEGER NOT NULL DEFAULT 0,              -- 减少行数
    zero_item_count         INTEGER NOT NULL DEFAULT 0,              -- 不变行数（通常不建议保留）

    total_adjust_qty        NUMERIC(18,6) NOT NULL DEFAULT 0,        -- 调整数量净值（可正可负）
    total_increase_qty      NUMERIC(18,6) NOT NULL DEFAULT 0,        -- 增加总量
    total_decrease_qty      NUMERIC(18,6) NOT NULL DEFAULT 0,        -- 减少总量

    total_adjust_amount     NUMERIC(18,6) NOT NULL DEFAULT 0,        -- 调整金额净值
    total_increase_amount   NUMERIC(18,6) NOT NULL DEFAULT 0,        -- 增加金额
    total_decrease_amount   NUMERIC(18,6) NOT NULL DEFAULT 0,        -- 减少金额

    -- 来源
    source_bill_type        VARCHAR(30) NULL,                        -- stock_check / import / api / manual
    source_bill_id          BIGINT NULL,
    source_bill_no          VARCHAR(50) NULL,

    -- 原因
    reason_code             VARCHAR(50) NULL,                        -- DAMAGED / FOUND / LOST / DATA_FIX ...
    reason_name             VARCHAR(100) NULL,
    remark                  VARCHAR(500) NULL,

    -- 乐观锁
    version                 INTEGER NOT NULL DEFAULT 0,

    -- 审计
    created_by              BIGINT NULL,
    created_name            VARCHAR(50) NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_by              BIGINT NULL,
    updated_name            VARCHAR(50) NULL,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    approved_by             BIGINT NULL,
    approved_name           VARCHAR(50) NULL,

    is_deleted              SMALLINT NOT NULL DEFAULT 0
);
```

adjust\_type 常见值：

| 值 | 说明 |
| --- | --- |
| INIT | 库存初始化 |
| PROFIT | 盘盈 |
| LOSS | 盘亏 |
| DAMAGE | 报废 |
| MANUAL | 手工调整 |

库存调整明细表：tb\_stock\_adjust\_item

```sql
tb_stock_adjust_item
-----------------
CREATE TABLE tb_stock_adjust_item (
    id                          BIGINT PRIMARY KEY,

    -- 多租户
    tenant_id                   BIGINT NOT NULL,

    -- 主表关联
    adjust_id                   BIGINT NOT NULL,
    line_no                     INTEGER NOT NULL,

    -- 行级调整模式（支持 mixed）
    line_adjust_mode            VARCHAR(20) NOT NULL DEFAULT 'delta',
    -- delta 差量调整
    -- target 定量调整
    -- attr 属性调整

    -- 库存维度（非常关键）
    warehouse_id                BIGINT NOT NULL,
    owner_id                    BIGINT NULL,
    area_id                     BIGINT NULL,
    location_id                 BIGINT NULL,

    -- 物料
    sku_id                      BIGINT NOT NULL,
    sku_code                    VARCHAR(50) NOT NULL,
    sku_name                    VARCHAR(200) NOT NULL,
    spec                        VARCHAR(200) NULL,
    model                       VARCHAR(100) NULL,

    -- 单位
    unit_id                     BIGINT NULL,
    unit_name                   VARCHAR(50) NULL,
    base_unit_id                BIGINT NULL,
    base_unit_name              VARCHAR(50) NULL,
    unit_rate                   NUMERIC(18,6) NOT NULL DEFAULT 1,

    -- 批次/库存属性（调整前维度）
    lot_no                      VARCHAR(100) NULL,
    production_date             DATE NULL,
    expire_date                 DATE NULL,

    -- 调整前数量（强烈建议保留快照）
    before_qty                  NUMERIC(18,6) NOT NULL DEFAULT 0,
    before_base_qty             NUMERIC(18,6) NOT NULL DEFAULT 0,

    -- 调整输入
    adjust_qty                  NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 差量（交易单位）
    adjust_base_qty             NUMERIC(18,6) NOT NULL DEFAULT 0,    -- 差量（基本单位）

    target_qty                  NUMERIC(18,6) NULL,                  -- 定量调整后的数量（交易单位）
    target_base_qty             NUMERIC(18,6) NULL,                  -- 定量调整后的数量（基本单位）

    -- 最终结果（建议落库，避免每次计算）
    after_qty                   NUMERIC(18,6) NOT NULL DEFAULT 0,
    after_base_qty              NUMERIC(18,6) NOT NULL DEFAULT 0,

    -- 调整方向
    adjust_direction            VARCHAR(20) NOT NULL DEFAULT 'none',
    -- increase / decrease / none

    -- 成本 / 金额
    unit_cost                   NUMERIC(18,6) NOT NULL DEFAULT 0,
    adjust_amount               NUMERIC(18,6) NOT NULL DEFAULT 0,

    -- 属性调整（第二版/预留字段）
    target_owner_id             BIGINT NULL,
    target_area_id              BIGINT NULL,
    target_location_id          BIGINT NULL,
    target_lot_no               VARCHAR(100) NULL,
    target_production_date      DATE NULL,
    target_expire_date          DATE NULL,

    -- 是否启用SN
    sn_required                 SMALLINT NOT NULL DEFAULT 0,

    -- 行状态
    line_status                 VARCHAR(20) NOT NULL DEFAULT 'pending',
    -- pending / confirmed / adjusted / cancelled

    -- 来源库存记录（非常推荐）
    stock_balance_id            BIGINT NULL,

    -- 来源明细
    source_item_id              BIGINT NULL,
    source_bill_type            VARCHAR(30) NULL,
    source_bill_id              BIGINT NULL,

    -- 原因
    reason_code                 VARCHAR(50) NULL,
    reason_name                 VARCHAR(100) NULL,
    remark                      VARCHAR(500) NULL,

    -- 审计
    created_by                  BIGINT NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by                  BIGINT NULL,
    updated_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    is_deleted                  SMALLINT NOT NULL DEFAULT 0
);
```

主表 bill\_status：

-   draft
-   submitted
-   approved
-   executing
-   completed
-   cancelled
-   closed

主表 execute\_status：

-   pending
-   partial
-   done
-   reversed

明细 line\_status：

-   pending
-   confirmed
-   adjusted
-   cancelled

reason\_code 常见值：

```text
DAMAGED -- 损坏
FOUND   -- 发现
LOST    -- 丢失
DATA_FIX -- 数据修正
```

调整执行流程:

```text
创建调整单
      │
      ▼
录入明细
      │
      ▼
提交审核
      │
      ▼
审核通过
      │
      ▼
更新库存
      │
      ▼
写入 tb_inventory_log
```

## 6、VMI库存管理

VMI 是仓储和供应链管理中的一个重要概念，英文是 Vendor Managed Inventory，中文通常叫 供应商管理库存。  
VMI（Vendor Managed Inventory） 指的是：

> 由供应商负责管理客户的库存，而不是客户自己管理库存。

也就是说：

-   库存属于客户
-   库存管理权在供应商

供应商根据客户的销售或库存数据，主动补货，保证库存处于合理水平。  
VMI 的关键是 库存数据共享：

客户需要把这些数据提供给供应商：

-   当前库存
-   销售数据
-   安全库存
-   需求预测

***VMI 的优点***

1 对客户

-   降低库存
-   减少缺货
-   减少采购工作
-   提高供应稳定性

2 对供应商

-   销售更稳定
-   更好预测需求
-   与客户关系更紧密

| 维度 | 普通库存 | VMI库存 |
| --- | --- | --- |
| 库存所有权 | 企业 | 供应商 |
| 库存位置 | 企业仓库 | 企业仓库 |
| 补货触发 | 企业采购 | 供应商 |
| 消耗确认 | 出库 | 领用 / 结算 |
| 结算方式 | 采购入库 | 消耗结算 |

VMI 库存流程:

```text
供应商仓库
     │
     ▼
VMI补货单
     │
     ▼
客户VMI仓库存
     │
     ▼
客户生产使用
     │
     ▼
VMI消耗记录
     │
     ▼
VMI结算
     │
     ▼
供应商收款
```

### VMI仓库表

```sql
vmi_warehouse
-
id
tenant_id
org_id

warehouse_code -- 仓库编码
warehouse_name -- 仓库名称
pinyin_code -- 拼音码

customer_id -- 客户
supplier_id  -- 供应商
address -- 地址
contact_name -- 联系人
contact_phone -- 联系电话

status -- 状态
created_at
```

### VMI库存表

不想污染普通库存表，所以使用 vmi\_inventory 表。

```sql
vmi_inventory
------------
id
tenant_id
org_id

warehouse_id -- 仓库
supplier_id -- 供应商
customer_id -- 客户

sku_id -- 商品
batch_no -- 批次
serial_no -- 序列号

on_hand_qty -- 在库数量
reserved_qty -- 锁定数量
available_qty -- 可用数量

avg_cost -- 平均成本
total_cost -- 总成本

created_at
```

逻辑：

```text
供应商拥有库存
库存放在客户仓库
客户使用后再结算
```

### VMI 补货计划表

```sql
vmi_replenishment_plan
---------------------
id
tenant_id

supplier_id -- 供应商
customer_id -- 客户
sku_id -- 商品SKU

min_qty -- 最小补货数量
max_qty -- 最大补货数量
replenish_qty -- 补货数量

lead_time_days -- 预期交货时间

status
```

作用：

-   库存低于 min\_qty
-   自动补货到 max\_qty

### VMI库存协议

VMI 库存协议（Vendor Managed Inventory Agreement）是指：

> 供应商根据客户的销售或库存数据，主动补货，保证库存处于合理水平。

```sql
vmi_agreement
-------------
id
tenant_id

supplier_id
sku_id -- 商品
warehouse_id -- 仓库

min_qty -- 最小补货数量
max_qty -- 最大补货数量
safety_qty -- 安全库存数量

settle_mode -- 结算方式
price -- 价格

status -- 状态
created_at
```

供应商负责保证:

```text
min_qty <= 库存 <= max_qty
```

结算方式 settle\_mode 常见值：

| 值 | 说明 |
| --- | --- |
| CONSUME | 按消耗结算 |
| PERIOD | 周期结算 |

### VMI补货单

```sql
vmi_replenishment
--------
id
tenant_id

supplier_id -- 供应商
customer_id -- 客户
warehouse_id -- 仓库

status -- 状态
created_at
```

补货单子表

```sql
vmi_replenishment_item
-
id
tenant_id

replenishment_id -- 补货单ID
sku_id -- 商品
batch_no -- 批次
serial_no -- 序列号

qty -- 补货数量
price -- 价格
amount -- 金额

```

### VMI领用（库存消耗）

```sql
vmi_consumption
---------------
id
tenant_id
org_id

supplier_id -- 供应商
sku_id -- 物料
warehouse_id -- 仓库

qty -- 消耗数量
price -- 价格
amount -- 金额
source_doc -- 源单据
source_type -- 源单据类型

status -- 状态
created_at

```

source\_type的内容：

-   SALE
-   PRODUCTION
-   TRANSFER

### VMI结算单

```sql
vmi_settlement
------------
id
tenant_id

supplier_id
period_start -- 期初
period_end -- 期末

total_amount -- 总金额

status -- 状态
created_at
```

结算单子表

```sql
vmi_settlement_item
-
id
tenant_id

settlement_id -- 结算单ID
material_id -- 物料

qty -- 结算数量
price -- 价格
amount -- 金额

```

## 6、财务模块

核心表结构总览, 建议至少有这些表：

1）应收单 ar\_receivable

销售、其他收入、客户费用等形成的应收

2）应付单 ap\_payable

采购、物流费用、仓储费用、供应商费用等形成的应付

3）收款单 fin\_receipt

实际收到客户的钱（或其他来源）

4）付款单 fin\_payment

实际付给供应商/承运商/仓储服务商的钱

5）收款核销明细 fin\_receipt\_writeoff

收款单 与 应收单 的核销关系

6）付款核销明细 fin\_payment\_writeoff

付款单 与 应付单 的核销关系

### 资金账户表

```sql
create table fin_account (
    id                  bigint primary key,
    tenant_id           bigint not null,
    org_id              bigint null,

    account_code        varchar(50) not null,
    account_name        varchar(100) not null,
    account_type        varchar(30) not null,   -- CASH / BANK / WECHAT / ALIPAY / OTHER

    bank_name           varchar(100) null,
    bank_account_no     varchar(100) null,
    account_holder      varchar(100) null,

    currency_code       varchar(10) not null,
    balance             decimal(18,2) not null default 0,

    status              varchar(20) not null,   -- ENABLED / DISABLED

    created_at          datetime not null,
    updated_at          datetime not null,
    is_deleted          bit not null default 0
);
```

### 应收单设计（AR）

一般由 销售出库 / 销售结算 / 仓储服务费 / 物流费 / 其他费用 生成

```sql
create table ar_receivable (
    id                    bigint primary key,
    tenant_id             bigint not null,
    org_id                bigint null,
    warehouse_id          bigint null,

    receivable_no         varchar(50) not null,      -- 应收单号
    receivable_type       varchar(30) not null,      -- SALES / STORAGE_FEE / LOGISTICS_FEE / OTHER
    source_biz_type       varchar(30) not null,      -- 销售单/出库单/费用单等
    source_biz_id         bigint null,
    source_biz_no         varchar(50) null,

    customer_id           bigint not null,
    customer_code         varchar(50) null,
    customer_name         varchar(200) null,

    biz_date              date not null,
    due_date              date null,                 -- 到期日

    currency_code         varchar(10) not null,
    exchange_rate         decimal(18,8) not null default 1,
    base_currency_code    varchar(10) not null,

    receivable_amount     decimal(18,2) not null,    -- 原币应收金额
    received_amount       decimal(18,2) not null default 0, -- 已核销收款金额（原币）
    unreceived_amount     decimal(18,2) not null,    -- 未收金额（原币）

    base_receivable_amount decimal(18,2) not null,   -- 本位币金额
    base_received_amount   decimal(18,2) not null default 0,
    base_unreceived_amount decimal(18,2) not null,

    status                varchar(20) not null,      -- DRAFT / CONFIRMED / PARTIAL / PAID / CLOSED / CANCELLED
    writeoff_status       varchar(20) not null,      -- UNWRITEOFF / PARTIAL / FULL
    settle_status         varchar(20) not null,      -- UNSETTLED / PARTIAL / SETTLED

    remark                varchar(500) null,

    created_by            bigint null,
    created_name          varchar(50) null,
    created_at            datetime not null,
    updated_by            bigint null,
    updated_name          varchar(50) null,
    updated_at            datetime not null,
    is_deleted            bit not null default 0,
    version               int not null default 0
);
```

### 应付单设计（AP）

一般由 采购入库 / 供应商账单 / 物流费用 / 仓租费用 / 加工费 / 其他费用 生成

```sql
create table ap_payable (
    id                    bigint primary key,
    tenant_id             bigint not null,
    org_id                bigint null,
    warehouse_id          bigint null,

    payable_no            varchar(50) not null,
    payable_type          varchar(30) not null,      -- PURCHASE / STORAGE_FEE / LOGISTICS_FEE / PROCESS_FEE / OTHER
    source_biz_type       varchar(30) not null,
    source_biz_id         bigint null,
    source_biz_no         varchar(50) null,

    supplier_id           bigint not null,
    supplier_code         varchar(50) null,
    supplier_name         varchar(200) null,

    biz_date              date not null,
    due_date              date null,

    currency_code         varchar(10) not null,
    exchange_rate         decimal(18,8) not null default 1,
    base_currency_code    varchar(10) not null,

    payable_amount        decimal(18,2) not null,
    paid_amount           decimal(18,2) not null default 0,
    unpaid_amount         decimal(18,2) not null,

    base_payable_amount   decimal(18,2) not null,
    base_paid_amount      decimal(18,2) not null default 0,
    base_unpaid_amount    decimal(18,2) not null,

    status                varchar(20) not null,      -- DRAFT / CONFIRMED / PARTIAL / PAID / CLOSED / CANCELLED
    writeoff_status       varchar(20) not null,      -- UNWRITEOFF / PARTIAL / FULL
    settle_status         varchar(20) not null,      -- UNSETTLED / PARTIAL / SETTLED

    remark                varchar(500) null,

    created_by            bigint null,
    created_name          varchar(50) null,
    created_at            datetime not null,
    updated_by            bigint null,
    updated_name          varchar(50) null,
    updated_at            datetime not null,
    is_deleted            bit not null default 0,
    version               int not null default 0
);
```

### 收款单设计（实际资金流入）

客户打款、平台回款、其他收入到账

```sql
create table fin_receipt (
    id                    bigint primary key,
    tenant_id             bigint not null,
    org_id                bigint null,
    warehouse_id          bigint null,

    receipt_no            varchar(50) not null,      -- 收款单号
    receipt_type          varchar(30) not null,      -- SALES_RECEIPT / ADVANCE_RECEIPT / REFUND_IN / OTHER_INCOME
    receipt_scene         varchar(30) not null,      -- NORMAL / PRE_RECEIVE / ADJUSTMENT / REVERSE

    payer_type            varchar(20) not null,      -- CUSTOMER / PLATFORM / OTHER
    payer_id              bigint null,
    payer_code            varchar(50) null,
    payer_name            varchar(200) null,

    biz_date              date not null,
    receipt_date          date not null,             -- 实际到账日期

    currency_code         varchar(10) not null,
    exchange_rate         decimal(18,8) not null default 1,
    base_currency_code    varchar(10) not null,

    receipt_amount        decimal(18,2) not null,    -- 原币收款金额
    writeoff_amount       decimal(18,2) not null default 0,  -- 已核销金额
    unwritten_amount      decimal(18,2) not null,    -- 未核销金额（可作预收）

    base_receipt_amount   decimal(18,2) not null,
    base_writeoff_amount  decimal(18,2) not null default 0,
    base_unwritten_amount decimal(18,2) not null,

    pay_method            varchar(30) not null,      -- CASH / BANK / WECHAT / ALIPAY / TRANSFER / OTHER
    account_id            bigint null,               -- 资金账户
    account_name          varchar(100) null,
    bank_account_no       varchar(100) null,         -- 对方账户（可选）
    bank_serial_no        varchar(100) null,         -- 银行流水号

    status                varchar(20) not null,      -- DRAFT / CONFIRMED / POSTED / PARTIAL_WRITEOFF / FULL_WRITEOFF / CANCELLED
    approval_status       varchar(20) not null,      -- PENDING / APPROVED / REJECTED / NONE

    source_biz_type       varchar(30) null,          -- 可直接挂来源业务（非必须）
    source_biz_id         bigint null,
    source_biz_no         varchar(50) null,

    reverse_of_id         bigint null,               -- 冲销原单ID
    reverse_flag          bit not null default 0,

    remark                varchar(500) null,

    created_by            bigint null,
    created_name          varchar(50) null,
    created_at            datetime not null,
    updated_by            bigint null,
    updated_name          varchar(50) null,
    updated_at            datetime not null,
    is_deleted            bit not null default 0,
    version               int not null default 0
);
```

### 付款单设计（实际资金流出）

采购付款、费用付款、供应商预付款、退款给客户等

```sql
create table fin_payment (
    id                    bigint primary key,
    tenant_id             bigint not null,
    org_id                bigint null,
    warehouse_id          bigint null,

    payment_no            varchar(50) not null,      -- 付款单号
    payment_type          varchar(30) not null,      -- PURCHASE_PAYMENT / ADVANCE_PAYMENT / EXPENSE_PAYMENT / REFUND_OUT / OTHER_PAYMENT
    payment_scene         varchar(30) not null,      -- NORMAL / PREPAY / ADJUSTMENT / REVERSE

    payee_type            varchar(20) not null,      -- SUPPLIER / CUSTOMER / CARRIER / OTHER
    payee_id              bigint null,
    payee_code            varchar(50) null,
    payee_name            varchar(200) null,

    biz_date              date not null,
    payment_date          date not null,

    currency_code         varchar(10) not null,
    exchange_rate         decimal(18,8) not null default 1,
    base_currency_code    varchar(10) not null,

    payment_amount        decimal(18,2) not null,
    writeoff_amount       decimal(18,2) not null default 0,
    unwritten_amount      decimal(18,2) not null,

    base_payment_amount   decimal(18,2) not null,
    base_writeoff_amount  decimal(18,2) not null default 0,
    base_unwritten_amount decimal(18,2) not null,

    pay_method            varchar(30) not null,      -- CASH / BANK / WECHAT / ALIPAY / TRANSFER / OTHER
    account_id            bigint null,
    account_name          varchar(100) null,
    bank_account_no       varchar(100) null,
    bank_serial_no        varchar(100) null,

    status                varchar(20) not null,      -- DRAFT / CONFIRMED / POSTED / PARTIAL_WRITEOFF / FULL_WRITEOFF / CANCELLED
    approval_status       varchar(20) not null,      -- PENDING / APPROVED / REJECTED / NONE

    source_biz_type       varchar(30) null,
    source_biz_id         bigint null,
    source_biz_no         varchar(50) null,

    reverse_of_id         bigint null,
    reverse_flag          bit not null default 0,

    remark                varchar(500) null,

    created_by            bigint null,
    created_name          varchar(50) null,
    created_at            datetime not null,
    updated_by            bigint null,
    updated_name          varchar(50) null,
    updated_at            datetime not null,
    is_deleted            bit not null default 0,
    version               int not null default 0
);
```

### 收款核销表

解决：一笔收款核销多个应收、一个应收分多次收款

```sql
create table fin_receipt_writeoff (
    id                    bigint primary key,
    tenant_id             bigint not null,

    receipt_id            bigint not null,
    receipt_no            varchar(50) not null,

    receivable_id         bigint not null,
    receivable_no         varchar(50) not null,

    writeoff_date         date not null,

    currency_code         varchar(10) not null,
    writeoff_amount       decimal(18,2) not null,    -- 原币核销金额
    base_writeoff_amount  decimal(18,2) not null,    -- 本位币核销金额

    discount_amount       decimal(18,2) not null default 0, -- 折扣/抹零
    fee_amount            decimal(18,2) not null default 0, -- 手续费（如平台扣点）
    exchange_gain_loss    decimal(18,2) not null default 0, -- 汇兑损益（可选）

    status                varchar(20) not null,      -- NORMAL / REVERSED

    reverse_of_id         bigint null,
    remark                varchar(500) null,

    created_by            bigint null,
    created_name          varchar(50) null,
    created_at            datetime not null,
    updated_by            bigint null,
    updated_name          varchar(50) null,
    updated_at            datetime not null,
    is_deleted            bit not null default 0
);
```

### 付款核销表

解决：一笔付款核销多个应付、一个应付分多次付款

```sql
create table fin_payment_writeoff (
    id                    bigint primary key,
    tenant_id             bigint not null,

    payment_id            bigint not null,
    payment_no            varchar(50) not null,

    payable_id            bigint not null,
    payable_no            varchar(50) not null,

    writeoff_date         date not null,

    currency_code         varchar(10) not null,
    writeoff_amount       decimal(18,2) not null,
    base_writeoff_amount  decimal(18,2) not null,

    discount_amount       decimal(18,2) not null default 0, -- 供应商折扣
    fee_amount            decimal(18,2) not null default 0,
    exchange_gain_loss    decimal(18,2) not null default 0,

    status                varchar(20) not null,      -- NORMAL / REVERSED

    reverse_of_id         bigint null,
    remark                varchar(500) null,

    created_by            bigint null,
    created_name          varchar(50) null,
    created_at            datetime not null,
    updated_by            bigint null,
    updated_name          varchar(50) null,
    updated_at            datetime not null,
    is_deleted            bit not null default 0
);
```

为什么不能只做“收款表 + 付款表”?

如果你只做：

-   收款表
-   付款表

会立刻遇到这些问题：

1）部分收款

客户应收 10000，今天收 3000，下周收 7000  
→ 没有核销表很难处理

2）合并收款

客户一次打款 50000，核销 5 张销售单  
→ 必须有明细关联

3）预收款

客户先打款，后出库开单  
→ 需要“未核销余额”机制

4）退款

原来收了 10000，后来退 2000  
→ 需要反向单 / 红冲

所以 核销层是财务模块的核心。

应收来源（source\_biz\_type）:

```text
SO：销售订单
SOUT：销售出库单
STORAGE_BILL：仓储费账单
INBOUND_SERVICE_BILL：入库服务费账单
OUTBOUND_SERVICE_BILL：出库服务费账单
PICK_PACK_BILL：拣货/打包服务费
LOGISTICS_BILL_OUT：代发物流费
VALUE_ADDED_BILL：增值服务费（贴标、分装、质检）
MANUAL_AR：手工应收
```

应付来源（source\_biz\_type）:

```text
PO：采购订单
PIN：采购入库单
SUPPLIER_BILL：供应商账单
CARRIER_BILL：承运商账单
WAREHOUSE_RENT_BILL：仓租账单
LABOR_BILL：人工/装卸费
VALUE_ADDED_COST_BILL：加工/耗材成本
MANUAL_AP：手工应付
```

收款单状态 fin\_receipt.status:

```text
DRAFT：草稿
CONFIRMED：已确认
POSTED：已过账（已影响资金）
PARTIAL_WRITEOFF：部分核销
FULL_WRITEOFF：全部核销
CANCELLED：已作废
```

付款单状态 fin\_payment.status 同上。

应收 / 应付状态:

***单据状态 status:***

-   DRAFT
-   CONFIRMED
-   CLOSED
-   CANCELLED

***核销状态 writeoff\_status:***

-   UNWRITEOFF
-   PARTIAL
-   FULL

禁止直接改余额，必须通过事务更新：  
例如核销时：

-   插入 fin\_receipt\_writeoff
-   更新 ar\_receivable.received\_amount
-   更新 ar\_receivable.unreceived\_amount
-   更新 fin\_receipt.writeoff\_amount
-   更新 fin\_receipt.unwritten\_amount
-   更新状态

必须放在同一事务里。

**典型业务流程：**

***场景 1：销售出库后形成应收***

-   销售出库单审核通过
-   生成 ar\_receivable
-   状态：UNWRITEOFF

***场景 2：客户打款（预收或正常收款）***

-   新增 fin\_receipt
-   unwritten\_amount = receipt\_amount
-   若未指定应收单 → 作为预收款保留

***场景 3：核销收款***

-   插入 fin\_receipt\_writeoff
-   更新 ar\_receivable.received\_amount
-   更新 ar\_receivable.unreceived\_amount
-   更新 fin\_receipt.writeoff\_amount
-   更新 fin\_receipt.unwritten\_amount
-   更新双方状态

***场景 4：采购入库形成应付***

-   采购入库/供应商账单审核
-   生成 ap\_payable

***场景 5：付款核销***

-   新增 fin\_payment
-   插入 fin\_payment\_writeoff
-   更新 ap\_payable
-   更新 fin\_payment

## ERP 审批流设计

企业通常需要审批：

```text
采购订单审批
费用审批
销售审批
```

结构：

```text
tb_workflow
tb_workflow_node
tb_workflow_instance
tb_workflow_task
```

```sql
tb_workflow
---------
id
tenant_id

workflow_name -- 工作流名称
biz_type -- 业务类型

```

```sql
tb_workflow_node
--------------
id
tenant_id

workflow_id -- 工作流ID
node_name -- 节点名称
node_type -- 节点类型

approver_type -- 审批类型

```

```sql
tb_workflow_instance
------------------
id
tenant_id

workflow_id -- 工作流ID
biz_type -- 业务类型
biz_id -- 业务ID

status

```

```sql
tb_workflow_task
--------------
id
tenant_id

workflow_instance_id -- 工作流实例ID
node_id -- 节点ID

status
created_at

```

## ERP其他内容

### ERP 单据号生成

ERP 单据号生成规则：单据类型 + 日期+流水号

1.  单据类型：采购订单、销售订单、入库单、出库单
    
    | 单据 | 前缀 |
    | --- | --- |
    | 采购订单 | PO |
    | 销售订单 | SO |
    | 入库单 | IN |
    | 出库单 | OUT |
    
2.  日期：年月日
    
3.  流水号：自增序列
    

例如：

```text
SO202108010001
PO202108010002
IN202108010003
```

### ERP 状态机设计

单据必须使用 状态机。  
例如：销售订单：

```text
草稿
  ↓
已提交
  ↓
已审核
  ↓
已发货
  ↓
已完成
```

状态字段：status

```text
DRAFT
SUBMITTED
APPROVED
SHIPPED
FINISHED
CANCELLED
```

### ERP 单位设计原则

-   业务单位：采购、销售、库存、财务等
-   基本单位：库存、库存流水、批次、序列号等
-   业务单位和基本单位的换算关系：基本单位数量 = 业务单位数量 \* 换算率

库存全部用：基本单位

单据存两个数量：业务单位 数量、基本单位 数量

换算只做一次：单据保存时,计算 base\_quantity, 之后库存只用：base\_quantity

### 库存成本核算

库存成本有三种主流方式：

| 方法 | ERP |
| --- | --- |
| 移动加权 | 最常见 |
| FIFO | 制造业 |
| 月结加权 | 财务系统 |

1.移动加权平均成本

```text
新成本 =
(原库存金额 + 新入库金额)
/
(原库存数量 + 新入库数量)
```

示例：

库存：

数量 100  
成本 10  
金额 1000

采购：

数量 50  
单价 12  
金额 600

新成本：

(1000 + 600) / (100 + 50)  
\= 10.67

库存表增加成本字段：

```sql
inventory
----------
id
tenant_id

sku_id
warehouse_id

on_hand_qty

avg_cost
total_cost

```

关系：  
total\_cost = on\_hand\_qty \* avg\_cost

库存流水增加金额字段：

```sql
inventory_log
--------------
change_qty
change_amount
```

例如：

```text
销售出库
数量 -10
成本 10.67
金额 -106.7
```

ERP 成本问题核心,系统必须能回答：

```text
某个商品当前成本是多少？
某次销售利润是多少？
库存总价值是多少？
```

这些都依赖：

```text
tb_inventory
tb_inventory_log
```

### 库存相关表到底要不要加 org\_id

结论先说清楚（企业 ERP 常见做法）：

| 表 | 是否需要 `org_id` |
| --- | --- |
| tb\_inventory | ❌ 不需要 |
| tb\_inventory\_log | ❌ 不需要 |
| tb\_inventory\_batch | ❌ 不需要 |
| tb\_inventory\_serial | ❌ 不需要 |
| tb\_inventory\_reservation | ❌ 不需要 |

原因只有一个：

仓库已经有 org\_id，库存表通过 warehouse\_id 就能确定组织。

这是 ERP 设计里的一个重要原则：避免冗余组织字段

查询库存：

```sql
SELECT i.*
FROM tb_inventory i
JOIN tb_warehouse w ON i.warehouse_id = w.id
WHERE w.org_id IN (...)
```

什么时候才会加 org\_id ?

只有两种情况：

情况1：表不依赖仓库

例如：

```sql
tb_sales_order
tb_purchase_order
tb_customer
tb_supplier
```

这些必须有：org\_id

情况2：需要极致查询性能

### 最终模块结构

```text
SaaS平台
 ├ 租户
 ├ 套餐
 └ 授权

权限系统
 ├ 用户
 ├ 角色
 ├ 权限
 └ 机构

基础数据
 ├ 商品
 ├ 分类
 ├ 单位
 ├ 客户
 └ 供应商

库存
 ├ 仓库
 ├ 库位
 ├ 库存
 ├ 批次
 ├ 序列号
 ├ 库存流水
 └ 库存锁定

采购
 ├ 采购单
 └ 采购明细
 └ 入库

销售
 ├ 销售单
 └ 销售明细
 └ 出库

出入库
 ├ 入库
 └ 出库

财务
 ├ 收款
 └ 付款
 └ 成本核算

VMI库存管理
 ├ VMI仓库
 └ VMI付款库存
```

 

posted on 2026-03-24 12:40  [伍华聪](https://www.cnblogs.com/wuhuacong)  阅读(288)  评论(0)    [收藏](javascript:void\(0\))  [举报](javascript:void\(0\))
