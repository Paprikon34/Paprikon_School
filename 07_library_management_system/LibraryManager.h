#ifndef LIBRARY_MANAGER_H
#define LIBRARY_MANAGER_H

#include <string>
#include <vector>
#include "Book.h"
#include "User.h"

class LibraryManager {
private:
    std::vector<Book> books;
    std::vector<User> users;
    std::string dataFilePath;

public:
    LibraryManager(const std::string& path);

    // Persistence
    void loadData();
    void saveData() const;

    // Book operations
    void addBook(const Book& book);
    void displayBooks() const;
    void searchBooksByGenre(const std::string& genre) const;
    void searchAvailableBooks() const;

    // User operations
    void addUser(const User& user);
    void displayUsers() const;

    // Interactions
    void borrowBook(int bookId, int userId);
    void returnBook(int bookId, int userId);

    // Helper
    Book* findBook(int id);
    User* findUser(int id);
};

#endif
