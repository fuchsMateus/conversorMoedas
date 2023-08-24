import requests
import tkinter as tk
from tkinter import ttk

class ConversorDeMoedas:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Moedas")
        self.root.geometry("400x300")
        self.style = ttk.Style()

        self.style.configure("TLabel", background="white", font=("Helvetica", 11))
        self.root.configure(background="white")

        self.label_moeda1 = ttk.Label(root, text="Moeda de origem:")
        self.label_moeda1.pack(pady=10)

        self.combobox_moeda1 = ttk.Combobox(root, values=self.get_moedas())
        self.combobox_moeda1.pack()

        self.label_moeda2 = ttk.Label(root, text="Moeda de destino:")
        self.label_moeda2.pack(pady=10)

        self.combobox_moeda2 = ttk.Combobox(root, values=self.get_moedas())
        self.combobox_moeda2.pack()

        self.combobox_moeda1.set("USD")
        self.combobox_moeda2.set("BRL")

        self.label_quantidade = ttk.Label(root, text="Quantidade:")
        self.label_quantidade.pack(pady=10)

        self.entry_quantidade = ttk.Entry(root)
        self.entry_quantidade.pack()
        self.entry_quantidade.insert(0, "1")
        self.entry_quantidade.bind('<KeyRelease>', self.converter)

        self.label_resultado = ttk.Label(root, text="", font=("Helvetica", 14, "bold"))
        self.label_resultado.pack(pady=20)

        self.combobox_moeda1.bind("<<ComboboxSelected>>", self.converter)
        self.combobox_moeda2.bind("<<ComboboxSelected>>", self.converter)

        # Exibir o resultado da conversão inicial
        self.converter()


    def get_moedas(self):
        return ["USD", "BRL", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "INR", "MXN", "NZD", "RUB", "ZAR"]

    def converter(self, event=None):
        try:
            quantidade = float(self.entry_quantidade.get())

            if quantidade < 0.01:
                self.label_resultado.config(text="Quantidade deve ser maior que 0.01")
                return

            moeda1 = self.combobox_moeda1.get()
            moeda2 = self.combobox_moeda2.get()

            if moeda1 == moeda2:
                self.label_resultado.config(text="Escolha moedas diferentes")
                return

            requisicao = requests.get(f'https://economia.awesomeapi.com.br/all/{moeda1}-{moeda2}')

            cotacao = requisicao.json()

            valor_atual = float(cotacao[moeda1]['bid'])
            valor_convertido = valor_atual * quantidade
            nome_moedas = cotacao[moeda1]['name']


            # Determinar o número de casas decimais
            if valor_convertido < 0.0001:
                num_casas_decimais = 6
            elif valor_convertido < 0.001:
                num_casas_decimais = 5
            elif valor_convertido < 0.01:
                num_casas_decimais = 4
            elif valor_convertido < 0.1:
                num_casas_decimais = 3
            else:
                num_casas_decimais = 2


            resultado = f"{nome_moedas}\n{quantidade} {moeda1} = {valor_convertido:.{num_casas_decimais}f} {moeda2}"
            self.label_resultado.config(text=resultado)

        except requests.exceptions.RequestException:
            self.label_resultado.config(text="Erro de conexão. Verifique sua internet.")
        except ValueError:
            self.label_resultado.config(text="Valor inválido")
        except KeyError:
            self.label_resultado.config(text="Conversão não disponível")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorDeMoedas(root)
    root.mainloop()