using System;
using System.Collections.Generic;

namespace SpaceGuildBack;
public abstract class LocationBase
{
    public List<LocationBase> Links { get; set; } = new List<LocationBase>();
    public List<string> PlayerTokens { get; set; } = new List<string>();

    public void AddLink(LocationBase location)
    {
        Links.Add(location);
    }

    public void RemoveLink(LocationBase location)
    {
        Links.Remove(location);
    }

    public void ReceiveToken(string token)
    {
        PlayerTokens.Add(token);
    }

    public void SendToken(string token, LocationBase destination)
    {
        if (PlayerTokens.Contains(token))
        {
            PlayerTokens.Remove(token);
            destination.ReceiveToken(token);
        }
    }
}

