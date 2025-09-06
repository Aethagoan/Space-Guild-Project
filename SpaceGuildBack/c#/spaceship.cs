namespace SpaceGuild;
class Ship
{
    private int Health { get; set; } = 0;
    public Engine Engine { get; set; } = new Engine();
    public Weapon Weapon { get; set; } = new Weapon();
    public Shield Shield { get; set; } = new Shield();
    public Cargo Cargo { get; set; } = new Cargo();
    public Sensor Sensor { get; set; } = new Sensor();
    public StealthCloak StealthCloak { get; set; } = new StealthCloak();

    public Ship()
    {
        // Constructor remains empty
    }
}
