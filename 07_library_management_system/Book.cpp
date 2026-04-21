#include "Book.h"
#include <iostream>

// Default constructor
Book::Book() : id(0), title(""), author(""), genre(""), is_available(false), borrower("None") {}

// Parameterized constructor
Book::Book(int id, std::string title, std::string author, std::string genre)
    : id(id), title(title), author(author), genre(genre), is_available(true), borrower("None") {}

// Getters
int Book::getId() const { return id; }
std::string Book::getTitle() const { return title; }
std::string Book::getAuthor() const { return author; }
std::string Book::getGenre() const { return genre; }
bool Book::isAvailable() const { return is_available; }
std::string Book::getBorrower() const { return borrower; }

// Actions
void Book::borrowBook(const std::string& userName) {
    if (is_available) {
        is_available = false;
        borrower = userName;
    }
}

void Book::returnBook() {
    is_available = true;
    borrower = "None";
}

void Book::display() const {
    std::cout << "[" << id << "] " << title << " by " << author 
              << " (" << genre << ") - ";
    if (is_available) {
        std::cout << "Available" << std::endl;
    } else {
        std::cout << "Borrowed by " << borrower << std::endl;
    }
}

// JSON Serialization
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

// Deserialization from JSON
Book Book::fromJson(const json& j) {
    Book b;
    // Using .value() is very robust; if a key is missing from JSON, it uses the default value
    b.id = j.value("id", 0);
    b.title = j.value("title", "Unknown Title");
    b.author = j.value("author", "Unknown Author");
    b.genre = j.value("genre", "Unknown");
    b.is_available = j.value("is_available", true);
    b.borrower = j.value("borrower", "None");
    return b;
}
