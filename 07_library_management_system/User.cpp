#include "User.h"
#include <iostream>

// Výchozí konstruktor (Default constructor)
User::User() : id(0), name("Unknown"), borrowed_count(0) {}

// Parametrický konstruktor (Parameterized constructor)
User::User(int id, std::string name) : id(id), name(name), borrowed_count(0) {}

// Gettery (Accessors)
int User::getId() const { return id; }
std::string User::getName() const { return name; }
int User::getBorrowedCount() const { return borrowed_count; }

/**
 * Zvýšení počtu vypůjčených knih (Increment borrowed count)
 */
void User::borrowBook() {
    borrowed_count++;
}

/**
 * Snížení počtu vypůjčených knih (Decrement borrowed count)
 */
void User::returnBook() {
    if (borrowed_count > 0) {
        borrowed_count--;
    }
}

/**
 * Zobrazení informací o uživateli (Display user info)
 */
void User::display() const {
    std::cout << "[" << id << "] " << name << " - Borrowed books: " << borrowed_count << std::endl;
}

// JSON Serializace (JSON Serialization)
json User::toJson() const {
    return json{
        {"id", id},
        {"name", name},
        {"borrowed_count", borrowed_count}
    };
}

/**
 * Deserializace z JSONu (Deserialization from JSON)
 */
User User::fromJson(const json& j) {
    User u;
    u.id = j.value("id", 0);
    u.name = j.value("name", "Unknown");
    u.borrowed_count = j.value("borrowed_count", 0);
    return u;
}
