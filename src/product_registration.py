class ProductRegistration:
    def __init__(self):
        self.products = []
        self.load_products()

    
    def lines(self):
        # method of lines
        print("-=" * 20)

    def menu(self):
        # method with the menu options 
        self.lines()
        print("Choose one of the options below: ")
        print("1. Register product")
        print("2. List products")
        print("3. Remove product")
        print("4. Exit")
        self.lines()

    def register_product(self):
        # method to register product
        name = input("Enter product name: ")
        try:
            price = float(input("Enter product price: R$"))
            if price < 0:
                print("\033[33mPrice cannot be negative.\033[0m")
                return
        except ValueError:
            print("\033[31mERROR. Incorrect value\033[0m")
            return

        last_id = self.products[-1]["id"] if self.products else 0
        new_id = last_id + 1

        self.products.append({"id": new_id, "name": name, "price": price})
        print(f"\033[32mProduct '{name}' registered successfully.\033[0m")

    def list_products(self):
        # method to list registered products
        if not self.products:
            print("\033[33mNo products registered.\033[0m")
        else:
            print("\nRegistered products: ")
            for product in self.products:
                print(f"{product["id"]} - {product["name"]} - R${product["price"]:.2f}")
    
    def remove_product(self):
        # method to remove product
        if not self.products:
            print("\033[33mNo product to remove.\033[0m")
            return
        
        try:
            id_to_remove = int(input("Product ID that you want to remove: "))
        except ValueError:
            print("\033[31mERROR. Invalid ID format.\033[0m")
            return
        
        original_len = len(self.products)
        self.products = [p for p in self.products if p["id"] != id_to_remove]

        if len(self.products) < original_len:
            self.save_products_txt()
            print("\033[32mProduct removed successfully!\033[0m")
        else:
            print("\033[33mProduct not found.\033[0m")

    def save_products_txt(self):
        # method to save products registered in a .txt file
        with open("products.txt", "w", encoding="utf-8") as file:
            for register in self.products:
                file.write(f"{register["id"]} - {register["name"]} - {register["price"]}\n")

    def load_products(self):
        # method to load products saved in the .txt file
        try:
            with open("products.txt", "r", encoding="utf-8") as file:
                self.products = []
                for line in file:
                    parts = line.strip().split(" - ")
                    if len(parts) == 3:
                        product = {
                            "id": int(parts[0]),
                            "name": parts[1],
                            "price": float(parts[2]),
                        }
                        self.products.append(product)
        except FileExistsError:
            self.products = []

    def chosen_option(self):
        # method to choose the desired option 
        while True:
            self.menu()

            try:
                option = int(input("Enter your option: "))
            except ValueError:
                print("\033[31mERROR. Invalid option.\033[0m")
                continue

            if option == 1:
                self.register_product() 
            elif option == 2:
                self.list_products()
            elif option == 3:
                self.remove_product()
            elif option == 4:
                self.save_products_txt()
                break
            else:
                print("\033[31mERROR\033[0m: Invalid option.")
