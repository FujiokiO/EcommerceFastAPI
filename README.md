# 小组开发说明

## 从哪里开始？

1. 善用本文件的目录
2. fork 本项目，clone 自己的项目
2. 用 pycharm 直接打开
3. 复制 `.env.example` 另存为 `.env`

## 如何参与开发？

1. 用 `git` 进行版本控制，修改文件用 `git add [那个文件]`
   如果是pycharm几乎是自动的，不用特意处理；一定数量的修改后 `git commit -m "此处写提交的信息，例如 add order_route""`
2. 及时进行同步 `git push -u origin main`
3. 及时关注本仓库的更新，对自己的仓库同步。功能测试没问题后提交 `pull request`

## TODO List

- [ ] 注册、重置密码的邮件发送，以及下订单之后的邮件通知

# 《需求规格说明书》

> [!IMPORTANT]
> 已有的需求说明，未整合校验

## 一、引言

### 1.1 背景

随着互联网的普及和电子商务的飞速发展，网上购物已经成为人们日常生活的重要组成部分。在这种背景下，网上鲜花店作为一种新型的商业模式，越来越受到消费者的欢迎。为了满足市场需求，本项目旨在为网上鲜花店提供一个完整的、可靠的管理系统，以便于店主和客户进行方便的交易和管理。

### 1.2 目的

本文档的目的是详细描述网上鲜花店管理系统的功能需求，以便于开发团队进行软件开发。涵盖基础数据维护、查询、鲜花采购管理、鲜花销售、以及盘点和统计等各个方面的需求。通过实现这些功能，可以帮助店主更好地管理鲜花店，同时为客户提供更好的购物体验。

## 二、系统功能描述

### 2.1 基础数据维护

#### 2.1.1 用户和权限管理

功能描述：系统应提供用户和权限管理功能，包括用户注册、登录、修改个人信息、密码找回等。此外，系统应区分店主和客户的权限，以便根据不同用户类型提供相应的功能和服务。

输入：用户信息（如用户名、密码等）

输出：用户注册、登录、修改个人信息等操作的结果

#### 2.1.2 鲜花基本信息和分类管理

功能描述：系统应提供鲜花信息和分类的管理功能，包括添加、修改、删除鲜花信息和分类。店主可以根据需要对鲜花信息和分类进行维护，以便客户能够方便地查询和购买鲜花。

输入：鲜花信息（如名称、分类、价格等）

输出：鲜花信息和分类的添加、修改、删除等操作的结果

### 2.2 查询

#### 2.2.1 店主查询所有的订单

功能描述：系统应提供店主查询所有订单的功能，包括已完成、未完成和已取消的订单。店主可以根据订单状态、时间范围等条件进行筛选，以便了解订单情况并进行相应的处理。

输入：查询条件（如订单状态、时间范围等）

输出：符合条件的订单列表

#### 2.2.2 店主查询鲜花库存量

功能描述：系统应提供店主查询鲜花库存量的功能，以便店主了解各类鲜花的库存情况并及时进行补货。店主可以根据鲜花分类、名称等条件进行筛选，以便快速查找目标鲜花的库存量。

输入：查询条件（如鲜花分类、名称等）

输出：符合条件的鲜花库存列表

#### 2.2.3 鲜花基本信息查询

功能描述：系统应提供鲜花基本信息查询功能，以便客户和店主了解鲜花的详细信息。用户可以根据鲜花分类、名称等条件进行筛选，以便快速查找目标鲜花的信息。

输入：查询条件（如鲜花分类、名称等）

输出：符合条件的鲜花信息列表

#### 2.2.4 客户查询自己的订单内容、是否已被受理

功能描述：系统应提供客户查询自己订单内容和受理状态的功能，以便客户了解订单进度。客户可以根据订单状态、时间范围等条件进行筛选，以便快速查找目标订单。

输入：查询条件（如订单状态、时间范围等）

输出：符合条件的订单列表

### 2.3 鲜花采购管理

#### 2.3.1 鲜花采购后，进行入库登记

功能描述：系统应提供鲜花采购入库登记功能，以便店主记录鲜花的采购信息和更新库存。店主在采购鲜花后，需要在系统中输入采购的鲜花信息（如名称、数量、价格等），系统将自动更新库存信息。

输入：采购的鲜花信息（如名称、数量、价格等）

输出：入库登记操作的结果和库存信息更新

#### 2.3.2 每日检测商品库存量，当某种商品库存量不足时，系统发出缺货通知，同时生成采购计划

