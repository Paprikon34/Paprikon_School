#ifndef USER_H
#define USER_H

#include <string>
#include "json.hpp"

using json = nlohmann::json;

class User {
private:
    int id;
    std::string name;
    int borrowed_count;

public:
    User();
    User(int id, std::string name);

    int getId() const;
    std::string getName() const;
    int getBorrowedCount() const;

    void borrowBook();
    void returnBook();
    void display() const;

    json toJson() const;
    static User fromJson(const json& j);
};

#endif
