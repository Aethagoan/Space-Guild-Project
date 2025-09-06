

using System;

namespace SpaceGuildBack;

public class canScan 
{
    public static void Scan(){}
}

public class canGather 
{
    public static void Gather(){}
}

public class canAttack 
{
    public static void Attack(){}
}

public class canMove 
{
    public static void Move(string token, Location destination){}
}

public class canRepair 
{
    public static void Repair(){}
}

public class canMissions {

    public void Missions() {
        Console.WriteLine("printing missions!");
    }
}

public class canMarket {
    public static void Market(){}
}


// public class Station : canMove,canMarket,canMissions,canRepair
public class StationCanMove : canMove {}
public class StationCanMarket : StationCanMove { }



