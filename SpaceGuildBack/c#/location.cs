using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Components.Routing;

namespace SpaceGuildBack;

public abstract class Location : canMove
{
    public List<Location> Links { get; set; } = new List<Location>();
    public List<string> PlayerTokens { get; set; } = new List<string>();

    public void AddLink(Location location)
    {
        Links.Add(location);
    }

    public void RemoveLink(Location location)
    {
        Links.Remove(location);
    }

    public void ReceiveToken(string token)
    {
        PlayerTokens.Add(token);
    }

    public void Move(string token, Location destination)
    {
        if (Links.Contains(destination) && PlayerTokens.Contains(token))
        {
            PlayerTokens.Remove(token);
            destination.ReceiveToken(token);
        }
        
    }
}


public class Orbit : Location
{
    
}

public class Station : Location
{
    
}



