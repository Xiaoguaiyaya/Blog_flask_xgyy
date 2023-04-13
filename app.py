from flask import *

import config
from decorators import login_limit

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = "flaskblog"

app.debug = True

# 注册蓝图
from view import *

app.register_blueprint(index)
app.register_blueprint(blog)

from model import *

import openai

chat_gpt_key = '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'
# 将 Key 进行传入
openai.api_key = chat_gpt_key

def completion(prompt):
    response = openai.Completion.create(
        # text-davinci-003 是指它的模型
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048,
        n=1,
        stop=None
    )

    message = response.choices[0].text
    #message=prompt
    return message

# 上下文处理器，定义用户当前是否登录状态，全局可访问
@app.context_processor
def login_statue():
	# 获取session中的username
	username = session.get('username')
	# 如果username不为空，则已登录，否则没有登录
	if username:
		try:
			# 登录后，查询用户信息并返回用户信息
			user = User.query.filter(User.username == username).first();
			if user:
				return {"username": username, 'name': user.name, 'password': user.password}
		except Exception as e:
			return e
	# 如果没有登录，返回空
	return {}


# 404页面
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404;


# 500页面
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('404.html'), 404;


@app.route('/tiw',methods=["POST","GET"])
@login_limit
def hello_world():  # put application's code here
    return render_template('test.html')

@app.route('/ans',methods=["POST","GET"])
@login_limit
def ans():  # put application's code here
    result = request.form.get('name')
    answer = completion(result)
    return render_template('test.html', answer=answer)

if __name__ == '__main__':
	app.run(host='192.168.33.39' ,port=12345)
