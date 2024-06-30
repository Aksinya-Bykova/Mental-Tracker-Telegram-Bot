from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from google_sheet_editor import GoogleTable
from config import settings
from command_functions import CommandFuncs

def main():
    updater = Updater(settings["TOKEN"])
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', CommandFuncs.start)
    dispatcher.add_handler(start_handler)
    
    chat_id_handler = CommandHandler('get_chat_id', CommandFuncs.get_chat_id)
    dispatcher.add_handler(chat_id_handler)
    
    graph_image_handler = CommandHandler('graph_image', CommandFuncs.graph_image)
    dispatcher.add_handler(graph_image_handler)
    
    shap_handler = CommandHandler('shap', CommandFuncs.shap)
    dispatcher.add_handler(shap_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', CommandFuncs.register)],
        states={
            'GETTING_OPTIMIZE_METRIC': [MessageHandler(Filters.text & ~Filters.command, CommandFuncs.get_optimization_metric)],
            'GETTING METRIC 1': [MessageHandler(Filters.text & ~Filters.command, CommandFuncs.get_metric1)],
            'GETTING METRIC 2': [MessageHandler(Filters.text & ~Filters.command, CommandFuncs.get_metric2)],
            'GETTING METRIC 3': [MessageHandler(Filters.text & ~Filters.command, CommandFuncs.get_metric3)],
            'GETTING METRIC 4': [MessageHandler(Filters.text & ~Filters.command, CommandFuncs.get_metric4)],
            'GETTING METRIC 5': [MessageHandler(Filters.text & ~Filters.command, CommandFuncs.get_metric5)],
            'END METRICS': [MessageHandler(Filters.text & ~Filters.command, CommandFuncs.get_metric6)],
            'DONE': [CommandHandler('stop_set_metrics', CommandFuncs.stop_set_metrics)]
        },
        fallbacks=[CommandHandler('stop_set_metrics', CommandFuncs.stop_set_metrics)],
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
