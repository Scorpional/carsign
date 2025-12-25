# 通勤/包车企业调度系统 MVP

FastAPI + PostgreSQL + Docker Compose，一键启动展示“订单→排班→派车→出车→回单→报表”闭环，含 JWT 鉴权与基础 RBAC。

## 快速启动（本地/服务器）
```bash
cp .env.example .env
docker compose up -d --build
```
- Web: http://localhost:8080 （Nginx 反代到 API）
- API: http://localhost:8000 （Swagger: http://localhost:8000/api/docs）
- 默认管理员：`admin@example.com` / `Admin123!`（可在 `.env` 修改）

## 目录说明
- `app/` FastAPI 应用、路由、模板、静态资源
- `app/migrations/` Alembic 迁移
- `uploads/` 回单/照片（容器卷挂载）
- `deploy/nginx.conf` 反向代理
- `app/seed.py` 测试数据种子

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
- 备份数据库: `docker compose exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql`
- 恢复: `cat backup.sql | docker compose exec -T db psql -U $POSTGRES_USER $POSTGRES_DB`
- 备份文件: 打包 `uploads/`

## 健康检查
- DB: Docker healthcheck
- API: `GET /health`

## 权限
- 角色：admin 全权限；dispatcher 可派车/管理台账；driver 仅自己的行程
- JWT 过期时间：`.env` 中配置
- 上传限制：类型 png/jpg/pdf，大小 10MB

## 部署到 Zeabur（示例流程）
1. 推送本仓库到 GitHub。
2. 在 Zeabur 新建项目并连接该仓库，选择 docker-compose 部署。
3. 配置环境变量：`POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB/DATABASE_URL/JWT_SECRET/ADMIN_EMAIL/ADMIN_PASSWORD`。
4. 挂载持久化存储到 `/app/uploads`。
5. 暴露端口：web 服务 8080（外部），api 服务 8000（内部即可）。
6. 如需演示数据：执行 `docker compose run --rm api python app/seed.py`。

## 演示流程
1. 管理员登录，创建车辆/司机/订单（`/api/docs`）。
2. 调度员为订单生成派车单（自动冲突校验与行程号）。
3. 司机登录（邮箱需与人员表 phone 对应），`/api/trips/mine` 查看并更新状态：accepted → departed → arrived → finished。
4. 司机上传回单 `/api/trips/{id}/upload`。
5. 导出报表：`/api/export/orders`, `dispatch`, `trips`, `vehicle_usage`, `driver_attendance`。
6. 操作日志接口 `/api/logs` 查看关键留痕。
