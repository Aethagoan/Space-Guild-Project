# Space Guild Release Plan

**Last Updated:** 24 Feb 2026  
**Current Version:** Pre-alpha (0.0.x)  
**Next Target:** v0.1.0 - Backend Feature Complete

---

## Release Strategy Overview

### Development Phases
1. **v0.1.0** - Backend Feature Complete (Current Focus)
2. **v0.2.0** - Frontend Integration & Playable MVP
3. **v0.3.0** - SOL System Content Complete
4. **v0.4.0** - Multi-system Expansion
5. **v1.0.0** - Public Launch

---

## v0.1.0 - Backend Feature Complete
**Target:** 1-2 weeks  
**Focus:** Core backend systems, station interactions, testing infrastructure

### Critical Path Items

#### 1. Station System Implementation
- [ ] Create Station entity type in `data.py`
  - Station inventory (items/components for sale)
  - Docking bay capacity
  - Faction ownership
  - Station type (shipyard, vendor, research, etc.)
- [ ] Station CRUD operations with proper locking
- [ ] Dock/undock ship actions
- [ ] Station vendor API endpoints
  - `GET /station/<id>/inventory` - View available items
  - `POST /station/<id>/buy` - Purchase items/components
  - `POST /station/<id>/sell` - Sell items/components
- [ ] Shipyard functionality
  - Component installation/removal
  - Ship purchase system
  - Ship tier validation

#### 2. SOL System Content Generation
- [ ] Create location graph structure for SOL system
  - Earth orbit, Moon orbit, stations
  - Venus orbit + stations
  - Mars orbit + stations + moons
  - Mercury orbit + station
  - Asteroid Belt regions (3 zones)
  - Jupiter orbit + atmosphere station + IO
  - Saturn orbit + atmosphere + ring stations
  - Uranus orbit + stations
  - Kuiper regions (4 zones)
  - Sun orbital
  - SOL->ALPHA warp gate
- [ ] Define faction ownership per location
- [ ] Create starter stations with inventory
  - Earth Orbital Station Zero (starter hub)
  - Basic vendor inventory templates
  - Shipyard component availability by tier
- [ ] Location metadata (danger level, resources, description)

#### 3. Logging & Event System
- [ ] Implement ship log storage in `data.py`
  - Per-ship message queue/log
  - Timestamp + event type + message
  - Max log size with rotation
- [ ] Regional event logging (subscriber pattern)
  - Location-based event broadcast
  - Ship enters/leaves notifications
  - Combat events visible to region
  - Item pickup/drop notifications
- [ ] API endpoints for logs
  - `GET /ship/<id>/log` - Retrieve ship's log
  - `GET /location/<id>/events` - Last tick events at location
- [ ] Event generation in actions
  - Combat actions append to attacker/defender logs
  - Movement actions notify origin/destination regions
  - Collection actions notify region

#### 4. Testing Infrastructure
- [ ] Expand test coverage in `Test_SpaceGuild.py`
  - Station interaction tests
  - Buy/sell transaction tests
  - Combat scenario tests
  - Movement and docking tests
  - Component degradation tests
- [ ] Create test data fixtures
  - Sample SOL system locations
  - Test stations with inventory
  - Multiple test players/ships
- [ ] Integration tests
  - Full tick cycle with multiple actions
  - Concurrent action processing
  - Lock contention scenarios
- [ ] Performance tests
  - 100+ ships in same location
  - Heavy combat scenarios
  - Large station inventories

#### 5. Backend Polish & Documentation
- [ ] Add `requirements.txt` with dependencies
- [ ] API documentation
  - Document all endpoints with examples
  - Request/response schemas
  - Error codes and handling
- [ ] Code documentation
  - Docstrings for all public functions
  - Inline comments for complex logic
- [ ] Configuration system
  - Game balance variables (damage multipliers, repair costs)
  - Tick rate configuration
  - Data persistence settings

### Secondary Features (Nice-to-have for v0.1.0)
- [ ] Ship statistics calculation based on components
- [ ] Economy system (credits/currency)
- [ ] Item/component rarity tiers
- [ ] Basic NPC ship behavior
- [ ] Anomaly/random event framework

---

