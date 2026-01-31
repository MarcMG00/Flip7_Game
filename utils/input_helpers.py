def choose_from_list(prompt: str, options: list):
    if len(options) < 1:
        print("No hay nadie a quien dar la carta especial")
    elif len(options) == 1:
        print("Solo hay un jugador posible")
        return options[0]
    else:
        print(prompt)
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        while True:
            try:
                choice = int(input("> "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
            except ValueError:
                pass
            print("Entrada inválida.")