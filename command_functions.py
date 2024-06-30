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
shap_text="""**Understanding SHAP Graphs**
SHapley Additive exPlanations charts help explain how each factor (e.g., amount of sleep, physical activity, social interactions) affects your stress level or mood. This is important so that you can better understand which aspects of your lifestyle or environment most affect your well-being.

**How do I read SHAP charts?**

1. Graph Of The Influence Of Features (SHAP Summary Plot):
- Color Labels: Each color represents the value of a feature (for example, red is a high value, blue is a low value).
    - Y axis: Various factors that affect your stress level/mood (e.g. amount of sleep, physical activity).
    - X-axis: The influence of each factor on the prediction of the model. A positive value indicates an increase in stress/mood levels, a negative value indicates a decrease.

2. SHAP Force Plot:
- X-Axis: Each individual prediction.
    - Color Bar: Various factors influencing the prediction are shown, where the width of the bar indicates the strength of the influence. The red stripes indicate factors that increase stress/mood levels, and the blue stripes indicate factors that lower it.

**Why is this necessary?**

These graphs will help you:
- Identify key factors: Understand which specific aspects of your life most strongly affect your well-being.
- Take action: For example, if you see that lack of sleep greatly increases your stress level, you can focus on improving the quality and duration of sleep.
- Improve your quality of life: Using these insights, you can make lifestyle changes to improve your mood and reduce stress levels.

**Remember that SHAP charts provide personalized recommendations based on your data, helping you make informed decisions to improve your health and well-being.**"
"""

class CommandFuncs:        
    def start(update, context):
        with open('pictures/preview1.png', 'rb') as image:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=preview_text)
            
    def shap(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=shap_text, parse_mode='Markdown')
            
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
