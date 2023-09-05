# FastAPI Admin Pro

As sponsor, you can make feature request [here](https://github.com/fastapi-admin/fastapi-admin-pro/discussions/3), and I
will consider to implement it.

## Introduction

`fastapi-admin` is a fast admin dashboard based on [FastAPI](https://github.com/tiangolo/fastapi)
and [TortoiseORM](https://github.com/tortoise/tortoise-orm/) with [tabler](https://github.com/tabler/tabler) ui,
inspired by Django admin.

## Installation

```shell
> pip install git+https://github.com/fastapi-admin/fastapi-admin-pro.git
```

## Requirements

- [Redis](https://redis.io)

## Online Demo

You can check a online demo [here](https://fastapi-admin-pro.long2ice.io/admin/login).

- username: `admin`
- password: `123456`

## Screenshots

![login](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/login.png)

![dashboard](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/dashboard.png)

## Documentation

See documentation at <https://fastapi-admin-docs.long2ice.io>.

## Run examples in local

1. Clone repo.
2. Create `.env` file.

   ```dotenv
   DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin
   REDIS_URL=redis://localhost:6379/0
   ```

3. Run `docker-compose up -d --build`.
4. Visit <http://localhost:8000/admin/init> to create first admin.

## License

After you have be invited, you can read and clone and develop yourself, but please **don't distribute the source code**
of pro version. Thanks!
