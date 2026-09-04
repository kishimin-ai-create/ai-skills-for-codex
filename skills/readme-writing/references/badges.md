# Tech Stack バッジの確定値

`## Tech Stack` に並べる shields.io バッジの、ロゴスラッグとブランド色。スラッグを推測すると壊れた画像が表示され、README の第一印象がそこで損なわれる。表に無い技術は推測せず、後述の無地バッジにする。

## 基本形

```text
https://img.shields.io/badge/-<表示名>-<HEX>.svg?logo=<スラッグ>&style=for-the-badge&logoColor=white
```

- `<表示名>` の空白は `%20`、`-` は `--` にエスケープする。
- 背景色が明るい技術（黄、水色、黄緑）は `logoColor=white` だとロゴが消える。表の「logoColor」列に `black` とある場合はそちらを使う。
- ロゴが無い、またはスラッグが不明な技術は無地バッジにする。

```text
https://img.shields.io/badge/-<表示名>-000000.svg?style=for-the-badge
```

## 言語 / ランタイム

| 技術 | HEX | logo | logoColor |
| ---- | --- | ---- | --------- |
| TypeScript | `3178C6` | `typescript` | white |
| JavaScript | `F7DF1E` | `javascript` | **black** |
| Python | `3776AB` | `python` | white |
| Go | `00ADD8` | `go` | white |
| Rust | `000000` | `rust` | white |
| Ruby | `CC342D` | `ruby` | white |
| PHP | `777BB4` | `php` | white |
| .NET | `512BD4` | `dotnet` | white |
| Node.js | `339933` | `nodedotjs` | white |
| Bun | `000000` | `bun` | white |
| Deno | `70FFAF` | `deno` | **black** |

## フレームワーク

| 技術 | HEX | logo | logoColor |
| ---- | --- | ---- | --------- |
| React | `61DAFB` | `react` | **black** |
| Next.js | `000000` | `nextdotjs` | white |
| Vue.js | `4FC08D` | `vuedotjs` | white |
| Svelte | `FF3E00` | `svelte` | white |
| Vite | `646CFF` | `vite` | white |
| Hono | `E36002` | `hono` | white |
| FastAPI | `009688` | `fastapi` | white |
| Django | `092E20` | `django` | white |
| Flask | `000000` | `flask` | white |
| Ruby on Rails | `D30001` | `rubyonrails` | white |
| Laravel | `FF2D20` | `laravel` | white |
| Spring Boot | `6DB33F` | `springboot` | white |

## データ / ORM

| 技術 | HEX | logo | logoColor |
| ---- | --- | ---- | --------- |
| PostgreSQL | `4169E1` | `postgresql` | white |
| MySQL | `4479A1` | `mysql` | white |
| SQLite | `003B57` | `sqlite` | white |
| Redis | `FF4438` | `redis` | white |
| Prisma | `2D3748` | `prisma` | white |
| Drizzle ORM | `C5F74F` | `drizzle` | **black** |

## テスト / 品質

| 技術 | HEX | logo | logoColor |
| ---- | --- | ---- | --------- |
| Vitest | `6E9F18` | `vitest` | white |
| Jest | `C21325` | `jest` | white |
| pytest | `0A9EDC` | `pytest` | white |
| Playwright | `2EAD33` | `playwright` | white |
| Storybook | `FF4785` | `storybook` | white |
| ESLint | `4B32C3` | `eslint` | white |
| Prettier | `F7B93E` | `prettier` | **black** |
| Ruff | `D7FF64` | `ruff` | **black** |

## インフラ / CI

| 技術 | HEX | logo | logoColor |
| ---- | --- | ---- | --------- |
| Docker | `2496ED` | `docker` | white |
| Kubernetes | `326CE5` | `kubernetes` | white |
| Terraform | `844FBA` | `terraform` | white |
| GitHub Actions | `2088FF` | `githubactions` | white |
| Cloudflare Workers | `F38020` | `cloudflareworkers` | white |
| Tailwind CSS | `06B6D4` | `tailwindcss` | white |

## ロゴが無い技術の例

Pillow、mypy、Black、pandas の一部など、simple-icons に無い、または表示が安定しない技術は無地で書く。glyph-forge の README も Pillow をこの形にしている。

```text
https://img.shields.io/badge/-Pillow-000000.svg?style=for-the-badge
```

## スラッグを確認したい場合

`https://simpleicons.org/` で技術名を検索すると、スラッグとブランド色が確認できる。確認できないまま推測して書くくらいなら、無地バッジにする方が結果が良い。