## v0.2.0 - Frontend Integration & Playable MVP
**Target:** 2-3 weeks after v0.1.0  
**Status:** Planned

### Goals
- Landing page with game pitch
- Login page (basic auth, upgrade to JWT later)
- Game page with three-panel interface
  - Left: Navigation menu
  - Center: Clickable interaction area
  - Right: Details and actions panel
- Terminal-style text interface
- 5-second tick cycle with auto-refresh
- Basic ship controls (move, attack, collect, dock)
- Station interaction UI
- Player registration flow

### Technical Requirements
- Web framework decision (React, Vue, vanilla JS?)
- WebSocket or polling for tick updates
- State management on frontend
- API client integration
- Basic styling (terminal aesthetic)

---

## v0.3.0 - SOL System Content Complete
**Target:** 1 month after v0.2.0  
**Status:** Planned

### Goals
- All SOL system locations fully implemented in code
- Faction system mechanics (reputation, territory)
- Rich station variety with unique inventories
- Quest/mission framework
- Economy balance pass
- Player progression systems

---

## v0.4.0 - Multi-system Expansion
**Target:** 2-3 months after v0.3.0  
**Status:** Planned

### Goals
- Implement Outer System 1 (Science/Scavenger system)
- Warp gate travel mechanics
- Faction politics and player alignment
- Advanced NPC behaviors
- The Nebula region
- Black Hole region

---

## v1.0.0 - Public Launch
**Target:** TBD  
**Status:** Long-term goal

### Goals
- All 7+ star systems implemented
- Complete faction storylines
- Player-driven economy
- Guild/organization system
- Polished UI/UX
- Performance optimization
- Security hardening
- Public deployment infrastructure

---

## Development Workflow

### Branch Strategy
- `main` - Stable, tested code
- `dev` - Integration branch for active development
- `feature/*` - Individual feature branches

### Testing Protocol
1. Write tests for new functionality
2. Run full test suite before merging
3. Manual playtesting for game balance
4. Performance profiling for critical paths

### Commit Standards
- Use descriptive commit messages
- Reference issue/task numbers when applicable
- Keep commits focused and atomic

---

## Current Blockers & Risks

### Technical Risks
1. **Concurrency bugs** - Complex locking may cause deadlocks
   - Mitigation: Comprehensive integration tests
2. **JSON performance** - May not scale to hundreds of players
   - Mitigation: Performance testing, consider Redis/SQL later
3. **Tick timing** - 5-second ticks may feel slow/fast
   - Mitigation: Make tick rate configurable, playtest

### Content Risks
1. **Content generation time** - Creating all locations manually is slow
   - Mitigation: Template/tool-based generation
2. **Balance issues** - Combat/economy may need iteration
   - Mitigation: Configurable balance variables, rapid testing

### Scope Risks
1. **Feature creep** - Easy to over-scope before MVP
   - Mitigation: Strict adherence to release plan
2. **Frontend delay** - UI work may take longer than expected
   - Mitigation: Start frontend in parallel during v0.1.0 polish phase

---

## Success Metrics

### v0.1.0 Success Criteria
- [ ] All critical path items completed
- [ ] Test coverage >60% for core systems
- [ ] API documented and stable
- [ ] 2+ people can run backend locally without issues
- [ ] Performance: 50+ concurrent ships in single location without lag

### v0.2.0 Success Criteria
- [ ] Functional end-to-end gameplay loop
- [ ] Player can: register → spawn → move → dock → trade → combat
- [ ] 5+ alpha testers provide feedback
- [ ] No critical bugs in core gameplay

---

## Notes & Decisions

### Why JSON over SQL?
- Fast single-ID lookups (primary operation)
- Simple persistence without ORM complexity
- Easy to inspect/debug game state
- Can migrate to Redis/SQL later if needed

### Why tick-based actions?
- Prevents real-time spam/botting
- Creates strategic decision-making windows
- Easier to balance than real-time
- Server load is predictable and batchable

### Why permanent component degradation?
- Creates economy sink (need to buy new components)
- Rewards careful play
- Interesting risk/reward for combat
- Prevents invincible ships

---

## Contact & Feedback
For questions about this release plan, contact the development team or open an issue in the repository.
