from tkinter import Label, Button, Frame, Canvas, Scrollbar, Tk, messagebox, StringVar, OptionMenu
import requests
import re


def ping_coin_gecko():
    response = requests.get("https://api.coingecko.com/api/v3/ping")
    if response.status_code == 200:
        ping_box.configure(text="Coin Gecko works")
    else:
        ping_box.configure(text="Error, something's wrong")


def printID():
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    file = open("crypto_all.txt", "w")
    for coin in response.json():
        file.write(coin["id"] + "\n")
    file.close()


def read_selected_crypto():
    result = []
    file = open("crypto_selected.txt", "r")
    for coin in file.readlines():
        if coin[-1] == '\n':
            coin = coin[:-1]
        result.append(coin)
    file.close()
    return result


def clear_canvas():
    canvas_list = scrollable_frame.grid_slaves()
    for l in canvas_list:
        l.destroy()


def get_coin_response(name):
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/"+name)
    return response.json()


def add_row(row, name, abr, price, hour_change, day_change, week_change, market_cap, more_info):
    nameCol = Label(scrollable_frame, text=name, bg="#89cff0")
    nameCol.grid(row=row, column=0, sticky="EW")

    abr_col = Label(scrollable_frame, text=abr, bg="#89cff0")
    abr_col.grid(row=row, column=1, sticky="EW")

    price_col = Label(scrollable_frame, text=price, bg="#89cff0")
    price_col.grid(row=row, column=2, sticky="EW")

    hour_change_col = Label(scrollable_frame, text=hour_change, bg="#89cff0")
    hour_change_col.grid(row=row, column=3, sticky="EW")

    day_change_col = Label(scrollable_frame, text=day_change, bg="#89cff0")
    day_change_col.grid(row=row, column=4, sticky="EW")

    week_change_col = Label(scrollable_frame, text=week_change, bg="#89cff0")
    week_change_col.grid(row=row, column=5, sticky="EW")

    market_cap_col = Label(scrollable_frame, text=market_cap, bg="#89cff0")
    market_cap_col.grid(row=row, column=6, sticky="EW")

    if more_info:
        info_button = Button(scrollable_frame, text="more info",
                             command=lambda: show_coin_info(name))
        info_button.grid(row=row, column=7, sticky="EW")


def show_prices():
    list_of_coins = read_selected_crypto()
    clear_canvas()
    add_row(0, "CryptoCurrency", "Abbreviation", "Price", "1h change",
               "24h change", "7d change", "market cap", False)
    for num, coin in enumerate(list_of_coins, 1):
        response = get_coin_response(coin)
        add_row(num, coin, response["symbol"],
                response["market_data"]["current_price"]["usd"],
                response["market_data"]["price_change_percentage_1h_in_currency"]["usd"],
                response["market_data"]["price_change_percentage_24h_in_currency"]["usd"],
                response["market_data"]["price_change_percentage_7d_in_currency"]["usd"],
                response["market_data"]["market_cap"]["usd"],
                True)
    for x in range(7):
        scrollable_frame.columnconfigure(x, weight=1)


def how_to():
    text = "To add a crypto currency you need to add it's ID into crypto_selected.txt. The print ID's button adds all of the available crypto currencies into crypto_all.txt. Find the ID of the crypto you want to add in crypto_all.txt then add a new line with the ID into crypto_selected.txt"
    messagebox.showinfo("Instructions", text)


def show_coin_info(coin):
    response = get_coin_response(coin)
    text = response["description"]["en"]
    text = clean_tags(text)
    messagebox.showinfo("Description", text)


def clean_tags(input):
    pattern = re.compile('<.*?>')
    out = re.sub(pattern, '', input)
    return out


starting_height = 600
starting_width = 450

root = Tk()

root.minsize(starting_height, starting_width)
root.wm_title("Crypto currency checker")
root.configure(bg="#00FFFF")

coin_gecko_label = Label(
    root, text="Data is from the Coin Gecko API.", bg="#00FFFF")
coin_gecko_label.place(relx=0.70, rely=0.95, relheight=0.05, relwidth=0.30)


app = Frame(root)
app.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)


exit_button = Button(app, text="exit", command=root.destroy)
exit_button.place(relx=0.05, rely=0.05, relheight=0.1, relwidth=0.12)

minimize_button = Button(app, text="mini.", command=root.iconify)
minimize_button.place(relx=0.2, rely=0.05, relheight=0.1, relwidth=0.08)

ping_button = Button(app, text="ping", command=ping_coin_gecko)
ping_button.place(relx=0.55, rely=0.05, relheight=0.1, relwidth=0.1)

ping_box = Label(app, anchor="w", justify="left", text="-output-")
ping_box.place(relx=0.7, rely=0.05, relheight=0.1, relwidth=0.5)

how_to_button = Button(app, text="how to add crypto", command=how_to)
how_to_button.place(relx=0.05, rely=0.20, relheight=0.1, relwidth=0.25)

print_button = Button(app, text="print IDs", command=printID)
print_button.place(relx=0.85, rely=0.35, relheight=0.1, relwidth=0.1)

show_price_button = Button(app, text="show prices", command=show_prices)
show_price_button.place(relx=0.05, rely=0.35, relheight=0.1, relwidth=0.15)

lower_frame = Frame(app, bg="#89cff0")
lower_frame.place(relx=0, rely=0.5, relheight=0.5, relwidth=1)

lower_canvas = Canvas(lower_frame, bg="#89cff0")
lower_canvas.pack(side="left", fill="both", expand=True)

lower_scrl = Scrollbar(lower_frame, orient="vertical",
                       command=lower_canvas.yview)
lower_scrl.pack(side="right", fill="y")

scrollable_frame = Frame(lower_canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: lower_canvas.configure(
        scrollregion=lower_canvas.bbox("all")
    )
)

lower_canvas.create_window(
    (0, 0), window=scrollable_frame, anchor="nw", tags="frame")
lower_canvas.bind("<Configure>", lambda e: lower_canvas.itemconfig(
    "frame", width=lower_canvas.winfo_width()))
lower_canvas.configure(yscrollcommand=lower_scrl.set)


root.mainloop()
