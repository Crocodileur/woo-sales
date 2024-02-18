from woocommerce import API
import json
from google_currency import convert  
import shutil
import os
from colorama import init, Fore, Style

###############################################################################################################
#                                               CONSTANTS                                                     #
###############################################################################################################

init()
ord = 0
wb = 0
sal = 0

###############################################################################################################
#                                               FUNCTIONS                                                     #
###############################################################################################################
def fetch_datas(): # ask to user datas of the website : consumer_key, consumer_secret and store url.
    while True:
        name = input('Please enter your Store name : ')
        url = input('Please enter your Store URL : ')
        consumer_key = input('Please enter your consumer key : ')
        consumer_secret = input('Please enter your consumer secret key : ')
        
        data_dic = { # dictionary containing store name, url, consumer key and consumer secret
            name: [url, consumer_key, consumer_secret]
        }
        
        write_json(data_dic)
        
        again = input('Do you want to add another website ? : ')
        if again in ['y','Y','yes','Yes','YES']:
            pass
        else:
            break
    

def total_sales(sales_datas):
    total_sales = 0
    for items in sales_datas:
        total_sales += float(items.get('total'))
    return total_sales


def get_centered_input(prompt, color1='blue', color2='blue', style=Style.NORMAL):
    console_width = shutil.get_terminal_size().columns
    lines = prompt.split('\n')
    centered_lines = [' ' * ((console_width - len(line)) // 2) + line for line in lines]

    centered_prompt = '\n'.join(centered_lines)

    if "|" in centered_prompt:
        before_bar, after_bar = centered_prompt.split("|", 1)
        colored_prompt = style + getattr(Fore, color1.strip().upper()) + before_bar + Fore.RESET + getattr(Fore, color2.strip().upper()) + after_bar + Style.RESET_ALL
    else:
        colored_prompt = style + getattr(Fore, color1.strip().upper()) + centered_prompt + Style.RESET_ALL

    user_input = input(colored_prompt).replace("|", "")
    return user_input


def main_menu():
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            startup = int(get_centered_input('1) Add a Website\n2) List Websites\n3) See Total Sales\n4) View websites datas\n5) Exit\n\n| > ', 'blue','MAGENTA',Style.BRIGHT))
            if startup not in [1,2,3,4,5]:
                raise Exception
            else:
                break
        except:
            pass
    return startup


def write_json(filename='datas.json'):
    website_name = get_centered_input('Please enter your website name : ')
    url = get_centered_input('Please enter your website URL : ')
    consumer_key = get_centered_input('Please enter your consumer key : ')
    consumer_secret = get_centered_input('Please enter your consumer secret : ')
    datas = (url,consumer_key,consumer_secret)
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[website_name] = datas
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 3)


def get_json_datas(filename='datas.json'):
    data_list = {}  # Dict that will contain all sales data
    
    with open(filename,'r+') as file:
        # Load json data into a dict.
        file_data = json.load(file)
        for items in file_data: # for all websites in the json file, we fetch datas and store it into the data_list dict.
            wcapi = API(
                        url=file_data[items][0],
                        consumer_key=file_data[items][1],
                        consumer_secret=file_data[items][2],
                        version="wc/v3"
                        )
            api_datas = wcapi.get("orders")
            data_list[items] = json.loads(api_datas.text)
            
    return data_list


def capitalize_each_word(sentence):
    return ' '.join(word.capitalize() for word in sentence.split())


def print_centered(text, color1='blue', color2='blue', style=Style.NORMAL):
    console_width = shutil.get_terminal_size().columns
    padding = (console_width - len(text)) // 2

    if "|" in text:
        before_bar, after_bar = text.split("|", 1)
        centered_text = ' ' * padding + style + getattr(Fore, color1.strip().upper()) + before_bar + Fore.RESET + getattr(Fore, color2.strip().upper()) + after_bar + Style.RESET_ALL
    else:
        centered_text = ' ' * padding + style + getattr(Fore, color1.strip().upper()) + text + Style.RESET_ALL

    print(centered_text)

###############################################################################################################
#                                                 MAIN                                                        #
###############################################################################################################

if __name__ == "__main__" :
    gmain =0
    all_websites_datas = get_json_datas() # Function that fetch all datas websites from json file and get datas from API.
    os.system("title " + "WooDatas - v0.1")
    for items in all_websites_datas:
            try:
                store_currency = all_websites_datas[items][0].get('currency') # Get store currency
                total_money = total_sales(all_websites_datas[items])
                total_money = eval(json.loads(convert(store_currency, 'EUR', total_money))['amount'])
                
                gmain += round(total_money,2)
                os.system("title " + "WooDatas - Sales : " + str(gmain)+"€")
            except:
                pass
    while True:
        # Get datas from json file and store datas in a dictionnary
        main_menu_choice = main_menu()
        if main_menu_choice == 1:
            write_json()
        elif main_menu_choice == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(len(all_websites_datas.keys())):
                print_centered(str(i+1)+'.'+' '+str(list(all_websites_datas)[i]) + '\n')
            get_centered_input('> ', "MAGENTA")

        elif main_menu_choice == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            global_main = 0
            for items in all_websites_datas:
                try:
                    store_currency = all_websites_datas[items][0].get('currency') # Get store currency
                    total_money = total_sales(all_websites_datas[items])
                    total_money = eval(json.loads(convert(store_currency, 'EUR', total_money))['amount'])
                    if round(total_money,2) != 0:
                        print_centered(str(capitalize_each_word(items)) + ' :| ' +  str(round(total_money,2))+'€','blue','green')
                    else:
                        print_centered(str(capitalize_each_word(items)) + ' :| ' +  str(round(total_money,2))+'€','Fore.WHITE',Style.DIM)
                    global_main += round(total_money,2)
                except:
                    print_centered(str(capitalize_each_word(items)) + ' :| 0€','blue','red')
            print('\n')
            print_centered(str('Global Sales :| ' + str(round(global_main,2)) + '€') ,'blue','yellow')
            print('\n')
            get_centered_input('> ','MAGENTA')
        
        
        elif main_menu_choice == 4:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_centered('Which Website do you want to see the data from?','blue',Style.BRIGHT)
                for i in range(len(all_websites_datas.keys())):
                        print_centered('('+str(i+1)+')'+' '+str(list(all_websites_datas)[i]))
                print_centered('(X) Exit')
                data_show = get_centered_input('> ', "MAGENTA")
                if data_show in ['x','X']:
                    break
                try:
                    data_show = int(data_show)
                except:
                    continue
                if data_show <= len(all_websites_datas): # If number entered by user is valid, print all data of the wanted website
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_centered(str(capitalize_each_word(list(all_websites_datas.keys())[data_show-1])) + ' |Datas\n' ,'cyan','blue') # Which website data are from
                    try:
                        print_centered(str('Order amount :| '+ str(len(all_websites_datas[list(all_websites_datas)[data_show-1]]))),'blue','cyan') # Order amount
                        ord = 1
                        
                        print_centered('Website Currency :| '+ str(all_websites_datas[list(all_websites_datas)[data_show-1]][0].get('currency')) ,'blue','cyan') # Website currency
                        wb = 1
                    
                        total_money = total_sales(all_websites_datas[list(all_websites_datas)[data_show-1]])
                        total_money = eval(json.loads(convert(all_websites_datas[list(all_websites_datas)[data_show-1]][0].get('currency'), 'EUR', total_money))['amount'])
                        print_centered('Total Sales :| '+ str(round(total_money,2))+'€', 'blue','cyan') # Total money made
                        ord = 0
                        sal = 0
                        wb = 0
                    except:
                        if ord == 0:
                            print_centered(str('Order amount :| 0'),'blue','cyan') # Order amount
                        if wb == 0:
                            print_centered('Website Currency :| Unknown' ,'blue','cyan') # Website currency  
                        print_centered('Total Sales :| 0€', 'blue','cyan') # Total money made
                    total_items_sold = 0
                    try:
                        for i in range (len(all_websites_datas[list(all_websites_datas)[data_show-1]])):
                            total_items_sold += len(all_websites_datas[list(all_websites_datas)[data_show-1]][i].get('line_items'))
                        print_centered('Total items Sold :| ' + str(total_items_sold), 'blue','cyan')
                    except:
                        print_centered('Total items Sold :| 0', 'blue','cyan')

                    #print((all_websites_datas[list(all_websites_datas)[data_show-1]]))
                    print('\n')
                    get_centered_input('> ', "MAGENTA")


        elif main_menu_choice == 5:
            os.system('cls' if os.name == 'nt' else 'clear')
            break