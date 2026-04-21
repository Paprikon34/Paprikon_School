#ifndef BOOK_H
#define BOOK_H

#include <string>
#include "json.hpp"

using json = nlohmann::json;

class Book {
private:
    int id;
    std::string title;
    std::string author;
    std::string genre;
    bool is_available;
    std::string borrower;

public:
    // Constructors
    Book();
    Book(int id, std::string title, std::string author, std::string genre);

    // Getters
    int getId() const;
    std::string getTitle() const;
    std::string getAuthor() const;
    std::string getGenre() const;
    bool isAvailable() const;
    std::string getBorrower() const;

    // Actions
    void borrowBook(const std::string& userName);
    void returnBook();
    void display() const;

    // JSON Serialization
    json toJson() const;
    static Book fromJson(const json& j);
};

#endif
