// restful api

using SpaceGuildBack;


var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");


Orbit earth = new Orbit();
Station earthgroundzero = new Station();

earth.AddLink(earthgroundzero);
earthgroundzero.AddLink(earth);

earth.ReceiveToken("whatever dude");

Console.WriteLine(earth.PlayerTokens.Count);
Console.WriteLine(earthgroundzero.PlayerTokens.Count);
Console.WriteLine();

earth.Move("whatever dude", earthgroundzero);

Console.WriteLine(earth.PlayerTokens.Count);
Console.WriteLine(earthgroundzero.PlayerTokens.Count);
earthgroundzero.Missions();
Console.WriteLine();

earthgroundzero.Move("whatever dude", earth);

Console.WriteLine(earth.PlayerTokens.Count);
Console.WriteLine(earthgroundzero.PlayerTokens.Count);
Console.WriteLine();




// app.Run();
