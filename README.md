# Open Lg Box

利用 [Luogu 网](https://www.luogu.com.cn/) 公开的用户奖项认证信息以及 [OIerDB](https://oier.baoshuo.dev/) 的公开信息进行身份猜测。

## 部署

1. 下载 Python，请注意项目在 Python 3.14 上开发；
2. 安装依赖，可以在项目目录下使用 `python -m pip install -r requirements.txt`；
3. 下载项目 [OIerDb-data-generator](https://github.com/OIerDb-ng/OIerDb-data-generator/)，并按照项目要求生成数据，本项目运行需要 `dist/result.txt` 和 `static/contests.json` 两个文件。

## 配置

新建 `config` 文件夹，并在文件夹下新建 `config.json` 文件。

文件内容需要形如：

```json
{
    "uid": <your-uid>,
    "client_id": <your-client-id>,
    "oierdb_result": "./config/result.txt",
    "oierdb_contests": "./config/contests.json"
}
```

其中 `uid` 和 `client_id` 是 Luogu cookies 的两项，`oierdb_result` 和 `oierdb_contests` 存储项目 `OIerDb-data-generator` 中获取的两个文件的位置。

考虑到 cookies 比文件地址更容易变化，且在不提供 cookies 的情形下也可以获取部分信息，`uid` 和 `client_id` 的配置是可选的。

`oierdb_result` 和 `oierdb_contests` 的缺失不会导致报错，但无法筛选出可能的选手。

## 运行

执行 `python -u main.py -h` 查看帮助：

```plaintext
usage: main.py [-h] [-s] [-u UID] [-c CLIENT_ID] [-i INITIALS] [--only-search] user

Find matching OIER records based on Luogu user achievements.

positional arguments:
  user                  Luogu user (name or uid)

options:
  -h, --help            show this help message and exit
  -s, --strict          Enable strict matching (all records must match)
  -u, --uid UID         Luogu API UID
  -c, --client_id CLIENT_ID
                        Luogu API Client ID
  -i, --initials INITIALS
                        Filter by guessed initials (use `,` to separate multiple)
  --only-search         Only search for user info without filtering OIERDB
```

简单来讲，可以运行以下命令执行最基础的功能：

```bash
python -u main.py <user>
```

其中 `<user>` 可以选择 uid 或 username，这里的自动判断是基于洛谷用户搜索 API，并选择 API 提供的第一个用户，不排除用户名为数字导致歧义的情形，但在出现实例前不计划修复。

还有一些可选选项。

### `--strict`

严格匹配奖项，选择这一个选项后，项目程序会将用户在洛谷显示且 OIerDB 上记录的奖项与 OIerDB 上的比赛记录严格匹配。

若假定用户在 Luogu 认证了全部奖项，可以开启此选项。

由于 Luogu 的评级与 CCF 评级略有差异（更严格，因此洛谷评级不会大于 CCF 评级），因此不支持评级的严格匹配。

### `--uid`, `--client_id`

命令行指定 Luogu cookies，会覆盖 `config/config.json` 的设置。

### `--initials`

缩写指定，可以选择若干个姓名缩写，然后脚本只会匹配符合缩写的选手。

多个姓名使用 `,` 分开。

### `--only-search`

只读取在 Luogu 上公布的数据，不筛选。