功能描述：系统应提供每日检测商品库存量的功能，以便及时发现库存不足的情况。当某种商品库存量低于预设阈值时，系统应自动发出缺货通知，并生成采购计划，提醒店主进行补货。

输入：无

输出：缺货通知和采购计划

#### 2.3.3 鲜花报损操作，并记录报损原因

功能描述：系统应提供鲜花报损操作功能，以便店主记录因质量问题、运输损坏等原因导致的鲜花报损。店主需要在系统中输入报损的鲜花信息（如名称、数量、报损原因等），系统将自动更新库存信息。

输入：报损的鲜花信息（如名称、数量、报损原因等）

输出：报损操作的结果和库存信息更新

### 2.4 鲜花销售

#### 2.4.1 客户分类浏览鲜花信息

功能描述：系统应提供客户按照分类浏览鲜花信息的功能，以便客户快速找到感兴趣的鲜花。客户可以根据鲜花分类进行筛选，系统将显示符合条件的鲜花信息列表。

输入：鲜花分类

输出：符合条件的鲜花信息列表

#### 2.4.2 客户选择想要购买的鲜花，直接将其加入订单

功能描述：系统应提供客户选择鲜花并加入订单的功能，以便客户进行购买。客户在浏览鲜花信息时，可以直接将感兴趣的鲜花加入订单，并输入购买数量。系统将自动计算订单总价，并在提交订单后更新库存信息。

输入：鲜花ID、购买数量

输出：订单信息更新

#### 2.4.3 客户也可以先将选择的鲜花加入购物车。对购物车的操作包括：显示购物车内容、添加新选鲜花、更改鲜花数量、提交购物车中的所有物品、清空购物车等

功能描述：系统应提供购物车功能，以便客户临时保存感兴趣的鲜花，并在稍后进行购买。客户可以将选择的鲜花加入购物车，对购物车进行操作，如显示购物车内容、添加新选鲜花、更改鲜花数量等。当客户决定购买购物车中的物品时，可以一键提交购物车中的所有物品，生成订单。

输入：购物车操作（如添加鲜花、更改数量等）

输出：购物车内容更新

#### 2.4.4 客户提交订单，购买鲜花

功能描述：系统应提供客户提交订单的功能，以便客户完成购买。在提交订单前，客户需要确认订单内容、填写收货地址和联系方式等信息。提交订单后，系统将自动更新库存信息，并将订单状态设置为“未受理”。

输入：订单信息（如收货地址、联系方式等）

输出：订单提交结果和库存信息更新

### 2.5 盘点和统计

#### 2.5.1 店主对订单进行受理处理

功能描述：系统应提供店主对订单进行受理处理的功能，包括确认库存、调整订单状态、发货等。店主可以查看所有未处理的订单，并根据实际情况进行处理。处理完成后，系统将自动更新订单状态。

输入：订单ID

输出：订单状态更新

#### 2.5.2 每日分类统计销售额

功能描述：系统应提供每日分类统计销售额的功能，以便店主了解各类鲜花的销售情况。系统将自动按照鲜花分类统计每日销售额，并生成报表，供店主查阅。

输入：无

输出：每日各分类销售额报表

#### 2.5.3 每月盘点，分类统计销售额、统计库存量，计算销售利润

功能描述：系统应提供每月盘点功能，以便店主了解鲜花店的经营状况。系统将自动进行每月盘点，生成报表，包括各分类销售额、库存量以及利润。店主可以通过查看报表了解店铺的整体运营情况，并根据实际情况调整经营策略。

输入：无

输出：每月盘点报表

## 三、ER图

## 四、其他需求

### 4.1 性能需求

系统应具备较高的性能，以保证在高并发情况下依然能够正常运行。为此，开发团队需要采用合适的技术和架构，优化数据库查询和处理速度，确保系统在大量用户访问时仍能提供良好的响应速度和稳定性。

### 4.2 安全需求

系统应具备一定的安全性，保护用户数据和隐私。开发团队需要考虑数据加密、访问控制、身份验证等安全措施，防止数据泄露和非法访问。此外，系统还应提供备份和恢复功能，以防数据丢失。

### 4.3 可用性需求

系统应具备良好的可用性，提供简洁明了的用户界面和易于理解的操作流程。开发团队需要关注用户体验，确保系统易于使用，符合用户的使用习惯。此外，系统还应提供在线帮助和教程，以便用户快速上手。

### 4.4 可扩展性需求

系统应具备良好的可扩展性，以便在未来根据业务需求进行功能扩展和升级。开发团队需要采用模块化设计，确保各个功能之间的低耦合，便于单独修改和更新。此外，系统还应提供API接口，以便与其他系统进行集成和数据交换。

