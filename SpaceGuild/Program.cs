// AIDAN ANDERSON - 10 MAY 25 - The driver program!

using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using Internal;
using MySql.Data.MySqlClient;

namespace SpaceGuild;

class Program {
    // Entry point!
    static void Main(string[] args) {

    //args validation goes here

        Console.WriteLine("Welcome to SpaceGuild Startup!");

        string inputstring = "";
        string connectionString = "";
        MySqlConnection connection;

        string[] allconnectionstrings = File.ReadAllLines("./SpaceGuildLogic/Database/connectionstrings.txt");
        if (allconnectionstrings.Length == 0) {
            Console.WriteLine();
            Console.Write("We noticed that there are no connections... Want to create a new one (will be default)? (Y/N)> ");
            string yesNo = Console.ReadLine().ToLower();
            while (!(yesNo == "y" || yesNo == "n" )){
                Console.WriteLine();
                Console.Write("(y/n)> ");
                yesNo = Console.ReadLine().ToLower();
            }
            if (yesNo == "y") CreateNewConnection();
            if (yesNo == "n") return;
        }


        Console.WriteLine();
        Console.Write("Which database/save are we using? (d / default OR o / other OR n / new)> ");
        inputstring = Console.ReadLine().ToLower();
        string[] validinputs = {"d","default","o","other","n","new"};  
        while (!validinputs.Contains(inputstring)){
            Console.WriteLine();
            Console.Write("invalid input, try again (d / default OR o / other OR n / new)> ");
            inputstring = Console.ReadLine().ToLower();
        }

        

        if (inputstring == "d" || inputstring == "default"){

            connectionString = allconnectionstrings[0];
            // connection = new MySqlConnection(connectionString);

        } 
        else if (inputstring == "o" || inputstring == "other"){

            int i = 0;

            foreach (string connector in allconnectionstrings) {
                Console.WriteLine($"[{i}] {connector}");
                i++;
            }

            Console.WriteLine();
            Console.Write($"Choose an option [0-{allconnectionstrings.Length - 1}]> ");

            string connectionChoice = Console.ReadLine();
            int parsedChoice = -1;

            try {
                int.TryParse(connectionChoice, out parsedChoice);
            } 
            catch {
                Console.WriteLine("something went wrong with the input.");
            }

            while (parsedChoice < 0 || parsedChoice > allconnectionstrings.Length - 1){
                Console.WriteLine();
                Console.Write($"Choose an option [0-{allconnectionstrings.Length - 1}]> ");
                try {
                    int.TryParse(connectionChoice, out parsedChoice);
                } 
                catch {
                    Console.WriteLine("something went wrong with the input.");
                }
            }

            connectionString = allconnectionstrings[parsedChoice];

        } 
        else if (inputstring == "n" || inputstring == "new"){

            connectionString = CreateNewConnection();
            
            Console.WriteLine();
            Console.Write("Is this a fresh database/do we need to generate tables? (Y/N)> ");

            string yesNo = Console.ReadLine().ToLower();

            while (!(yesNo == "y" || yesNo == "n" )){
                Console.WriteLine();
                Console.Write("(y/n)> ");
                yesNo = Console.ReadLine().ToLower();
            }

            if (yesNo == "y") {
                // open connection,
                connection = new MySqlConnection(connectionString);

                // create tables.
                




                // close the connection (will reopen momentarily.)
                connection.Close();
                Console.WriteLine("Tables created!");

            }
            else if (yesNo == "n") {
                Console.WriteLine("No Tables Generated. :)");
            };

        }
        else 
        {
            throw new Exception("Invalid input made it through?");
        }




        Console.WriteLine("Connecting to the database...");
        try {
            connection = new MySqlConnection(connectionString);

        }
        catch (Exception ex) {
            Console.WriteLine(ex.Message);
            throw new Exception("Connection had a problem.");
        }





















        connection.Close();


    } // end main

// functions

    static string CreateNewConnection() {
        Console.WriteLine();
        Console.Write("What's the IP?> ");
        string ip = Console.ReadLine();
        Console.WriteLine();
        Console.Write("What's the port?> ");
        string port = Console.ReadLine();
        Console.WriteLine();
        Console.Write("What's the username?> ");
        string username = Console.ReadLine();
        Console.WriteLine();
        Console.Write("What's the password?> ");
        string password = Console.ReadLine();

        string newconnection = $"\nServer={ip};Port={port};Database=SpaceGuild;User={username};Password={password};";

        File.AppendAllText("./SpaceGuildLogic/Database/connectionstrings.txt",newconnection);
        Console.WriteLine("Connection String Stored!");

        return newconnection;  
    } // end createnewconnection







} // end program class