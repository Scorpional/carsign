# 通勤/包车企业调度系统 MVP

FastAPI + PostgreSQL + Docker Compose，一键启动展示“订单→排班→派车→出车→回单→报表”闭环，含 JWT 鉴权与基础 RBAC。

## 快速启动（本地/服务器，单容器 SQLite）
```bash
cp .env.example .env
docker compose up -d --build
```
- Web/API: http://localhost:8080 （同端口，Swagger: http://localhost:8080/api/docs）
- 默认管理员：`admin@example.com` / `Admin123!`（可在 `.env` 修改）

## 目录说明
- `app/` FastAPI 应用、路由、模板、静态资源
- `app/migrations/` Alembic 迁移
- `uploads/` 回单/照片（容器卷挂载）
- `app/seed.py` 测试数据种子
- `data/` SQLite 持久化（部署时挂载卷）

## 数据迁移
容器启动自动执行 `alembic upgrade head`。手动：
```bash
docker compose run --rm api alembic upgrade head
```

## 初始化管理员
启动时自动跑 `python app/init_admin.py`。需要重新创建时：
```bash
docker compose run --rm api python app/init_admin.py
```

## 种子数据（可选）
```bash
docker compose run --rm api python app/seed.py
```

## 备份/恢复
- SQLite 备份：打包/复制 `data/app.db`
- 上传文件：打包 `uploads/`

## 健康检查
- DB: Docker healthcheck
- API: `GET /health`

## 权限
- 角色：admin 全权限；dispatcher 可派车/管理台账；driver 仅自己的行程
- JWT 过期时间：`.env` 中配置
- 上传限制：类型 png/jpg/pdf，大小 10MB

## 部署到 Zeabur（单容器，无外部 DB）
1. 连接 GitHub 仓库，直接用 Dockerfile 构建。
2. 环境变量：`DATABASE_URL=sqlite:///./data/app.db`，`JWT_SECRET`，`ADMIN_EMAIL`，`ADMIN_PASSWORD`（其余 Postgres 变量可忽略）。
3. 持久化存储：挂载卷到 `/app/data`（SQLite）与 `/app/uploads`（回单）。
4. 启动命令已写入 Dockerfile 默认 CMD（/app/start.sh），Zeabur 不必额外配置：  
   - 正常模式：自动创建目录、init_admin，然后 `uvicorn app.main:app`。  
   - 静态演示模式：设置 `DEMO_STATIC=1` 环境变量，将直接启动 `python -m http.server 8000` 访问 `/demo`（无需数据库）。
5. 暴露端口：8000 -> 对外 8080。
6. 需要演示数据（动态模式）：`docker compose run --rm app python app/seed.py`（Zeabur 可开一次性任务执行）。

## 演示流程
1. 管理员登录，创建车辆/司机/订单（`/api/docs`）。
2. 调度员为订单生成派车单（自动冲突校验与行程号）。
3. 司机登录（邮箱需与人员表 phone 对应），`/api/trips/mine` 查看并更新状态：accepted → departed → arrived → finished。
4. 司机上传回单 `/api/trips/{id}/upload`。
5. 导出报表：`/api/export/orders`, `dispatch`, `trips`, `vehicle_usage`, `driver_attendance`。
6. 操作日志接口 `/api/logs` 查看关键留痕。
