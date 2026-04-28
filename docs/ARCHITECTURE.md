# 系統架構文件 (Architecture)

這份文件說明「食譜收藏夾系統」的技術架構與專案結構設計。

## 1. 技術架構說明

本專案採用經典的伺服器端渲染 (Server-Side Rendering) 架構，不採用前後端分離，以求快速開發與簡化部署流程。

### 選用技術與原因

*   **後端框架：Python + Flask**
    *   **原因**：Flask 是一個輕量級的微框架，彈性極高，非常適合用來打造個人專案或 MVP (Minimum Viable Product)。它的學習曲線平緩，且能快速建置出可用的 Web 應用。
*   **模板引擎：Jinja2**
    *   **原因**：Jinja2 是 Flask 預設搭配的模板引擎。它可以讓我們在 HTML 檔案中寫入 Python 風格的邏輯（例如 if 判斷式、for 迴圈），負責將後端處理好的資料動態渲染成 HTML 頁面並回傳給使用者。
*   **資料庫：SQLite (搭配 SQLAlchemy)**
    *   **原因**：SQLite 是輕量級的關聯式資料庫，不需要額外安裝資料庫伺服器，資料都儲存在單一檔案中，非常適合本機開發及個人輕量使用。我們將透過 SQLAlchemy (ORM) 來操作資料庫，這樣能用 Python 程式碼來取代原生 SQL 語法，提高開發效率與安全性（可防範 SQL Injection）。
*   **前端樣式：純 CSS 或輕量化 CSS 框架**
    *   **原因**：保持專案輕量，並滿足基本的手機觀看（RWD）需求。

### Flask MVC 模式說明

我們將採用類似 MVC (Model-View-Controller) 的設計模式來組織程式碼：

*   **Model (模型)**：負責定義資料結構與資料庫互動。
    *   在我們的專案中，對應 `app/models/` 目錄下的檔案。例如定義 `Recipe` (食譜)、`Tag` (標籤) 等資料表結構。
*   **View (視圖)**：負責呈現使用者介面。
    *   由 `Jinja2` 模板負責，對應 `app/templates/` 目錄。Controller 會將資料傳遞給 View，View 將資料填入 HTML 中，最後顯示在瀏覽器上。
*   **Controller (控制器)**：負責接收使用者的請求 (Request)，處理商業邏輯，並決定要回傳哪個 View。
    *   在 Flask 中，這由路由 (Routes) 函式來擔任。對應 `app/routes/` 目錄下的檔案。

## 2. 專案資料夾結構

為了讓專案具備良好的可維護性與擴展性，我們採用以下資料夾結構：

```text
web_app_development/
├── app/                    # 應用程式主目錄
│   ├── __init__.py         # 初始化 Flask 應用程式與設定
│   ├── models/             # (Model) 資料庫模型定義
│   │   ├── __init__.py
│   │   └── recipe.py       # 食譜、分類等資料表結構
│   ├── routes/             # (Controller) Flask 路由與邏輯
│   │   ├── __init__.py
│   │   └── recipe.py       # 處理食譜的 CRUD (新增/讀取/更新/刪除) 請求
│   ├── templates/          # (View) Jinja2 HTML 模板
│   │   ├── base.html       # 共用版型 (Header, Footer, Navbar)
│   │   └── recipes/        # 食譜相關的頁面 (列表、新增、編輯、詳細內容)
│   └── static/             # 靜態資源 (CSS, JS, 圖片)
│       ├── css/            # 樣式表
│       ├── js/             # 前端腳本
│       └── uploads/        # 使用者上傳的食譜圖片
├── instance/               # 存放會隨環境變動且不進版控的檔案
│   └── database.db         # SQLite 資料庫檔案
├── docs/                   # 專案文件
│   ├── PRD.md              # 產品需求文件
│   └── ARCHITECTURE.md     # 系統架構文件 (本文件)
├── requirements.txt        # Python 依賴套件清單 (例如 flask, flask-sqlalchemy 等)
├── .gitignore              # Git 忽略清單 (例如忽略 instance/, __pycache__/ 等)
└── app.py                  # 程式啟動入口
```

## 3. 元件關係圖

以下關係圖展示了使用者在瀏覽器操作時，系統內部的運作流程：

```mermaid
flowchart TD
    Browser[瀏覽器 (使用者)]

    subgraph "Flask 應用程式 (伺服器端)"
        Router[Flask Route (Controller)\n接收 Request，決定處理邏輯]
        Model[Database Model\nSQLAlchemy ORM]
        Template[Jinja2 Template (View)\n渲染 HTML 頁面]
    end

    DB[(SQLite 資料庫\n儲存食譜與分類資料)]

    %% 請求流程
    Browser -- "1. 發送 HTTP 請求\n(例如 GET /recipes)" --> Router
    Router -- "2. 查詢或更新資料" --> Model
    Model -- "3. 讀寫資料庫" --> DB
    DB -- "4. 回傳查詢結果" --> Model
    Model -- "5. 將資料交給 Route" --> Router
    Router -- "6. 傳遞資料並指定 Template" --> Template
    Template -- "7. 產生最終 HTML\n含動態資料" --> Router
    Router -- "8. 回傳 HTTP 回應\n(HTML 網頁)" --> Browser
```

## 4. 關鍵設計決策

1.  **使用 SQLAlchemy 作為 ORM (物件關聯對映)**
    *   **原因**：直接寫 SQL 語法容易出錯且較難維護。使用 SQLAlchemy 可以讓我們用 Python 物件的方式來操作資料庫，提升程式碼的易讀性，同時自動處理 SQL Injection 防護。
2.  **採用類似 MVC 的資料夾結構，而非單一檔案開發**
    *   **原因**：雖然 Flask 允許將所有程式碼寫在一個 `app.py` 中，但為了未來加入更多功能（如分類、標籤、搜尋），提早將路由、模型、模板分離到不同的資料夾，可以降低檔案複雜度，方便維護。
3.  **不採用前後端分離 (SPA)**
    *   **原因**：此專案為個人使用的輕量級 MVP，不需要複雜的客戶端狀態管理。由伺服器端 (Jinja2) 直接渲染 HTML 能最快實作出所需功能，且架構單純，SEO (如果未來需要公開) 也較佳。
4.  **圖片處理策略：本機儲存與靜態資料夾**
    *   **原因**：為了簡化部署與開發，使用者上傳的圖片會直接儲存在 `app/static/uploads/` 目錄下。雖然這不適合大規模的雲端部署，但在「個人食譜管理」的輕量需求下，這是最直接且低成本的做法。若圖片太多，未來可考慮限制圖片上傳大小。
