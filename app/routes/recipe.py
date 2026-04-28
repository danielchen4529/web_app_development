from flask import Blueprint, request, render_template, redirect, url_for, flash

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
@recipe_bp.route('/recipes', methods=['GET'])
def index():
    """
    輸入: URL 參數 q (搜尋關鍵字，選填)
    處理邏輯: 查詢所有食譜，若有搜尋關鍵字則進行過濾
    輸出: 渲染 recipes/index.html 模板
    """
    pass

@recipe_bp.route('/recipes/new', methods=['GET'])
def new():
    """
    輸入: 無
    處理邏輯: 取得所有分類資料，準備給新增表單的下拉選單使用
    輸出: 渲染 recipes/new.html 模板
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create():
    """
    輸入: 表單資料 (title, ingredients, instructions, category_id, image)
    處理邏輯: 驗證表單資料，儲存圖片至 static/uploads/，呼叫 Recipe.create() 存入資料庫
    輸出: 成功則重導向至詳細頁 (GET /recipes/<id>)，失敗則重新渲染 new.html 並顯示錯誤
    """
    pass

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def detail(id):
    """
    輸入: URL 參數 id
    處理邏輯: 呼叫 Recipe.get_by_id(id) 取得指定食譜
    輸出: 渲染 recipes/detail.html 模板，若找不到資料回傳 404
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit(id):
    """
    輸入: URL 參數 id
    處理邏輯: 取得指定食譜以及所有分類資料，準備填入表單
    輸出: 渲染 recipes/edit.html 模板，若找不到資料回傳 404
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update(id):
    """
    輸入: URL 參數 id 以及更新的表單資料
    處理邏輯: 取得指定食譜，驗證並更新表單資料與圖片，呼叫 Recipe.update()
    輸出: 成功則重導向至詳細頁，失敗則重新渲染 edit.html，找不到資料回傳 404
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    輸入: URL 參數 id
    處理邏輯: 取得指定食譜，刪除關聯圖片後呼叫 Recipe.delete() 移除資料庫紀錄
    輸出: 重導向至首頁 (GET /)
    """
    pass
