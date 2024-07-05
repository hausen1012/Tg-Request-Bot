import os
import yaml
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 检查是否存在 config.yaml 文件
if os.path.exists('./data/config.yaml'):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
else:
    config = {'services': []}  # 如果 config.yaml 不存在，使用空配置

# 加载环境变量
API_TOKEN = os.getenv('API_TOKEN')
ROW_WIDTH = int(os.getenv('ROW_WIDTH', 4))

bot = telebot.TeleBot(API_TOKEN)

# 将配置文件加载到内存中
services = config['services']

# 处理 /start 命令
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=4)  # 每行显示两个按钮
    buttons = [InlineKeyboardButton(service['name'], callback_data=service['name']) for service in services]
    markup.add(*buttons)
    message_text = "🔥请选择一个服务🔥\n" + "\n".join([f"{i+1}. {service['name']}" for i, service in enumerate(services)])
    bot.send_message(message.chat.id, text=message_text, reply_markup=markup)

# 处理菜单选择
@bot.callback_query_handler(func=lambda call: True)
def handle_menu_selection(call):
    service = next((s for s in services if s['name'] == call.data), None)
    if service:
        if 'param' in service:
            tip = service.get('tips', f"请发送参数 '{service['param']}' 的值：")
            msg = bot.send_message(call.message.chat.id, tip)
            bot.register_next_step_handler(msg, lambda message: handle_service_request(message, service))
        else:
            handle_service_request(None, service, call.message.chat.id)

def handle_service_request(message, service, chat_id=None):
    if chat_id is None:
        chat_id = message.chat.id
    param_value = message.text if message else None
    if service['method'] == 'POST':
        response = requests.post(service['url'], data={service['param']: param_value} if param_value else None)
    else:
        response = requests.get(service['url'], params={service['param']: param_value} if param_value else None)
  
    response_text = response.text.strip()
    if response.status_code == 200:
        bot.send_message(chat_id, f"请求成功: {response_text}" if response_text else "请求成功")
    else:
        bot.send_message(chat_id, f"请求失败: {response_text}" if response_text else "请求失败")

# 启动 bot
bot.polling()