## 五、总结

本文档描述了网上鲜花店管理系统的功能需求，包括基础数据维护、查询、鲜花采购管理、鲜花销售、以及盘点和统计等各个方面，帮助店主更好地管理鲜花店，同时为客户提供更好的购物体验。此外，项目还提出了性能、安全、可用性和可扩展性等其他需求，为接下来团队的开发工作做出指引。

> [!IMPORTANT]
> 已有的模块说明，由冗余

## **用户管理模块**

- **用户注册和登录认证功能**：
    - 使用 JWT（JSON Web Tokens）实现用户身份验证和登录管理。注册时需要用户名、密码和确认密码。
    - 登录时使用用户名/密码进行验证，成功登录后颁发 JWT 令牌，在每次请求时发送令牌进行验证。
    - 需要邮件验证注册流程以确保用户邮箱的有效性。
- **用户角色**：
    - • 包括两种角色：用户和管理员，使用 RBAC（基于角色的访问控制） 实现角色管理和权限控制。
    - 管理员具备管理商品、订单和用户信息的权限。
- **个人资料管理**：
    - 用户可以查看和编辑个人信息，包括姓名、地址、联系方式等。
    - 允许用户上传并管理个人头像。

## **商品管理模块**

- **商品展示**：
    - 响应式商品展示页面，支持价格、品牌和类别的筛选条件和排序方式。
    - 商品详情页面展示详细信息、多张图片、描述、价格和规格，并提供规格选择功能。
- **商品管理**：
    - 管理员可添加、编辑和删除商品信息。
    - 商品编辑时支持多张图片上传和商品规格设置。
- **优惠券和活动管理**：
    - 提供优惠券发放和使用功能，用户可以领取、查看和使用优惠券。
    - 支持不同类型的优惠券，如满减券、折扣券。
    - 管理员可以创建和管理促销活动，如限时折扣、团购。

## **购物车、订单和支付模块**

- **购物车功能**：
    - 用户可对购物车内商品进行添加、删除和数量调整操作，保存至数据库。
    - 提供匿名用户也能够使用购物车的功能，购物车内容会在用户登录后与用户账户关联。
- **订单管理和支付**：
    - 用户可以查看订单历史和订单状态，并能取消未支付订单。
    - 订单状态实现自动更新，比如支付成功后自动变更状态为“已支付”。
    - 集成支付宝支付系统，使用支付宝提供的 API 实现支付流程。保障支付过程的安全性和可靠性，处理支付失败和异常情况。
- **物流跟踪：**
    - 用户可以在订单页面或个人账户页面查看订单的物流状态和实时位置。
    - 使用物流服务提供商的 API 或集成第三方物流跟踪系统，展示订单的详细物流信息。

## **其他功能**

- **推荐系统**：
    - 基于用户历史购买记录和浏览行为，考虑用户偏好和商品相似度因素，使用协同过滤或深度学习模型等算法实现个性化推荐。
- **评价和评论**：
    - 用户可对商品进行评价和评论，支持点赞或举报评论功能。
    - 管理员对评论进行审核，过滤敏感词汇和不当内容。
- **邮件通知功能**：
    - 发送订单确认邮件，包括订单详情和支付信息。
    - 发送特别促销信息给用户，根据用户偏好和历史购买记录发送个性化邮件。
- **销售数据分析和报表**：
    - 收集并展示销售数据、用户行为数据，如销售额、用户访问量、热销商品等。
    - 提供可视化报表，如图表、统计图等形式展示数据，方便管理员分析业务状况。
    - 提供定制化的报表生成功能，允许管理员根据需求生成特定时间段的报表。可以导出数据，支持 Excel、CSV 格式。
- **在线客服和售后服务**：
    - 实现实时聊天或留言板功能，让用户可以向客服提出问题和反馈。
    - 提供多种联系方式，如在线聊天、电子邮件、客服热线。
    - 提供退货、换货和退款的流程，允许用户提交售后申请并追踪处理进度。

> [!IMPORTANT]
> 已有的组件划分

