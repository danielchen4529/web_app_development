# 路由設計文件 (ROUTES)

本文件規劃「食譜收藏夾系統」的所有路由，定義每個頁面的 URL 路徑、HTTP 方法、輸入輸出以及對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 食譜清單 | GET | `/` 或 `/recipes` | `templates/recipes/index.html` | 顯示所有食譜，支援關鍵字搜尋 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipes/new.html` | 顯示填寫食譜的表單 |
| 建立食譜 | POST | `/recipes` | — | 接收表單資料、儲存圖片與寫入資料庫，完成後重導向至列表或詳細頁 |
| 食譜詳細頁面 | GET | `/recipes/<int:id>` | `templates/recipes/detail.html` | 顯示單一食譜的詳細資訊 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit` | `templates/recipes/edit.html` | 顯示原有食譜資料的編輯表單 |
| 更新食譜 | POST | `/recipes/<int:id>/edit` | — | 接收編輯後的表單資料並更新資料庫，完成後重導向至詳細頁 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete`| — | 刪除資料庫中的食譜紀錄，完成後重導向至首頁 |

*(註：由於系統使用原生 HTML 表單，更新與刪除操作會使用 POST 方法代替 PUT / DELETE)*

## 2. 每個路由的詳細說明

### 2.1 首頁 / 食譜清單
*   **輸入**：URL 參數 `?q=關鍵字` (選填，用於搜尋)
*   **處理邏輯**：
    *   如果有 `q` 參數，呼叫 `Recipe.query.filter(Recipe.title.contains(q))` 等方法過濾。
    *   如果沒有 `q` 參數，呼叫 `Recipe.get_all()` 取得所有食譜。
*   **輸出**：渲染 `recipes/index.html` 模板，傳入 `recipes` 變數。
*   **錯誤處理**：無特殊錯誤，若無資料則傳遞空陣列。

### 2.2 新增食譜頁面
*   **輸入**：無
*   **處理邏輯**：呼叫 `Category.get_all()` 取得所有分類，供下拉選單使用。
*   **輸出**：渲染 `recipes/new.html` 模板，傳入 `categories` 變數。
*   **錯誤處理**：無。

### 2.3 建立食譜
*   **輸入**：表單資料 (`title`, `ingredients`, `instructions`, `category_id`) 與檔案上傳 (`image`)
*   **處理邏輯**：
    1.  驗證必填欄位 (title, ingredients, instructions)。
    2.  若有圖片上傳，將檔案儲存至 `static/uploads/` 並取得路徑。
    3.  呼叫 `Recipe.create(...)` 建立新紀錄。
*   **輸出**：成功後重導向 (Redirect) 至 `/recipes/<new_id>` (詳細頁)。
*   **錯誤處理**：若驗證失敗，將錯誤訊息存入 Flash Messages，並重新渲染 `recipes/new.html` 讓使用者修正。

### 2.4 食譜詳細頁面
*   **輸入**：URL 變數 `id`
*   **處理邏輯**：呼叫 `Recipe.get_by_id(id)` 取得指定食譜。
*   **輸出**：渲染 `recipes/detail.html` 模板，傳入 `recipe` 變數。
*   **錯誤處理**：若查無此 id，回傳 404 頁面。

### 2.5 編輯食譜頁面
*   **輸入**：URL 變數 `id`
*   **處理邏輯**：
    1.  呼叫 `Recipe.get_by_id(id)` 取得指定食譜。
    2.  呼叫 `Category.get_all()` 取得所有分類。
*   **輸出**：渲染 `recipes/edit.html` 模板，傳入 `recipe` 與 `categories` 變數。
*   **錯誤處理**：若查無此 id，回傳 404 頁面。

### 2.6 更新食譜
*   **輸入**：URL 變數 `id`，表單資料與檔案上傳 (`image`)
*   **處理邏輯**：
    1.  取得指定食譜。
    2.  驗證必填表單資料。
    3.  處理新上傳的圖片 (若有)。
    4.  呼叫 `recipe.update(...)` 更新資料庫。
*   **輸出**：成功後重導向 (Redirect) 至 `/recipes/<id>`。
*   **錯誤處理**：若查無此 id，回傳 404 頁面。驗證失敗則重新渲染 `recipes/edit.html`。

### 2.7 刪除食譜
*   **輸入**：URL 變數 `id`
*   **處理邏輯**：
    1.  取得指定食譜。
    2.  刪除關聯的圖片檔案 (選用)。
    3.  呼叫 `recipe.delete()` 刪除資料庫紀錄。
*   **輸出**：成功後重導向 (Redirect) 至 `/` (首頁)。
*   **錯誤處理**：若查無此 id，回傳 404 頁面。

## 3. Jinja2 模板清單

所有的模板將繼承自一個基礎的 `base.html`，以保持整體的 UI 一致性（如：共用導覽列、頁尾）。

| 檔案名稱 | 繼承自 | 說明 |
| :--- | :--- | :--- |
| `base.html` | (無) | **共用版型**，包含 `<head>`、Navbar、Flash 訊息顯示區域與 Footer。 |
| `recipes/index.html` | `base.html` | **列表頁**，顯示搜尋框與食譜卡片陣列。 |
| `recipes/new.html` | `base.html` | **新增頁**，提供填寫食譜內容與上傳圖片的表單。 |
| `recipes/detail.html`| `base.html` | **詳細頁**，完整顯示圖片、食材清單、料理步驟與編輯/刪除按鈕。 |
| `recipes/edit.html` | `base.html` | **編輯頁**，顯示預設值為原有資料的表單。 |
