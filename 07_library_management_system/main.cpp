#include <iostream>
#include <string>
#include "LibraryManager.h"

void displayMenu() {
    std::cout << "\n=== Library Management System ===\n";
    std::cout << "1. Display all books\n";
    std::cout << "2. Display available books\n";
    std::cout << "3. Search books by genre\n";
    std::cout << "4. Display all users\n";
    std::cout << "5. Add new book\n";
    std::cout << "6. Add new user\n";
    std::cout << "7. Borrow a book\n";
    std::cout << "8. Return a book\n";
    std::cout << "9. Save and Exit\n";
    std::cout << "Choice: ";
}

int main() {
    LibraryManager manager("data/library.json");
    bool running = true;

    while (running) {
        displayMenu();
        int choice;
        std::cin >> choice;

        if (std::cin.fail()) {
            std::cin.clear();
            std::cin.ignore(10000, '\n');
            std::cout << "Invalid input. Please enter a number.\n";
            continue;
        }

        switch (choice) {
            case 1:
                manager.displayBooks();
                break;
            case 2:
                manager.searchAvailableBooks();
                break;
            case 3: {
                std::string genre;
                std::cout << "Enter genre: ";
                std::cin >> std::ws;
                std::getline(std::cin, genre);
                manager.searchBooksByGenre(genre);
                break;
            }
            case 4:
                manager.displayUsers();
                break;
            case 5: {
                int id;
                std::string title, author, genre;
                std::cout << "Enter Book ID: ";
                std::cin >> id;
                std::cout << "Enter Title: ";
                std::cin >> std::ws;
                std::getline(std::cin, title);
                std::cout << "Enter Author: ";
                std::getline(std::cin, author);
                std::cout << "Enter Genre: ";
                std::getline(std::cin, genre);
                manager.addBook(Book(id, title, author, genre));
                break;
            }
            case 6: {
                int id;
                std::string name;
                std::cout << "Enter User ID: ";
                std::cin >> id;
                std::cout << "Enter Name: ";
                std::cin >> std::ws;
                std::getline(std::cin, name);
                manager.addUser(User(id, name));
                break;
            }
            case 7: {
                int bookId, userId;
                std::cout << "Enter Book ID to borrow: ";
                std::cin >> bookId;
                std::cout << "Enter User ID: ";
                std::cin >> userId;
                manager.borrowBook(bookId, userId);
                break;
            }
            case 8: {
                int bookId, userId;
                std::cout << "Enter Book ID to return: ";
                std::cin >> bookId;
                std::cout << "Enter User ID: ";
                std::cin >> userId;
                manager.returnBook(bookId, userId);
                break;
            }
            case 9:
                manager.saveData();
                running = false;
                std::cout << "Exiting...\n";
                break;
            default:
                std::cout << "Invalid choice. Try again.\n";
        }
    }

    return 0;
}
