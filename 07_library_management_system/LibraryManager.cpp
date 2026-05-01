#include "LibraryManager.h"
#include <iostream>
#include <fstream>

LibraryManager::LibraryManager(const std::string& path) : dataFilePath(path) {
    loadData();
}

void LibraryManager::loadData() {
    std::ifstream file(dataFilePath);
    if (!file.is_open()) {
        std::cerr << "Warning: Could not open " << dataFilePath << ". Starting with empty database." << std::endl;
        return;
    }

    json j;
    try {
        file >> j;
        
        if (j.contains("books")) {
            for (const auto& item : j["books"]) {
                books.push_back(Book::fromJson(item));
            }
        }
        
        if (j.contains("users")) {
            for (const auto& item : j["users"]) {
                users.push_back(User::fromJson(item));
            }
        }
        std::cout << "Data loaded successfully." << std::endl;
    } catch (const json::parse_error& e) {
        std::cerr << "Error parsing JSON data: " << e.what() << ". Starting with empty database." << std::endl;
    }
}

void LibraryManager::saveData() const {
    json j;
    j["books"] = json::array();
    for (const auto& book : books) {
        j["books"].push_back(book.toJson());
    }

    j["users"] = json::array();
    for (const auto& user : users) {
        j["users"].push_back(user.toJson());
    }

    std::ofstream file(dataFilePath);
    if (file.is_open()) {
        file << j.dump(4);
        std::cout << "Data saved successfully." << std::endl;
    } else {
        std::cerr << "Error: Could not save data to " << dataFilePath << std::endl;
    }
}

void LibraryManager::addBook(const Book& book) {
    books.push_back(book);
    std::cout << "Book added successfully.\n";
}

void LibraryManager::displayBooks() const {
    if (books.empty()) {
        std::cout << "No books in the library.\n";
        return;
    }
    for (const auto& book : books) {
        book.display();
    }
}

void LibraryManager::searchBooksByGenre(const std::string& genre) const {
    bool found = false;
    for (const auto& book : books) {
        if (book.getGenre() == genre) {
            book.display();
            found = true;
        }
    }
    if (!found) {
        std::cout << "No books found in genre: " << genre << "\n";
    }
}

void LibraryManager::searchAvailableBooks() const {
    bool found = false;
    for (const auto& book : books) {
        if (book.isAvailable()) {
            book.display();
            found = true;
        }
    }
    if (!found) {
        std::cout << "No available books right now.\n";
    }
}

void LibraryManager::addUser(const User& user) {
    users.push_back(user);
    std::cout << "User added successfully.\n";
}

void LibraryManager::displayUsers() const {
    if (users.empty()) {
        std::cout << "No users registered.\n";
        return;
    }
    for (const auto& user : users) {
        user.display();
    }
}

Book* LibraryManager::findBook(int id) {
    for (auto& book : books) {
        if (book.getId() == id) {
            return &book;
        }
    }
    return nullptr;
}

User* LibraryManager::findUser(int id) {
    for (auto& user : users) {
        if (user.getId() == id) {
            return &user;
        }
    }
    return nullptr;
}

void LibraryManager::borrowBook(int bookId, int userId) {
    Book* book = findBook(bookId);
    User* user = findUser(userId);

    if (!book) {
        std::cout << "Book with ID " << bookId << " not found.\n";
        return;
    }
    if (!user) {
        std::cout << "User with ID " << userId << " not found.\n";
        return;
    }

    if (!book->isAvailable()) {
        std::cout << "Book is currently not available.\n";
        return;
    }

    book->borrowBook(user->getName());
    user->borrowBook();
    std::cout << "Book '" << book->getTitle() << "' borrowed by " << user->getName() << ".\n";
}

void LibraryManager::returnBook(int bookId, int userId) {
    Book* book = findBook(bookId);
    User* user = findUser(userId);

    if (!book) {
        std::cout << "Book with ID " << bookId << " not found.\n";
        return;
    }
    if (!user) {
        std::cout << "User with ID " << userId << " not found.\n";
        return;
    }

    if (book->isAvailable()) {
        std::cout << "Book is already available.\n";
        return;
    }

    if (book->getBorrower() != user->getName()) {
        std::cout << "Book was not borrowed by this user.\n";
        return;
    }

    book->returnBook();
    user->returnBook();
    std::cout << "Book '" << book->getTitle() << "' returned by " << user->getName() << ".\n";
}
