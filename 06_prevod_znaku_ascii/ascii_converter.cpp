#include <iostream>
#include <string>

int main() {
    using std::cout;
    using std::cin;
    using std::endl;
    using std::string;

    char again;

    do {
        cout << "Program prevadi znaky na jejich ciselne hodnoty a naopak.\n";

        string vstup;
        char znak;

        
        while (true) {
            cout << "Zadejte jeden znak: ";
            cin >> vstup;  

            if (vstup.length() == 1) {
                znak = vstup[0];
                break;              
            } else {
                cout << "Prosim napiste jeden znak.\n";
                
            }
        }
     
        cout << "Ciselna hodnota znaku " << znak
             << " je: " << (int)znak << endl;

        int cislo;
        cout << "\nZadejte cele cislo (napr. 65 pro 'A'(nektera cila pod 33 nemusi fungovat)): ";
        cin >> cislo;
        cout << "Znak odpovidajici cislu " << cislo << " je: " << (char)cislo << endl;

        cout << "\nChcete pokracovat? (y/n): ";
        cin >> again;

    } while (again == 'y' || again == 'Y');

    return 0;
}
