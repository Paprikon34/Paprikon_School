#include "Book.h"
#include <iostream>

// Výchozí konstruktor (Default constructor)
Book::Book() : id(0), title(""), author(""), genre(""), is_available(false), borrower("None") {}

// Parametrický konstruktor (Parameterized constructor)
Book::Book(int id, std::string title, std::string author, std::string genre)
    : id(id), title(title), author(author), genre(genre), is_available(true), borrower("None") {}

// Gettery (Accessors)
int Book::getId() const { return id; }
std::string Book::getTitle() const { return title; }
std::string Book::getAuthor() const { return author; }
std::string Book::getGenre() const { return genre; }
bool Book::isAvailable() const { return is_available; }
std::string Book::getBorrower() const { return borrower; }

// Akce (Actions)

/**
 * Vypůjčení knihy (Borrowing the book)
 */
void Book::borrowBook(const std::string& userName) {
    if (is_available) {
        is_available = false;
        borrower = userName;
    }
}

/**
 * Vrácení knihy (Returning the book)
 */
void Book::returnBook() {
    is_available = true;
    borrower = "None";
}

/**
 * Zobrazení informací o knize (Displaying book info)
 */
void Book::display() const {
    std::cout << "[" << id << "] " << title << " by " << author 
              << " (" << genre << ") - ";
    if (is_available) {
        std::cout << "Available" << std::endl;
    } else {
        std::cout << "Borrowed by " << borrower << std::endl;
    }
}

// JSON Serializace (JSON Serialization)
json Book::toJson() const {
    return json{
        {"id", id},
        {"title", title},
        {"author", author},
        {"genre", genre},
        {"is_available", is_available},
        {"borrower", borrower}
    };
}

/**
 * Deserializace z JSONu (Deserialization from JSON)
 */
Book Book::fromJson(const json& j) {
    Book b;
    // Použití .value() je robustní; pokud klíč chybí, použije se výchozí hodnota
    // Using .value() is robust; if a key is missing, it uses the default value
    b.id = j.value("id", 0);
    b.title = j.value("title", "Unknown Title");
    b.author = j.value("author", "Unknown Author");
    b.genre = j.value("genre", "Unknown");
    b.is_available = j.value("is_available", true);
    b.borrower = j.value("borrower", "None");
    return b;
}
