#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <windows.h>
#include <limits>

class Product {
public:
    std::string name;
    double price;

    Product(const std::string& n, double p) : name(n), price(p) {}
};

class Order {
public:
    std::vector<Product> products;
    std::vector<int> quantities;
    double totalAmount;

    Order() : totalAmount(0) {}

    void addProduct(const Product& product, int quantity) {
        products.push_back(product);
        quantities.push_back(quantity);
        totalAmount += product.price * quantity;
    }
};

class CoffeeShop {
private:
    std::vector<Product> menu;
    HANDLE hConsole;

    const std::string currentDateTime() {
        time_t now = time(0);
        struct tm tstruct;
        char buf[80];
        tstruct = *localtime(&now);
        strftime(buf, sizeof(buf), "%Y-%m-%d.%X", &tstruct);
        return buf;
    }

    void clear() {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    void cls() {
        system("cls");
    }

    void displayTitle() const {
        SetConsoleTextAttribute(hConsole, 14);
        std::cout << R"(
                                                                                               
  _|_|_|    _|_|    _|_|_|_|  _|_|_|_|  _|_|_|_|  _|_|_|_|      _|    _|  _|    _|  _|_|_|    
_|        _|    _|  _|        _|        _|        _|            _|    _|  _|    _|  _|    _|  
_|        _|    _|  _|_|_|    _|_|_|    _|_|_|    _|_|_|        _|_|_|_|  _|    _|  _|_|_|    
_|        _|    _|  _|        _|        _|        _|            _|    _|  _|    _|  _|    _|  
  _|_|_|    _|_|    _|        _|        _|_|_|_|  _|_|_|_|      _|    _|    _|_|    _|_|_|    
        
    )";
    }

    void coffeeCup() const {
        std::cout << R"(
             ( (
              ) )
           ........
           |      |]
           \      /
            `----'
        )";
    }

public:
    CoffeeShop() {
        menu.push_back(Product("Espresso", 50.00));
        menu.push_back(Product("Americano", 60.00));
        menu.push_back(Product("Latte", 70.00));
        menu.push_back(Product("Cappuccino", 70.00));
        menu.push_back(Product("Mocha", 80.00));
        menu.push_back(Product("Macchiato", 80.00));
        menu.push_back(Product("Flat White", 70.00));
        menu.push_back(Product("Affogato", 90.00));
        menu.push_back(Product("Cold Brew", 65.00));
        menu.push_back(Product("Iced Coffee", 60.00));
        menu.push_back(Product("Water", 20.00));
        menu.push_back(Product("Tea", 40.00));
        menu.push_back(Product("Hot Chocolate", 60.00));
    }

    void run() {
        system("mode 100");
        hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        std::string username, password;
        int orderChoice, additional, menuOption;

        displayTitle();
        coffeeCup();

        for (int a = 1; a < 8; a++) {
            Sleep(300);
            SetConsoleTextAttribute(hConsole, 10);
            std::cout << "...";
        }
        Sleep(2000);
        cls();

        while (true) {
            SetConsoleTextAttribute(hConsole, 14);
            std::cout << "\n\t\t\t =================================================" << std::endl;
            std::cout << "\t\t\t %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
            std::cout << "\n\t\t\t\t       Welcome to Coffee Hub";
            std::cout << "\n\t\t\t %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%";
            std::cout << "\n\t\t\t =================================================" << std::endl;
            SetConsoleTextAttribute(hConsole, 15);
            std::cout << "\n\n\t\t\t\t      Please Login to Continue" << std::endl;
            std::cout << "\n\t\t\t\t      User Name: ";
            std::cin >> username;

            if (username == "aarmish") {
                SetConsoleTextAttribute(hConsole, 15);
                std::cout << "\n\t\t\t\t      Password: ";
                std::cin >> password;
                std::cout << std::endl;
                if (password == "123") {
                    cls();
                    break; // Correct login, exit loop
                } else {
                    cls();
                    SetConsoleTextAttribute(hConsole, 12);
                    std::cout << "\n\t\t\t\tInvalid password. Try again." << std::endl;
                    SetConsoleTextAttribute(hConsole, 15);
                }
            } else {
                cls();
                SetConsoleTextAttribute(hConsole, 12);
                std::cout << "\n\t\t\t\tInvalid username. Try again." << std::endl;
                SetConsoleTextAttribute(hConsole, 15);
            }
        }

        Order currentOrder;
        Sleep(500);
        cls();
        SetConsoleTextAttribute(hConsole, 10);
        std::cout << "\n\n\t\t\t\t=====>>>>PICK YOUR ORDER<<<<=====\n\n";
        SetConsoleTextAttribute(hConsole, 14);
        std::cout << "\t\t=====================================================================\n";
        SetConsoleTextAttribute(hConsole, 15);
        std::cout << "\t\t\t  PRODUCT NUMBER\tPRODUCT\t\t\tPRICE\n";
        SetConsoleTextAttribute(hConsole, 14);
        std::cout << "\t\t=====================================================================\n";
        SetConsoleTextAttribute(hConsole, 15);

        for (int i = 0; i < menu.size(); ++i) {
            std::cout << "\t\t\t         " << i + 1 << "\t    " << menu[i].name << "\t\t\tPhp " << menu[i].price << "\n";
        }
        SetConsoleTextAttribute(hConsole, 14);
        std::cout << "\t\t=====================================================================\n";
        std::cout << "\t\t=====================================================================\n";

        do {
            int quantity = 0;
            std::cout << "\n\t\t Enter the product number to order: ";
            std::cin >> orderChoice;
            if (std::cin.fail() || orderChoice < 1 || orderChoice > menu.size()) {
                std::cout << "\t\t Invalid product number. Try again.\n";
                clear();
                continue;
            }
            
            std::cout << "\t\t Enter quantity: ";
            std::cin >> quantity;
            if (std::cin.fail() || quantity <= 0) {
                std::cout << "\t\t Invalid quantity. Try again.\n";
                clear();
                continue;
            }
            currentOrder.addProduct(menu[orderChoice - 1], quantity);

            std::cout << "\t\t Would you like to order anything else? [1] Yes [0] No: ";
            std::cin >> additional;
            if (std::cin.fail()) {
                clear();
                additional = 0; // Default to no if invalid input
            }
        } while (additional == 1);

        std::cout << "\n\t\tYou have ordered:\n";
        for (size_t i = 0; i < currentOrder.products.size(); ++i) {
            std::cout << "\t\t" << currentOrder.products[i].name << " x " << currentOrder.quantities[i] << "\n";
        }
        std::cout << "\n\t\tYour total amount is: Php " << currentOrder.totalAmount << "\n";
        std::cout << "\n\t\tEnter [ 0 ] to logout: ";
        std::cin >> menuOption;
        cls();
    }
};


