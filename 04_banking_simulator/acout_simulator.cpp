// Bank account simulator 
// Including all essential stuff
#include <iostream>
#include <string>
#include <stdlib.h>
#include <time.h>

//setup using to not use std:: every time (not using namespace)
using std::cout;
using std::cin;
using std::string;
using std::endl;

// account main function
int main() {
    std::srand(time(nullptr)); // seed once

    //variables
    string user_name;
    double balance = 0.0;
    double deposit_amount = 0.0;
    double withdraw_amount = 0.0;

    //getting user name
    cout << "Welcome to Account Simulator!" << endl;
    cout << "Please enter your name: ";
    std::getline(cin >> std::ws, user_name); // std::ws to ignore leading whitespace

    cout << "Hello, " << user_name << "! Your starting balance is $" << balance << endl;

    //initial deposit
    cout << "Enter amount to deposit initially: $";
    cin >> deposit_amount;
    if (deposit_amount > 0) {
        balance += deposit_amount;
        cout << "You have deposited $" << deposit_amount
             << ". New balance is $" << balance << endl;
    } else {
        cout << "Invalid deposit amount, starting balance remains $" << balance << endl;
    }

    //setup main menu
    bool running = true;
    while (running) {
        cout << "\nMain Menu:" << endl;
        cout << "Your current balance is $" << balance << endl;
        cout << "1. Deposit Money" << endl;
        cout << "2. Invest Money" << endl;
        cout << "3. Withdraw Money" << endl;
        cout << "4. Exit" << endl;
        cout << "Choose an option (1-4): ";

        int choice;
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter amount to deposit: $";
                cin >> deposit_amount;
                if (deposit_amount > 0) {
                    balance += deposit_amount;
                    cout << "You have deposited $" << deposit_amount
                         << ". New balance is $" << balance << endl;
                } else {
                    cout << "Invalid deposit amount." << endl;
                }
                break;
            case 2: {
                cout << "Enter amount to invest: $";
                cin >> deposit_amount;

                if (deposit_amount <= 0) {
                    cout << "Invalid investment amount." << endl;
                    break;
                }
                if (deposit_amount > balance) {
                    cout << "You cannot invest more than your balance!" << endl;
                    break;
                }

                balance -= deposit_amount; // move money into investment

                // For simplicity, we assume investment is instant and increases the invested money by 1% - 5%, 
                // but there's a chance of loss (chance to lose all the invested money is 10%)
                double gain_percentage = (std::rand() % 5 + 1) / 100.0; // Random gain between 1% and 5%
                int loss_chance = std::rand() % 10; // 10% chance to lose all (0..9)

                if (loss_chance == 0) {
                    cout << "Unfortunately, your investment of $"
                         << deposit_amount << " was lost!" << endl;
                } else {
                    double gain = deposit_amount * gain_percentage;
                    double final_amount = deposit_amount + gain;
                    balance += final_amount;
                    cout << "Your investment of $" << deposit_amount
                         << " has gained $" << gain
                         << "! You now get back $" << final_amount << endl;
                }
                break;
            }
            case 3:
                cout << "Enter amount to withdraw: $";
                cin >> withdraw_amount;
                if (withdraw_amount <= 0) {
                    cout << "Invalid withdrawal amount." << endl;
                } else if (withdraw_amount > balance) {
                    cout << "Insufficient funds! Your balance is $"
                         << balance << endl;
                } else {
                    balance -= withdraw_amount;
                    cout << "You have withdrawn $"
                         << withdraw_amount
                         << ". New balance is $" << balance << endl;
                }
                break;
            case 4:
                cout << "Thank you for using Account Simulator, "
                     << user_name << "! Goodbye!" << endl;
                running = false;
                break;
            default:
                cout << "Invalid option. Please choose between 1 and 4."
                     << endl;
        }
    }
    return 0;
}
