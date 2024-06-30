from telegram.ext import ConversationHandler
from data_frame import find_shap, send_image_to_user
from google_sheet_editor import GoogleTable
from config import settings
from user_config import user_settings

preview_text="Firstable you need to /register"
register_text="Please create a google sheet and give us a link. Copy [this table template](https://docs.google.com/spreadsheets/d/14ZrJ2bnlziSelyY8X-dMbkKAMlxGfmcG-6qdyKLh5gg/edit?usp=sharing) and make yours"
optimize_metric_text="Great! Send us a metric which you want to optimize from 0 to 10. For example your mood or stress level"
set_metric1_text="Now set the first metric which you want to track. \nAttention! It must be valuable, like meters, hours, etc., but don't print a unit \nExamples: 2.39, 30, -1.0, 65536"
set_metric2_text="We received your metric, you can add 4 other or /stop_set_metrics"
set_metric3_text="Received! You can add 3 other or /stop_set_metrics"
set_metric4_text="Received! You can add 2 other or /stop_set_metrics"
set_metric5_text="Received! You can add 1 other or /stop_set_metrics"
set_metric6_text="Received!"
stop_text="Stopped receving metrics"

class CommandFuncs:        
    def start(update, context):
        with open('pictures/preview1.png', 'rb') as image:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=preview_text)
            
    def info(update, context):
        with open('pictures/preview2.png', 'rb') as image:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption="Let's /register")
            
    def register(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=register_text, parse_mode='Markdown')
        return 'GETTING_OPTIMIZE_METRIC'
    
    def get_optimization_metric(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=optimize_metric_text)
        user_input = update.message.text.strip()
        user_settings["TABLE_URL"] = user_input
        return 'GETTING METRIC 1'
        
    def get_metric1(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=set_metric1_text)
        gt=GoogleTable(settings["CREDITS_NAME"], user_settings["TABLE_URL"])
        gt._update_cell(1, 1, update.message.text)
        return 'GETTING METRIC 2'
    
    def get_metric2(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=set_metric2_text)
        gt=GoogleTable(settings["CREDITS_NAME"], user_settings["TABLE_URL"])
        gt._update_cell(1, 2, update.message.text)
        return 'GETTING METRIC 3'
    
    def get_metric3(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=set_metric3_text)
        gt=GoogleTable(settings["CREDITS_NAME"], user_settings["TABLE_URL"])
        gt._update_cell(1, 3, update.message.text)
        return 'GETTING METRIC 4'
    
    def get_metric4(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=set_metric4_text)
        gt=GoogleTable(settings["CREDITS_NAME"], user_settings["TABLE_URL"])
        gt._update_cell(1, 4, update.message.text)
        return 'GETTING METRIC 5'
    
    def get_metric5(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=set_metric5_text)
        gt=GoogleTable(settings["CREDITS_NAME"], user_settings["TABLE_URL"])
        gt._update_cell(1, 5, update.message.text)
        return 'END METRICS'
    
    def get_metric6(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=set_metric6_text)
        return ConversationHandler.END
    
    def stop_set_metrics(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=stop_text)
        return ConversationHandler.END
    
    def get_chat_id(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=f"Your chat ID is: {chat_id}")
        
    def graph_image(update, context):
        gt=GoogleTable(settings["CREDITS_NAME"], user_settings["TABLE_URL"])
        metric_name = gt._read_cell(1, 1)
        
        if metric_name:
            find_shap(gt, metric_name)
            # Sending the generated plot to the user
            send_image_to_user('shap_summary_plot.png')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Cell A1 is empty. Please provide a valid metric name.")