namespace SpaceGuild {
    public enum ComponentTier {
        Tier0,
        Tier1,
        Tier2,
        Tier3,
        Tier4,
        Tier5,
        Tier6
    }

    public abstract class ShipComponent {
        public string Name { get; set; }
        public int Health { get; set; }
        public double DamageMultiplier { get; set; }
        public ComponentTier Tier { get; set; }

        public ShipComponent(string name, int health, double damageMultiplier, ComponentTier tier) {
            Name = name;
            Health = health;
            DamageMultiplier = damageMultiplier;
            Tier = tier;
        }

        public virtual void Repair(int amount) {
            if (Health + amount > MaxHealth) {
                Health = MaxHealth;
            } else {
                Health += amount;
            }
        }

        public abstract int MaxHealth { get; }
    }

    public class Engine : ShipComponent {
        public Engine() : base("Engine/Warp Drive/Propulsion", 100, 1.0, ComponentTier.Tier0) { }

        public override int MaxHealth => 100;
    }

    public class Weapon : ShipComponent {
        public Weapon() : base("Weapons", 50, 1.0, ComponentTier.Tier0) { }

        public override int MaxHealth => 50;
    }

    public class Shield : ShipComponent {
        public int ShieldPool { get; set; }

        public Shield() : base("Shields", 200, 1.0, ComponentTier.Tier0) {
            ShieldPool = Health;
        }

        public override int MaxHealth => 200;

        public void TakeDamage(int amount) {
            if (ShieldPool > 0) {
                ShieldPool -= amount;
            } else {
                Health -= amount;
            }
        }
    }

    public class CargoItem {
        public string Name { get; set; }
        public int Size { get; set; }

        public CargoItem(string name, int size) {
            Name = name;
            Size = size;
        }
    }

    public class Cargo : ShipComponent {
        public int Capacity { get; set; }
        private List<CargoItem> Items { get; set; } = new List<CargoItem>();

        public Cargo() : base("Cargo", 100, 1.0, ComponentTier.Tier0) {
            Capacity = 100;
        }

        public override int MaxHealth => 100;

        public bool AddItem(string name, int size) {
            if (Capacity - size >= 0) {
                Items.Add(new CargoItem(name, size));
                Capacity -= size;
                return true;
            }
            return false;
        }
    }

    public class Sensor : ShipComponent {
        public int ScanRange { get; set; }
        public double DetailLevel { get; set; }

        public Sensor() : base("Sensors", 30, 1.0, ComponentTier.Tier0) {
            ScanRange = 5;
            DetailLevel = 0.8;
        }

        public override int MaxHealth => 30;
    }

    public class StealthCloak : ShipComponent {
        public bool Active { get; set; }

        public StealthCloak() : base("Stealth Cloak", 20, 1.0, ComponentTier.Tier0) {
            Active = false;
        }

        public override int MaxHealth => 20;

        public void Activate() {
            Active = true;
        }

        public void Deactivate() {
            Active = false;
        }
    }

    class Ship {
        public Engine Engine { get; set; } = new Engine();
        public Weapon Weapon { get; set; } = new Weapon();
        public Shield Shield { get; set; } = new Shield();
        public Cargo Cargo { get; set; } = new Cargo();
        public Sensor Sensor { get; set; } = new Sensor();
        public StealthCloak StealthCloak { get; set; } = new StealthCloak();
    
        public Ship() {
            // Constructor remains empty
        }
    }
}