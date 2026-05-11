#ifndef USER_H
#define USER_H

#include <string>
#include "json.hpp"

// Alias pro JSON knihovnu (Alias for JSON library)
using json = nlohmann::json;

/**
 * @class User
 * @brief Reprezentuje čtenáře v systému (Represents a reader in the system)
 */
class User {
private:
    int id;                   // ID uživatele (User ID)
    std::string name;         // Jméno uživatele (User Name)
    int borrowed_count;       // Počet vypůjčených knih (Number of borrowed books)

public:
    // Konstruktory (Constructors)
    User();
    User(int id, std::string name);

    // Gettery (Accessors)
    int getId() const;
    std::string getName() const;
    int getBorrowedCount() const;

    // Akce (Actions)
    void borrowBook();
    void returnBook();
    void display() const;

    // JSON Serializace (JSON Serialization)
    json toJson() const;
    static User fromJson(const json& j);
};

#endif
