using System;
using Xunit;

namespace SpaceGuild;
public class CargoTests
{
    [Fact]
    public void TestCargoAddItem()
    {
        Cargo cargo = new Cargo();
        Assert.True(cargo.AddItem("Item1", 90));
        Assert.False(cargo.AddItem("Item2", 20));
        Assert.False(cargo.AddItem("Item3", 30));
    }
}
