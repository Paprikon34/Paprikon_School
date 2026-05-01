#include "User.h"
#include <iostream>

User::User() : id(0), name("Unknown"), borrowed_count(0) {}

User::User(int id, std::string name) : id(id), name(name), borrowed_count(0) {}

int User::getId() const { return id; }
std::string User::getName() const { return name; }
int User::getBorrowedCount() const { return borrowed_count; }

void User::borrowBook() {
    borrowed_count++;
}

void User::returnBook() {
    if (borrowed_count > 0) {
        borrowed_count--;
    }
}

void User::display() const {
    std::cout << "[" << id << "] " << name << " - Borrowed books: " << borrowed_count << std::endl;
}

json User::toJson() const {
    return json{
        {"id", id},
        {"name", name},
        {"borrowed_count", borrowed_count}
    };
}

User User::fromJson(const json& j) {
    User u;
    u.id = j.value("id", 0);
    u.name = j.value("name", "Unknown");
    u.borrowed_count = j.value("borrowed_count", 0);
    return u;
}
