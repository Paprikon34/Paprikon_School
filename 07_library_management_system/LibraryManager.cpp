#include "LibraryManager.h"
#include <iostream>
#include <fstream>

LibraryManager::LibraryManager(const std::string& path) : dataFilePath(path) {
    loadData();
}

/**
 * Načtení dat z JSON souboru (Loading data from JSON file)
 */
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
        std::cout << "Data loaded successfully (" << books.size() << " books, " << users.size() << " users)." << std::endl;
    } catch (const json::parse_error& e) {
        std::cerr << "Error parsing JSON data: " << e.what() << ". Starting with empty database." << std::endl;
    }
}

/**
 * Uložení dat do JSON souboru (Saving data to JSON file)
 */
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
        std::cout << "Data saved successfully to " << dataFilePath << std::endl;
    } else {
        std::cerr << "Error: Could not save data to " << dataFilePath << std::endl;
    }
}

/**
 * Přidání nové knihy (Adding a new book)
 */
void LibraryManager::addBook(const Book& book) {
    books.push_back(book);
    std::cout << "Book '" << book.getTitle() << "' added successfully.\n";
}

/**
 * Zobrazení všech knih (Display all books)
 */
void LibraryManager::displayBooks() const {
    if (books.empty()) {
        std::cout << "No books in the library.\n";
        return;
    }
    std::cout << "\n--- Library Inventory ---\n";
    for (const auto& book : books) {
        book.display();
    }
}

/**
 * Hledání knih podle žánru (Search books by genre)
 */
void LibraryManager::searchBooksByGenre(const std::string& genre) const {
    bool found = false;
    std::cout << "\n--- Search Results (Genre: " << genre << ") ---\n";
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

/**
 * Zobrazení dostupných knih (Display available books)
 */
void LibraryManager::searchAvailableBooks() const {
    bool found = false;
    std::cout << "\n--- Available Books ---\n";
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

/**
 * Přidání nového uživatele (Adding a new user)
 */
void LibraryManager::addUser(const User& user) {
    users.push_back(user);
    std::cout << "User '" << user.getName() << "' added successfully.\n";
}

/**
 * Zobrazení všech uživatelů (Display all users)
 */
void LibraryManager::displayUsers() const {
    if (users.empty()) {
        std::cout << "No users registered.\n";
        return;
    }
    std::cout << "\n--- Registered Users ---\n";
    for (const auto& user : users) {
        user.display();
    }
}

/**
 * Najít knihu podle ID (Find book by ID)
 */
Book* LibraryManager::findBook(int id) {
    for (auto& book : books) {
        if (book.getId() == id) {
            return &book;
        }
    }
    return nullptr;
}

/**
 * Najít uživatele podle ID (Find user by ID)
 */
User* LibraryManager::findUser(int id) {
    for (auto& user : users) {
        if (user.getId() == id) {
            return &user;
        }
    }
    return nullptr;
}

/**
 * Logika půjčení knihy (Borrowing logic)
 */
void LibraryManager::borrowBook(int bookId, int userId) {
    Book* book = findBook(bookId);
    User* user = findUser(userId);

    if (!book) {
        std::cout << "Error: Book with ID " << bookId << " not found.\n";
        return;
    }
    if (!user) {
        std::cout << "Error: User with ID " << userId << " not found.\n";
        return;
    }

    if (!book->isAvailable()) {
        std::cout << "Error: Book '" << book->getTitle() << "' is currently not available.\n";
        return;
    }

    book->borrowBook(user->getName());
    user->borrowBook();
    std::cout << "Success: Book '" << book->getTitle() << "' borrowed by " << user->getName() << ".\n";
}

/**
 * Logika vrácení knihy (Returning logic)
 */
void LibraryManager::returnBook(int bookId, int userId) {
    Book* book = findBook(bookId);
    User* user = findUser(userId);

    if (!book) {
        std::cout << "Error: Book with ID " << bookId << " not found.\n";
        return;
    }
    if (!user) {
        std::cout << "Error: User with ID " << userId << " not found.\n";
        return;
    }

    if (book->isAvailable()) {
        std::cout << "Info: Book '" << book->getTitle() << "' is already available.\n";
        return;
    }

    if (book->getBorrower() != user->getName()) {
        std::cout << "Error: Book was not borrowed by " << user->getName() << ".\n";
        return;
    }

    book->returnBook();
    user->returnBook();
    std::cout << "Success: Book '" << book->getTitle() << "' returned by " << user->getName() << ".\n";
}
