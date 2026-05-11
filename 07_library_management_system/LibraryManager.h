#ifndef LIBRARY_MANAGER_H
#define LIBRARY_MANAGER_H

#include <string>
#include <vector>
#include "Book.h"
#include "User.h"

/**
 * @class LibraryManager
 * @brief Hlavní správce knihovny (Main library manager)
 * Zajišťuje logiku půjčování, vyhledávání a persistence.
 */
class LibraryManager {
private:
    std::vector<Book> books;         // Seznam knih (List of books)
    std::vector<User> users;         // Seznam uživatelů (List of users)
    std::string dataFilePath;        // Cesta k JSON souboru (Path to JSON file)

public:
    LibraryManager(const std::string& path);

    // Persistence (Ukládání a načítání)
    void loadData();
    void saveData() const;

    // Operace s knihami (Book operations)
    void addBook(const Book& book);
    void displayBooks() const;
    void searchBooksByGenre(const std::string& genre) const;
    void searchAvailableBooks() const;

    // Operace s uživateli (User operations)
    void addUser(const User& user);
    void displayUsers() const;

    // Interakce (Interactions)
    void borrowBook(int bookId, int userId);
    void returnBook(int bookId, int userId);

    // Pomocné metody (Helper methods)
    Book* findBook(int id);
    User* findUser(int id);
};

#endif
