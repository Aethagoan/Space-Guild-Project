// AIDAN ANDERSON - 10 MAY 25 - The driver program!

using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using Internal;

namespace SpaceGuild;

class Program {
    // Entry point!
    static void Main(string[] args) {

    //args validation goes here

        Console.WriteLine("Welcome to SpaceGuild Startup!");

        string inputstring = "";
        Console.Write("Which database/save are we using? (d / default OR o / other OR n / new)>");
        inputstring = Console.ReadLine();
        if (inputstring.ToLower() == "d" || inputstring.ToLower() = "default"){

        } 
        else if (inputstring.ToLower() == "o" || inputstring.ToLower() = "other"){

        } 
        else if (inputstring.ToLower() == "n" || inputstring.ToLower() = "new"){

        }
        else {
            string[] validinputs = {"d","default","o","other","n","new"};  
            while (!validinputs.Contains(inputstring.ToLower())){
                Console.WriteLine("invalid input, try again (d / default OR o / other OR n / new)")
            }
        }





        string connectionString = 

























    }
}

// 
