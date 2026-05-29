# 持股分帳本 · Stock Ledger

> 共用股票帳戶的兩人分帳追蹤工具，獨立計算各自的持股成本與損益。

## 功能特色

- 📊 **總覽儀表板**：圓餅圖、損益長條圖、持股成本比較
- 💹 **持股分析**：依人員分開顯示持股數、均攤成本、已實現 / 未實現損益
- ⟳ **自動抓取現價**：支援台灣上市（TSE）與上櫃（OTC）股票，多重 proxy 策略確保在各種環境可用
- ✍️ **手動輸入現價**：自動抓取失敗時可直接輸入
- 📂 **CSV 匯入匯出**：兩人透過傳 CSV 檔同步資料，無需帳號或後端
- 💾 **本地儲存**：所有資料存在瀏覽器 localStorage，不上傳任何伺服器

## 使用方式

### 直接開啟（本機）
直接在瀏覽器開啟 `index.html` 即可使用（注意：本機 file:// 環境下，自動抓取股價可能受 CORS 限制，請改用手動輸入或部署到 GitHub Pages）。

### GitHub Pages 部署（推薦）

1. 在 GitHub 建立新的 **Public** repository
2. 把 `index.html` 上傳到 repository 根目錄
3. 進入 repository 的 **Settings → Pages**
4. Source 選 `Deploy from a branch`，Branch 選 `main`，資料夾選 `/ (root)`
5. 儲存後等待約 1 分鐘，即可透過 `https://你的帳號.github.io/repo名稱/` 訪問

### 資料同步方式

1. 人員 A 在「新增交易」輸入一筆交易
2. 到「CSV 匯入匯出」→「下載 CSV」
3. 把 CSV 檔傳給人員 B（LINE、Email 等均可）
4. 人員 B 開啟工具，到「CSV 匯入匯出」→「合併匯入」，即完成同步

## 股票代號格式

輸入台灣股票代號即可，例如：
- 上市股票：`2330`（台積電）、`2454`（聯發科）
- 上櫃股票：`6271`（同名公司）

## 技術說明

- 純 HTML + CSS + JavaScript，無任何後端依賴
- 使用 [Chart.js](https://www.chartjs.org/) 繪製圖表
- 股價來源：台灣證交所（TWSE）API，透過多重 CORS proxy 策略抓取
- 備援：Yahoo Finance API（支援上市 `.TW` / 上櫃 `.TWO`）