1. **后端组件划分**（使用 FastAPI）：
    - **`main.py`**：FastAPI 应用程序的入口文件，包含应用的启动代码和配置。
    - **`app/`**：应用的主目录。

    - **路由模块**：负责处理各种请求，并将其路由到相应的处理程序或控制器。
      **`app/api/`**：包含所有 API 路由文件，每个模块可以有自己的路由文件。

    - **服务层**：负责业务逻辑的实现和处理，例如用户管理、订单处理等功能。
      **`app/services/`**：包含业务逻辑的服务层，实现对数据库操作的封装和处理。

    - **数据访问层**：用于与数据库交互的层，执行数据库操作。
      **`app/db/`**：包含数据库配置、模型定义和 CRUD 操作。
        - **`base.py`**：连接 PostgreSQL 数据库的配置和 SQLAlchemy 实例（可能会舍弃（如果全用这个SQL就不需要写了），只保留初始化创建数据库的部分）。
        - **`crud/`**：存放模型的 CRUD 操作文件，每个模块可以有对应的 CRUD 文件。
    - **`app/models/`**：包含数据库模型定义文件，如用户模型、商品模型等。
    - **`app/utils/`**：存放工具函数或辅助功能的模块，比如安全相关的函数。
2. **前端组件划分**（使用 Gatsby，具体不了解）：
    - **页面组件**：负责页面的展示和交互，例如商品展示页面、用户个人资料页面等。
    - **组件库**：包含各种可复用的 UI 组件，如导航栏、卡片、表单组件等。
    - **服务层**（可选）：负责与后端 API 进行交互，获取数据并处理数据展示。

# 《系统用例分析》

> [!IMPORTANT]
> 已有的用例分析，未整合校验

## 1. 用例识别

### 1.1 用户注册与登录

- **参与者**：用户
- **前置条件**：用户访问网站或应用程序
- **触发事件**：用户点击注册/登录按钮
- **主要流程**：
    1. 用户填写注册信息（姓名、邮箱、密码等）并提交。
    2. 已注册用户输入用户名和密码进行登录。
- **后置条件**：用户成功注册/登录或者出现注册/登录失败提示。

### 1.2 浏览商品

- **参与者**：用户
- **前置条件**：用户已登录
- **触发事件**：用户进入商品浏览页面
- **主要流程**：
    1. 用户浏览鲜花商品。
    2. 用户可以按照不同分类、价格范围等筛选商品。
- **后置条件**：用户选择或浏览商品成功。

### 1.3 购买商品

- **参与者**：用户
- **前置条件**：用户已登录且选择了商品
- **触发事件**：用户点击购买按钮
- **主要流程**：
    1. 用户将选定的商品加入购物车。
    2. 用户确认购买商品并选择配送地址、支付方式。
- **后置条件**：订单生成并显示购买成功或失败信息。

### 1.4 支付订单

- **参与者**：用户
- **前置条件**：用户已确认购买商品
- **触发事件**：用户选择支付方式
- **主要流程**：
    1. 用户选择支付方式（如信用卡、支付宝等）。
    2. 系统处理支付请求并返回支付结果。
- **后置条件**：订单支付成功或失败。

### 1.5 管理个人信息

- **参与者**：用户
- **前置条件**：用户已登录
- **触发事件**：用户进入个人信息管理页面
- **主要流程**：
    1. 用户可以修改个人资料、管理收货地址等个人信息。
- **后置条件**：用户成功更新个人信息。

### 1.6 订单管理

- **参与者**：用户、管理员
- **前置条件**：用户或管理员已登录
- **触发事件**：用户或管理员进入订单管理页面
- **主要流程**：
    1. 用户可以查看订单历史记录、订单状态和订单详情。
    2. 管理员可以处理订单（发货、取消订单等）。
- **后置条件**：订单状态更新或管理员处理订单成功。

### 1.7 管理商品

- **参与者**：管理员
- **前置条件**：管理员已登录
- **触发事件**：管理员进入商品管理页面
- **主要流程**：
    1. 管理员可以添加、编辑或删除商品信息。
    2. 可以设置商品的价格、库存等信息。
- **后置条件**：商品信息成功更新。

### 1.8 评论与评分

- **参与者**：用户
- **前置条件**：用户已购买商品
- **触发事件**：用户进入商品评价页面
- **主要流程**：
    1. 用户对购买过的商品进行评价和评分。
    2. 其他用户可以查看评价来决定购买。
- **后置条件**：评价成功提交并显示。

## 2. 用例建模

- 用例图：展示参与者和用例之间的关系和交互。
- 活动图：描述用例的活动流程，例如购买商品的流程图。
- 顺序图：展示参与者之间或参与者与系统之间的交互顺序，比如订单支付时的顺序图。

## 3. 用例分析

- 确认每个用例是否覆盖了实际业务需求。
- 确认用例描述的准确性和完整性。
- 确保用例满足用户和系统的交互需求。

## 4. 验证和确认

- 与利益相关者共同确认用例的正确性和完整性。
- 确保用例描述与实际需求一致，满足用户期望。