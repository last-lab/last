# ChangeLog

## 0.1

### 0.1.4

- Fix bug in bulk action link.
- Add `Boolean` filter.
- Fix multiple json field input.
- Fix translations build.
- Add `Link` display.
- Improve datetime and date input

### 0.1.3

- Fix action link.
- Fix `get_m2m_field`.
- Refactor `ComputeField`.
- Upgrade `aioredis` to `2.0`.
- Make `get_current_admin` error to `401` and add `401` error page.

### 0.1.2

- Use `str` type for `pk` path param.
- Fix `Image` input. (#1)
- `filters` can accept `str` type and default use 'Search' filter.
- Add google recaptcha v2 support.

### 0.1.1

- Add another layout.
- Add `column_attributes`.
- Add import and export and `resource.get_toolbar_actions()`.
- Add `DistinctColumn` filter.
- Fix datetime filter.
- Add `resource.get_compute_fields`.

### 0.1.0

- First release.
