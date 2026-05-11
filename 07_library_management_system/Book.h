#ifndef BOOK_H
#define BOOK_H

#include <string>
#include "json.hpp"

// Alias pro JSON knihovnu (Alias for JSON library)
using json = nlohmann::json;

/**
 * @class Book
 * @brief Reprezentuje knihu v systému (Represents a book in the system)
 */
class Book {
private:
    int id;                   // Unikátní ID knihy (Unique ID of the book)
    std::string title;        // Název knihy (Title of the book)
    std::string author;       // Autor knihy (Author of the book)
    std::string genre;        // Žánr (Genre)
    bool is_available;        // Dostupnost (Availability)
    std::string borrower;     // Jméno vypůjčitele (Name of the borrower)

public:
    // Konstruktory (Constructors)
    Book();
    Book(int id, std::string title, std::string author, std::string genre);

    // Gettery (Accessors)
    int getId() const;
    std::string getTitle() const;
    std::string getAuthor() const;
    std::string getGenre() const;
    bool isAvailable() const;
    std::string getBorrower() const;

    // Akce (Actions)
    void borrowBook(const std::string& userName);
    void returnBook();
    void display() const;

    // JSON Serializace (JSON Serialization)
    json toJson() const;
    static Book fromJson(const json& j);
};

#endif
