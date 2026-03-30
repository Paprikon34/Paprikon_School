#include "json.hpp"
#include <fstream>
#include <iostream>


using json = nlohmann::json;
using std::cin;
using std::cout;
using std::endl;
using std::ifstream;
using std::string;
int main() {

  cout << "**********Pokedex Loader**********\n";
  cout << "made by Paprikon\n";
  ifstream file("../pokemon.json");

  if (!file.is_open()) {
    std::cerr << "Failed to open pokemon.json\n";
    return 1;
  }

  json pokedex;
  file >> pokedex;

  while (true) {
    string name;
    cout << "\nEnter pokemon name: ";
    cin >> name;

    if (!pokedex.contains(name)) {
      cout << "Pokemon not found\n";
    } else {
      auto &p = pokedex[name];

      cout << "\nPokedex ID: " << p["id"] << "\n";
      cout << "Region: " << p["region"] << "\n";
      cout << "Gender: " << p["gender"] << "\n";

      cout << "Types:\n";
      for (auto &t : p["types"]) {
        cout << "- " << t << "\n";
      }

      cout << "Abilities:\n";
      for (auto &a : p["abilities"]) {
        cout << "- " << a["name"];
        if (a["is_hidden"]) {
          cout << " (Hidden Ability)";
        }
        cout << "\n";
      }

      cout << "Weaknesses:\n";
      for (auto &w : p["weaknesses"]) {
        cout << "- " << w << "\n";
      }

      cout << "Evolution line:\n";
      for (auto &e : p["evolution"]) {
        cout << "- " << e << "\n";
      }
    }

    cout << "\nSearch for another pokemon? (y/n): ";
    char choice;
    cin >> choice;
    if (choice != 'y' && choice != 'Y') {
      break;
    }
  }

  cout << "Thanks for using Pokedex Loader!\n";
  return 0;
}
