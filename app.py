from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# 用列表存储留言，每条留言是一个字典 { 'id': 序号, 'content': 内容 }
messages = []
counter = 1   # 用于生成递增 ID

# HTML 模板（直接写在字符串中，方便单文件运行）
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>局域网留言板</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 20px auto; padding: 0 15px; }
        h2 { color: #333; }
        .msg-list { list-style: none; padding: 0; }
        .msg-item { background: #f5f5f5; margin: 8px 0; padding: 10px; border-radius: 4px; }
        .msg-id { font-weight: bold; color: #666; margin-right: 8px; }
        textarea { width: 100%; height: 80px; padding: 8px; box-sizing: border-box; }
        input[type="submit"] { background: #007bff; color: white; border: none; padding: 10px 25px;
                              border-radius: 4px; cursor: pointer; font-size: 16px; }
        input[type="submit"]:hover { background: #0056b3; }
        a.refresh { display: inline-block; margin-top: 15px; color: #007bff; text-decoration: none; }
        a.refresh:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h2>局域网留言板</h2>

    <!-- 留言表单 -->
    <form method="POST" action="/add">
        <textarea name="content" placeholder="请输入您的留言..." required></textarea><br>
        <input type="submit" value="提交留言">
    </form>

    <!-- 刷新链接 -->
    <a class="refresh" href="{{ url_for('index') }}">刷新查看最新留言</a>

    <!-- 留言列表 -->
    <h3>全部留言 ({{ messages|length }})</h3>
    {% if messages %}
    <ul class="msg-list">
        {% for msg in messages | reverse %}   <!-- 最新留言显示在最上面 -->
        <li class="msg-item">
            <span class="msg-id">#{{ msg.id }}</span>
            {{ msg.content }}
        </li>
        {% endfor %}
    </ul>
    {% else %}
    <p>暂无留言，快来写下第一条吧！</p>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, messages=messages)

@app.route('/add', methods=['POST'])
def add_message():
    global counter
    content = request.form.get('content', '').strip()
    if content:
        messages.append({'id': counter, 'content': content})
        counter += 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 监听所有网络接口，允许局域网其他设备访问
    app.run(host='0.0.0.0', port=5000, debug=False)