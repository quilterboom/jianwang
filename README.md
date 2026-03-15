# 鉴往 - 投资犯错记录系统

> 悟已往之不谏，知来者之可追

## 项目功能

### 用户功能
- ✅ 用户注册、登录、退出
- ✅ 个人统计面板：累计犯错次数、无犯错记录天数
- ✅ 记录犯错信息：投资类型选择、犯错原因填写
- ✅ 历史记录查询：按时间倒序展示所有犯错记录
- ✅ 自动统计：保存记录后犯错次数+1，无犯错天数自动归零
- ✅ 无犯错天数自动计算：每天自动+1

### 投资类型
- 币圈
- A股
- 基金
- 债券
- 期货
- 期权
- 房地产
- 其他

## 技术栈

### 后端
- Django 5.0.3
- Django REST Framework
- MySQL 8.0
- Python 3.12

### 前端
- 原生 HTML/CSS/JavaScript
- Tailwind CSS
- Font Awesome

## 项目结构

```
/data/test_project/
├── jianwang/              # Django项目配置
├── core/                  # 核心应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图函数
│   ├── serializers.py     # 序列化器
│   └── urls.py            # API路由
├── frontend/              # 前端页面
│   └── index.html         # 单页面应用
├── venv/                  # Python虚拟环境
├── requirements.txt       # Python依赖
├── .env                   # 环境变量配置
└── README.md              # 项目说明
```

## 访问方式

开发服务器已启动，访问地址：
```
http://服务器IP:3001
```

## 本地开发

### 启动服务
```bash
# 进入项目目录
cd /data/test_project

# 激活虚拟环境
source venv/bin/activate

# 启动开发服务器
python manage.py runserver 0.0.0.0:3001
```

### 管理后台
创建超级用户：
```bash
python manage.py createsuperuser
```
访问后台：`http://服务器IP:3001/admin`

## 数据库配置

- 数据库名：Demo
- 用户名：root
- 密码：Lyp552034#
- 主机：127.0.0.1
- 端口：3306

## API 接口

- `POST /api/register/` - 用户注册
- `POST /api/login/` - 用户登录
- `POST /api/logout/` - 退出登录
- `GET /api/profile/` - 获取用户信息
- `GET /api/investment-types/` - 获取投资类型列表
- `GET /api/mistake-records/` - 获取犯错记录列表
- `POST /api/mistake-records/` - 创建新的犯错记录
- `GET /api/mistake-records/<id>/` - 获取单条记录详情
- `PUT /api/mistake-records/<id>/` - 更新记录
- `DELETE /api/mistake-records/<id>/` - 删除记录

## 注意事项

1. 开发服务器仅用于测试，生产环境请使用 Gunicorn + Nginx 部署
2. 请确保 MySQL 服务正常运行
3. 定期备份数据库数据
4. 生产环境请修改 `SECRET_KEY` 并关闭 `DEBUG` 模式
